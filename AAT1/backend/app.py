"""AAT1 Flask app: spaCy POS tagging and NER.

Run from this folder:  python app.py
UI and API:            http://localhost:5001
"""
import os

from flask import Flask, jsonify, request, send_from_directory

import nlp

PORT = 5001
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


@app.get("/api/sample")
def sample():
    return jsonify({"paragraph": read_text("paragraph.txt")})


@app.post("/api/pos-ner")
def analyse():
    body = request.get_json(force=True, silent=True) or {}
    paragraph = (body.get("paragraph") or "").strip() or read_text("paragraph.txt")
    return jsonify(nlp.pos_ner(paragraph))


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
