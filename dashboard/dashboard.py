"""
dashboard.py

An interactive dashboard for exploring customer segments.

Run it with:
    python -m streamlit run dashboard/dashboard.py

This will open a page in your browser. Streamlit re-runs this whole
script top-to-bottom every time you interact with something (like a
dropdown) -- that's its whole "trick" for being simple to write.
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        background: linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.25),
            rgba(124, 58, 237, 0.18)
        );
        border: 1px solid rgba(96, 165, 250, 0.35);
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    }

    .hero-badge {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.18);
        color: #93c5fd;
        border: 1px solid rgba(96, 165, 250, 0.35);
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 750;
        line-height: 1.1;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        color: #b8c1cc;
        font-size: 16px;
        max-width: 760px;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #161b22, #11161d);
        border: 1px solid #30363d;
        border-top: 3px solid #3b82f6;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }

    [data-testid="stMetricLabel"] {
        color: #aab2bf;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* ---------- Main dashboard navigation tabs ---------- */
    [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #121820;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 10px;
        margin-top: 12px;
        margin-bottom: 18px;
    }

    [data-baseweb="tab"] {
        height: 58px;
        padding: 0 24px;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
    }

    [data-baseweb="tab"] p {
        color: #c9d1d9;
        font-size: 18px;
        font-weight: 700;
    }

    [data-baseweb="tab"]:hover {
        background-color: #1f2937;
        border-color: #58a6ff;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1f6feb, #6f42c1);
        border-color: #58a6ff;
        box-shadow: 0 6px 18px rgba(31, 111, 235, 0.25);
    }

    [data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff;
    }

    [data-baseweb="tab-highlight"] {
        display: none;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #171b24 0%, #11161d 100%);
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem;
    }

    .sidebar-heading {
        padding: 0 2px 14px 2px;
    }

    .sidebar-heading h2 {
        color: #ffffff;
        font-size: 24px;
        line-height: 1.2;
        margin: 0 0 6px 0;
    }

    .sidebar-heading p {
        color: #8b949e;
        font-size: 13px;
        line-height: 1.45;
        margin: 0;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #0e1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        overflow: hidden;
    }

    .upload-guide {
        background: linear-gradient(
            145deg,
            rgba(31, 111, 235, 0.16),
            rgba(111, 66, 193, 0.10)
        );
        border: 1px solid rgba(88, 166, 255, 0.35);
        border-radius: 12px;
        margin-bottom: 12px;
        padding: 14px;
    }

    .upload-guide-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .upload-guide p {
        color: #b8c1cc;
        font-size: 13px;
        line-height: 1.5;
        margin: 3px 0;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background-color: #0e1117;
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        padding: 14px 10px;
    }

    .sidebar-status {
        border-radius: 10px;
        font-size: 14px;
        font-weight: 650;
        margin: 12px 0 18px 0;
        padding: 11px 13px;
    }

    .sidebar-status.uploaded {
        background-color: rgba(46, 160, 67, 0.12);
        border: 1px solid rgba(46, 160, 67, 0.45);
        color: #7ee787;
    }

    .sidebar-status.demo {
        background-color: rgba(31, 111, 235, 0.13);
        border: 1px solid rgba(88, 166, 255, 0.40);
        color: #79c0ff;
    }

    .sidebar-section-title {
        color: #ffffff;
        font-size: 19px;
        font-weight: 700;
        margin: 8px 0 2px 0;
    }

    .sidebar-section-help {
        color: #8b949e;
        font-size: 13px;
        margin: 0 0 12px 0;
    }

    .sidebar-result-card {
        background: linear-gradient(
            135deg,
            rgba(31, 111, 235, 0.18),
            rgba(111, 66, 193, 0.16)
        );
        border: 1px solid rgba(88, 166, 255, 0.4);
        border-radius: 12px;
        margin: 18px 0 10px 0;
        padding: 15px 16px;
    }

    .sidebar-result-label {
        color: #b8c1cc;
        display: block;
        font-size: 13px;
        margin-bottom: 3px;
    }

    .sidebar-result-number {
        color: #ffffff;
        display: inline-block;
        font-size: 28px;
        font-weight: 750;
        margin-right: 5px;
    }

    .sidebar-result-total {
        color: #8b949e;
        font-size: 13px;
    }

    [data-testid="stSidebar"] .stButton > button {
        border: 1px solid #3b82f6;
        border-radius: 10px;
        font-weight: 650;
        min-height: 42px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="hero-badge">CUSTOMER INTELLIGENCE</div>
    <div class="hero-title">Customer Segmentation Dashboard</div>
    <div class="hero-subtitle">
        Explore customer groups based on income, spending behaviour,
        purchase frequency and age.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar heading ----------
st.sidebar.markdown(
    """
    <div class="sidebar-heading">
        <h2>⚙️ Dashboard Controls</h2>
        <p>Choose the data and narrow down the customers you want to view.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Load and validate data ----------
