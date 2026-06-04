# pages/1_Overview.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data,
    get_kpis,
    filter_data,
    get_industries,
    get_regions
)

from utils.charts import (
    funding_by_industry,
    revenue_by_region,
    funding_vs_valuation,
    valuation_distribution,
    top_10_valued_startups
)

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
df = load_data("startup_data.csv")
df = clean_data(df)

# -----------------------------
# Title
# -----------------------------
st.title("🚀 Startup Analytics Dashboard")
st.markdown("### Executive Overview")

st.divider()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + get_industries(df)
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + get_regions(df)
)

filtered_df = filter_data(
    df,
    industry=industry,
    region=region
)

# -----------------------------
# KPI Section
# -----------------------------
kpis = get_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Startups",
        f"{kpis['total_startups']:,}"
    )

with col2:
    st.metric(
        "Funding",
        f"${kpis['total_funding']:,.2f} M"
    )

with col3:
    st.metric(
        "Revenue",
        f"${kpis['total_revenue']:,.2f} M"
    )

with col4:
    st.metric(
        "Avg Valuation",
        f"${kpis['avg_valuation']:,.2f} M"
    )

with col5:
    st.metric(
        "Avg Employees",
        f"{kpis['avg_employees']:,.0f}"
    )

st.divider()

# -----------------------------
# Charts Row 1
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        funding_by_industry(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        revenue_by_region(filtered_df),
        use_container_width=True
    )

# -----------------------------
# Charts Row 2
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        funding_vs_valuation(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        valuation_distribution(filtered_df),
        use_container_width=True
    )

st.divider()

# -----------------------------
# Top Startups
# -----------------------------
st.subheader("🏆 Top 10 Valued Startups")

top10 = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.plotly_chart(
    top_10_valued_startups(filtered_df),
    use_container_width=True
)

st.dataframe(
    top10[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Valuation (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

st.divider()

# -----------------------------
# Industry Breakdown
# -----------------------------
st.subheader("📈 Industry Breakdown")

industry_summary = (
    filtered_df.groupby("Industry")
    .agg(
        Startups=("Startup Name", "count"),
        Funding=("Funding Amount (M USD)", "sum"),
        Revenue=("Revenue (M USD)", "sum"),
        Avg_Valuation=("Valuation (M USD)", "mean")
    )
    .reset_index()
)

st.dataframe(
    industry_summary,
    use_container_width=True
)

# -----------------------------
# Revenue Leaderboard
# -----------------------------
st.subheader("💰 Revenue Leaderboard")

revenue_df = (
    filtered_df.sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    revenue_df,
    x="Startup Name",
    y="Revenue (M USD)",
    color="Industry",
    title="Top Revenue Generating Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Dataset Preview
# -----------------------------
with st.expander("🔍 View Raw Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# -----------------------------
# Footer Insights
# -----------------------------
st.divider()

highest_funding = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

highest_revenue = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

st.success(
    f"""
### Key Insights

✅ Most funded industry: **{highest_funding}**

✅ Highest revenue region: **{highest_revenue}**

✅ Total startups analyzed: **{len(filtered_df)}**

✅ Dashboard updated dynamically based on selected filters.
"""
)
