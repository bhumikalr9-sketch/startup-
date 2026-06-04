# pages/4_Regional_Analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data,
    filter_data,
    get_regions,
    get_industries
)

from utils.charts import (
    revenue_by_region,
    regional_startup_count
)

st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------------------
# Load Data
# ----------------------------------------

df = load_data("startup_data.csv")
df = clean_data(df)

# ----------------------------------------
# Header
# ----------------------------------------

st.title("🌍 Regional Analysis Dashboard")
st.markdown(
    "Analyze startup performance across different regions."
)

st.divider()

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------

st.sidebar.header("Regional Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + get_regions(df)
)

industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + get_industries(df)
)

filtered_df = filter_data(
    df,
    industry=industry,
    region=region
)

# ----------------------------------------
# KPI Metrics
# ----------------------------------------

total_regions = filtered_df["Region"].nunique()

total_startups = len(filtered_df)

total_revenue = filtered_df["Revenue (M USD)"].sum()

total_funding = filtered_df["Funding Amount (M USD)"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Regions",
        total_regions
    )

with col2:
    st.metric(
        "Startups",
        f"{total_startups:,}"
    )

with col3:
    st.metric(
        "Revenue",
        f"${total_revenue:,.2f} M"
    )

with col4:
    st.metric(
        "Funding",
        f"${total_funding:,.2f} M"
    )

st.divider()

# ----------------------------------------
# Revenue Distribution
# ----------------------------------------

st.subheader("💰 Revenue Distribution by Region")

st.plotly_chart(
    revenue_by_region(filtered_df),
    use_container_width=True
)

# ----------------------------------------
# Startup Count
# ----------------------------------------

st.subheader("🚀 Startup Count by Region")

st.plotly_chart(
    regional_startup_count(filtered_df),
    use_container_width=True
)

# ----------------------------------------
# Revenue by Region
# ----------------------------------------

st.subheader("📈 Regional Revenue Ranking")

revenue_df = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
)

fig = px.bar(
    revenue_df,
    x="Region",
    y="Revenue (M USD)",
    color="Region",
    title="Revenue Ranking by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Funding by Region
# ----------------------------------------

st.subheader("💵 Funding by Region")

funding_df = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
)

fig = px.bar(
    funding_df,
    x="Region",
    y="Funding Amount (M USD)",
    color="Region",
    title="Funding Distribution by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Market Share by Region
# ----------------------------------------

st.subheader("📊 Average Market Share")

market_df = (
    filtered_df.groupby("Region")
    ["Market Share (%)"]
    .mean()
    .reset_index()
    .sort_values(
        "Market Share (%)",
        ascending=False
    )
)

fig = px.bar(
    market_df,
    x="Region",
    y="Market Share (%)",
    color="Region",
    title="Average Market Share by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Valuation Analysis
# ----------------------------------------

st.subheader("💎 Average Valuation by Region")

valuation_df = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
)

fig = px.bar(
    valuation_df,
    x="Region",
    y="Valuation (M USD)",
    color="Region",
    title="Average Startup Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Startup Distribution
# ----------------------------------------

st.subheader("🌎 Startup Distribution")

startup_dist = (
    filtered_df.groupby("Region")
    .size()
    .reset_index(name="Count")
)

fig = px.pie(
    startup_dist,
    names="Region",
    values="Count",
    title="Startup Share by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Regional Summary Table
# ----------------------------------------

st.subheader("📋 Regional Performance Summary")

summary = (
    filtered_df.groupby("Region")
    .agg(
        Startups=("Startup Name", "count"),
        Revenue=("Revenue (M USD)", "sum"),
        Funding=("Funding Amount (M USD)", "sum"),
        Avg_Valuation=("Valuation (M USD)", "mean"),
        Avg_Employees=("Employees", "mean"),
        Avg_Market_Share=("Market Share (%)", "mean")
    )
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True
)

# ----------------------------------------
# Top Startups by Region
# ----------------------------------------

st.subheader("🏆 Top Valued Startups")

top_startups = (
    filtered_df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    top_startups[
        [
            "Startup Name",
            "Region",
            "Industry",
            "Valuation (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# ----------------------------------------
# Revenue vs Valuation
# ----------------------------------------

st.subheader("📈 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Region",
    size="Employees",
    hover_name="Startup Name",
    title="Regional Revenue vs Valuation Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# Smart Insights
# ----------------------------------------

st.subheader("🧠 Regional Insights")

top_region_revenue = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

top_region_funding = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region_valuation = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

st.success(
    f"""
### Key Regional Insights

✅ Highest revenue region: **{top_region_revenue}**

✅ Highest funded region: **{top_region_funding}**

✅ Highest average valuation region: **{top_region_valuation}**

✅ Total startups analyzed: **{total_startups}**

✅ Total regions covered: **{total_regions}**
"""
)

# ----------------------------------------
# Raw Data Explorer
# ----------------------------------------

with st.expander("🔍 View Regional Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ----------------------------------------
# Download Report
# ----------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Regional Report",
    data=csv,
    file_name="regional_analysis.csv",
    mime="text/csv"
)
