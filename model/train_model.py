import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("data/cloud_usage_enriched.csv")

df["date"] = pd.to_datetime(df["date"])

# ==========================
# DAILY AGGREGATION
# ==========================

daily = (
    df.groupby("date")["co2e_kg"]
    .sum()
    .reset_index()
)

# ==========================
# FEATURE ENGINEERING
# ==========================

daily["lag_7"] = daily["co2e_kg"].shift(7)
daily["lag_14"] = daily["co2e_kg"].shift(14)

daily["rolling_7"] = (
    daily["co2e_kg"]
    .rolling(7)
    .mean()
)

daily["dow"] = daily["date"].dt.dayofweek

daily = daily.dropna()

print("Feature Engineered Shape:")
print(daily.shape)

# ==========================
# TRAIN TEST SPLIT
# ==========================

train = daily[:-30]
test = daily[-30:]

features = [
    "lag_7",
    "lag_14",
    "rolling_7",
    "dow"
]

X_train = train[features]
y_train = train["co2e_kg"]

X_test = test[features]
y_test = test["co2e_kg"]

# ==========================
# MODEL TRAINING
# ==========================

model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel Trained Successfully")

# ==========================
# PREDICTION
# ==========================

y_pred = model.predict(X_test)

# ==========================
# RMSE
# ==========================

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

print("\nRMSE:")
print(rmse)

mean_daily = y_test.mean()

print("\nMean Daily CO2e:")
print(mean_daily)

error_percent = (rmse / mean_daily) * 100

print("\nError %:")
print(round(error_percent, 2))

if error_percent < 10:
    print("\nGood Model (<10% Error)")
else:
    print("\nNeeds Improvement (>10% Error)")

# ==========================
# PLOT
# ==========================

plt.figure(figsize=(10, 5))

plt.plot(
    test["date"],
    y_test,
    label="Actual"
)

plt.plot(
    test["date"],
    y_pred,
    label="Predicted"
)

plt.title("Actual vs Predicted CO2e")

plt.xlabel("Date")
plt.ylabel("CO2e (kg)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "model/forecast_plot.png"
)

plt.close()

# ==========================
# SAVE MODEL
# ==========================

joblib.dump(
    model,
    "model/co2e_model.pkl"
)

print("\nSaved:")
print("model/co2e_model.pkl")
print("model/forecast_plot.png")