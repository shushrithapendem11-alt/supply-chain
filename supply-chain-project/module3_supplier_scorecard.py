"""
Module 3: Supplier Performance Scorecard (KPI Tracking)

Business context:
  "Monitors supplier performance (delivery, quality, cost). Generates
  and publishes Key Process Indicators (KPI)." (from JD)

What this script does:
  1. Loads supplier data (on-time delivery %, defect rate %, cost variance %).
  2. Calculates a weighted composite score per supplier (0-100).
  3. Ranks suppliers and flags any that need a risk review.
  4. Saves a bar chart comparing suppliers to outputs/.

Run:
    python3 module3_supplier_scorecard.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# Weights reflect relative importance of each KPI (should sum to 1.0)
WEIGHTS = {
    "delivery": 0.4,
    "quality": 0.4,
    "cost": 0.2,
}

# Below this composite score, flag supplier for a risk review
RISK_REVIEW_THRESHOLD = 70


def load_data():
    return pd.read_csv("data/suppliers.csv")


def score_suppliers(df):
    df = df.copy()

    # Delivery score: on_time_delivery_pct already 0-100
    df["delivery_score"] = df["on_time_delivery_pct"]

    # Quality score: lower defect rate is better. Convert to a 0-100 scale
    # (assume 5% defect rate or worse = 0 score, 0% defects = 100 score)
    df["quality_score"] = (1 - (df["defect_rate_pct"] / 5.0)).clip(lower=0) * 100

    # Cost score: penalize positive cost variance (actual cost overruns),
    # reward negative variance (came in under quoted cost)
    df["cost_score"] = (100 - df["cost_variance_pct"]).clip(lower=0, upper=100)

    df["composite_score"] = (
        df["delivery_score"] * WEIGHTS["delivery"]
        + df["quality_score"] * WEIGHTS["quality"]
        + df["cost_score"] * WEIGHTS["cost"]
    ).round(1)

    df["risk_flag"] = df["composite_score"].apply(
        lambda s: "REVIEW NEEDED" if s < RISK_REVIEW_THRESHOLD else "OK"
    )

    return df.sort_values("composite_score", ascending=False)


def plot_scorecard(df):
    plt.figure(figsize=(10, 5))
    colors = ["#d9534f" if flag == "REVIEW NEEDED" else "#5cb85c" for flag in df["risk_flag"]]
    plt.bar(df["supplier"], df["composite_score"], color=colors)
    plt.axhline(RISK_REVIEW_THRESHOLD, color="gray", linestyle="--", label=f"Risk threshold ({RISK_REVIEW_THRESHOLD})")
    plt.title("Supplier Performance Scorecard")
    plt.ylabel("Composite Score (0-100)")
    plt.xticks(rotation=20, ha="right")
    plt.legend()
    plt.tight_layout()
    path = "outputs/supplier_scorecard.png"
    plt.savefig(path)
    plt.close()
    return path


def main():
    df = load_data()
    scored_df = score_suppliers(df)
    chart_path = plot_scorecard(scored_df)

    print(scored_df[["supplier", "composite_score", "risk_flag"]].to_string(index=False))

    scored_df.to_csv("outputs/module3_supplier_scorecard.csv", index=False)
    print(f"\nSaved: outputs/module3_supplier_scorecard.csv and {chart_path}")


if __name__ == "__main__":
    main()
