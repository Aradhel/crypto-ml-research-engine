import unittest

from src.market_research.trade_math import replay_sl_tp


class ReplayTests(unittest.TestCase):
    def test_long_take_profit(self):
        reason, price = replay_sl_tp([{"high": 106, "low": 99}], "LONG", 98, 105)
        self.assertEqual((reason, price), ("take_profit", 105))

    def test_short_take_profit(self):
        reason, price = replay_sl_tp([{"high": 101, "low": 94}], "SHORT", 102, 95)
        self.assertEqual((reason, price), ("take_profit", 95))

    def test_same_candle_is_stop_first(self):
        reason, _ = replay_sl_tp([{"high": 106, "low": 97}], "LONG", 98, 105)
        self.assertEqual(reason, "stop_loss")

    def test_order_is_preserved(self):
        candles = [{"high": 104, "low": 97}, {"high": 106, "low": 99}]
        reason, _ = replay_sl_tp(candles, "LONG", 98, 105)
        self.assertEqual(reason, "stop_loss")


if __name__ == "__main__":
    unittest.main()

