import math
import unittest

import pandas as pd

from src.inventory import abc_classification, eoq, reorder_point, safety_stock, z_score


class InventoryFormulaTests(unittest.TestCase):
    def test_z_score_95(self):
        self.assertAlmostEqual(z_score(0.95), 1.645, places=3)

    def test_z_score_invalid(self):
        with self.assertRaises(ValueError):
            z_score(1.0)

    def test_safety_stock(self):
        # Z(0.95) * 10 * sqrt(4) = 1.645 * 20
        self.assertAlmostEqual(safety_stock(10, 4, 0.95), 32.9, places=1)

    def test_reorder_point(self):
        self.assertEqual(reorder_point(20, 5, 30), 130)

    def test_eoq(self):
        # sqrt(2 * 1000 * 50 / 2) = sqrt(50000)
        self.assertAlmostEqual(eoq(1000, 50, 2), math.sqrt(50000))

    def test_eoq_zero_demand(self):
        self.assertEqual(eoq(0, 50, 2), 0.0)

    def test_abc(self):
        rev = pd.Series({"a": 700, "b": 200, "c": 60, "d": 40})
        cls = abc_classification(rev)
        self.assertEqual(cls["a"], "A")
        self.assertEqual(cls["b"], "B")
        self.assertEqual(cls["d"], "C")


if __name__ == "__main__":
    unittest.main()
