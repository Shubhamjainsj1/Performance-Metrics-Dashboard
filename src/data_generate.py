# src/generate_sample_data.py
"""
Generates sample dataset of delivery/agent performance, incentives, and order-level KPIs.
Outputs data/sample_orders.csv
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "sample_orders.csv")

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate(n=5000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    start = datetime(2024, 1, 1)
    end = datetime(2025, 7, 31)

    agents = [f"agent_{i:03d}" for i in range(1, 51)]
    cities = ["Mumbai", "Bengaluru", "Delhi", "Hyderabad", "Kolkata"]

    rows = []
    for i in range(n):
        order_id = f"ORD{100000+i}"
        agent = random.choice(agents)
        city = random.choice(cities)
        order_date = random_date(start, end)
        pickup_to_drop_mins = max(5, int(np.random.exponential(scale=20)))
        distance_km = round(np.random.gamma(shape=2, scale=3), 2)
        order_value = round(np.random.normal(300, 120), 2)
        rating = round(np.clip(np.random.normal(4.5, 0.7), 1.0, 5.0), 1)

        # simple incentive rule: if on-time proportion high, extra incentive
        on_time = np.random.choice([1,0], p=[0.88,0.12])
        incentive = 0
        if rating >= 4.5 and on_time:
            incentive = round(np.random.choice([10,20,30]),2)

        rows.append({
            "order_id": order_id,
            "agent_id": agent,
            "city": city,
            "order_ts": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "pickup_to_drop_mins": pickup_to_drop_mins,
            "distance_km": distance_km,
            "order_value": max(10.0, order_value),
            "rating": rating,
            "on_time": on_time,
            "incentive": incentive
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print("Wrote", OUT)
    return OUT

if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
    generate(8000)
