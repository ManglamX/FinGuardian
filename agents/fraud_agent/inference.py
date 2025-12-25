# agents/fraud_agent/inference.py

import pandas as pd
from agents.fraud_agent.model import load_model
from agents.fraud_agent.rules import extract_risk_factors

FEATURE_COLUMNS = [
    "amount",
    "hour_of_day",
    "txn_frequency_1h",
    "is_new_account",
    "is_suspicious_type",
]

def _prepare_features(txn: dict) -> pd.DataFrame:
    """
    Prepare a single-transaction DataFrame with
    the same feature names used during training.
    """
    return pd.DataFrame([{
        "amount": txn["amount"],
        "hour_of_day": txn["hour_of_day"],
        "txn_frequency_1h": txn["txn_frequency_1h"],
        "is_new_account": int(txn["is_new_account"]),
        "is_suspicious_type": int(txn["is_suspicious_type"]),
    }], columns=FEATURE_COLUMNS)

def detect_fraud(txn: dict, user_profile: dict) -> dict:
    """
    Main fraud detection entry point.
    Called by FastAPI / ADK / orchestrator.
    """

    model = load_model()

    # ML inference
    X = _prepare_features(txn)
    anomaly_score = -model.decision_function(X)[0]

    # Rule-based explanations
    risk_factors = extract_risk_factors(txn, user_profile)

    # Combine ML + rules (production-style logic)
    rule_weight = 0.15 * len(risk_factors)
    fraud_score = anomaly_score + rule_weight
    fraud_score = max(0.0, min(1.0, fraud_score))

    # Risk labeling
    if fraud_score >= 0.75:
        label = "HIGH_RISK"
    elif fraud_score >= 0.45:
        label = "MEDIUM_RISK"
    else:
        label = "LOW_RISK"

    return {
        "fraud_score": float(round(fraud_score, 2)),
        "fraud_label": label,
        "risk_factors": risk_factors,
    }
