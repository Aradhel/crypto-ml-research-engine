from __future__ import annotations

import json
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.market_research.pipeline import run_demo

app = Flask(__name__, template_folder="templates", static_folder="static")
REPORT = ROOT / "artifacts" / "demo" / "report.json"


def load_report():
    if not REPORT.exists():
        run_demo(REPORT.parent)
    return json.loads(REPORT.read_text(encoding="utf-8"))


@app.get("/")
def index():
    return render_template("index.html", report=load_report())


@app.get("/api/report")
def report():
    return jsonify(load_report())


@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic-demo", "trading": "disabled"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

