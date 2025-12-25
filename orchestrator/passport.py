from datetime import datetime

def build_passport(fraud, compliance, credit, final_decision):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "decision": final_decision,
        "agents": {
            "fraud": fraud,
            "compliance": compliance,
            "credit": credit
        }
    }
