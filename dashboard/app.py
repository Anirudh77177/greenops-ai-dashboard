import streamlit as st
import requests
import pandas as pd

st.title("🌱 GreenOps Dashboard")

summary = requests.get(
    "http://127.0.0.1:8000/metrics/summary"
).json()

daily = requests.get(
    "http://127.0.0.1:8000/metrics/daily"
).json()

st.metric(
    "Total CO2e (kg)",
    summary["total_co2e"]
)

st.metric(
    "Total Cost (USD)",
    summary["total_cost"]
)

st.metric(
    "Highest Emission Team",
    summary["top_team"]
)

st.subheader("Daily CO2e Trend")

daily_df = pd.DataFrame(daily)

st.line_chart(
    daily_df.set_index("date")["co2e_kg"]
)

if st.button("Show Forecast"):

    forecast = requests.get(
        "http://127.0.0.1:8000/forecast"
    ).json()

    forecast_df = pd.DataFrame(
        forecast["forecast"],
        columns=["forecast"]
    )

    st.subheader(
        "30 Day Forecast"
    )

    st.line_chart(
        forecast_df
    )