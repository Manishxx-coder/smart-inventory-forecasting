"""Inventory optimisation formulas: safety stock, reorder point, EOQ, ABC analysis."""
from __future__ import annotations

import math
from statistics import NormalDist

import pandas as pd


def z_score(service_level: float) -> float:
    """Z-value for a cycle service level (e.g. 0.95 -> 1.645)."""
    if not 0.5 <= service_level < 1:
        raise ValueError("service_level must be in [0.5, 1).")
    return NormalDist().inv_cdf(service_level)


def safety_stock(daily_std: float, lead_time_days: float, service_level: float = 0.95) -> float:
    """SS = Z * sigma_daily * sqrt(lead time)."""
    return z_score(service_level) * daily_std * math.sqrt(lead_time_days)


def reorder_point(daily_demand: float, lead_time_days: float, safety_stock_units: float) -> float:
    """ROP = demand during lead time + safety stock."""
    return daily_demand * lead_time_days + safety_stock_units


def eoq(annual_demand: float, ordering_cost: float, holding_cost_per_unit: float) -> float:
    """Economic Order Quantity = sqrt(2 D S / H)."""
    if annual_demand <= 0 or holding_cost_per_unit <= 0:
        return 0.0
    return math.sqrt(2 * annual_demand * ordering_cost / holding_cost_per_unit)


def abc_classification(revenue: pd.Series, a_cut: float = 0.70, b_cut: float = 0.90) -> pd.Series:
    """Classify items A/B/C by cumulative share of revenue (Pareto)."""
    ordered = revenue.sort_values(ascending=False)
    cum_share = ordered.cumsum() / ordered.sum()
    # An item is A if the cumulative share *before* it is still under the cut-off.
    prev = cum_share.shift(fill_value=0)
    classes = pd.Series("C", index=ordered.index)
    classes[prev < b_cut] = "B"
    classes[prev < a_cut] = "A"
    return classes.reindex(revenue.index)


def build_inventory_plan(
    products: pd.DataFrame,
    daily_history: dict[str, pd.Series],
    forecasts: dict[str, pd.Series],
    service_level: float = 0.95,
    overstock_days: int = 60,
) -> pd.DataFrame:
    """Create the replenishment plan for every product.

    `daily_history[pid]` - historical daily units, `forecasts[pid]` - future daily forecast.
    """
    rows = []
    for _, p in products.iterrows():
        pid = p["product_id"]
        hist, fc = daily_history[pid], forecasts[pid]
        daily_demand = float(fc.mean())
        daily_std = float(hist.tail(90).std(ddof=1))
        ss = safety_stock(daily_std, p["lead_time_days"], service_level)
        rop = reorder_point(daily_demand, p["lead_time_days"], ss)
        holding = p["unit_cost"] * p["holding_cost_rate"]
        q_eoq = eoq(daily_demand * 365, p["ordering_cost"], holding)
        stock = float(p["current_stock"])
        days_cover = stock / daily_demand if daily_demand > 0 else float("inf")

        if stock <= rop:
            status = "Reorder now"
            # Order enough to get back above ROP, at least one EOQ.
            order_qty = max(q_eoq, rop + q_eoq - stock)
        elif days_cover > overstock_days:
            status, order_qty = "Overstock", 0.0
        else:
            status, order_qty = "Healthy", 0.0

        rows.append(
            {
                "product_id": pid,
                "product_name": p["product_name"],
                "category": p["category"],
                "current_stock": int(stock),
                "avg_daily_forecast": round(daily_demand, 1),
                "safety_stock": math.ceil(ss),
                "reorder_point": math.ceil(rop),
                "eoq": math.ceil(q_eoq),
                "days_of_cover": round(days_cover, 1),
                "status": status,
                "suggested_order_qty": math.ceil(order_qty),
                "order_cost": round(math.ceil(order_qty) * p["unit_cost"], 2),
            }
        )
    return pd.DataFrame(rows)
