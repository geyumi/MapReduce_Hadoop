import pandas as pd

# Load the dataset
df = pd.read_csv("btcusd_1-min_data.csv")

# Drop rows with missing values (optional)
df = df.dropna()

# Convert timestamp column from Unix time to readable datetime
df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")

# Rearrange columns: move Date to the front and drop raw Timestamp
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

# Print first few rows to confirm
print(df.head())

# Save preprocessed data
df.to_csv("cleaned_btcusd_data.csv", index=False)
