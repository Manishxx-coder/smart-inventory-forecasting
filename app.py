"""Smart Inventory & Demand Forecasting System - Streamlit app.

Run locally:   streamlit run app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data_generator import generate_all
from src.forecasting import MODEL_NAMES, best_model, evaluate_models, forecast
from src.inventory import abc_classification, build_inventory_plan

st.set_page_config(page_title="Smart Inventory & Demand Forecasting", page_icon="📦", layout="wide")


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def load_sample():
    return generate_all(days=730)


def load_uploaded(sales_file, products_file):
    sales = pd.read_csv(sales_file, parse_dates=["date"])
    products = pd.read_csv(products_file)
    required_sales = {"date", "product_id", "units_sold"}
    required_prod = {
        "product_id", "product_name", "category", "unit_cost", "unit_price",
        "lead_time_days", "ordering_cost", "holding_cost_rate", "current_stock",
    }
    if not required_sales <= set(sales.columns):
        raise ValueError(f"Sales CSV needs columns: {sorted(required_sales)}")
    if not required_prod <= set(products.columns):
        raise ValueError(f"Products CSV needs columns: {sorted(required_prod)}")
    return products, sales


def daily_series(sales: pd.DataFrame) -> dict[str, pd.Series]:
    out = {}
    for pid, g in sales.groupby("product_id"):
        s = g.groupby("date")["units_sold"].sum().astype(float)
        s = s.reindex(pd.date_range(s.index.min(), s.index.max(), freq="D"), fill_value=0.0)
        out[pid] = s
    return out


@st.cache_data(show_spinner="Running forecasts...")
def run_forecasts(sales: pd.DataFrame, horizon: int, model_choice: str):
    hist = daily_series(sales)
    fcs, used = {}, {}
    for pid, s in hist.items():
        model = best_model(s) if model_choice == "Auto (best model)" else model_choice
        fcs[pid] = forecast(s, horizon, model)
        used[pid] = model
    return hist, fcs, used


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
st.sidebar.title("📦 Controls")
source = st.sidebar.radio("Data source", ["Sample data", "Upload CSV files"])

if source == "Upload CSV files":
    sales_up = st.sidebar.file_uploader("Sales history CSV", type="csv")
    prod_up = st.sidebar.file_uploader("Products CSV", type="csv")
    if not (sales_up and prod_up):
        st.info("Upload both files in the sidebar, or switch to **Sample data**. "
                "Download the sample CSVs from the *Data* tab to see the required format.")
        st.stop()
    try:
        products, sales = load_uploaded(sales_up, prod_up)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Could not read files: {exc}")
        st.stop()
else:
    products, sales = load_sample()

horizon = st.sidebar.slider("Forecast horizon (days)", 7, 90, 30)
model_choice = st.sidebar.selectbox("Forecast model", ["Auto (best model)"] + MODEL_NAMES)
service_level = st.sidebar.slider("Target service level", 0.80, 0.99, 0.95, 0.01)

history, forecasts, models_used = run_forecasts(sales, horizon, model_choice)
plan = build_inventory_plan(products, history, forecasts, service_level)

# --------------------------------------------------------------------------- #
# Header + KPIs
# --------------------------------------------------------------------------- #
st.title("Smart Inventory & Demand Forecasting System")
st.caption("Forecast demand, calculate safety stock / reorder points / EOQ, and get purchase recommendations.")

n_reorder = int((plan["status"] == "Reorder now").sum())
n_over = int((plan["status"] == "Overstock").sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Products tracked", len(plan))
c2.metric("Need reorder now", n_reorder)
c3.metric("Overstocked", n_over)
c4.metric("Purchase budget needed", f"₹{plan['order_cost'].sum():,.0f}")

tab_plan, tab_fc, tab_abc, tab_acc, tab_data = st.tabs(
    ["🛒 Inventory plan", "📈 Demand forecast", "🏷️ ABC analysis", "🎯 Model accuracy", "🗂️ Data"]
)

# --------------------------------------------------------------------------- #
# Tab 1 - inventory plan
# --------------------------------------------------------------------------- #
with tab_plan:
    st.subheader("Replenishment recommendations")

    def colour(row):
        palette = {"Reorder now": "#ffd6d6", "Overstock": "#fff3cd", "Healthy": "#d9f2d9"}
        return [f"background-color: {palette[row['status']]}"] * len(row)

    st.dataframe(plan.style.apply(colour, axis=1), use_container_width=True, hide_index=True)
    st.download_button("Download plan (CSV)", plan.to_csv(index=False), "inventory_plan.csv", "text/csv")
    st.markdown(
        "**How it works** - Safety stock = Z × σ × √lead time · Reorder point = demand during lead time + "
        "safety stock · EOQ = √(2DS/H). Stock at or below the reorder point triggers an order."
    )

# --------------------------------------------------------------------------- #
# Tab 2 - forecast
# --------------------------------------------------------------------------- #
with tab_fc:
    names = dict(zip(products["product_id"], products["product_name"]))
    pid = st.selectbox("Product", list(names), format_func=lambda x: f"{x} - {names[x]}")
    show_days = st.slider("History to show (days)", 30, 365, 120)
    h = history[pid].tail(show_days).rename("Actual")
    f = forecasts[pid].rename("Forecast")
    chart_df = pd.concat([h, f], axis=1)
    st.line_chart(chart_df)
    st.caption(f"Model used: **{models_used[pid]}** · Next {horizon} days forecast total: "
               f"**{f.sum():,.0f} units**")

# --------------------------------------------------------------------------- #
# Tab 3 - ABC
# --------------------------------------------------------------------------- #
with tab_abc:
    price = products.set_index("product_id")["unit_price"]
    recent = sales[sales["date"] >= sales["date"].max() - pd.Timedelta(days=365)]
    revenue = recent.groupby("product_id")["units_sold"].sum() * price
    abc = pd.DataFrame({"revenue": revenue, "class": abc_classification(revenue)})
    abc.insert(0, "product", abc.index.map(names))
    abc = abc.sort_values("revenue", ascending=False)
    st.subheader("Revenue contribution (last 12 months)")
    st.bar_chart(abc.set_index("product")["revenue"])
    st.dataframe(abc, use_container_width=True)
    st.caption("A = top ~70% of revenue (tight control), B = next ~20%, C = remaining ~10%.")

# --------------------------------------------------------------------------- #
# Tab 4 - accuracy
# --------------------------------------------------------------------------- #
with tab_acc:
    pid2 = st.selectbox("Product ", list(names), format_func=lambda x: f"{x} - {names[x]}", key="acc")
    st.write("Back-test on the last 28 days (lower is better):")
    st.dataframe(evaluate_models(history[pid2], holdout=28).round(2), use_container_width=True, hide_index=True)
    st.caption("wMAPE = weighted mean absolute percentage error.")

# --------------------------------------------------------------------------- #
# Tab 5 - data
# --------------------------------------------------------------------------- #
with tab_data:
    st.subheader("Products")
    st.dataframe(products, use_container_width=True, hide_index=True)
    st.download_button("Download products.csv", products.to_csv(index=False), "products.csv", "text/csv")
    st.subheader("Sales history (latest 200 rows)")
    st.dataframe(sales.sort_values("date").tail(200), use_container_width=True, hide_index=True)
    st.download_button("Download sales_history.csv", sales.to_csv(index=False), "sales_history.csv", "text/csv")
