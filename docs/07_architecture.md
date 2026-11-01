# 7. Architecture and Design

```
            +--------------------+
            |  Streamlit UI      |   app.py
            |  (dashboard)       |
            +---------+----------+
                      |
      +---------------+----------------+
      |                                |
+-----v-------+   +-------------+  +---v-----------+
| data_       |   | forecasting |  | inventory     |
| generator   |   | .py         |  | .py           |
| (sample/CSV)|   | MA / HW / RF|  | SS, ROP, EOQ, |
+-----+-------+   +------+------+  | ABC, plan     |
      |                  |         +---+-----------+
      +---- sales/products data -------+
```

**Style:** layered, modular monolith. UI (presentation) → business logic (`src/`) → data.
**Design principles:** single responsibility per module, pure functions for formulas (easy to unit test),
caching of expensive forecasts with `st.cache_data`.

## Data model
- `products(product_id PK, product_name, category, unit_cost, unit_price, lead_time_days, ordering_cost, holding_cost_rate, current_stock)`
- `sales(date, product_id FK, units_sold, on_promo)`

## Technology choices
| Need | Choice | Reason |
|---|---|---|
| UI | Streamlit | Python-only, free live hosting |
| Data | pandas / numpy | Standard |
| ML | scikit-learn | Reliable Random Forest |
| Forecast baseline | Holt-Winters written from scratch | Fewer dependencies, easier deployment |
| Testing | unittest | No extra dependency |
| CI | GitHub Actions | Free with GitHub |
