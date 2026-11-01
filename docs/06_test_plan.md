# 6. Test Plan and Results

## 6.1 Strategy
| Level | What | How |
|---|---|---|
| Unit | Metrics, formulas (safety stock, ROP, EOQ, ABC), each forecasting model | `tests/` with `unittest` |
| Integration | Data → forecast → inventory plan pipeline | `PlanTests.test_inventory_plan` |
| System / UAT | Dashboard flows UC-1 to UC-4 | Manual checklist below |
| Regression | Re-run all tests on every push | GitHub Actions (`.github/workflows/ci.yml`) |

Run the automated tests: `python -m unittest discover -s tests -v`

## 6.2 Sample test cases
| ID | Requirement | Input | Expected | Result |
|---|---|---|---|---|
| TC-01 | FR-06 | σ=10, L=4, service 95% | Safety stock ≈ 32.9 | Pass |
| TC-02 | FR-06 | demand 20, L=5, SS=30 | ROP = 130 | Pass |
| TC-03 | FR-06 | D=1000, S=50, H=2 | EOQ = √50000 ≈ 223.6 | Pass |
| TC-04 | FR-03 | Each model, horizon 14 | 14 non-negative values with next-day dates | Pass |
| TC-05 | FR-03 | Unknown model name | `ValueError` | Pass |
| TC-06 | FR-04 | Back-test table | Contains all models, sorted by wMAPE | Pass |
| TC-07 | FR-07/08 | Full pipeline | Status valid; orders > 0 only for "Reorder now" | Pass |
| TC-08 | FR-09 | Revenue 700/200/60/40 | A, B, ..., C classes | Pass |

## 6.3 Manual UAT checklist
- [ ] App opens with sample data and shows KPIs
- [ ] Changing service level changes safety stock / reorder points
- [ ] Forecast chart updates when product / model changes
- [ ] Uploading a CSV with missing columns shows an error
- [ ] Download buttons produce valid CSV files
