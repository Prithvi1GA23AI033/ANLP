# AAT4 — Topic Modelling with LDA

**Course:** Advance Natural Language Processing (AML23702)  
**Student:** P Prithvi Raj Kandan · USN 1GA23AI033 · Dept. of AI & ML, Global Academy of Technology

CountVectorizer builds a document-term matrix. Latent Dirichlet Allocation discovers topics and returns the **top five words** of each topic, plus the dominant topic of every document.

## Layout

| Path | Role |
|---|---|
| `backend/app.py` | Flask app on **port 5004** |
| `backend/nlp.py` | LDA |
| `backend/Q4_LDA_Topic_Modelling.ipynb` | Step-by-step notebook |
| `frontend/` | Single page for this question |
| `data/documents.txt` | Cricket, cooking, and space sample (one document per line) |
| `data/documents_alt.txt` | Football, hospital, and machine-learning sample used in the notebook |

## Run

```bash
cd AAT4/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5004. The page calls `http://localhost:5004/api/lda`.

Run the notebook from `AAT4/backend` so it can read `../data`. On a corpus this small the topics move when the random seed changes. The page defaults to 3 topics and seed 5.

## API

`GET /api/sample` returns the documents in `data/documents.txt` plus `n_topics: 3` and `seed: 5`.

`POST /api/lda`

```json
{"documents": ["The cricket team won the match."], "n_topics": 3, "seed": 5}
```

Each item in `topics` has exactly five `words` and matching `weights`.
