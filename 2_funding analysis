# pages/2_Funding_Analysis.py

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
    funding_by_industry,
    funding_distribution,
    funding_vs_valuation,
    correlation_heatmap
)

st.set_page_config(
    page_title="Funding Analysis",
    page_icon="💰",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data("startup_data.csv")
df = clean_data(df)

# --------------------------------------------------
# Page Title
# --------------------------------------------------

st.title("💰 Funding Analysis Dashboard")
st.markdown(
    "Analyze startup funding trends, distributions, and investment patterns."
)

st.divider()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Funding Filters")

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

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_funding = filtered_df["Funding Amount (M USD)"].sum()

avg_funding = filtered_df["Funding Amount (M USD)"].mean()

max_funding = filtered_df["Funding Amount (M USD)"].max()

median_funding = filtered_df["Funding Amount (M USD)"].median()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Funding",
    f"${total_funding:,.2f} M"
)

col2.metric(
    "Average Funding",
    f"${avg_funding:,.2f} M"
)

col3.metric(
    "Highest Funding",
    f"${max_funding:,.2f} M"
)

col4.metric(
    "Median Funding",
    f"${median_funding:,.2f} M"
)

st.divider()

# --------------------------------------------------
# Funding Distribution
# --------------------------------------------------

st.subheader("📊 Funding Distribution")

st.plotly_chart(
    funding_distribution(filtered_df),
    use_container_width=True
)

# --------------------------------------------------
# Funding By Industry
# --------------------------------------------------

st.subheader("🏭 Funding by Industry")

st.plotly_chart(
    funding_by_industry(filtered_df),
    use_container_width=True
)

# --------------------------------------------------
# Funding vs Valuation
# --------------------------------------------------

st.subheader("🚀 Funding vs Valuation")

st.plotly_chart(
    funding_vs_valuation(filtered_df),
    use_container_width=True
)

# --------------------------------------------------
# Top Funded Startups
# --------------------------------------------------

st.subheader("🏆 Top Funded Startups")

top_funded = (
    filtered_df
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_funded,
    x="Startup Name",
    y="Funding Amount (M USD)",
    color="Industry",
    title="Top 15 Funded Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Industry Funding Table
# --------------------------------------------------

st.subheader("📋 Industry Funding Summary")

industry_table = (
    filtered_df.groupby("Industry")
    .agg(
        Total_Funding=("Funding Amount (M USD)", "sum"),
        Average_Funding=("Funding Amount (M USD)", "mean"),
        Startup_Count=("Startup Name", "count")
    )
    .reset_index()
    .sort_values(
        "Total_Funding",
        ascending=False
    )
)

st.dataframe(
    industry_table,
    use_container_width=True
)

# --------------------------------------------------
# Region Funding Analysis
# --------------------------------------------------

st.subheader("🌍 Funding by Region")

region_funding = (
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
    region_funding,
    x="Region",
    y="Funding Amount (M USD)",
    color="Region",
    title="Funding Distribution Across Regions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Funding Correlation
# --------------------------------------------------

st.subheader("🔍 Correlation Analysis")

st.plotly_chart(
    correlation_heatmap(filtered_df),
    use_container_width=True
)

# --------------------------------------------------
# Funding Insights
# --------------------------------------------------

st.subheader("📈 Funding Insights")

most_funded_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

most_funded_region = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

largest_startup = (
    filtered_df.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"""
### Key Findings

✅ Most funded industry: **{most_funded_industry}**

✅ Most funded region: **{most_funded_region}**

✅ Highest funded startup: **{largest_startup['Startup Name']}**

✅ Total funding analyzed: **${total_funding:,.2f} Million**

✅ Average funding per startup: **${avg_funding:,.2f} Million**
"""
)

# --------------------------------------------------
# Download Data
# --------------------------------------------------

st.divider()

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="funding_analysis.csv",
    mime="text/csv"
)
