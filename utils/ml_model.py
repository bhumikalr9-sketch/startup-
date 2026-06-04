# utils/ml_model.py

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

def prepare_data(df):

    features = [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]

    target = "Valuation (M USD)"

    X = df[features]
    y = df[target]

    return X, y


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

def train_model(df):

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    return model, metrics


# --------------------------------------------------
# PREDICT VALUATION
# --------------------------------------------------

def predict_valuation(
    model,
    funding,
    revenue,
    employees,
    market_share
):

    input_data = pd.DataFrame({
        "Funding Amount (M USD)": [funding],
        "Revenue (M USD)": [revenue],
        "Employees": [employees],
        "Market Share (%)": [market_share]
    })

    prediction = model.predict(
        input_data
    )[0]

    return round(prediction, 2)


# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

def feature_importance(
    model,
    feature_names
):

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance":
        model.feature_importances_
    })

    importance_df = (
        importance_df
        .sort_values(
            by="Importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return importance_df


# --------------------------------------------------
# TOP FEATURE
# --------------------------------------------------

def get_top_feature(
    model,
    feature_names
):

    importance = feature_importance(
        model,
        feature_names
    )

    return importance.iloc[0]["Feature"]


# --------------------------------------------------
# MODEL SUMMARY
# --------------------------------------------------

def model_summary(
    model,
    metrics
):

    summary = {
        "Model":
        "Random Forest Regressor",

        "Trees":
        model.n_estimators,

        "MAE":
        round(metrics["MAE"], 2),

        "RMSE":
        round(metrics["RMSE"], 2),

        "R2":
        round(metrics["R2"], 4)
    }

    return summary


# --------------------------------------------------
# BULK PREDICTIONS
# --------------------------------------------------

def predict_dataframe(
    model,
    dataframe
):

    features = [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]

    df = dataframe.copy()

    df["Predicted Valuation"] = model.predict(
        df[features]
    )

    return df


# --------------------------------------------------
# SAMPLE STARTUPS
# --------------------------------------------------

def generate_sample_predictions(
    model
):

    sample_df = pd.DataFrame({

        "Funding Amount (M USD)":
        [10, 25, 50, 100, 200],

        "Revenue (M USD)":
        [5, 15, 35, 75, 150],

        "Employees":
        [20, 50, 100, 300, 600],

        "Market Share (%)":
        [2, 5, 10, 20, 35]
    })

    sample_df["Predicted Valuation"] = (
        model.predict(sample_df)
    )

    return sample_df


# --------------------------------------------------
# STARTUP HEALTH SCORE
# --------------------------------------------------

def calculate_health_score(
    funding,
    revenue,
    market_share
):

    score = (
        funding * 0.30 +
        revenue * 0.50 +
        market_share * 0.20
    )

    return round(score, 2)


# --------------------------------------------------
# GROWTH CATEGORY
# --------------------------------------------------

def growth_category(
    valuation
):

    if valuation < 100:
        return "Early Stage"

    elif valuation < 500:
        return "Growth Stage"

    elif valuation < 1000:
        return "Scale-Up"

    else:
        return "Unicorn"


# --------------------------------------------------
# BUSINESS INSIGHT
# --------------------------------------------------

def generate_insight(
    valuation
):

    category = growth_category(
        valuation
    )

    if category == "Early Stage":
        return (
            "Startup is in the early-stage growth phase."
        )

    elif category == "Growth Stage":
        return (
            "Startup shows strong growth potential."
        )

    elif category == "Scale-Up":
        return (
            "Startup is scaling rapidly."
        )

    else:
        return (
            "Startup qualifies as a Unicorn."
        )
