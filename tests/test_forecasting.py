import unittest

import numpy as np
import pandas as pd

from src.data_generator import generate_all
from src.forecasting import (
    MODEL_NAMES,
    evaluate_models,
    forecast,
    mae,
    rmse,
    wmape,
)
from src.inventory import build_inventory_plan


def _series(n=200, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2025-01-01", periods=n, freq="D")
    weekly = 1 + 0.3 * np.sin(2 * np.pi * np.arange(n) / 7)
    return pd.Series(rng.poisson(50 * weekly), index=idx, dtype=float)


class MetricTests(unittest.TestCase):
    def test_metrics(self):
        self.assertEqual(mae([10, 20], [12, 18]), 2)
        self.assertAlmostEqual(rmse([10, 20], [12, 18]), 2)
        self.assertAlmostEqual(wmape([10, 20], [12, 18]), 100 * 4 / 30)

    def test_wmape_zero_actual(self):
        self.assertTrue(np.isnan(wmape([0, 0], [1, 1])))


class ForecastTests(unittest.TestCase):
    def test_all_models_return_horizon(self):
        s = _series()
        for m in MODEL_NAMES:
            f = forecast(s, 14, m)
            self.assertEqual(len(f), 14)
            self.assertTrue((f >= 0).all())
            self.assertEqual(f.index[0], s.index[-1] + pd.Timedelta(days=1))

    def test_unknown_model(self):
        with self.assertRaises(ValueError):
            forecast(_series(), 7, "Magic")

    def test_evaluation_table(self):
        table = evaluate_models(_series(), holdout=21)
        self.assertEqual(set(table["model"]), set(MODEL_NAMES))
        self.assertTrue(table["wmape"].is_monotonic_increasing)

    def test_seasonal_models_beat_flat_baseline(self):
        table = evaluate_models(_series(300), holdout=28).set_index("model")
        self.assertLess(table.loc["Holt-Winters", "wmape"], table.loc["Moving Average", "wmape"])


class PlanTests(unittest.TestCase):
    def test_inventory_plan(self):
        products, sales = generate_all(days=200)
        hist = {
            pid: g.set_index("date")["units_sold"].astype(float)
            for pid, g in sales.groupby("product_id")
        }
        fcs = {pid: forecast(s, 14, "Holt-Winters") for pid, s in hist.items()}
        plan = build_inventory_plan(products, hist, fcs, service_level=0.95)
        self.assertEqual(len(plan), len(products))
        self.assertTrue(set(plan["status"]) <= {"Reorder now", "Healthy", "Overstock"})
        reorder = plan[plan["status"] == "Reorder now"]
        self.assertTrue((reorder["suggested_order_qty"] > 0).all())
        healthy = plan[plan["status"] != "Reorder now"]
        self.assertTrue((healthy["suggested_order_qty"] == 0).all())


if __name__ == "__main__":
    unittest.main()
