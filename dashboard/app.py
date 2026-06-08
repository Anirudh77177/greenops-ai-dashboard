import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="GreenOps Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 GreenOps Dashboard")

API_URL = "http://127.0.0.1:8000"

# =========================
# API CALLS
# =========================

summary = requests.get(
    f"{API_URL}/metrics/summary"
).json()

daily = requests.get(
    f"{API_URL}/metrics/daily"
).json()

green = requests.get(
    f"{API_URL}/green-score"
).json()

# =========================
# GREEN SCORE
# =========================

st.subheader("🌿 Green Score")

grade = green["grade"]
gate = green["gate"]

if gate == "PASS":
    st.success(
        f"Grade: {grade} | Gate: {gate}"
    )

elif gate == "WARNING":
    st.warning(
        f"Grade: {grade} | Gate: {gate}"
    )

else:
    st.error(
        f"Grade: {grade} | Gate: {gate}"
    )

st.write(
    f"Average Daily CO2e: {green['avg_daily_co2e']} kg"
)

st.write(
    green["action"]
)

st.divider()

# =========================
# KPI METRICS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total CO2e (kg)",
        summary["total_co2e"]
    )

with col2:
    st.metric(
        "Total Cost (USD)",
        summary["total_cost"]
    )

with col3:
    st.metric(
        "Highest Emission Team",
        summary["top_team"]
    )

# =========================
# DAILY TREND
# =========================

st.subheader("📈 Daily CO2e Trend")

daily_df = pd.DataFrame(daily)

daily_df["date"] = pd.to_datetime(
    daily_df["date"]
)

st.line_chart(
    daily_df.set_index("date")["co2e_kg"]
)

# =========================
# FORECAST
# =========================

if st.button("Show Forecast"):

    forecast = requests.get(
        f"{API_URL}/forecast"
    ).json()

    forecast_df = pd.DataFrame(
        forecast["forecast"],
        columns=["forecast"]
    )

    st.subheader(
        "🔮 30 Day Forecast"
    )

    st.line_chart(
        forecast_df
    )