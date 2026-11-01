# 5. Cost and Effort Estimation

## 5.1 Basic COCOMO (organic mode)
Source size measured from the code (non-blank, non-comment lines in `app.py` and `src/`): **≈ 380 LOC = 0.38 KLOC**

- Effort E = 2.4 × (KLOC)^1.05 = 2.4 × 0.38^1.05 ≈ **0.87 person-months**
- Development time D = 2.5 × E^0.38 ≈ **2.4 months**
- Average staff = E / D ≈ **0.4 persons**

> COCOMO is calibrated for much larger systems, so for a project this small it underestimates the real effort
> (research, learning, documentation, testing). Planned effort is therefore based on the bottom-up estimate below.

## 5.2 Bottom-up estimate (person-days)
| Activity | Days |
|---|---|
| Requirements and planning | 4 |
| Design | 3 |
| Data module | 3 |
| Forecasting module | 6 |
| Inventory module | 4 |
| Dashboard | 5 |
| Testing and CI | 4 |
| Deployment | 2 |
| Documentation and report | 5 |
| **Total** | **36 days** |

## 5.3 Cost (illustrative)
| Item | Basis | Cost (₹) |
|---|---|---|
| Developer effort | 36 days × ₹1,500/day (student-rate assumption) | 54,000 |
| Hosting (Streamlit Cloud, GitHub) | Free tier | 0 |
| Software licences | Open source | 0 |
| Contingency | 10% | 5,400 |
| **Total** | | **59,400** |

## 5.4 Expected benefit
If forecasting reduces stock-outs and overstock by even 5% of a ₹10,00,000 yearly inventory spend, the
saving is about ₹50,000 per year, so the investment pays back in roughly a year (figures illustrative).
