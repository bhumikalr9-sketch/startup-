# pages/5_Predictive_Insights.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_data,
    clean_data
)

from utils.ml_model import (
    train_model,
    predict_valuation,
    feature_importance
)

st.set_page_config(
    page_title="Predictive Insights",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = load_data("startup_data.csv")
df = clean_data(df)

# --------------------------------------------------
# Train Model
# --------------------------------------------------

model, metrics = train_model(df)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Predictive Insights Dashboard")
st.markdown(
    "Machine Learning powered startup valuation prediction."
)

st.divider()

# --------------------------------------------------
# Model Performance
# --------------------------------------------------

st.subheader("📊 Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAE",
        f"{metrics['MAE']:.2f}"
    )

with col2:
    st.metric(
        "RMSE",
        f"{metrics['RMSE']:.2f}"
    )

with col3:
    st.metric(
        "R² Score",
        f"{metrics['R2']:.3f}"
    )

st.divider()

# --------------------------------------------------
# Prediction Section
# --------------------------------------------------

st.subheader("🚀 Startup Valuation Predictor")

col1, col2 = st.columns(2)

with col1:

    funding = st.number_input(
        "Funding Amount (M USD)",
        min_value=0.0,
        value=50.0
    )

    revenue = st.number_input(
        "Revenue (M USD)",
        min_value=0.0,
        value=25.0
    )

with col2:

    employees = st.number_input(
        "Employees",
        min_value=1,
        value=100
    )

    market_share = st.slider(
        "Market Share (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0
    )

if st.button("Predict Valuation"):

    prediction = predict_valuation(
        model,
        funding,
        revenue,
        employees,
        market_share
    )

    st.success(
        f"Predicted Startup Valuation: ${prediction:,.2f} Million"
    )

st.divider()

# --------------------------------------------------
# Feature Importance
# --------------------------------------------------

st.subheader("📈 Feature Importance")

importance_df = feature_importance(
    model,
    [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]
)

fig = px.bar(
    importance_df,
    x="Feature",
    y="Importance",
    title="Feature Importance Analysis",
    text="Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Actual vs Predicted Simulation
# --------------------------------------------------

st.subheader("🎯 Valuation Distribution")

fig = px.histogram(
    df,
    x="Valuation (M USD)",
    nbins=30,
    title="Startup Valuation Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Funding vs Valuation
# --------------------------------------------------

st.subheader("💰 Funding vs Valuation")

fig = px.scatter(
    df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Funding Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Revenue vs Valuation
# --------------------------------------------------

st.subheader("📊 Revenue vs Valuation")

fig = px.scatter(
    df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Market Share (%)",
    hover_name="Startup Name",
    title="Revenue Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Top Predicted Drivers
# --------------------------------------------------

st.subheader("🧠 AI Insights")

top_feature = importance_df.iloc[0]["Feature"]

avg_val = df["Valuation (M USD)"].mean()

max_val = df["Valuation (M USD)"].max()

st.success(
    f"""
### Machine Learning Insights

✅ Most influential factor: **{top_feature}**

✅ Average startup valuation: **${avg_val:,.2f} Million**

✅ Highest startup valuation: **${max_val:,.2f} Million**

✅ Random Forest model used for prediction

✅ Model automatically learns relationships between funding, revenue, employees and market share
"""
)

# --------------------------------------------------
# Prediction Examples
# --------------------------------------------------

st.subheader("📋 Sample Predictions")

sample_data = pd.DataFrame({
    "Funding Amount (M USD)": [25, 50, 100, 200],
    "Revenue (M USD)": [10, 30, 60, 120],
    "Employees": [50, 100, 250, 500],
    "Market Share (%)": [5, 10, 20, 30]
})

sample_data["Predicted Valuation"] = model.predict(
    sample_data
)

st.dataframe(
    sample_data,
    use_container_width=True
)

# --------------------------------------------------
# Download Prediction Dataset
# --------------------------------------------------

st.divider()

csv = sample_data.to_csv(index=False)

st.download_button(
    label="⬇ Download Prediction Examples",
    data=csv,
    file_name="prediction_examples.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Raw Dataset
# --------------------------------------------------

with st.expander("🔍 View Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )
