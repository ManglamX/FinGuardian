def predict_regret(user_history: dict) -> dict:
    """
    Predicts likelihood of future regret based on past reversals/complaints.
    """
    score = 0.0
    reasons = []

    reversals = user_history.get("past_reversals", 0)
    complaints = user_history.get("past_complaints", 0)

    if reversals > 2:
        score += 0.4
        reasons.append("History of transaction reversals")

    if complaints > 0:
        score += 0.3
        reasons.append("History of disputes/complaints")

    return {
        "regret_score": min(score, 1.0),
        "regret_reasons": reasons
    }
