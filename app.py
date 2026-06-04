# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data,
    get_kpis
)

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Startup Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

@st.cache_data
def load_startup_data():
    df = load_data("data/startup_data.csv")
    df = clean_data(df)
    return df

df = load_startup_data()

kpis = get_kpis(df)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main-header{
    text-align:center;
    font-size:50px;
    font-weight:bold;
}

.sub-header{
    text-align:center;
    color:gray;
    font-size:20px;
}

.feature-card{
    padding:20px;
    border-radius:15px;
    background-color:#f7f7f7;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.title("Startup Analytics")

    st.success(
        """
        Navigate using:

        📊 Overview

        💰 Funding Analysis

        🏭 Industry Insights

        🌍 Regional Analysis

        🤖 Predictive Insights
        """
    )

    st.info(
        f"""
        Records : {len(df)}

        Industries : {df['Industry'].nunique()}

        Regions : {df['Region'].nunique()}
        """
    )

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.markdown(
    "<div class='main-header'>🚀 Startup Analytics Platform</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-header'>Business Intelligence • Data Analytics • Machine Learning</div>",
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------------------------
# KPI SECTION
# ----------------------------------------------------

st.subheader("📈 Executive Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Startups",
    f"{kpis['total_startups']:,}"
)

c2.metric(
    "Funding",
    f"${kpis['total_funding']:,.0f}M"
)

c3.metric(
    "Revenue",
    f"${kpis['total_revenue']:,.0f}M"
)

c4.metric(
    "Avg Valuation",
    f"${kpis['avg_valuation']:,.2f}M"
)

c5.metric(
    "Avg Employees",
    f"{kpis['avg_employees']:,.0f}"
)

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    funding_df = (
        df.groupby("Industry")
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
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    revenue_df = (
        df.groupby("Region")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        revenue_df,
        names="Region",
        values="Revenue (M USD)",
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------
# SECOND ROW
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Employees",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        df,
        x="Valuation (M USD)",
        nbins=30,
        title="Valuation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# TOP STARTUPS
# ----------------------------------------------------

st.subheader("🏆 Top 10 Valued Startups")

top10 = (
    df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[
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

# ----------------------------------------------------
# INDUSTRY PERFORMANCE
# ----------------------------------------------------

st.subheader("🏭 Industry Performance Summary")

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

# ----------------------------------------------------
# EXECUTIVE INSIGHTS
# ----------------------------------------------------

st.subheader("🧠 Executive Insights")

top_industry = (
    df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
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
### Key Business Insights

✅ Most Funded Industry: **{top_industry}**

✅ Highest Revenue Region: **{top_region}**

✅ Highest Valued Startup: **{top_startup}**

✅ Total Startups Analysed: **{len(df)}**

✅ Use the sidebar pages for deeper analytics.
"""
)

# ----------------------------------------------------
# DATA PREVIEW
# ----------------------------------------------------

with st.expander("🔍 View Dataset Preview"):

    st.dataframe(
        df.head(50),
        use_container_width=True
    )

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.divider()

st.markdown(
    """
    <center>
    <h4>🚀 Startup Analytics Platform</h4>
    Built using Streamlit, Plotly, Pandas and Scikit-Learn
    </center>
    """,
    unsafe_allow_html=True
)
