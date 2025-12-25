import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

DATA_PATH = "data/processed/paysim_fraud_features.csv"
MODEL_PATH = "fraud_agent/artifacts/fraud_model.pkl"

df = pd.read_csv(DATA_PATH)

X = df[
    ["amount", "hour_of_day", "txn_frequency_1h",
     "is_new_account", "is_suspicious_type"]
]

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(X)

joblib.dump(model, MODEL_PATH)

print("✅ Fraud Isolation Forest trained & saved")
