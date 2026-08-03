"""
Module 1: Demand Forecasting + Reorder Point / Safety Stock

Business context:
  "Forecasts and communicates ... requirements to suppliers. Coordinates
  demand signals through MRP to minimize inventory exposure." (from JD)

What this script does:
  1. Loads historical daily demand for each product.
  2. Forecasts near-term demand using a simple moving average.
  3. Calculates safety stock and reorder point using demand variability
     and supplier lead time (classic MRP inventory planning formulas).
  4. Saves a forecast-vs-actual chart per product to outputs/.

Run:
    python3 module1_demand_forecast.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Config ----
MOVING_AVG_WINDOW = 7      # days
SERVICE_LEVEL_Z = 1.65     # ~95% service level (z-score)
LEAD_TIME_DAYS = 14        # assumed supplier lead time for this example

def load_data():
    df = pd.read_csv("data/demand_history.csv", parse_dates=["date"])
    return df

def forecast_and_reorder_point(df, product):
    product_df = df[df["product"] == product].sort_values("date").copy()
    product_df["forecast"] = product_df["demand"].rolling(MOVING_AVG_WINDOW).mean()

    # Demand variability (standard deviation of daily demand)
    demand_std = product_df["demand"].std()
    avg_daily_demand = product_df["demand"].mean()

    # Safety stock = Z * std_dev * sqrt(lead time)
    safety_stock = SERVICE_LEVEL_Z * demand_std * np.sqrt(LEAD_TIME_DAYS)

    # Reorder point = (avg daily demand * lead time) + safety stock
    reorder_point = (avg_daily_demand * LEAD_TIME_DAYS) + safety_stock

    return product_df, safety_stock, reorder_point, avg_daily_demand

def plot_forecast(product_df, product, reorder_point):
    plt.figure(figsize=(10, 5))
    plt.plot(product_df["date"], product_df["demand"], label="Actual Demand", alpha=0.5)
    plt.plot(product_df["date"], product_df["forecast"], label=f"{MOVING_AVG_WINDOW}-Day Moving Avg Forecast", linewidth=2)
    plt.axhline(reorder_point, color="red", linestyle="--", label=f"Reorder Point ({reorder_point:.0f} units)")
    plt.title(f"Demand Forecast & Reorder Point — {product}")
    plt.xlabel("Date")
    plt.ylabel("Units")
    plt.legend()
    plt.tight_layout()
    out_path = f"outputs/forecast_{product}.png"
    plt.savefig(out_path)
    plt.close()
    return out_path

def main():
    df = load_data()
    summary_rows = []

    for product in df["product"].unique():
        product_df, safety_stock, reorder_point, avg_daily_demand = forecast_and_reorder_point(df, product)
        chart_path = plot_forecast(product_df, product, reorder_point)

        summary_rows.append({
            "product": product,
            "avg_daily_demand": round(avg_daily_demand, 1),
            "safety_stock_units": round(safety_stock, 1),
            "reorder_point_units": round(reorder_point, 1),
            "assumed_lead_time_days": LEAD_TIME_DAYS,
            "chart": chart_path,
        })
        print(f"{product}: avg daily demand={avg_daily_demand:.1f} | "
              f"safety stock={safety_stock:.1f} | reorder point={reorder_point:.1f}")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("outputs/module1_reorder_summary.csv", index=False)
    print("\nSaved: outputs/module1_reorder_summary.csv and chart images.")

if __name__ == "__main__":
    main()
