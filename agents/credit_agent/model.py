# agents/credit_agent/model.py

def compute_credit_score(user_profile: dict) -> tuple:
    """
    Compute an interpretable credit score using alternative data.
    Returns (score, reasons).
    """

    score = 300  # base score
    reasons = []

    txn_count = user_profile.get("txn_count", 0)
    avg_amount = user_profile.get("avg_transaction_amount", 0)
    txn_frequency = user_profile.get("avg_txn_frequency", 0)
    balance_stability = user_profile.get("balance_stability", 0.0)

    # Activity level
    if txn_count >= 50:
        score += 150
        reasons.append("Consistent transaction activity")
    elif txn_count >= 20:
        score += 100
        reasons.append("Moderate transaction activity")
    else:
        reasons.append("Limited transaction history")

    # Spending behavior
    if 500 <= avg_amount <= 5000:
        score += 120
        reasons.append("Stable spending behavior")
    elif avg_amount > 5000:
        score += 80
        reasons.append("High-value transactions observed")

    # Transaction regularity
    if txn_frequency <= 3:
        score += 80
        reasons.append("Regular account usage")
    elif txn_frequency <= 5:
        score += 40
        reasons.append("Occasional burst activity")

    # Balance stability (proxy for financial discipline)
    if balance_stability >= 0.7:
        score += 70
        reasons.append("Stable account balance over time")

    # Clamp score to realistic bounds
    score = max(300, min(900, score))

    return score, reasons
