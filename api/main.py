from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI(title="GreenOps API")

# Load Data
df = pd.read_csv("data/cloud_usage_enriched.csv")
df["date"] = pd.to_datetime(df["date"])

# Load Model
model = joblib.load("model/co2e_model.pkl")


@app.get("/health")
def health():
    """
    Health Check Endpoint
    """
    return {"status": "ok"}


@app.get("/metrics/summary")
def summary():
    """
    Summary Metrics
    """

    total_co2e = round(df["co2e_kg"].sum(), 2)
    total_cost = round(df["cost_usd"].sum(), 2)

    top_team = (
        df.groupby("team")["co2e_kg"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("region")["co2e_kg"]
        .sum()
        .idxmax()
    )

    return {
        "total_co2e": total_co2e,
        "total_cost": total_cost,
        "top_team": top_team,
        "top_region": top_region
    }


@app.get("/metrics/daily")
def daily_metrics():
    """
    Daily CO2e Trend
    """

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    return daily.to_dict(orient="records")


@app.get("/forecast")
def forecast():
    """
    Forecast Endpoint
    """

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    daily["lag_7"] = daily["co2e_kg"].shift(7)
    daily["lag_14"] = daily["co2e_kg"].shift(14)
    daily["rolling_7"] = daily["co2e_kg"].rolling(7).mean()
    daily["dow"] = daily["date"].dt.dayofweek

    daily = daily.dropna()

    features = [
        "lag_7",
        "lag_14",
        "rolling_7",
        "dow"
    ]

    latest = daily[features].tail(30)

    predictions = model.predict(latest)

    return {
        "forecast": predictions.tolist()
    }