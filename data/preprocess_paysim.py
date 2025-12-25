import pandas as pd

RAW_PATH = "data/raw/paysim.csv"
OUT_PATH = "data/processed/paysim_fraud_features.csv"

CHUNK_SIZE = 200_000
SAMPLE_LIMIT = 300_000

chunks = []
total_rows = 0
seen_accounts = set()

for chunk in pd.read_csv(RAW_PATH, chunksize=CHUNK_SIZE):
    # Sample chunk
    chunk = chunk.sample(frac=0.15, random_state=42)

    # Feature engineering
    chunk["hour_of_day"] = chunk["step"] % 24

    txn_counts = chunk.groupby(["nameOrig", "step"]).size()
    chunk["txn_frequency_1h"] = chunk.set_index(["nameOrig", "step"]).index.map(txn_counts)

    # New account flag
    chunk["is_new_account"] = chunk["nameOrig"].apply(
        lambda x: 0 if x in seen_accounts else 1
    )
    seen_accounts.update(chunk["nameOrig"].unique())

    # Suspicious transaction types
    chunk["is_suspicious_type"] = chunk["type"].isin(
        ["TRANSFER", "CASH_OUT"]
    ).astype(int)

    features = chunk[
        ["amount", "hour_of_day", "txn_frequency_1h",
         "is_new_account", "is_suspicious_type", "isFraud"]
    ]

    chunks.append(features)
    total_rows += len(features)

    if total_rows >= SAMPLE_LIMIT:
        break

df = pd.concat(chunks)
df.to_csv(OUT_PATH, index=False)

print(f"✅ Preprocessed {len(df)} rows for fraud training")
