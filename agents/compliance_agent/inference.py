# agents/compliance_agent/inference.py

from agents.compliance_agent.rules import evaluate_compliance_rules

def check_compliance(txn: dict) -> dict:
    """
    Main compliance agent entry point.
    """

    violated_rules = evaluate_compliance_rules(txn)

    if not violated_rules:
        return {
            "compliance_flag": False,
            "risk_level": "LOW",
            "violated_rules": []
        }

    # Risk grading based on number of violations
    if len(violated_rules) >= 3:
        risk_level = "HIGH"
    else:
        risk_level = "MEDIUM"

    return {
        "compliance_flag": True,
        "risk_level": risk_level,
        "violated_rules": violated_rules
    }
