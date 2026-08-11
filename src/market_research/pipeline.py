from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .evaluation import walk_forward_evaluate
from .features import build_features
from .synthetic import generate_market_data


def run_demo(output_dir: Path = Path("artifacts/demo")) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = generate_market_data()
    features = build_features(raw)
    summary, folds, predictions = walk_forward_evaluate(features)
    raw.tail(300).to_csv(output_dir / "synthetic_market.csv", index=False)
    pd.DataFrame(predictions).to_csv(output_dir / "paper_predictions.csv", index=False)
    report = {"summary": summary, "folds": folds}
    (output_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the synthetic research demo")
    parser.add_argument("--demo", action="store_true", help="Generate synthetic data and run evaluation")
    args = parser.parse_args()
    if args.demo:
        print(json.dumps(run_demo(), indent=2))

