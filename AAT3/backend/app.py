"""AAT3 Flask app: RAG over the Neo4j Movies dataset.

Run from this folder:  python app.py
UI and API:            http://localhost:5003

Set LLM_API_KEY to call an OpenAI-compatible chat endpoint. If it is unset,
the answer is a template built from the retrieved facts. Set NEO4J_URI to
query a live graph; otherwise data/movies.json is used. Do not commit .env.
"""
import os

from flask import Flask, jsonify, request, send_from_directory

import nlp

PORT = 5003
ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(ROOT, "..", "frontend")
DATA = os.path.join(ROOT, "..", "data")

app = Flask(__name__)


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


@app.before_request
def preflight():
    if request.method == "OPTIONS":
        return ("", 204)


def read_lines(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


@app.get("/api/sample")
def sample():
    return jsonify({"question": read_lines("question.txt")[0], "suggestions": read_lines("suggestions.txt")})


@app.get("/api/status")
def status():
    return jsonify({
        "knowledge_source": nlp.graph().mode,
        "llm": "configured" if os.getenv("LLM_API_KEY") else "not configured (template fallback)",
        "port": PORT,
    })


@app.post("/api/rag")
def answer():
    body = request.get_json(force=True, silent=True) or {}
    question = (body.get("question") or "").strip() or read_lines("question.txt")[0]
    return jsonify(nlp.rag(question))


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/style.css")
def css():
    return send_from_directory(FRONTEND, "style.css")


@app.get("/app.js")
def js():
    return send_from_directory(FRONTEND, "app.js")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", PORT)))
