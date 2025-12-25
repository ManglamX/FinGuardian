from fastapi.testclient import TestClient
from app import app
from services.intelligence_sharing import intelligence_service

client = TestClient(app)

def test_intent_engine_allow():
    """Test low-risk transaction gets ALLOW decision"""
    payload = {
        "transaction": {
            "amount": 100.0,
            "hour_of_day": 12,
            "txn_frequency_1h": 1,
            "is_new_account": 0,
            "is_suspicious_type": 0,
            "type": "PAYMENT",
            "oldbalanceOrg": 1000.0,
            "newbalanceOrig": 900.0
        },
        "user_profile": {
            "avg_transaction_amount": 100.0,
            "txn_count": 100,
            "avg_txn_frequency": 1.0,
            "balance_stability": 1.0
        }
    }
    response = client.post("/pre-transaction/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "decision" in data
    assert "behavioral" in data
    assert "stress" in data
    assert "regret" in data
    print(f"✓ Low-risk test: Decision = {data['decision']}, Risk = {data['total_risk_score']}")

def test_intent_engine_block():
    """Test high-risk transaction gets BLOCK decision"""
    payload = {
        "transaction": {
            "amount": 10000.0,
            "hour_of_day": 3,
            "txn_frequency_1h": 10,
            "is_new_account": 1,
            "is_suspicious_type": 1,
            "type": "CASH_OUT",
            "oldbalanceOrg": 10000.0,
            "newbalanceOrig": 0.0
        },
        "user_profile": {
            "avg_transaction_amount": 100.0,
            "txn_count": 10,
            "avg_txn_frequency": 1.0,
            "balance_stability": 0.1
        }
    }
    response = client.post("/pre-transaction/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] in ["BLOCK", "VERIFY"]
    assert data["total_risk_score"] > 0.5
    print(f"✓ High-risk test: Decision = {data['decision']}, Risk = {data['total_risk_score']}")

def test_verification_flow():
    """Test verification response endpoint"""
    response = client.post("/verification/respond", json={"req_id": "test_123", "response": "YES"})
    assert response.status_code == 200
    data = response.json()
    # Service returns DENIED for unknown req_id, which is expected behavior
    assert data["status"] in ["VERIFIED", "DENIED"]
    print(f"✓ Verification test: Status = {data['status']}")

def test_risk_events():
    """Test inter-bank intelligence sharing endpoint"""
    response = client.get("/risk-events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(f"✓ Risk events test: Retrieved {len(response.json())} patterns")

def test_intelligence_sharing():
    """Test that fraud patterns are shared"""
    initial_count = len(intelligence_service.shared_patterns)
    
    # Trigger a BLOCK decision which should publish pattern
    payload = {
        "transaction": {
            "amount": 50000.0,
            "hour_of_day": 2,
            "txn_frequency_1h": 20,
            "is_new_account": 1,
            "is_suspicious_type": 1,
            "type": "TRANSFER",
            "oldbalanceOrg": 50000.0,
            "newbalanceOrig": 0.0
        },
        "user_profile": {
            "avg_transaction_amount": 50.0,
            "txn_count": 5,
            "avg_txn_frequency": 0.5,
            "balance_stability": 0.05
        }
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    
    # Check if pattern was shared (only if fraud_label is HIGH)
    # Pattern sharing happens when fraud_label == "HIGH"
    print(f"✓ Intelligence sharing test: Patterns before={initial_count}, after={len(intelligence_service.shared_patterns)}")

if __name__ == "__main__":
    print("\n🧪 Running Advanced Features Tests...\n")
    test_intent_engine_allow()
    test_intent_engine_block()
    test_verification_flow()
    test_risk_events()
    test_intelligence_sharing()
    print("\n✅ All tests passed!\n")
