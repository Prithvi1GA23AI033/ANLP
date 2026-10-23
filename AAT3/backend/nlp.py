"""RAG over the Neo4j Movies graph (AAT3).

Uses a live Neo4j server when NEO4J_URI is set, otherwise the bundled JSON
export of the same :play movies dataset. An LLM writes the answer when
LLM_API_KEY is set; otherwise a labelled template is built from the facts.
"""
import json
import os
import re

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "movies.json")


class MovieGraph:
    """Knowledge source for AAT3."""

    def __init__(self):
        self.driver = None
        uri = os.getenv("NEO4J_URI")
        if uri:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(
                uri,
                auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "")),
            )
            self.driver.verify_connectivity()
            self.mode = "neo4j (" + uri + ")"
        else:
            with open(DATA_FILE, encoding="utf-8") as handle:
                self.data = json.load(handle)
            self.mode = "bundled JSON (data/movies.json)"
        self.titles = self._all_titles()
        self.names = self._all_names()

    def _q(self, cypher, **params):
        return [dict(record) for record in self.driver.execute_query(cypher, **params).records]

    def _all_titles(self):
        if self.driver:
            return [row["t"] for row in self._q("MATCH (m:Movie) RETURN m.title AS t")]
        return [movie["title"] for movie in self.data["movies"]]

    def _all_names(self):
        if self.driver:
            return [row["n"] for row in self._q("MATCH (p:Person) RETURN p.name AS n")]
        return [person["name"] for person in self.data["people"]]

    def movie_facts(self, title):
        if self.driver:
            rows = self._q(
                """MATCH (m:Movie {title:$t}) OPTIONAL MATCH (p:Person)-[r]->(m)
                RETURN m.released AS released, m.tagline AS tagline, p.name AS person, type(r) AS type,
                r.roles AS roles, r.rating AS rating, r.summary AS summary""",
                t=title,
            )
            movie = {"title": title, "released": rows[0]["released"], "tagline": rows[0]["tagline"]}
            rels = [row for row in rows if row["person"]]
        else:
            movie = next(item for item in self.data["movies"] if item["title"] == title)
            rels = [row for row in self.data["relationships"] if row["movie"] == title]
        facts = [f"{title} was released in {movie['released']}."]
        if movie.get("tagline"):
            facts.append(f'Tagline of {title}: "{movie["tagline"]}".')
        for kind, verb in [("DIRECTED", "Directed by"), ("WROTE", "Written by"), ("PRODUCED", "Produced by")]:
            people = sorted(row["person"] for row in rels if row["type"] == kind)
            if people:
                facts.append(f"{verb}: {', '.join(people)}.")
        cast = [
            f"{row['person']} as {', '.join(row.get('roles') or [])}"
            for row in rels
            if row["type"] == "ACTED_IN"
        ]
        if cast:
            facts.append(f"Cast of {title}: " + "; ".join(sorted(cast)) + ".")
        for row in rels:
            if row["type"] == "REVIEWED":
                facts.append(
                    f"{row['person']} reviewed {title}: rating {row.get('rating')}, \"{row.get('summary')}\"."
                )
        return facts

    def person_facts(self, name):
        if self.driver:
            born = self._q("MATCH (p:Person {name:$n}) RETURN p.born AS born", n=name)[0]["born"]
            rels = self._q(
                """MATCH (p:Person {name:$n})-[r]->(m:Movie)
                RETURN type(r) AS type, m.title AS movie, m.released AS released, r.roles AS roles""",
                n=name,
            )
        else:
            born = next(person for person in self.data["people"] if person["name"] == name).get("born")
            year = {movie["title"]: movie["released"] for movie in self.data["movies"]}
            rels = [
                dict(row, released=year[row["movie"]])
                for row in self.data["relationships"]
                if row["person"] == name
            ]
        facts = [f"{name} was born in {born}." if born else f"{name}: birth year not in the graph."]
        for kind, verb in [
            ("ACTED_IN", "acted in"),
            ("DIRECTED", "directed"),
            ("WROTE", "wrote"),
            ("PRODUCED", "produced"),
        ]:
            items = sorted({f"{row['movie']} ({row['released']})" for row in rels if row["type"] == kind})
            if items:
                facts.append(f"{name} {verb}: {', '.join(items)}.")
        return facts

    def movies_in_year(self, year):
        if self.driver:
            return sorted(row["t"] for row in self._q("MATCH (m:Movie {released:$y}) RETURN m.title AS t", y=year))
        return sorted(movie["title"] for movie in self.data["movies"] if movie["released"] == year)

    def retrieve(self, query, k=3):
        lowered = query.lower()
        context, hits = [], []
        for title in sorted(self.titles, key=len, reverse=True):
            if title.lower() in lowered and not any(title.lower() in hit.lower() for hit in hits):
                hits.append(title)
                context += self.movie_facts(title)
        for name in self.names:
            last = name.split()[-1]
            if name.lower() in lowered or (
                len(name.split()) > 1 and last.lower() in re.findall(r"\w+", lowered) and len(last) > 3
            ):
                hits.append(name)
                context += self.person_facts(name)
        for year in re.findall(r"\b(19\d\d|20\d\d)\b", query):
            movies = self.movies_in_year(int(year))
            context.append(f"Movies released in {year}: {', '.join(movies) if movies else 'none in the graph'}.")
            hits.append(year)
        if not hits:
            cards = {title: " ".join(self.movie_facts(title)[:2]) for title in self.titles}
            vectorizer = TfidfVectorizer(stop_words="english")
            matrix = vectorizer.fit_transform(list(cards.values()))
            scores = cosine_similarity(vectorizer.transform([query]), matrix).flatten()
            for index in scores.argsort()[::-1][:k]:
                if scores[index] > 0:
                    title = list(cards)[index]
                    hits.append(title)
                    context += self.movie_facts(title)[:3]
        return hits[:6], context[:25]


_graph = None


def graph():
    global _graph
    if _graph is None:
        _graph = MovieGraph()
    return _graph


def llm_generate(question, context):
    key = os.getenv("LLM_API_KEY")
    if not key or not context:
        return None
    base = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    prompt = (
        "Answer the question using ONLY the movie facts below. If the facts do not contain the answer, say so.\n\n"
        "Facts:\n- " + "\n- ".join(context) + f"\n\nQuestion: {question}\nAnswer:"
    )
    response = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        timeout=60,
        json={"model": model, "temperature": 0.2, "messages": [{"role": "user", "content": prompt}]},
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip(), model


def template_answer(question, hits, context):
    if not context:
        return "I could not find anything about that in the Neo4j Movies graph. Try a movie title or an actor's name."
    return "From the Movies graph: " + " ".join(context[:6])


def rag(question):
    source = graph()
    hits, context = source.retrieve(question)
    out = {
        "question": question,
        "retrieved_entities": hits,
        "context": context,
        "knowledge_source": source.mode,
    }
    try:
        generated = llm_generate(question, context)
    except Exception as exc:
        generated, out["llm_error"] = None, str(exc)[:200]
    if generated:
        out.update(answer=generated[0], generator=f"LLM ({generated[1]})")
    else:
        out.update(
            answer=template_answer(question, hits, context),
            generator="Template fallback (no LLM_API_KEY set)",
        )
    return out
