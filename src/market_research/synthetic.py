from __future__ import annotations

import numpy as np
import pandas as pd


def generate_market_data(rows: int = 2400, seed: int = 42) -> pd.DataFrame:
    """Create deterministic OHLCV data with several volatility regimes."""
    rng = np.random.default_rng(seed)
    timestamp = pd.date_range("2024-01-01", periods=rows, freq="4h", tz="UTC")
    regime = np.repeat([0, 1, 2, 1], repeats=[rows // 4] * 3 + [rows - 3 * (rows // 4)])
    drift = np.choose(regime, [0.00035, -0.00015, 0.00005])
    volatility = np.choose(regime, [0.009, 0.017, 0.012])
    returns = drift + rng.normal(0, volatility, rows)
    close = 30000 * np.exp(np.cumsum(returns))
    spread = np.abs(rng.normal(0.006, 0.003, rows))
    high = close * (1 + spread)
    low = close * (1 - spread)
    open_ = np.r_[close[0], close[:-1]]
    volume = rng.lognormal(mean=10.5, sigma=0.55, size=rows) * (1 + regime * 0.2)
    return pd.DataFrame({
        "timestamp": timestamp,
        "open": open_, "high": high, "low": low, "close": close,
        "volume": volume, "regime": regime,
    })

