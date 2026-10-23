"""spaCy POS tagging and named entity recognition (AAT1)."""
import spacy

nlp = spacy.load("en_core_web_sm")


def pos_ner(paragraph):
    doc = nlp(paragraph)
    tokens = [
        {
            "text": t.text,
            "pos": t.pos_,
            "tag": t.tag_,
            "lemma": t.lemma_,
            "pos_meaning": spacy.explain(t.pos_) or "",
        }
        for t in doc
        if not t.is_space
    ]
    entities = [
        {
            "text": e.text,
            "label": e.label_,
            "meaning": spacy.explain(e.label_) or "",
            "start": e.start_char,
            "end": e.end_char,
        }
        for e in doc.ents
    ]
    pos_counts = {}
    for token in tokens:
        pos_counts[token["pos"]] = pos_counts.get(token["pos"], 0) + 1
    return {
        "tokens": tokens,
        "entities": entities,
        "pos_counts": pos_counts,
        "model": "en_core_web_sm " + nlp.meta["version"],
    }
