# AAT1 — POS Tagging and Named Entity Recognition

**Course:** Advance Natural Language Processing (AML23702)  
**Student:** P Prithvi Raj Kandan · USN 1GA23AI033 · Dept. of AI & ML, Global Academy of Technology

spaCy (`en_core_web_sm`) tags every token in a paragraph and lists the named entities.

## Layout

| Path | Role |
|---|---|
| `backend/app.py` | Flask app on **port 5001** |
| `backend/nlp.py` | POS + NER logic |
| `backend/Q1_spaCy_POS_NER.ipynb` | Step-by-step notebook |
| `frontend/` | Single page for this question |
| `data/paragraph.txt` | Sample paragraph loaded by the API and the page |
| `data/extra_paragraph.txt` | Second paragraph used by the notebook |

## Run

```bash
cd AAT1/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

Open http://localhost:5001. The page calls `http://localhost:5001/api/pos-ner`.

Run the notebook from `AAT1/backend` so it can read `../data`.

## API

`GET /api/sample` returns the paragraph from `data/paragraph.txt`.

`POST /api/pos-ner`

```json
{"paragraph": "On 23 August 2023, the Vikram lander of Chandrayaan-3 touched down near the south pole of the Moon."}
```

Response fields: `tokens` (word, POS, tag, lemma), `entities` (text, label, character offsets), `pos_counts`, `model`.
