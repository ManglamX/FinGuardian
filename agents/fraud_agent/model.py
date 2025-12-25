# agents/fraud_agent/model.py

import joblib
import os

MODEL_PATH = os.path.join(
    "agents", "fraud_agent", "artifacts", "fraud_model.pkl"
)

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model
