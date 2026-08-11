from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURE_COLUMNS


@dataclass
class FoldResult:
    fold: int
    train_rows: int
    test_rows: int
    auc: float
    brier: float
    log_loss: float
    trades: int
    net_ev_pct: float


def _model() -> Pipeline:
    base = Pipeline([
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    return CalibratedClassifierCV(base, method="sigmoid", cv=3)


def walk_forward_evaluate(df, threshold: float = 0.55, cost_pct: float = 0.14,
                          folds: int = 5, embargo_rows: int = 6):
    """Expanding-window evaluation with an embargo between train and test."""
    n = len(df)
    test_size = n // (folds + 2)
    results, predictions = [], []
    for fold in range(folds):
        test_start = test_size * (fold + 2)
        test_end = min(test_start + test_size, n)
        train_end = max(0, test_start - embargo_rows)
        train, test = df.iloc[:train_end], df.iloc[test_start:test_end]
        if len(train) < 100 or len(test) < 20 or test["label"].nunique() < 2:
            continue
        model = _model()
        model.fit(train[FEATURE_COLUMNS], train["label"])
        proba = model.predict_proba(test[FEATURE_COLUMNS])[:, 1]
        selected = proba >= threshold
        net_returns = np.where(selected, test["future_return"].to_numpy() * 100 - cost_pct, 0.0)
        results.append(FoldResult(
            fold=fold + 1, train_rows=len(train), test_rows=len(test),
            auc=float(roc_auc_score(test["label"], proba)),
            brier=float(brier_score_loss(test["label"], proba)),
            log_loss=float(log_loss(test["label"], proba)),
            trades=int(selected.sum()),
            net_ev_pct=float(net_returns[selected].mean()) if selected.any() else 0.0,
        ))
        for ts, p, actual, selected_flag, pnl in zip(
                test["timestamp"], proba, test["label"], selected, net_returns):
            predictions.append({"timestamp": ts.isoformat(), "probability": float(p),
                                "actual": int(actual), "selected": bool(selected_flag),
                                "net_return_pct": float(pnl)})
    summary = {
        "folds": len(results),
        "avg_auc": float(np.mean([r.auc for r in results])) if results else None,
        "avg_brier": float(np.mean([r.brier for r in results])) if results else None,
        "avg_log_loss": float(np.mean([r.log_loss for r in results])) if results else None,
        "total_trades": int(sum(r.trades for r in results)),
        "avg_net_ev_pct": float(np.mean([r.net_ev_pct for r in results])) if results else None,
        "threshold": threshold,
        "round_trip_cost_pct": cost_pct,
        "paper_trading_only": True,
    }
    return summary, [asdict(r) for r in results], predictions

