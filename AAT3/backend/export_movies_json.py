"""Export the Neo4j Movies graph (loaded from ../data/movies.cypher) to ../data/movies.json.

Run once while Neo4j is running, from AAT3/backend:

    NEO4J_URI=bolt://localhost:7687 NEO4J_USER=neo4j NEO4J_PASSWORD=... python export_movies_json.py

The JSON file lets the RAG demo run without a Neo4j server. Do not put the password in a committed file.
"""
import json
import os

from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
auth = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", ""))
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "movies.json")

with GraphDatabase.driver(uri, auth=auth) as driver:
    movies = driver.execute_query(
        "MATCH (m:Movie) RETURN m.title AS title, m.released AS released, m.tagline AS tagline ORDER BY title"
    ).records
    people = driver.execute_query(
        "MATCH (p:Person) RETURN p.name AS name, p.born AS born ORDER BY name"
    ).records
    rels = driver.execute_query(
        "MATCH (p:Person)-[r]->(m:Movie) RETURN p.name AS person, type(r) AS type, "
        "r.roles AS roles, r.rating AS rating, r.summary AS summary, m.title AS movie"
    ).records

data = {
    "source": "Neo4j Movies example graph (:play movies / movies.cypher)",
    "movies": [dict(row) for row in movies],
    "people": [dict(row) for row in people],
    "relationships": [{key: value for key, value in dict(row).items() if value is not None} for row in rels],
}
with open(out_path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=1)
    handle.write("\n")
print(len(data["movies"]), "movies,", len(data["people"]), "people,", len(data["relationships"]), "relationships")
