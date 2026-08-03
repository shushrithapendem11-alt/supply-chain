"""
Generates synthetic supply chain datasets for this project:
1. demand_history.csv  -> daily demand for 3 products over 180 days
2. suppliers.csv       -> supplier performance & cost data

Run this once before running the other modules:
    python3 data/generate_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---------- 1. Demand history ----------
products = ["Part-A101", "Part-B202", "Part-C303"]
start_date = datetime(2025, 1, 1)
days = 180

rows = []
for product in products:
    base_demand = np.random.randint(80, 150)
    for d in range(days):
        date = start_date + timedelta(days=d)
        # weekly seasonality + random noise + slight upward trend
        seasonality = 15 * np.sin(2 * np.pi * d / 7)
        trend = d * 0.05
        noise = np.random.normal(0, 8)
        demand = max(0, int(base_demand + seasonality + trend + noise))
        rows.append([date.strftime("%Y-%m-%d"), product, demand])

demand_df = pd.DataFrame(rows, columns=["date", "product", "demand"])
demand_df.to_csv("data/demand_history.csv", index=False)

# ---------- 2. Supplier performance & cost data ----------
suppliers = [
    "Acme Components", "Global Parts Co", "Precision Manufacturing",
    "Zenith Industrial", "Northgate Supply"
]

supplier_rows = []
for i, supplier in enumerate(suppliers):
    supplier_rows.append({
        "supplier": supplier,
        "part": products[i % len(products)],
        "unit_cost": round(np.random.uniform(4.5, 22.0), 2),
        "lead_time_days": np.random.randint(7, 45),
        "on_time_delivery_pct": round(np.random.uniform(78, 99), 1),
        "defect_rate_pct": round(np.random.uniform(0.2, 5.0), 2),
        "cost_variance_pct": round(np.random.uniform(-8, 12), 2),  # actual vs quoted cost
        "orders_last_quarter": np.random.randint(10, 60),
    })

supplier_df = pd.DataFrame(supplier_rows)
supplier_df.to_csv("data/suppliers.csv", index=False)

print("Data generated:")
print(" - data/demand_history.csv  (", len(demand_df), "rows )")
print(" - data/suppliers.csv       (", len(supplier_df), "rows )")
