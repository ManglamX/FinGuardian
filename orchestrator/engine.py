from agents.fraud_agent.inference import run_fraud_inference
from agents.credit_agent.inference import run_credit_inference
from agents.compliance_agent.inference import run_compliance_check
from orchestrator.passport import build_passport

def run_transaction(transaction: dict):
    fraud = run_fraud_inference(transaction)
    credit = run_credit_inference(transaction)
    compliance = run_compliance_check(transaction)

    risk_score = (
        fraud["score"] * 0.5 +
        compliance["score"] * 0.3 +
        credit["score"] * 0.2
    )

    if fraud["flag"] or compliance["flag"]:
        decision = "BLOCK"
    elif risk_score > 0.6:
        decision = "FLAG"
    else:
        decision = "ALLOW"

    passport = build_passport(
        transaction,
        fraud,
        credit,
        compliance,
        decision,
        risk_score
    )

    return decision, passport
