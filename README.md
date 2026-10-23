# Advance Natural Language Processing (AML23702)

**Student:** P Prithvi Raj Kandan  
**USN:** 1GA23AI033  
**Department:** Artificial Intelligence & Machine Learning, Global Academy of Technology

Five lab exercises (AAT1–AAT5). Each folder is self-contained: its own Flask backend, single-page frontend, sample data, notebook, and requirements file. The pages keep one shared visual style and each one calls only its own local port.

| Folder | Question | Port | Endpoint |
|---|---|---|---|
| [AAT1](AAT1/README.md) | spaCy POS tagging and named entity recognition | 5001 | `POST /api/pos-ner` |
| [AAT2](AAT2/README.md) | IR question answering (TF-IDF + cosine similarity) | 5002 | `POST /api/qa` |
| [AAT3](AAT3/README.md) | RAG over the Neo4j Movies graph, with an LLM or a template fallback | 5003 | `POST /api/rag` |
| [AAT4](AAT4/README.md) | LDA topic modelling (top 5 words per topic) | 5004 | `POST /api/lda` |
| [AAT5](AAT5/README.md) | NLTK WordNet synonyms, definitions, and Lesk | 5005 | `POST /api/wordnet` |

Open the README inside an AAT folder for the install and run commands. From each `backend/` directory the short form is `pip install -r requirements.txt` and `python app.py`, after the one-time model downloads noted in that README.

AAT3 reads `LLM_API_KEY` from the environment when an LLM should write the answer. Leave it unset to use the labelled template fallback. `NEO4J_URI` is optional; without it the app uses `AAT3/data/movies.json`. Do not commit `.env` files or API keys. Names only are listed in `AAT3/backend/.env.example`.
