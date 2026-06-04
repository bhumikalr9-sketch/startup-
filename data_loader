# utils/charts.py

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def funding_by_industry(df):
    industry_funding = (
        df.groupby("Industry")["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    return fig


def revenue_by_region(df):
    region_revenue = (
        df.groupby("Region")["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_revenue,
        names="Region",
        values="Revenue (M USD)",
        title="Revenue Distribution by Region"
    )

    return fig


def funding_vs_valuation(df):
    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Employees",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    return fig


def valuation_distribution(df):
    fig = px.histogram(
        df,
        x="Valuation (M USD)",
        nbins=30,
        title="Valuation Distribution"
    )

    return fig


def funding_distribution(df):
    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Distribution"
    )

    return fig


def industry_treemap(df):
    industry = (
        df.groupby("Industry")
        .agg({
            "Funding Amount (M USD)": "sum"
        })
        .reset_index()
    )

    fig = px.treemap(
        industry,
        path=["Industry"],
        values="Funding Amount (M USD)",
        title="Industry Funding Treemap"
    )

    return fig


def market_share_by_industry(df):
    industry_share = (
        df.groupby("Industry")["Market Share (%)"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        industry_share,
        x="Industry",
        y="Market Share (%)",
        title="Average Market Share by Industry"
    )

    return fig


def employee_distribution(df):
    fig = px.box(
        df,
        x="Industry",
        y="Employees",
        title="Employee Distribution Across Industries"
    )

    return fig


def profitability_chart(df):
    profit_counts = (
        df["Profitable"]
        .value_counts()
        .reset_index()
    )

    profit_counts.columns = [
        "Profitable",
        "Count"
    ]

    fig = px.pie(
        profit_counts,
        names="Profitable",
        values="Count",
        title="Profitability Analysis"
    )

    return fig


def exit_status_chart(df):
    exit_counts = (
        df["Exit Status"]
        .value_counts()
        .reset_index()
    )

    exit_counts.columns = [
        "Exit Status",
        "Count"
    ]

    fig = px.bar(
        exit_counts,
        x="Exit Status",
        y="Count",
        title="Exit Status Distribution"
    )

    return fig


def revenue_vs_employees(df):
    fig = px.scatter(
        df,
        x="Employees",
        y="Revenue (M USD)",
        color="Industry",
        size="Valuation (M USD)",
        hover_name="Startup Name",
        title="Revenue vs Employees"
    )

    return fig


def top_10_valued_startups(df):
    top10 = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Startup Name",
        y="Valuation (M USD)",
        color="Industry",
        title="Top 10 Valued Startups"
    )

    return fig


def correlation_heatmap(df):

    numeric_cols = [
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]

    corr = df[numeric_cols].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            text=corr.round(2),
            texttemplate="%{text}",
            colorscale="Viridis"
        )
    )

    fig.update_layout(
        title="Correlation Heatmap"
    )

    return fig


def regional_startup_count(df):

    counts = (
        df.groupby("Region")
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        counts,
        x="Region",
        y="Count",
        title="Startup Count by Region"
    )

    return fig


def industry_revenue_ranking(df):

    revenue = (
        df.groupby("Industry")["Revenue (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Revenue (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        revenue,
        x="Industry",
        y="Revenue (M USD)",
        title="Industry Revenue Ranking"
    )

    return fig
