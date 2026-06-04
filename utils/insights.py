# utils/insights.py

import pandas as pd

# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------

def executive_insights(df):

    insights = {}

    insights["total_startups"] = len(df)

    insights["total_funding"] = round(
        df["Funding Amount (M USD)"].sum(),
        2
    )

    insights["total_revenue"] = round(
        df["Revenue (M USD)"].sum(),
        2
    )

    insights["avg_valuation"] = round(
        df["Valuation (M USD)"].mean(),
        2
    )

    insights["avg_employees"] = round(
        df["Employees"].mean(),
        0
    )

    return insights


# --------------------------------------------------
# TOP INDUSTRY
# --------------------------------------------------

def top_funded_industry(df):

    return (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )


# --------------------------------------------------
# TOP REVENUE INDUSTRY
# --------------------------------------------------

def top_revenue_industry(df):

    return (
        df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .idxmax()
    )


# --------------------------------------------------
# TOP REGION
# --------------------------------------------------

def top_region(df):

    return (
        df.groupby("Region")
        ["Revenue (M USD)"]
        .sum()
        .idxmax()
    )


# --------------------------------------------------
# TOP STARTUP
# --------------------------------------------------

def top_startup(df):

    startup = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .iloc[0]
    )

    return startup["Startup Name"]


# --------------------------------------------------
# MOST PROFITABLE REGION
# --------------------------------------------------

def profitable_region(df):

    if "Profitable" not in df.columns:
        return "N/A"

    region = (
        df.groupby("Region")
        ["Profitable"]
        .mean()
        .idxmax()
    )

    return region


# --------------------------------------------------
# PROFITABILITY RATE
# --------------------------------------------------

def profitability_rate(df):

    if "Profitable" not in df.columns:
        return 0

    return round(
        df["Profitable"].mean() * 100,
        2
    )


# --------------------------------------------------
# UNICORN COUNT
# --------------------------------------------------

def unicorn_count(df):

    return len(
        df[
            df["Valuation (M USD)"] >= 1000
        ]
    )


# --------------------------------------------------
# INDUSTRY LEADERBOARD
# --------------------------------------------------

def industry_leaderboard(df):

    leaderboard = (
        df.groupby("Industry")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "mean")
        )
        .reset_index()
        .sort_values(
            "Funding",
            ascending=False
        )
    )

    return leaderboard


# --------------------------------------------------
# REGION LEADERBOARD
# --------------------------------------------------

def region_leaderboard(df):

    leaderboard = (
        df.groupby("Region")
        .agg(
            Funding=("Funding Amount (M USD)", "sum"),
            Revenue=("Revenue (M USD)", "sum"),
            Valuation=("Valuation (M USD)", "mean")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    return leaderboard


# --------------------------------------------------
# MARKET LEADERS
# --------------------------------------------------

def market_leaders(df, n=10):

    return (
        df.sort_values(
            "Market Share (%)",
            ascending=False
        )
        .head(n)
    )


# --------------------------------------------------
# FASTEST GROWING STARTUPS
# --------------------------------------------------

def top_revenue_startups(df, n=10):

    return (
        df.sort_values(
            "Revenue (M USD)",
            ascending=False
        )
        .head(n)
    )


# --------------------------------------------------
# FUNDING EFFICIENCY
# --------------------------------------------------

def funding_efficiency(df):

    temp = df.copy()

    temp["Funding Efficiency"] = (
        temp["Revenue (M USD)"] /
        temp["Funding Amount (M USD)"]
    )

    return (
        temp.sort_values(
            "Funding Efficiency",
            ascending=False
        )
        .head(10)
    )


# --------------------------------------------------
# REGION INSIGHTS
# --------------------------------------------------

def regional_insights(df):

    top_rev_region = (
        df.groupby("Region")
        ["Revenue (M USD)"]
        .sum()
        .idxmax()
    )

    top_funding_region = (
        df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )

    top_valuation_region = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .mean()
        .idxmax()
    )

    return {
        "Top Revenue Region":
        top_rev_region,

        "Top Funding Region":
        top_funding_region,

        "Top Valuation Region":
        top_valuation_region
    }


# --------------------------------------------------
# INDUSTRY INSIGHTS
# --------------------------------------------------

def industry_insights(df):

    top_revenue = (
        df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .idxmax()
    )

    top_funding = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )

    top_valuation = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .idxmax()
    )

    return {
        "Top Revenue Industry":
        top_revenue,

        "Top Funding Industry":
        top_funding,

        "Top Valuation Industry":
        top_valuation
    }


# --------------------------------------------------
# GENERATE AI SUMMARY
# --------------------------------------------------

def generate_ai_summary(df):

    funded = top_funded_industry(df)

    revenue = top_revenue_industry(df)

    region = top_region(df)

    startup = top_startup(df)

    unicorns = unicorn_count(df)

    summary = f"""
Most funded industry: {funded}

Highest revenue industry: {revenue}

Top performing region: {region}

Highest valued startup: {startup}

Total unicorn startups: {unicorns}

These insights indicate strong growth opportunities
across leading industries and regions.
"""

    return summary


# --------------------------------------------------
# HEALTH REPORT
# --------------------------------------------------

def startup_health_report(df):

    profitable_pct = profitability_rate(df)

    unicorns = unicorn_count(df)

    avg_valuation = round(
        df["Valuation (M USD)"].mean(),
        2
    )

    return {
        "Profitability Rate (%)":
        profitable_pct,

        "Unicorn Count":
        unicorns,

        "Average Valuation":
        avg_valuation
    }
