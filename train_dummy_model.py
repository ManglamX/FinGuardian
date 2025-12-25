import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest

# Define features matching inference.py
FEATURE_COLUMNS = [
    "amount",
    "hour_of_day",
    "txn_frequency_1h",
    "is_new_account",
    "is_suspicious_type",
]

# Create dummy training data
data = pd.DataFrame([
    [100.0, 10, 1, 0, 0],
    [5000.0, 23, 5, 1, 1],
    [200.0, 12, 2, 0, 0],
    [50.0, 9, 1, 0, 0],
    [10000.0, 3, 10, 1, 1]
], columns=FEATURE_COLUMNS)

# Train model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(data)

# Save model
save_dir = os.path.join("agents", "fraud_agent", "artifacts")
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "fraud_model.pkl")

joblib.dump(model, save_path)
print(f"Dummy model saved to {save_path}")
