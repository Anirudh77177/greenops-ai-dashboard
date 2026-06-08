from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
import io
import os

# Load .env file
load_dotenv()

# Connection String
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not CONN_STR:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env")

# Connect to Azure Storage
client = BlobServiceClient.from_connection_string(CONN_STR)

# Get Blob
blob_client = (
    client
    .get_container_client("greenops-data")
    .get_blob_client("cloud_usage_dataset.xlsx")
)

# Download file
data = blob_client.download_blob().readall()

# Read Excel
df = pd.read_excel(io.BytesIO(data))

print("Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nTotal Cost:")
print(df["cost_usd"].sum())