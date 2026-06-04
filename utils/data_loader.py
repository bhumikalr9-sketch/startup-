# utils/data_loader.py

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(file_path="startup_data.csv"):
    """
    Load startup dataset
    """

    df = pd.read_csv(file_path)

    return df


def clean_data(df):
    """
    Clean dataset
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Fill missing numeric values
    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values
    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    return df


def get_kpis(df):
    """
    Generate KPI metrics
    """

    metrics = {
        "total_startups": len(df),

        "total_funding":
        round(
            df["Funding Amount (M USD)"].sum(),
            2
        ),

        "total_revenue":
        round(
            df["Revenue (M USD)"].sum(),
            2
        ),

        "avg_valuation":
        round(
            df["Valuation (M USD)"].mean(),
            2
        ),

        "avg_employees":
        round(
            df["Employees"].mean(),
            0
        )
    }

    return metrics


def filter_data(
        df,
        industry=None,
        region=None,
        profitable=None):

    filtered = df.copy()

    if industry and industry != "All":
        filtered = filtered[
            filtered["Industry"] == industry
        ]

    if region and region != "All":
        filtered = filtered[
            filtered["Region"] == region
        ]

    if profitable and profitable != "All":
        filtered = filtered[
            filtered["Profitable"] == profitable
        ]

    return filtered


def get_industries(df):
    return sorted(
        df["Industry"]
        .dropna()
        .unique()
        .tolist()
    )


def get_regions(df):
    return sorted(
        df["Region"]
        .dropna()
        .unique()
        .tolist()
    )


def get_top_startups(
        df,
        top_n=10):

    return (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(top_n)
    )


def get_summary(df):

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "industries":
        df["Industry"].nunique(),

        "regions":
        df["Region"].nunique(),

        "average_funding":
        round(
            df["Funding Amount (M USD)"]
            .mean(),
            2
        ),

        "average_revenue":
        round(
            df["Revenue (M USD)"]
            .mean(),
            2
        )
    }

    return summary
