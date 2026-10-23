# AAT2 — Information-Retrieval Question Answering

**Course:** Advance Natural Language Processing (AML23702)  
**Student:** P Prithvi Raj Kandan · USN 1GA23AI033 · Dept. of AI & ML, Global Academy of Technology

A small document collection is split into sentences, vectorised with TF-IDF, and ranked against the question by cosine similarity. The top sentence is the answer.

## Layout

| Path | Role |
|---|---|
| `backend/app.py` | Flask app on **port 5002** |
| `backend/nlp.py` | TF-IDF retrieval |
| `backend/Q2_IR_Question_Answering.ipynb` | Step-by-step notebook |
| `frontend/` | Single page for this question |
| `data/documents.txt` | Sample collection (one document per line) |
| `data/question.txt` | Default question |
| `data/suggestions.txt` | Extra questions shown as chips |
| `data/glossary.txt` | Short one-sentence corpus used in the notebook |

## Run

```bash
cd AAT2/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt_tab')"
python app.py
```

Open http://localhost:5002. The page calls `http://localhost:5002/api/qa`.

Run the notebook from `AAT2/backend` so it can read `../data`.

## API

`GET /api/sample` returns the documents, default question, and suggestions loaded from `data/`.

`POST /api/qa`

```json
{"question": "When is Engineers' Day celebrated in India?", "documents": ["Engineers' Day is celebrated in India on 15 September."]}
```

Response fields: `answer`, `ranked` (sentence, document number, cosine score), `num_sentences`.
