def predict_financial_stress(user_profile: dict) -> dict:
    """
    Predicts short-term financial stress based on balance and obligations.
    """
    score = 0.0
    reasons = []

    # Mock fields (in a real app, these would come from a rich profile)
    balance = user_profile.get("balance_stability", 1000) * 1000 # converting normalized to mock value
    monthly_obligations = user_profile.get("avg_transaction_amount", 500) * 4 # Mock estimate

    # 1. Low Balance Threshold
    if balance < 500:
        score += 0.3
        reasons.append("Low account balance")

    # 2. High Obligation Ratio
    if monthly_obligations > balance * 0.8:
        score += 0.5
        reasons.append("High debt-to-liquid-asset ratio")

    return {
        "stress_score": min(score, 1.0),
        "stress_reasons": reasons
    }
