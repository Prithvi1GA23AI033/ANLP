"""LDA topic modelling. Each topic is reported with its top five words (AAT4)."""
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def lda_topics(documents, n_topics=3, top_n=5, seed=5):
    vectorizer = CountVectorizer(stop_words="english")
    doc_term = vectorizer.fit_transform(documents)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=seed)
    doc_topic = lda.fit_transform(doc_term)
    words = vectorizer.get_feature_names_out()
    topics = []
    for index, component in enumerate(lda.components_):
        top = component.argsort()[-top_n:][::-1]
        topics.append({
            "topic": index + 1,
            "words": [words[j] for j in top],
            "weights": [round(float(component[j] / component.sum()), 3) for j in top],
        })
    docs = [
        {
            "doc": index + 1,
            "text": text,
            "topic": int(doc_topic[index].argmax()) + 1,
            "prob": round(float(doc_topic[index].max()), 3),
        }
        for index, text in enumerate(documents)
    ]
    return {"topics": topics, "documents": docs, "vocab_size": len(words), "seed": seed}
