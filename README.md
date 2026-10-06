# Rosa's Pizza Promise Planner

This Streamlit app compares delivery promises using the seeded delivery-time simulator from `rosa-starter`. For each promise, it counts orders and late deliveries, then estimates net profit as:

`orders × profit margin − late orders × (refund cost + churned orders × profit margin)`

`core.py` contains the calculation without any Streamlit code. `app.py` displays the inputs and remembers the latest recommendation when a control changes. The default zone and time block match the Part II example in the assignment notebook.

## Run locally

Install the project dependencies with `uv sync`, then start the app:

```powershell
uv run streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`.
