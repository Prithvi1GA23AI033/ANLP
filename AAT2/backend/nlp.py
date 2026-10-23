"""IR-based question answering with TF-IDF and cosine similarity (AAT2)."""
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


def retrieve(question, documents, top_k=3):
    sentences, source = [], []
    for doc_index, doc in enumerate(documents):
        for sentence in nltk.sent_tokenize(doc):
            sentences.append(sentence.strip())
            source.append(doc_index + 1)
    if not sentences:
        return {
            "question": question,
            "answer": "No relevant sentence found.",
            "ranked": [],
            "num_sentences": 0,
        }
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(sentences)
    scores = cosine_similarity(vectorizer.transform([question]), matrix).flatten()
    order = scores.argsort()[::-1][:top_k]
    ranked = [
        {"sentence": sentences[i], "doc": source[i], "score": round(float(scores[i]), 4)}
        for i in order
    ]
    best = ranked[0] if ranked and ranked[0]["score"] > 0 else None
    return {
        "question": question,
        "answer": best["sentence"] if best else "No relevant sentence found.",
        "ranked": ranked,
        "num_sentences": len(sentences),
    }
