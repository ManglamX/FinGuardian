# orchestrator/controller.py

from agents.fraud_agent.inference import detect_fraud
from agents.compliance_agent.inference import check_compliance
from agents.credit_agent.inference import assess_credit
from alerts.twilio_notifier import send_sms_alert
from orchestrator.passport import build_passport


def analyze_transaction(transaction: dict, user_profile: dict) -> dict:
    # 1. Run agents (REAL function names)
    fraud_result = detect_fraud(transaction, user_profile)
    compliance_result = check_compliance(transaction)
    credit_result = assess_credit(user_profile)

    # 2. Decision logic
    if compliance_result["compliance_flag"] or fraud_result["fraud_label"] == "HIGH":
        overall_status = "BLOCK"
    elif credit_result["credit_risk"] == "HIGH":
        overall_status = "FLAG"
    else:
        overall_status = "CLEAR"

    # 3. Build decision passport (internal)
    passport = build_passport(
        fraud_result,
        compliance_result,
        credit_result,
        overall_status
    )

    # 4. Twilio alert
    if overall_status == "BLOCK":
        send_sms_alert(
            "High-risk transaction blocked for your account",
            to_number="+918766529331"
        )

    # 5. API response (schema-safe)
    return {
        "fraud": fraud_result,
        "compliance": compliance_result,
        "credit": credit_result,
        "overall_status": overall_status
    }
