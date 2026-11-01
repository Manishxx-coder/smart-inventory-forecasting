# 📦 Smart Inventory and Demand Forecasting System

A Python + Streamlit application that forecasts product demand and tells you **what to reorder, when, and how much**.
Built as a **Software Project Management** project - the `docs/` folder contains the full set of project
management artefacts (charter, SRS, WBS/schedule, risk register, cost estimation, test plan, architecture).

**Live demo:** _add your Streamlit URL here after deployment_

## Features
- Demand forecasting with **Moving Average**, **Holt-Winters** and **Random Forest** (auto-selects the best per product)
- Back-testing with MAE, RMSE and wMAPE
- **Safety stock, reorder point and EOQ** based on your target service level
- Status per product: *Reorder now / Healthy / Overstock* with suggested order quantity and cost
- **ABC (Pareto) analysis**
- Works with built-in sample data or your own CSV files
- CSV export, unit tests, GitHub Actions CI

## Project structure
```
smart-inventory-forecasting/
├── app.py                  # Streamlit dashboard
├── requirements.txt
├── src/
│   ├── data_generator.py   # synthetic sales + product data
│   ├── forecasting.py      # models + evaluation
│   └── inventory.py        # SS, ROP, EOQ, ABC, replenishment plan
├── data/                   # sample CSVs (also the upload format)
├── tests/                  # unit + integration tests
├── docs/                   # project management documents
└── .github/workflows/ci.yml
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Run tests: `python -m unittest discover -s tests -v`

## Using your own data
Upload two CSVs in the sidebar (examples in `data/`):
- `sales_history.csv`: `date, product_id, units_sold`
- `products.csv`: `product_id, product_name, category, unit_cost, unit_price, lead_time_days, ordering_cost, holding_cost_rate, current_stock`

## Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Smart Inventory and Demand Forecasting System"
git branch -M main
git remote add origin https://github.com/<your-username>/smart-inventory-forecasting.git
git push -u origin main
```

## Deploy live on Streamlit Community Cloud (free)
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → choose your repository, branch `main`, main file `app.py`.
3. Click **Deploy**. In a few minutes you get a public URL - paste it at the top of this README.

## Tech stack
Python · pandas · NumPy · scikit-learn · Streamlit · GitHub Actions

## Author
Manish Yadav - Software Project Management project
