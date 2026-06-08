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
    return {"status": "ok"}


@app.get("/metrics/summary")
def summary():

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

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    return daily.to_dict(orient="records")


@app.get("/forecast")
def forecast():

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


@app.get("/green-score")
def green_score():

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    avg_daily = round(
        daily["co2e_kg"].mean(),
        2
    )

    if avg_daily < 2:
        grade = "A"
        action = "Excellent — no action needed"
        gate = "PASS"

    elif avg_daily < 5:
        grade = "B"
        action = "Good — minor optimisation advised"
        gate = "PASS"

    elif avg_daily < 10:
        grade = "C"
        action = "Moderate — review VM sizing"
        gate = "PASS"

    elif avg_daily < 20:
        grade = "D"
        action = "Immediate rightsizing required"
        gate = "WARNING"

    else:
        grade = "F"
        action = "Critical — pipeline soft gate triggered"
        gate = "BLOCKED"

    return {
        "grade": grade,
        "avg_daily_co2e": avg_daily,
        "action": action,
        "gate": gate
    }