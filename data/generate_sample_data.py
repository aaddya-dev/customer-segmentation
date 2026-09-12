"""
generate_sample_data.py

Creates a synthetic customer dataset so you can practice the whole
segmentation pipeline before plugging in real company data.

Run it with:
    python generate_sample_data.py

It will create a file called customers.csv in the same folder.
"""

import numpy as np
import pandas as pd

# A "seed" makes the random data reproducible -- same numbers every run.
np.random.seed(42)

n_customers = 500

# We build a few natural "true" groups so the clustering has something
# real to find -- this mimics how real customer bases usually look.

# Group 1: young, low income, low spenders (~40% of customers)
group1 = pd.DataFrame({
    "age": np.random.randint(18, 30, 200),
    "annual_income": np.random.randint(15000, 40000, 200),
    "spending_score": np.random.randint(10, 40, 200),
    "purchase_frequency": np.random.randint(1, 5, 200),
})

# Group 2: middle-aged, mid income, regular spenders (~40%)
group2 = pd.DataFrame({
    "age": np.random.randint(30, 50, 200),
    "annual_income": np.random.randint(40000, 80000, 200),
    "spending_score": np.random.randint(40, 70, 200),
    "purchase_frequency": np.random.randint(5, 12, 200),
})

# Group 3: high income, high-value frequent spenders (~20%)
group3 = pd.DataFrame({
    "age": np.random.randint(35, 60, 100),
    "annual_income": np.random.randint(80000, 150000, 100),
    "spending_score": np.random.randint(70, 100, 100),
    "purchase_frequency": np.random.randint(12, 25, 100),
})

customers = pd.concat([group1, group2, group3], ignore_index=True)

# Give each customer a simple ID
customers.insert(0, "customer_id", range(1, len(customers) + 1))

# Shuffle rows so the "true" groups aren't in obvious blocks
customers = customers.sample(frac=1, random_state=42).reset_index(drop=True)

customers.to_csv("customers.csv", index=False)
print(f"Created customers.csv with {len(customers)} rows.")
print(customers.head())
