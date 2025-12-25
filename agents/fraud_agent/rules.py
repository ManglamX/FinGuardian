# agents/fraud_agent/rules.py

def extract_risk_factors(txn: dict, user_profile: dict):
    """
    Rule-based explainability layer.
    Produces deterministic, human-readable fraud reasons.
    """

    risks = []

    avg_amt = user_profile.get("avg_transaction_amount", 0)
    txn_count = user_profile.get("txn_count", 0)

    # High amount compared to user behavior
    if avg_amt and txn["amount"] > 3 * avg_amt:
        risks.append("Transaction amount much higher than user's normal pattern")

    # New / first-time account behavior
    if txn.get("is_new_account", 0):
        risks.append("Transaction from a newly observed account")

    # High-risk transaction types (PaySim logic)
    if txn.get("is_suspicious_type", 0):
        risks.append("High-risk transaction type detected")

    # Rapid burst behavior
    if txn.get("txn_frequency_1h", 0) > 5:
        risks.append("Multiple transactions in a short time window")

    # Limited historical data
    if txn_count < 5:
        risks.append("Limited historical transaction data for this user")

    if not risks:
        risks.append("Transaction behavior falls within normal patterns")

    return risks
