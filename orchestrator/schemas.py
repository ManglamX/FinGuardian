# orchestrator/schemas.py

from pydantic import BaseModel
from typing import List, Optional


class Transaction(BaseModel):
    amount: float
    hour_of_day: int
    txn_frequency_1h: int
    is_new_account: int
    is_suspicious_type: int

    # Optional PaySim fields (for compliance agent)
    type: Optional[str] = None
    oldbalanceOrg: Optional[float] = None
    newbalanceOrig: Optional[float] = None


class UserProfile(BaseModel):
    avg_transaction_amount: float
    txn_count: int
    avg_txn_frequency: Optional[float] = 0
    balance_stability: Optional[float] = 0.0


class AnalysisRequest(BaseModel):
    transaction: Transaction
    user_profile: UserProfile


class FraudResponse(BaseModel):
    fraud_score: float
    fraud_label: str
    risk_factors: List[str]


class ComplianceResponse(BaseModel):
    compliance_flag: bool
    risk_level: str
    violated_rules: List[str]


class CreditResponse(BaseModel):
    credit_score: int
    credit_risk: str
    credit_reasons: List[str]


class BehavioralResponse(BaseModel):
    behavior_score: float
    behavior_reasons: List[str]

class StressResponse(BaseModel):
    stress_score: float
    stress_reasons: List[str]

class RegretResponse(BaseModel):
    regret_score: float
    regret_reasons: List[str]

class AnalysisResponse(BaseModel):
    fraud: FraudResponse
    compliance: ComplianceResponse
    credit: CreditResponse
    behavioral: Optional[BehavioralResponse] = None
    stress: Optional[StressResponse] = None
    regret: Optional[RegretResponse] = None
    overall_status: str
    decision: str  # ALLOW, PAUSE, VERIFY, BLOCK
    total_risk_score: float # 0-1
    explanation: List[str]
