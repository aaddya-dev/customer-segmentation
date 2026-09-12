"""
eda.py

Exploratory Data Analysis for the customer dataset.
Run it with:
    python notebooks/eda.py

Produces histograms, boxplots, and a correlation heatmap saved as
image files so the whole team can look at the same charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Point this at the real dataset once it's downloaded, e.g.:
# df = pd.read_csv("data/raw/Mall_Customers.csv")
df = pd.read_csv("data/raw/Mall_Customers.csv")

print("Shape (rows, columns):", df.shape)
print("\nColumn info:")
print(df.info())
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

numeric_cols = df.select_dtypes(include="number").columns.tolist()

# ---------- Histograms: distribution of each numeric column ----------
df[numeric_cols].hist(figsize=(10, 6), bins=20)
plt.tight_layout()
plt.savefig("data/processed/eda_histograms.png", dpi=120)
print("\nSaved eda_histograms.png")

# ---------- Boxplots: spot outliers ----------
fig, axes = plt.subplots(1, len(numeric_cols), figsize=(4 * len(numeric_cols), 4))
for ax, col in zip(axes, numeric_cols):
    sns.boxplot(y=df[col], ax=ax)
    ax.set_title(col)
plt.tight_layout()
plt.savefig("data/processed/eda_boxplots.png", dpi=120)
print("Saved eda_boxplots.png")

# ---------- Correlation heatmap: how columns relate to each other ----------
plt.figure(figsize=(6, 5))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlation between numeric columns")
plt.tight_layout()
plt.savefig("data/processed/eda_correlation.png", dpi=120)
print("Saved eda_correlation.png")
