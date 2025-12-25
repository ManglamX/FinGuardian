# agents/credit_agent/inference.py

from agents.credit_agent.model import compute_credit_score

def assess_credit(user_profile: dict) -> dict:
    """
    Main credit assessment entry point.
    """

    credit_score, reasons = compute_credit_score(user_profile)

    if credit_score >= 750:
        risk = "LOW"
    elif credit_score >= 600:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "credit_score": credit_score,
        "credit_risk": risk,
        "credit_reasons": reasons,
    }
