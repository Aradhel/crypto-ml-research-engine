from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = ["ret_1", "momentum_6", "volatility_12", "volume_z", "range_pct", "rsi_14"]


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Build generic, causal features using closed candles only."""
    df = frame.sort_values("timestamp").copy()
    df["ret_1"] = df["close"].pct_change()
    df["momentum_6"] = df["close"].pct_change(6)
    df["volatility_12"] = df["ret_1"].rolling(12).std()
    volume_mean = df["volume"].rolling(24).mean()
    volume_std = df["volume"].rolling(24).std()
    df["volume_z"] = (df["volume"] - volume_mean) / volume_std
    df["range_pct"] = (df["high"] - df["low"]) / df["close"]
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi_14"] = 100 - (100 / (1 + rs))
    df["future_return"] = df["close"].shift(-1) / df["close"] - 1
    df["label"] = (df["future_return"] > 0).astype(int)
    return df.dropna(subset=FEATURE_COLUMNS + ["future_return"]).reset_index(drop=True)

