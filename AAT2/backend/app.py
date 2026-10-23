"""AAT2 Flask app: IR question answering (TF-IDF + cosine).

Run from this folder:  python app.py
UI and API:            http://localhost:5002
"""
import os

from flask import Flask, jsonify, request, send_from_directory

import nlp

PORT = 5002
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
    return jsonify({
        "documents": read_lines("documents.txt"),
        "question": read_lines("question.txt")[0],
        "suggestions": read_lines("suggestions.txt"),
    })


@app.post("/api/qa")
def answer():
    body = request.get_json(force=True, silent=True) or {}
    documents = body.get("documents") or read_lines("documents.txt")
    question = (body.get("question") or "").strip() or read_lines("question.txt")[0]
    return jsonify(nlp.retrieve(question, documents))


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
