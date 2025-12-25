import os
import sys
import json
from dotenv import load_dotenv

# Ensure we can import from the root directory
sys.path.append(os.getcwd())

# Load env (though agents might check it themselves, good to have it ready)
load_dotenv()

from agents.fraud_agent.inference import detect_fraud
from agents.compliance_agent.inference import check_compliance
from agents.credit_agent.inference import assess_credit
from orchestrator.controller import analyze_transaction

def test_fraud_agent(txn, profile):
    print("--- Testing Fraud Agent ---")
    try:
        result = detect_fraud(txn, profile)
        print("SUCCESS:", json.dumps(result, indent=2))
    except Exception as e:
        print("FAILED:", e)
    print()

def test_compliance_agent(txn):
    print("--- Testing Compliance Agent ---")
    try:
        result = check_compliance(txn)
        print("SUCCESS:", json.dumps(result, indent=2))
    except Exception as e:
        print("FAILED:", e)
    print()

def test_credit_agent(profile):
    print("--- Testing Credit Agent ---")
    try:
        result = assess_credit(profile)
        print("SUCCESS:", json.dumps(result, indent=2))
    except Exception as e:
        print("FAILED:", e)
    print()

def test_orchestrator(txn, profile):
    print("--- Testing Orchestrator (Full Flow) ---")
    try:
        result = analyze_transaction(txn, profile)
        print("SUCCESS:", json.dumps(result, indent=2))
    except Exception as e:
        print("FAILED:", e)
    print()

if __name__ == "__main__":
    # Mock Data
    mock_transaction = {
        "amount": 9500.0,
        "hour_of_day": 14,
        "txn_frequency_1h": 5,
        "is_new_account": 0,
        "is_suspicious_type": 0,
        "type": "TRANSFER",
        "oldbalanceOrg": 10000.0,
        "newbalanceOrig": 500.0
    }

    mock_profile = {
        "txn_count": 50,
        "avg_transaction_amount": 500.0,
        "avg_txn_frequency": 2.5,
        "balance_stability": 0.9
    }

    test_fraud_agent(mock_transaction, mock_profile)
    test_compliance_agent(mock_transaction)
    test_credit_agent(mock_profile)
    test_orchestrator(mock_transaction, mock_profile)
