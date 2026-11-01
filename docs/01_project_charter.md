# 1. Project Charter

| Field | Details |
|---|---|
| Project title | Smart Inventory and Demand Forecasting System |
| Project manager / developer | Manish Yadav |
| Course | Software Project Management |
| Technology | Python, pandas, scikit-learn, Streamlit, GitHub |
| Duration | 8 weeks (see `03_wbs_and_schedule.md`) |

## Problem statement
Small and mid-size retailers decide stock levels by intuition. This causes **stock-outs** (lost sales) and
**overstock** (blocked capital, wastage). A data-driven system is needed to predict demand and recommend
when and how much to reorder.

## Objectives (SMART)
1. Forecast daily demand per product for a 7-90 day horizon with wMAPE below 20% on back-tests.
2. Compute safety stock, reorder point and EOQ for every product automatically.
3. Flag products as *Reorder now / Healthy / Overstock* and suggest order quantities.
4. Deliver a live web dashboard (Streamlit) and source code on GitHub within 8 weeks.

## Scope
**In scope:** data ingestion (CSV / sample data), 3 forecasting models, inventory formulas, ABC analysis,
dashboard, CSV export, automated tests, documentation.
**Out of scope:** real-time POS integration, multi-warehouse routing, supplier portals, user authentication.

## Stakeholders
| Stakeholder | Interest |
|---|---|
| Store owner / inventory manager | Fewer stock-outs, lower holding cost |
| Purchase department | Clear order quantities and budget |
| Project guide / evaluator | Process, documentation, working software |
| Developer (PM) | Delivery on time and in scope |

## Assumptions and constraints
- Historical daily sales data is available (sample data is generated when not).
- Free tools only (GitHub, Streamlit Community Cloud).
- Single developer; part-time effort.

## Success criteria
All objectives met, all unit tests passing in CI, app publicly reachable, documentation complete.
