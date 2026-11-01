# 2. Software Requirements Specification (SRS)

## 2.1 Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The system shall load sample data or user-uploaded sales and product CSV files. | High |
| FR-02 | The system shall validate required columns and show a clear error when missing. | High |
| FR-03 | The system shall forecast daily demand with Moving Average, Holt-Winters and Random Forest. | High |
| FR-04 | The system shall back-test models on a 28-day hold-out and report MAE, RMSE and wMAPE. | High |
| FR-05 | The system shall automatically pick the best model per product ("Auto" mode). | Medium |
| FR-06 | The system shall compute safety stock, reorder point and EOQ using a user-selected service level. | High |
| FR-07 | The system shall classify each product as Reorder now / Healthy / Overstock. | High |
| FR-08 | The system shall suggest order quantity and cost for products needing reorder. | High |
| FR-09 | The system shall perform ABC (Pareto) analysis on 12-month revenue. | Medium |
| FR-10 | The system shall let users download the plan and data as CSV. | Medium |

## 2.2 Non-functional requirements
| ID | Requirement |
|---|---|
| NFR-01 | Performance: dashboard refresh with 8 products / 2 years of data in under 15 seconds (results cached). |
| NFR-02 | Usability: single-page dashboard, controls in a sidebar, no training required. |
| NFR-03 | Portability: runs on Windows / Linux / macOS with Python 3.10+. |
| NFR-04 | Maintainability: modular code (`src/`), type hints, unit tests, CI pipeline. |
| NFR-05 | Reliability: models fall back gracefully when history is too short. |

## 2.3 Input data format
**sales_history.csv**: `date, product_id, units_sold` (optional `on_promo`)
**products.csv**: `product_id, product_name, category, unit_cost, unit_price, lead_time_days, ordering_cost, holding_cost_rate, current_stock`

## 2.4 Use cases
| Use case | Actor | Summary |
|---|---|---|
| UC-1 View inventory plan | Inventory manager | Opens app, sees which products to reorder and quantities. |
| UC-2 Inspect forecast | Inventory manager | Selects product and checks forecast chart and model used. |
| UC-3 Upload own data | Inventory manager | Uploads CSV files; app recomputes everything. |
| UC-4 Export plan | Purchase officer | Downloads the recommended orders as CSV. |

## 2.5 Formulas used
- Safety stock = Z × σ(daily demand) × √(lead time)
- Reorder point = average daily demand × lead time + safety stock
- EOQ = √(2 × annual demand × ordering cost / holding cost per unit)
- wMAPE = Σ|actual − forecast| / Σ actual × 100
