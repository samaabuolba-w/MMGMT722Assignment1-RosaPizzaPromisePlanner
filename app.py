import streamlit as st

from core import COSTS, TIME_BLOCKS, ZONES, evaluate_promises, promise_values


st.set_page_config(page_title="Rosa's Pizza Promise Planner", layout="centered")
st.title("Rosa's Pizza")
st.caption("Promise-time profit planner")

zone_column, time_column = st.columns(2)
with zone_column:
    zone = st.selectbox("Delivery zone", ZONES, index=ZONES.index("Far West"))
with time_column:
    time_block = st.selectbox(
        "Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve")
    )

promise_minimum, promise_maximum = st.slider(
    "Promise-time range (minutes)",
    min_value=5,
    max_value=50,
    value=(5, 50),
    step=5,
)

margin_column, churn_column, refund_column = st.columns(3)
with margin_column:
    margin = st.number_input(
        "Profit per order ($)", min_value=0.0, value=float(COSTS["margin"]), step=0.5
    )
with churn_column:
    churn_orders = st.number_input(
        "Churned orders per late order",
        min_value=0.0,
        value=float(COSTS["churn_orders"]),
        step=0.1,
    )
with refund_column:
    refund_cost = st.number_input(
        "Refund per late order ($)", min_value=0.0, value=float(COSTS["refund"]), step=1.0
    )

if st.button("Recommend a promise", type="primary"):
    selected_costs = {
        "margin": margin,
        "churn_orders": churn_orders,
        "refund": refund_cost,
    }
    promises = promise_values(promise_minimum, promise_maximum)
    best, options = evaluate_promises(zone, time_block, promises, selected_costs)
    st.session_state["analysis_result"] = {
        "zone": zone,
        "time_block": time_block,
        "promise_range": (promise_minimum, promise_maximum),
        "best": best,
        "options": options,
    }

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.subheader("Recommendation")
    st.caption(
        f"Last calculation: {result['zone']} / {result['time_block']} / "
        f"{result['promise_range'][0]}-{result['promise_range'][1]} minutes"
    )
    promise_column, profit_column, late_column = st.columns(3)
    promise_column.metric("Recommended promise", f"{result['best']['Promise (minutes)']} min")
    profit_column.metric("Net profit", f"${result['best']['Net profit ($)']:,.2f}")
    late_column.metric("Late orders", result["best"]["Late orders"])
    st.dataframe(result["options"], hide_index=True, use_container_width=True)