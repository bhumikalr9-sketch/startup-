# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data,
    get_kpis
)

st.set_page_config(
    page_title="Startup Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def get_data():
    df = load_data("startup_data.csv")
    df = clean_data(df)
    return df

df = get_data()

kpis = get_kpis(df)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .main-title{
        font-size:42px;
        font-weight:bold;
        text-align:center;
        color:#1f77b4;
    }

    .sub-title{
        text-align:center;
        font-size:18px;
        color:gray;
    }

    .metric-box{
        padding:15px;
        border-radius:10px;
        background-color:#f7f7f7;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("🚀 Startup Analytics")

st.sidebar.success(
    """
    Navigation

    📊 Overview

    💰 Funding Analysis

    🏭 Industry Insights

    🌍 Regional Analysis

    🤖 Predictive Insights
    """
)

st.sidebar.info(
    f"""
    Dataset Records: {len(df)}

    Industries: {df['Industry'].nunique()}

    Regions: {df['Region'].nunique()}
    """
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown(
    "<p class='main-title'>🚀 Startup Analytics Platform</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='sub-title'>
    Deep Analytics • Business Intelligence • Machine Learning Insights
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Startups",
        f"{kpis['total_startups']:,}"
    )

with col2:
    st.metric(
        "Funding",
        f"${kpis['total_funding']:,.0f}M"
    )

with col3:
    st.metric(
        "Revenue",
        f"${kpis['total_revenue']:,.0f}M"
    )

with col4:
    st.metric(
        "Avg Valuation",
        f"${kpis['avg_valuation']:,.2f}M"
    )

with col5:
    st.metric(
        "Employees",
        f"{kpis['avg_employees']:,.0f}"
    )

st.divider()

# ---------------------------------------------------
# QUICK INSIGHTS
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_funding = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Top Industries by Funding"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    region_revenue = (
        df.groupby("Region")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_revenue,
        names="Region",
        values="Revenue (M USD)",
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ---------------------------------------------------
# TOP STARTUPS
# ---------------------------------------------------

st.subheader("🏆 Top 10 Valued Startups")

top_startups = (
    df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_startups[
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

# ---------------------------------------------------
# INDUSTRY SUMMARY
# ---------------------------------------------------

st.subheader("🏭 Industry Summary")

industry_summary = (
    df.groupby("Industry")
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

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Executive Insights")

top_funding_industry = (
    df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_revenue_region = (
    df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

top_startup = (
    df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"""
### Key Findings

✅ Most funded industry: **{top_funding_industry}**

✅ Highest revenue region: **{top_revenue_region}**

✅ Highest valued startup: **{top_startup}**

✅ Dataset contains **{len(df)} startups**

✅ Explore detailed insights using the pages in the sidebar.
"""
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Startup Analytics Platform | Built with Streamlit, Plotly & Scikit-Learn"
)
