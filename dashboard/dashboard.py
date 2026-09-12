"""
dashboard.py

An interactive dashboard for exploring customer segments.

Run it with:
    streamlit run dashboard.py

This will open a page in your browser. Streamlit re-runs this whole
script top-to-bottom every time you interact with something (like a
dropdown) -- that's its whole "trick" for being simple to write.
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("Customer Segmentation Dashboard")

# ---------- Load data ----------
# Lets you upload your own CSV, or falls back to the demo file.
uploaded_file = st.sidebar.file_uploader("Upload customers_segmented.csv", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("customers_segmented.csv")
    st.sidebar.info("Using the demo dataset (customers_segmented.csv). Upload your own to replace it.")

# ---------- Sidebar filter ----------
segments = df["segment"].unique().tolist()
selected_segments = st.sidebar.multiselect("Filter by segment", segments, default=segments)
filtered = df[df["segment"].isin(selected_segments)]

# ---------- Top-level numbers ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(filtered))
col2.metric("Avg. Income", f"${filtered['annual_income'].mean():,.0f}")
col3.metric("Avg. Spending Score", f"{filtered['spending_score'].mean():.1f}")

# ---------- Scatter plot ----------
st.subheader("Income vs. Spending Score by Segment")
fig, ax = plt.subplots(figsize=(8, 5))
for segment in filtered["segment"].unique():
    subset = filtered[filtered["segment"] == segment]
    ax.scatter(subset["annual_income"], subset["spending_score"], label=segment, alpha=0.6)
ax.set_xlabel("Annual Income")
ax.set_ylabel("Spending Score")
ax.legend()
st.pyplot(fig)

# ---------- Segment breakdown table ----------
st.subheader("Segment Averages")
st.dataframe(filtered.groupby("segment")[["age", "annual_income", "spending_score", "purchase_frequency"]].mean().round(1))

# ---------- Raw data ----------
st.subheader("Customer Data")
st.dataframe(filtered)
