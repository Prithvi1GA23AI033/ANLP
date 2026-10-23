"""AAT4 Flask app: LDA topic modelling.

Run from this folder:  python app.py
UI and API:            http://localhost:5004
"""
import os

from flask import Flask, jsonify, request, send_from_directory

import nlp

PORT = 5004
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
    return jsonify({"documents": read_lines("documents.txt"), "n_topics": 3, "seed": 5})


@app.post("/api/lda")
def topics():
    body = request.get_json(force=True, silent=True) or {}
    documents = body.get("documents") or read_lines("documents.txt")
    n_topics = int(body.get("n_topics", 3))
    seed = int(body.get("seed", 5))
    return jsonify(nlp.lda_topics(documents, n_topics=n_topics, seed=seed))


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
