# app.py


from orchestrator.schemas import AnalysisRequest, AnalysisResponse
from orchestrator.controller import analyze_transaction
from services.verification_service import verification_service
from services.intelligence_sharing import intelligence_service
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agent-Based GenAI Financial Intelligence System",
    description="Fraud, Compliance & Credit Intelligence Backend",
    version="2.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "Backend is running 🚀"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(req: AnalysisRequest):
    return analyze_transaction(
        req.transaction.dict(),
        req.user_profile.dict()
    )

@app.post("/pre-transaction/evaluate", response_model=AnalysisResponse)
def evaluate_intent(req: AnalysisRequest):
    """
    Alias for /analyze, specifically for pre-transaction intent window.
    """
    return analyze_transaction(
        req.transaction.dict(),
        req.user_profile.dict()
    )

@app.post("/verification/respond")
def respond_verification(req_id: str = Body(...), response: str = Body(...)):
    """
    Process user verification response (YES/NO).
    """
    success = verification_service.verify_response(req_id, response)
    return {"status": "VERIFIED" if success else "DENIED", "req_id": req_id}

@app.get("/risk-events")
def get_risk_events():
    """
    Fetch recent inter-bank fraud intelligence.
    """
    return intelligence_service.fetch_recent_patterns()

