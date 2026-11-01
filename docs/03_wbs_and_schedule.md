# 3. Work Breakdown Structure and Schedule

## 3.1 WBS
1. **Initiation** - charter, stakeholder list, feasibility
2. **Planning** - SRS, schedule, risk register, cost estimate
3. **Design** - architecture, module design, data model
4. **Development**
   - 4.1 Data generator / loader
   - 4.2 Forecasting models and evaluation
   - 4.3 Inventory optimisation module
   - 4.4 Streamlit dashboard
5. **Testing** - unit tests, integration test, user acceptance test
6. **Deployment** - GitHub repository, CI, Streamlit Cloud
7. **Closure** - final report, presentation, lessons learned

## 3.2 Schedule (8 weeks)
| Week | Activity | Deliverable | Depends on |
|---|---|---|---|
| 1 | Initiation and planning | Charter, SRS | - |
| 2 | Design | Architecture diagram, data model | SRS |
| 3 | Data module | `data_generator.py`, CSV format | Design |
| 4 | Forecasting module | `forecasting.py` + tests | Data module |
| 5 | Inventory module | `inventory.py` + tests | Forecasting |
| 6 | Dashboard | `app.py` | Modules 3-5 |
| 7 | Testing and fixes | Test report, CI green | Dashboard |
| 8 | Deployment and closure | Live URL, final report | Testing |

## 3.3 Gantt chart (text)
```
Week:              1  2  3  4  5  6  7  8
Initiation/Plan    ██
Design                ██
Data module              ██
Forecasting                 ██
Inventory                      ██
Dashboard                         ██
Testing                              ██
Deploy/Closure                          ██
```

## 3.4 Critical path
SRS → Design → Forecasting module → Inventory module → Dashboard → Testing → Deployment.
Any delay in the forecasting module delays the whole project (it has zero slack).

## 3.5 Milestones
| # | Milestone | Week |
|---|---|---|
| M1 | Requirements approved | 1 |
| M2 | Design complete | 2 |
| M3 | Core engine (data + forecast + inventory) working | 5 |
| M4 | Dashboard demo | 6 |
| M5 | Live deployment | 8 |
