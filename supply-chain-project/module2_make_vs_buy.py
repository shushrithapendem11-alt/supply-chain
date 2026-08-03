"""
Module 2: Make-vs-Buy (Outsourcing) Breakeven Analysis

Business context:
  "Provides input to outsourcing decisions by performing make versus
  buy analysis." (from JD)

What this script does:
  1. Compares the cost of making a part in-house (fixed setup/tooling
     cost + variable cost per unit) vs. buying it from a supplier
     (fixed cost, usually $0, + unit price).
  2. Calculates the breakeven volume where both options cost the same.
  3. Recommends "Make" or "Buy" for a few example scenarios.
  4. Saves a comparison chart to outputs/.

Run:
    python3 module2_make_vs_buy.py
"""

import matplotlib.pyplot as plt
import pandas as pd


def breakeven_volume(make_fixed_cost, make_variable_cost, buy_unit_price, buy_fixed_cost=0):
    """
    Returns the volume at which Make cost == Buy cost.
    Below breakeven -> Buy is cheaper. Above breakeven -> Make is cheaper.
    """
    denominator = buy_unit_price - make_variable_cost
    if denominator <= 0:
        # Make's variable cost per unit is >= the buy price, so Buy is
        # cheaper per unit at any volume -- there's no breakeven crossover.
        return None
    return (make_fixed_cost - buy_fixed_cost) / denominator


def recommend(volume, breakeven, make_fixed, make_var, buy_price):
    make_total = make_fixed + make_var * volume
    buy_total = buy_price * volume
    decision = "MAKE" if make_total < buy_total else "BUY"
    return decision, make_total, buy_total


def plot_scenario(name, make_fixed, make_var, buy_price, max_volume, breakeven):
    volumes = list(range(0, max_volume, max(1, max_volume // 100)))
    make_costs = [make_fixed + make_var * v for v in volumes]
    buy_costs = [buy_price * v for v in volumes]

    plt.figure(figsize=(9, 5))
    plt.plot(volumes, make_costs, label="Make (in-house)", linewidth=2)
    plt.plot(volumes, buy_costs, label="Buy (supplier)", linewidth=2)
    if breakeven and 0 < breakeven < max_volume:
        plt.axvline(breakeven, color="red", linestyle="--", label=f"Breakeven ≈ {breakeven:.0f} units")
    plt.title(f"Make vs Buy Cost Comparison — {name}")
    plt.xlabel("Order Volume (units)")
    plt.ylabel("Total Cost ($)")
    plt.legend()
    plt.tight_layout()
    path = f"outputs/make_vs_buy_{name.replace(' ', '_')}.png"
    plt.savefig(path)
    plt.close()
    return path


def main():
    # Example scenarios — swap these numbers for real part data
    scenarios = [
        {"name": "Part-A101", "make_fixed_cost": 25000, "make_variable_cost": 6.20, "buy_unit_price": 9.75, "expected_annual_volume": 4000},
        {"name": "Part-B202", "make_fixed_cost": 60000, "make_variable_cost": 3.10, "buy_unit_price": 6.40, "expected_annual_volume": 12000},
        {"name": "Part-C303", "make_fixed_cost": 9000,  "make_variable_cost": 11.00, "buy_unit_price": 8.50, "expected_annual_volume": 2500},
    ]

    results = []
    for s in scenarios:
        be = breakeven_volume(s["make_fixed_cost"], s["make_variable_cost"], s["buy_unit_price"])
        decision, make_total, buy_total = recommend(
            s["expected_annual_volume"], be, s["make_fixed_cost"], s["make_variable_cost"], s["buy_unit_price"]
        )
        chart = plot_scenario(
            s["name"], s["make_fixed_cost"], s["make_variable_cost"], s["buy_unit_price"],
            max_volume=max(s["expected_annual_volume"] * 2, 1000), breakeven=be
        )
        results.append({
            "part": s["name"],
            "breakeven_units": round(be, 0) if be else "N/A (make always cheaper)",
            "expected_annual_volume": s["expected_annual_volume"],
            "make_total_cost": round(make_total, 2),
            "buy_total_cost": round(buy_total, 2),
            "recommendation": decision,
            "chart": chart,
        })
        print(f"{s['name']}: breakeven={be}, at expected volume -> {decision} "
              f"(Make=${make_total:,.0f} vs Buy=${buy_total:,.0f})")

    pd.DataFrame(results).to_csv("outputs/module2_make_vs_buy_summary.csv", index=False)
    print("\nSaved: outputs/module2_make_vs_buy_summary.csv and chart images.")


if __name__ == "__main__":
    main()
