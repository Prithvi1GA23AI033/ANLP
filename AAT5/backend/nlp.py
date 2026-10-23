"""WordNet synonyms, definitions, and Lesk word-sense disambiguation (AAT5)."""
import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

for package, resource in (
    ("wordnet", "corpora/wordnet"),
    ("omw-1.4", "corpora/omw-1.4"),
    ("punkt_tab", "tokenizers/punkt_tab"),
):
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(package, quiet=True)


def wordnet_senses(word, contexts):
    word = word.strip().lower()
    senses = []
    for synset in wn.synsets(word):
        senses.append({
            "synset": synset.name(),
            "pos": synset.pos(),
            "definition": synset.definition(),
            "synonyms": sorted({lemma.name().replace("_", " ") for lemma in synset.lemmas()}),
            "examples": synset.examples()[:2],
        })
    all_synonyms = sorted({
        synonym
        for sense in senses
        for synonym in sense["synonyms"]
        if synonym.lower() != word.lower()
    })
    resolved = []
    for sentence in contexts:
        sense = lesk(nltk.word_tokenize(sentence), word)
        resolved.append({
            "sentence": sentence,
            "synset": sense.name() if sense else None,
            "definition": sense.definition() if sense else "No sense selected",
        })
    return {
        "word": word,
        "num_senses": len(senses),
        "senses": senses,
        "all_synonyms": all_synonyms,
        "contexts": resolved,
    }
