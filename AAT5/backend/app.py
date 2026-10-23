"""AAT5 Flask app: WordNet synonyms, definitions, and Lesk.

Run from this folder:  python app.py
UI and API:            http://localhost:5005
"""
import os

from flask import Flask, jsonify, request, send_from_directory

import nlp

PORT = 5005
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


def read_text(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as handle:
        return handle.read().strip()


def read_lines(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


@app.get("/api/sample")
def sample():
    return jsonify({"word": read_text("word.txt"), "contexts": read_lines("contexts.txt")})


@app.post("/api/wordnet")
def senses():
    body = request.get_json(force=True, silent=True) or {}
    word = (body.get("word") or "").strip() or read_text("word.txt")
    contexts = body.get("contexts")
    if not contexts:
        contexts = read_lines("contexts.txt")
    return jsonify(nlp.wordnet_senses(word, contexts))


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
