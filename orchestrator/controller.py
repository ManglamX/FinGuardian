# orchestrator/controller.py

from agents.fraud_agent.inference import detect_fraud
from agents.compliance_agent.inference import check_compliance
from agents.credit_agent.inference import assess_credit
from agents.behavioral_agent.inference import analyze_behavior
from agents.financial_stress_agent.inference import predict_financial_stress
from agents.regret_agent.inference import predict_regret

from services.intelligence_sharing import intelligence_service
from services.verification_service import verification_service
from alerts.twilio_notifier import send_sms_alert
from orchestrator.passport import build_passport

def analyze_transaction(transaction: dict, user_profile: dict) -> dict:
    # 1. Run Legacy Agents
    fraud_result = detect_fraud(transaction, user_profile)
    compliance_result = check_compliance(transaction)
    credit_result = assess_credit(user_profile)

    # 2. Run New Agents
    behavior_result = analyze_behavior(transaction, user_profile)
    stress_result = predict_financial_stress(user_profile)
    # Mocking user_history for regret agent as it's not in the request schema yet
    regret_result = predict_regret({"past_reversals": 0, "past_complaints": 0}) 

    # 3. Normalize Scores (0-1)
    s_fraud = fraud_result["fraud_score"]
    s_compliance = 1.0 if compliance_result["compliance_flag"] else 0.0
    # Normalize credit score (300-850) -> higher score means lower risk, so invert
    s_credit = max(0.0, min(1.0, (850 - credit_result["credit_score"]) / 550))
    s_behavior = behavior_result["behavior_score"]
    s_stress = stress_result["stress_score"]
    s_regret = regret_result["regret_score"]

    # 4. Decision Engine (Weighted Aggregation)
    # Weights
    W = {
        "fraud": 0.35, "compliance": 0.25, "behavior": 0.15, 
        "credit": 0.10, "stress": 0.10, "regret": 0.05
    }
    
    total_risk = (
        s_fraud * W["fraud"] + 
        s_compliance * W["compliance"] + 
        s_credit * W["credit"] +
        s_behavior * W["behavior"] + 
        s_stress * W["stress"] + 
        s_regret * W["regret"]
    )

    # 5. Determine Action
    decision = "ALLOW"
    if total_risk > 0.80 or compliance_result["compliance_flag"]:
        decision = "BLOCK"
    elif total_risk > 0.60:
        decision = "VERIFY"
    elif total_risk > 0.40:
        decision = "PAUSE"

    # Backward compatibility
    overall_status = decision if decision in ["BLOCK", "FLAG"] else "CLEAR"
    if decision == "VERIFY": overall_status = "FLAG"
    if decision == "PAUSE": overall_status = "FLAG"

    # 6. Service Integration (Side Effects)
    if decision == "BLOCK":
        send_sms_alert(f"Transaction BLOCKED. Risk Score: {total_risk:.2f}", "+918766529331")
        # Share intel
        if fraud_result["fraud_label"] == "HIGH":
            intelligence_service.publish_fraud_pattern(transaction)

    elif decision == "VERIFY":
        # Trigger verification
        verification_id = verification_service.trigger_verification("user_123", "txn_001")
        print(f"Triggered verification: {verification_id}")

    # 7. Collect Explanations
    explanation = (
        fraud_result.get("risk_factors", []) + 
        compliance_result.get("violated_rules", []) +
        credit_result.get("credit_reasons", []) +
        behavior_result.get("behavior_reasons", []) +
        stress_result.get("stress_reasons", [])
    )

    # 8. Build Response
    return {
        "fraud": fraud_result,
        "compliance": compliance_result,
        "credit": credit_result,
        "behavioral": behavior_result,
        "stress": stress_result,
        "regret": regret_result,
        "overall_status": overall_status,
        "decision": decision,
        "total_risk_score": round(total_risk, 2),
        "explanation": explanation
    }
