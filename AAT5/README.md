# AAT5 — WordNet Synonyms, Definitions, and Lesk

**Course:** Advance Natural Language Processing (AML23702)  
**Student:** P Prithvi Raj Kandan · USN 1GA23AI033 · Dept. of AI & ML, Global Academy of Technology

NLTK WordNet lists every sense of a word with its definition and synonyms. The Lesk algorithm then picks the sense whose gloss overlaps the context sentence.

## Layout

| Path | Role |
|---|---|
| `backend/app.py` | Flask app on **port 5005** |
| `backend/nlp.py` | WordNet lookup and Lesk |
| `backend/Q5_WordNet_Senses.ipynb` | Step-by-step notebook |
| `frontend/` | Single page for this question |
| `data/word.txt` | Default word (`spring`) |
| `data/contexts.txt` | One context sentence per line |
| `data/bank_word.txt`, `data/bank_contexts.txt` | Notebook example |
| `data/bass_word.txt`, `data/bass_contexts.txt` | Notebook example where Lesk is wrong |

## Run

```bash
cd AAT5/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; [nltk.download(p) for p in ['wordnet','omw-1.4','punkt_tab']]"
python app.py
```

Open http://localhost:5005. The page calls `http://localhost:5005/api/wordnet`.

Run the notebook from `AAT5/backend` so it can read `../data`.

## API

`GET /api/sample` returns the word and contexts from `data/`.

`POST /api/wordnet`

```json
{"word": "spring", "contexts": ["Flowers bloom early in the spring season."]}
```

Response fields: `senses` (synset, definition, synonyms), `all_synonyms`, and `contexts` (Lesk synset and definition for each sentence).
