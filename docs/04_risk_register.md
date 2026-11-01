# 4. Risk Register

Probability (P) and Impact (I) scored 1-5; Exposure = P × I.

| ID | Risk | P | I | Exposure | Mitigation | Contingency |
|---|---|---|---|---|---|---|
| R1 | No real sales data available | 4 | 3 | 12 | Built-in synthetic data generator | Use public retail datasets |
| R2 | Forecast accuracy too low | 3 | 4 | 12 | Three models + auto-selection, back-testing | Tune parameters, add features |
| R3 | Scope creep (extra features) | 3 | 3 | 9 | Fixed scope in charter, change-control | Move extras to "future work" |
| R4 | Streamlit Cloud deployment fails (dependency issue) | 2 | 4 | 8 | Pinned minimal `requirements.txt`, test locally | Deploy on Hugging Face Spaces / Render |
| R5 | Developer unavailable (illness / exams) | 3 | 4 | 12 | Buffer in schedule, weekly commits | Reduce optional features |
| R6 | Bugs in formulas | 2 | 5 | 10 | Unit tests with hand-computed values, CI | Peer review of formulas |
| R7 | Data loss | 1 | 5 | 5 | Git version control, GitHub remote | Restore from repository |
| R8 | Uploaded CSV in wrong format | 4 | 2 | 8 | Column validation with clear error message | Provide sample files |

**Top risks to watch:** R1, R2, R5 (exposure 12).
