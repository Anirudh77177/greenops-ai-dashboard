import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# LOAD DATASET
# ==========================

df = pd.read_excel("data/cloud_usage_dataset.xlsx")

print("=" * 50)
print("DATASET SHAPE")
print(df.shape)

print("\n" + "=" * 50)
print("DATA TYPES")
print(df.dtypes)

print("\n" + "=" * 50)
print("FIRST 10 ROWS")
print(df.head(10))

print("\n" + "=" * 50)
print("NULL VALUES")
print(df.isnull().sum())

# Remove missing values if any
df = df.dropna()

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# ==========================
# COST ANALYSIS
# ==========================

print("\n" + "=" * 50)
print("TOTAL COST (USD)")
print(df['cost_usd'].sum())

daily_cost = df.groupby('date')['cost_usd'].sum().mean()

print("\nAVERAGE DAILY COST (USD)")
print(daily_cost)

# ==========================
# CO2e CALCULATION
# ==========================

df['co2e_kg'] = (
    (df['cpu_hours'] * 0.0002)
    + ((df['storage_gb'] * 0.00006) / 30)
    + (df['data_transfer_gb'] * 0.001)
)

print("\n" + "=" * 50)
print("TOTAL CO2e (KG)")
print(df['co2e_kg'].sum())

# ==========================
# CO2e BY SERVICE TYPE
# ==========================

service_co2e = (
    df.groupby('service_type')['co2e_kg']
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 50)
print("CO2e BY SERVICE TYPE")
print(service_co2e)

# ==========================
# CO2e BY TEAM
# ==========================

team_co2e = (
    df.groupby('team')['co2e_kg']
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 50)
print("CO2e BY TEAM")
print(team_co2e)

# ==========================
# DAILY CO2e LINE CHART
# ==========================

daily_co2e = df.groupby('date')['co2e_kg'].sum()

plt.figure(figsize=(10, 5))
daily_co2e.plot()

plt.title("Daily CO2e Emissions")
plt.xlabel("Date")
plt.ylabel("CO2e (kg)")
plt.grid(True)

plt.tight_layout()
plt.savefig("data/daily_co2e.png")
plt.close()

# ==========================
# REGION CO2e BAR CHART
# ==========================

region_co2e = (
    df.groupby('region')['co2e_kg']
    .sum()
)

plt.figure(figsize=(8, 5))
region_co2e.plot(kind='bar')

plt.title("CO2e by Region")
plt.xlabel("Region")
plt.ylabel("CO2e (kg)")

plt.tight_layout()
plt.savefig("data/region_co2e.png")
plt.close()

# ==========================
# SAVE ENRICHED DATASET
# ==========================

df.to_csv(
    "data/cloud_usage_enriched.csv",
    index=False
)

print("\n" + "=" * 50)
print("FILES CREATED SUCCESSFULLY")
print("✓ cloud_usage_enriched.csv")
print("✓ daily_co2e.png")
print("✓ region_co2e.png")

print("\nHURDLE 1 COMPLETED SUCCESSFULLY")