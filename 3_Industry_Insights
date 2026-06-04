# pages/3_Industry_Insights.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data,
    filter_data,
    get_industries,
    get_regions
)

from utils.charts import (
    industry_treemap,
    market_share_by_industry,
    employee_distribution,
    industry_revenue_ranking
)

st.set_page_config(
    page_title="Industry Insights",
    page_icon="🏭",
    layout="wide"
)

# ----------------------------------
# Load Dataset
# ----------------------------------

df = load_data("startup_data.csv")
df = clean_data(df)

# ----------------------------------
# Page Header
# ----------------------------------

st.title("🏭 Industry Insights Dashboard")
st.markdown(
    "Analyze industry performance, revenue, market share, workforce, and valuation trends."
)

st.divider()

# ----------------------------------
# Sidebar Filters
# ----------------------------------

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

# ----------------------------------
# KPI Metrics
# ----------------------------------

total_industries = filtered_df["Industry"].nunique()

avg_valuation = filtered_df["Valuation (M USD)"].mean()

avg_revenue = filtered_df["Revenue (M USD)"].mean()

avg_market_share = filtered_df["Market Share (%)"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Industries",
    total_industries
)

col2.metric(
    "Avg Valuation",
    f"${avg_valuation:,.2f} M"
)

col3.metric(
    "Avg Revenue",
    f"${avg_revenue:,.2f} M"
)

col4.metric(
    "Avg Market Share",
    f"{avg_market_share:.2f}%"
)

st.divider()

# ----------------------------------
# Industry Treemap
# ----------------------------------

st.subheader("🌳 Industry Funding Treemap")

st.plotly_chart(
    industry_treemap(filtered_df),
    use_container_width=True
)

# ----------------------------------
# Revenue Ranking
# ----------------------------------

st.subheader("💰 Industry Revenue Ranking")

st.plotly_chart(
    industry_revenue_ranking(filtered_df),
    use_container_width=True
)

# ----------------------------------
# Market Share Analysis
# ----------------------------------

st.subheader("📈 Average Market Share")

st.plotly_chart(
    market_share_by_industry(filtered_df),
    use_container_width=True
)

# ----------------------------------
# Employee Distribution
# ----------------------------------

st.subheader("👨‍💼 Employee Distribution")

st.plotly_chart(
    employee_distribution(filtered_df),
    use_container_width=True
)

# ----------------------------------
# Industry Comparison Table
# ----------------------------------

st.subheader("📋 Industry Comparison")

industry_summary = (
    filtered_df.groupby("Industry")
    .agg(
        Startups=("Startup Name", "count"),
        Funding=("Funding Amount (M USD)", "sum"),
        Revenue=("Revenue (M USD)", "sum"),
        Avg_Valuation=("Valuation (M USD)", "mean"),
        Avg_Market_Share=("Market Share (%)", "mean"),
        Avg_Employees=("Employees", "mean")
    )
    .reset_index()
)

st.dataframe(
    industry_summary,
    use_container_width=True
)

# ----------------------------------
# Valuation Analysis
# ----------------------------------

st.subheader("💎 Industry Valuation Analysis")

valuation_df = (
    filtered_df.groupby("Industry")
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
    x="Industry",
    y="Valuation (M USD)",
    color="Industry",
    title="Average Industry Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Startup Count by Industry
# ----------------------------------

st.subheader("🚀 Startup Distribution")

startup_count = (
    filtered_df.groupby("Industry")
    .size()
    .reset_index(name="Count")
    .sort_values(
        "Count",
        ascending=False
    )
)

fig = px.pie(
    startup_count,
    names="Industry",
    values="Count",
    title="Startup Distribution Across Industries"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Revenue vs Valuation
# ----------------------------------

st.subheader("📊 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Valuation by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Top Industry Startups
# ----------------------------------

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
            "Industry",
            "Region",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Employees"
        ]
    ],
    use_container_width=True
)

# ----------------------------------
# Smart Insights
# ----------------------------------

st.subheader("🧠 AI Industry Insights")

top_revenue_industry = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

top_market_industry = (
    filtered_df.groupby("Industry")
    ["Market Share (%)"]
    .mean()
    .idxmax()
)

top_valuation_industry = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

st.success(
    f"""
### Industry Highlights

✅ Highest revenue industry: **{top_revenue_industry}**

✅ Highest average valuation industry: **{top_valuation_industry}**

✅ Highest market-share industry: **{top_market_industry}**

✅ Total industries analyzed: **{total_industries}**

✅ Dashboard updates dynamically based on filters.
"""
)

# ----------------------------------
# Raw Data
# ----------------------------------

with st.expander("🔍 View Industry Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ----------------------------------
# Download
# ----------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Industry Report",
    data=csv,
    file_name="industry_insights.csv",
    mime="text/csv"
)
