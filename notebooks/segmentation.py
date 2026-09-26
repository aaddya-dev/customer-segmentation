"""
segmentation.py

Loads customers_sample.csv, cleans it, runs K-Means clustering to find
customer segments, labels them, and saves a chart + labeled CSV.

Run it with:
    python notebooks/segmentation.py

Compared to Java/C++: there are no classes or type declarations
required here. Python infers types automatically, and most "data
science" work is just calling functions from libraries like pandas
and scikit-learn rather than writing algorithms by hand.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ---------- 1. Load the data ----------
df = pd.read_csv("data/raw/customers_sample.csv")
print(f"Loaded {len(df)} customers")
print(df.describe())  # quick sanity check: min/max/avg of each column

# ---------- 2. Clean the data ----------
# Drop any rows with missing values (real data will have these; our
# synthetic data won't, but this line is important for real datasets).
df = df.dropna()

# The columns we'll actually use to group customers.
features = ["age", "annual_income", "spending_score", "purchase_frequency"]

# ---------- 3. Scale the data ----------
# K-Means measures distance between customers. Income (e.g. 50000) and
# age (e.g. 30) are on wildly different scales, which would make income
# dominate the grouping unfairly. StandardScaler puts every column on
# the same scale (mean 0, spread 1) before clustering.
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features])

# ---------- 4. Find a good number of clusters (the "elbow method") ----------
# We try a range of cluster counts and look at how much "error" (inertia)
# each leaves behind. The elbow point -- where adding more clusters stops
# helping much -- is usually a good number to pick.
inertias = []
k_range = range(1, 10)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(scaled_features)
    inertias.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(list(k_range), inertias, marker="o")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia (lower = tighter clusters)")
plt.title("Elbow method: pick k where the curve bends")
plt.savefig("data/processed/elbow_plot.png", dpi=120, bbox_inches="tight")
print("Saved data/processed/elbow_plot.png -- look for where the line stops dropping sharply")

# ---------- 5. Run K-Means with a chosen k ----------
# Based on how we built the synthetic data, 3 is a natural choice.
# When you switch to real data, check elbow_plot.png first and adjust this.
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(scaled_features)

# ---------- 6. Label the clusters with human-readable names ----------
# Look at each cluster's average spending + income to decide its label.
cluster_summary = df.groupby("cluster")[features].mean()
print("\nCluster averages:")
print(cluster_summary)

# Rank clusters by spending_score to assign sensible labels automatically.
ranked = cluster_summary["spending_score"].sort_values().index.tolist()
label_map = {
    ranked[0]: "Low-Spending",
    ranked[1]: "Regular",
    ranked[2]: "High-Value",
}
df["segment"] = df["cluster"].map(label_map)

print("\nCustomers per segment:")
print(df["segment"].value_counts())

# ---------- 7. Save results ----------
df.to_csv("data/processed/customers_segmented.csv", index=False)
print("\nSaved data/processed/customers_segmented.csv with segment labels")

# ---------- 8. Visualize the segments ----------
plt.figure(figsize=(7, 5))
for segment in df["segment"].unique():
    subset = df[df["segment"] == segment]
    plt.scatter(subset["annual_income"], subset["spending_score"], label=segment, alpha=0.6)
plt.xlabel("Annual Income")
plt.ylabel("Spending Score")
plt.title("Customer Segments")
plt.legend()
plt.savefig("data/processed/segments_plot.png", dpi=120, bbox_inches="tight")
print("Saved data/processed/segments_plot.png")
