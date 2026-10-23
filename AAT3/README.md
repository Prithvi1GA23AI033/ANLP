# AAT3 — RAG over the Neo4j Movies Graph

**Course:** Advance Natural Language Processing (AML23702)  
**Student:** P Prithvi Raj Kandan · USN 1GA23AI033 · Dept. of AI & ML, Global Academy of Technology

The app retrieves movie, person, and year facts from the Neo4j *Movies* example graph, then writes an answer. If `LLM_API_KEY` is set, an OpenAI-compatible chat endpoint generates the answer. If it is not set, a **template fallback** is built from the retrieved facts and labelled as such.

## Layout

| Path | Role |
|---|---|
| `backend/app.py` | Flask app on **port 5003** |
| `backend/nlp.py` | Retrieval and generation |
| `backend/export_movies_json.py` | Rebuild `data/movies.json` from a live Neo4j |
| `backend/Q3_RAG_Neo4j_Movies.ipynb` | Step-by-step notebook |
| `backend/.env.example` | Variable names only. Do not commit a real `.env` |
| `frontend/` | Single page for this question |
| `data/movies.cypher` | Official Movies graph load script |
| `data/movies.json` | Offline export of the same graph |
| `data/question.txt` | Default question |
| `data/suggestions.txt` | Chip questions |
| `data/questions.txt` | Questions the notebook runs |

## Run (offline, no API key)

```bash
cd AAT3/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5003. The page calls `http://localhost:5003/api/rag`. With no environment variables the knowledge source is `data/movies.json` and the generator is the template fallback.

Run the notebook from `AAT3/backend` so `import nlp` and `../data` both resolve.

## Optional switches

Export these in the shell. Never commit the values.

| Variable | Effect |
|---|---|
| `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` | Query a live Neo4j server. Load the graph first, for example `cypher-shell -f ../data/movies.cypher`. |
| `LLM_API_KEY` | Enables LLM generation. Unset means the template fallback. |
| `LLM_BASE_URL` | Default `https://api.groq.com/openai/v1`. |
| `LLM_MODEL` | Default `llama-3.1-8b-instant`. |

## API

`GET /api/sample` reads `data/question.txt` and `data/suggestions.txt`.

`GET /api/status` reports the knowledge source and whether an LLM key is configured.

`POST /api/rag`

```json
{"question": "Who directed The Matrix and who played Neo?"}
```

Response fields: `answer`, `generator`, `retrieved_entities`, `context`, `knowledge_source`.
