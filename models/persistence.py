from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RiskEvent(BaseModel):
    transaction_id: str
    timestamp: datetime
    agents_scores: dict
    decision: str
    reasons: List[str]

class VerificationRequest(BaseModel):
    transaction_id: str
    user_id: str
    method: str  # SMS, IVR, APP
    status: str  # PENDING, VERIFIED, DENIED

class AuditLog(BaseModel):
    event_type: str
    details: dict
    timestamp: datetime