project_root = Path(__file__).resolve().parents[1]

processed_data_path = (
    project_root
    / "data"
    / "processed"
    / "customers_segmented.csv"
)

legacy_data_path = project_root / "customers_segmented.csv"

st.sidebar.markdown(
    """
    <div class="upload-guide">
        <div class="upload-guide-title">📄 Add Your Customer File</div>
        <p><strong>Step 1:</strong> Click <strong>Browse files</strong> below.</p>
        <p><strong>Step 2:</strong> Choose the customer CSV from your computer.</p>
        <p>No file yet? The dashboard will safely show sample data.</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader(
    "Choose your customer file",
    type=["csv"],
    help="Choose the CSV customer report provided by your customer system."
)

st.sidebar.caption("Accepted file type: CSV")

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        data_source_status = "✓ Your customer file is ready"
        data_source_class = "uploaded"

    else:
        if processed_data_path.exists():
            demo_path = processed_data_path
        elif legacy_data_path.exists():
            demo_path = legacy_data_path
        else:
            st.error(
                "No demo dataset was found. Run the segmentation "
                "script or upload a segmented CSV file."
            )
            st.stop()

        df = pd.read_csv(demo_path)
        data_source_status = "● Sample data is currently being shown"
        data_source_class = "demo"

except Exception as error:
    st.error(
        "We could not open that file. Please choose a customer report "
        "saved as a CSV file."
    )
    with st.expander("Technical details"):
        st.caption(str(error))
    st.stop()


required_columns = [
    "customer_id",
    "age",
    "annual_income",
    "spending_score",
    "purchase_frequency",
    "segment"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The selected CSV is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


numeric_columns = [
    "age",
    "annual_income",
    "spending_score",
    "purchase_frequency"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

rows_before_cleaning = len(df)

df = df.dropna(subset=required_columns)
df = df[df["segment"].astype(str).str.strip() != ""]

removed_rows = rows_before_cleaning - len(df)

if removed_rows > 0:
    st.warning(
        f"{removed_rows} invalid customer rows were excluded."
    )

if df.empty:
    st.error("The CSV does not contain any valid customer records.")
    st.stop()

st.sidebar.markdown(
    (
        f'<div class="sidebar-status {data_source_class}">'
        f'{data_source_status}</div>'
    ),
    unsafe_allow_html=True
)

if uploaded_file is not None:
    st.sidebar.caption(f"Selected file: {uploaded_file.name}")

# ---------- Sidebar filters ----------
st.sidebar.markdown(
    """
    <div class="sidebar-section-title">🎛️ Filter Customers</div>
    <div class="sidebar-section-help">
        Adjust these options to focus on the customers you need.
    </div>
    """,
    unsafe_allow_html=True
)

segments = sorted(df["segment"].unique().tolist())

if "segment_filter" in st.session_state:
    saved_segments = st.session_state["segment_filter"]
    if any(segment not in segments for segment in saved_segments):
        st.session_state["segment_filter"] = segments

selected_segments = st.sidebar.multiselect(
    "Customer segments",
    options=segments,
    default=segments,
    key="segment_filter"
)

minimum_age = int(df["age"].min())
maximum_age = int(df["age"].max())

if "age_filter" in st.session_state:
    saved_age = st.session_state["age_filter"]
    st.session_state["age_filter"] = (
        max(minimum_age, min(saved_age[0], maximum_age)),
        max(minimum_age, min(saved_age[1], maximum_age))
    )

selected_age = st.sidebar.slider(
    "Age range",
    min_value=minimum_age,
    max_value=maximum_age,
    value=(minimum_age, maximum_age),
    key="age_filter"
)

minimum_score = int(df["spending_score"].min())
maximum_score = int(df["spending_score"].max())

if "score_filter" in st.session_state:
    saved_score = st.session_state["score_filter"]
    st.session_state["score_filter"] = (
        max(minimum_score, min(saved_score[0], maximum_score)),
        max(minimum_score, min(saved_score[1], maximum_score))
    )

selected_score = st.sidebar.slider(
    "Spending score range",
    min_value=minimum_score,
    max_value=maximum_score,
    value=(minimum_score, maximum_score),
    key="score_filter"
)

filtered = df[
    (df["segment"].isin(selected_segments))
    & (df["age"].between(selected_age[0], selected_age[1]))
    & (
        df["spending_score"].between(
            selected_score[0],
            selected_score[1]
        )
    )
]

st.sidebar.markdown(
    f"""
    <div class="sidebar-result-card">
        <span class="sidebar-result-label">Customers found</span>
        <span class="sidebar-result-number">{len(filtered)}</span>
        <span class="sidebar-result-total">of {len(df)} total</span>
    </div>
    """,
    unsafe_allow_html=True
)


def reset_sidebar_filters():
    st.session_state["segment_filter"] = segments
    st.session_state["age_filter"] = (minimum_age, maximum_age)
    st.session_state["score_filter"] = (minimum_score, maximum_score)


st.sidebar.button(
    "↻ Reset All Filters",
    use_container_width=True,
    on_click=reset_sidebar_filters
)

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# ---------- Top-level numbers ----------
# ---------- Top-level numbers ----------
high_value_count = (filtered["segment"] == "High-Value").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(filtered))
col2.metric("High-Value Customers", high_value_count)
col3.metric("Average Income", f"{filtered['annual_income'].mean():,.0f}")
col4.metric(
    "Average Spending Score",
    f"{filtered['spending_score'].mean():.1f}"
)

# ---------- Scatter plot ----------
# ---------- Dashboard sections ----------
summary_tab, data_tab, charts_tab = st.tabs(
    [
        "📊 Segment Summary",
        "👥 Customer Data",
        "📈 Visual Analysis"
    ]
)

# ---------- Segment summary ----------
with summary_tab:
    st.subheader("Segment Overview")
    st.caption(
        "Compare the size and average behaviour of each customer segment."
    )

    segment_summary = (
        filtered.groupby("segment")
        .agg(
            Customers=("segment", "size"),
            Average_Age=("age", "mean"),
            Average_Income=("annual_income", "mean"),
            Average_Spending_Score=("spending_score", "mean"),
            Average_Purchase_Frequency=("purchase_frequency", "mean")
        )
        .round(1)
        .reset_index()
        .rename(
    columns={
        "segment": "Segment",
        "Average_Age": "Average Age",
        "Average_Income": "Average Income",
        "Average_Spending_Score": "Average Spending Score",
        "Average_Purchase_Frequency": "Average Purchase Frequency"
    }
)
    )

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Understanding the Segments")

    info1, info2, info3 = st.columns(3)

    with info1:
        st.success(
            "**High-Value**\n\n"
            "Customers with the strongest spending behaviour. "
            "They are important for loyalty programmes and premium offers."
        )

    with info2:
        st.info(
            "**Regular**\n\n"
            "Customers with moderate spending behaviour. "
            "They have potential to become high-value customers."
        )

    with info3:
        st.warning(
            "**Low-Spending**\n\n"
            "Customers with lower spending behaviour. "
            "Discounts or targeted offers may encourage more purchases."
        )


# ---------- Customer data ----------
with data_tab:
    st.subheader("Customer Records")
    st.caption(
        "The most valuable customers are displayed first by default."
    )

    display_data = filtered[
        [
            "customer_id",
            "age",
            "annual_income",
            "spending_score",
            "purchase_frequency",
            "segment"
        ]
    ].copy()

    display_data = display_data.rename(
        columns={
            "customer_id": "Customer ID",
            "age": "Age",
            "annual_income": "Annual Income",
            "spending_score": "Spending Score",
            "purchase_frequency": "Purchase Frequency",
            "segment": "Customer Segment"
        }
    )

    sort_column, position_column = st.columns([2, 1])

    with sort_column:
        arrange_by = st.selectbox(
            "Arrange customers by",
            [
                "Customer Value",
                "Age",
                "Annual Income",
                "Purchase Frequency",
                "Spending Score"
            ]
        )

    with position_column:
        show_order = st.selectbox(
            "Show",
            [
                "Top first",
                "Bottom first"
            ]
        )

    ascending_order = show_order == "Bottom first"

    if arrange_by == "Customer Value":
        value_priority = {
            "High-Value": 3,
            "Regular": 2,
            "Low-Spending": 1
        }

        display_data["_Value Priority"] = (
            display_data["Customer Segment"]
            .map(value_priority)
        )

        display_data = (
            display_data
            .sort_values(
                by=[
                    "_Value Priority",
                    "Spending Score",
                    "Purchase Frequency",
                    "Annual Income"
                ],
                ascending=[
                    ascending_order,
                    ascending_order,
                    ascending_order,
                    ascending_order
                ],
                kind="stable"
            )
            .drop(columns="_Value Priority")
        )

    else:
        display_data = display_data.sort_values(
            by=arrange_by,
            ascending=ascending_order,
            kind="stable"
        )

    display_data = display_data.reset_index(drop=True)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    csv_data = display_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Current Customer List",
        data=csv_data,
        file_name="customer_list.csv",
        mime="text/csv"
    )
# ---------- Visual analysis ----------
with charts_tab:
    st.subheader("Visual Analysis")
    st.caption(
        "Use these charts when a visual comparison of the segments is needed."
    )

    segment_colors = {
        "Regular": "#4C9BE8",
        "Low-Spending": "#FF8C42",
        "High-Value": "#45C46A",
    }

    scatter_column, distribution_column = st.columns([2, 1])

    with scatter_column:
        st.markdown("#### Income vs. Spending Score")

        scatter_figure, scatter_axis = plt.subplots(figsize=(8, 5))
        scatter_figure.patch.set_alpha(0)
        scatter_axis.set_facecolor("#0e1117")

        for segment in filtered["segment"].unique():
            subset = filtered[filtered["segment"] == segment]

            scatter_axis.scatter(
                subset["annual_income"],
                subset["spending_score"],
                label=segment,
                color=segment_colors.get(segment, "#AAB2BF"),
                alpha=0.75,
                s=45
            )

        scatter_axis.set_xlabel("Annual Income", color="#C9D1D9")
        scatter_axis.set_ylabel("Spending Score", color="#C9D1D9")
        scatter_axis.tick_params(colors="#C9D1D9")
        scatter_axis.grid(
            color="#30363D",
            linestyle="--",
            alpha=0.5
        )

        for spine in scatter_axis.spines.values():
            spine.set_color("#30363D")

        legend = scatter_axis.legend()
        legend.get_frame().set_facecolor("#161B22")
        legend.get_frame().set_edgecolor("#30363D")

        for text in legend.get_texts():
            text.set_color("#FFFFFF")

        st.pyplot(scatter_figure, use_container_width=True)
        plt.close(scatter_figure)

    with distribution_column:
        st.markdown("#### Customers per Segment")

        preferred_order = [
            "High-Value",
            "Regular",
            "Low-Spending"
        ]

        visible_segments = [
            segment
            for segment in preferred_order
            if segment in filtered["segment"].unique()
        ]

        segment_counts = (
            filtered["segment"]
            .value_counts()
            .reindex(visible_segments)
        )

        distribution_figure, distribution_axis = plt.subplots(
            figsize=(5, 5)
        )

        distribution_figure.patch.set_alpha(0)
        distribution_axis.set_facecolor("#0e1117")

        bars = distribution_axis.barh(
            segment_counts.index,
            segment_counts.values,
            color=[
                segment_colors.get(segment, "#AAB2BF")
                for segment in segment_counts.index
            ]
        )

        distribution_axis.bar_label(
            bars,
            padding=4,
            color="#FFFFFF"
        )

        distribution_axis.set_xlabel(
            "Number of Customers",
            color="#C9D1D9"
        )

        distribution_axis.tick_params(colors="#C9D1D9")
        distribution_axis.grid(
            axis="x",
            color="#30363D",
            linestyle="--",
            alpha=0.5
        )

        for spine in distribution_axis.spines.values():
            spine.set_color("#30363D")

        st.pyplot(
            distribution_figure,
            use_container_width=True
        )

        plt.close(distribution_figure)
