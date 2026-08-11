from __future__ import annotations


def replay_sl_tp(candles, direction: str, stop_loss: float, take_profit: float):
    """Replay ordered candles; same-candle ambiguity is resolved SL-first."""
    direction = direction.upper()
    for candle in candles:
        high, low = float(candle["high"]), float(candle["low"])
        if direction == "LONG":
            if low <= stop_loss:
                return "stop_loss", stop_loss
            if high >= take_profit:
                return "take_profit", take_profit
        elif direction == "SHORT":
            if high >= stop_loss:
                return "stop_loss", stop_loss
            if low <= take_profit:
                return "take_profit", take_profit
        else:
            raise ValueError("direction must be LONG or SHORT")
    return None, None

