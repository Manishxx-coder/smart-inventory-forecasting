"""Synthetic data generator for the Smart Inventory & Demand Forecasting System.

Produces a product master table and a daily sales history with trend,
weekly seasonality, yearly seasonality, promotions and random noise, so the
app works out-of-the-box without any real company data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PRODUCT_CATALOG = [
    # id, name, category, base daily demand, unit cost, unit price, lead time (days)
    ("P001", "Wireless Mouse", "Electronics", 38, 350, 599, 7),
    ("P002", "USB-C Cable", "Electronics", 60, 90, 199, 5),
    ("P003", "Notebook A4", "Stationery", 85, 25, 60, 4),
    ("P004", "Gel Pen Pack", "Stationery", 70, 40, 99, 4),
    ("P005", "Water Bottle", "Home", 30, 120, 299, 10),
    ("P006", "Desk Lamp", "Home", 14, 450, 899, 12),
    ("P007", "Protein Bar Box", "Grocery", 45, 300, 499, 6),
    ("P008", "Green Tea Pack", "Grocery", 52, 110, 220, 6),
]


def generate_products(seed: int = 42) -> pd.DataFrame:
    """Return the product master table (cost, price, lead time, stock...)."""
    rng = np.random.default_rng(seed)
    rows = []
    for pid, name, cat, base, cost, price, lead in PRODUCT_CATALOG:
        rows.append(
            {
                "product_id": pid,
                "product_name": name,
                "category": cat,
                "unit_cost": cost,
                "unit_price": price,
                "lead_time_days": lead,
                "ordering_cost": int(rng.integers(300, 900)),  # cost per purchase order
                "holding_cost_rate": 0.20,  # 20% of unit cost per year
                "current_stock": int(base * rng.integers(4, 20)),
            }
        )
    return pd.DataFrame(rows)


def generate_sales(days: int = 730, end_date: str | None = None, seed: int = 42) -> pd.DataFrame:
    """Return a daily sales history: date, product_id, units_sold, on_promo."""
    rng = np.random.default_rng(seed)
    end = pd.Timestamp(end_date) if end_date else pd.Timestamp.today().normalize()
    dates = pd.date_range(end=end, periods=days, freq="D")
    t = np.arange(days)
    records = []
    for pid, _name, cat, base, *_ in PRODUCT_CATALOG:
        trend = 1 + rng.uniform(-0.1, 0.4) * t / days
        weekly = 1 + 0.25 * np.sin(2 * np.pi * (dates.dayofweek.values - rng.integers(0, 7)) / 7)
        yearly_amp = 0.30 if cat in ("Grocery", "Home") else 0.15
        yearly = 1 + yearly_amp * np.sin(2 * np.pi * (dates.dayofyear.values / 365.25) + rng.uniform(0, 6))
        promo = rng.random(days) < 0.05
        promo_lift = np.where(promo, 1.6, 1.0)
        lam = base * trend * weekly * yearly * promo_lift
        units = rng.poisson(np.clip(lam, 0.1, None))
        records.append(
            pd.DataFrame({"date": dates, "product_id": pid, "units_sold": units, "on_promo": promo.astype(int)})
        )
    return pd.concat(records, ignore_index=True)


def generate_all(days: int = 730, seed: int = 42):
    """Convenience: (products_df, sales_df)."""
    return generate_products(seed), generate_sales(days=days, seed=seed)


if __name__ == "__main__":
    import pathlib

    out = pathlib.Path(__file__).resolve().parents[1] / "data"
    out.mkdir(exist_ok=True)
    products, sales = generate_all()
    products.to_csv(out / "products.csv", index=False)
    sales.to_csv(out / "sales_history.csv", index=False)
    print(f"Saved {len(products)} products and {len(sales)} sales rows to {out}")
