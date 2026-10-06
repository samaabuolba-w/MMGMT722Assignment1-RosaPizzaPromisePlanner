from starter import COSTS, TIME_BLOCKS, ZONES, delivery_times


def promise_values(minimum, maximum, step=5):
    if minimum <= 0 or maximum < minimum or step <= 0:
        raise ValueError("Promise range must be positive and step must be greater than zero.")
    if (maximum - minimum) % step:
        raise ValueError("Promise range must be divisible by its step.")
    return list(range(minimum, maximum + 1, step))


def evaluate_promises(zone, time_block, promises, costs, seed=1):
    if not promises:
        raise ValueError("At least one promise time is required.")

    cost_per_late_order = costs["refund"] + costs["churn_orders"] * costs["margin"]
    results = []

    for promise in promises:
        times = delivery_times(zone, time_block, promise, seed=seed)
        total_orders = len(times)
        late_orders = int((times > promise).sum())
        net_profit = total_orders * costs["margin"] - late_orders * cost_per_late_order
        results.append(
            {
                "Promise (minutes)": promise,
                "Total orders": total_orders,
                "Late orders": late_orders,
                "Net profit ($)": round(float(net_profit), 2),
            }
        )

    return max(results, key=lambda result: result["Net profit ($)"]), results


__all__ = ["COSTS", "TIME_BLOCKS", "ZONES", "evaluate_promises", "promise_values"]