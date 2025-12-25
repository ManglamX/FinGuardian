def analyze_behavior(transaction: dict, user_profile: dict) -> dict:
    """
    Analyzes transaction context for anomalous behavior.
    """
    score = 0.0
    reasons = []

    # 1. Time of Day Analysis (Late night risky window: 11PM - 4AM)
    hour = transaction.get("hour_of_day", 12)
    if hour >= 23 or hour <= 4:
        score += 0.3
        reasons.append("Unusual transaction time (late night)")

    # 2. Spending Velocity
    # Assuming 'txn_frequency_1h' is available
    freq = transaction.get("txn_frequency_1h", 0)
    avg_freq = user_profile.get("avg_txn_frequency", 1)
    
    if freq > avg_freq * 3:
        score += 0.4
        reasons.append("High spending velocity detected")

    # 3. Amount Deviation
    amount = transaction.get("amount", 0)
    avg_amt = user_profile.get("avg_transaction_amount", 100)
    
    if amount > avg_amt * 5:
        score += 0.2
        reasons.append("Significant deviation from average transaction amount")

    # Normalize score
    score = min(score, 1.0)

    return {
        "behavior_score": score,
        "behavior_reasons": reasons
    }
