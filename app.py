# app.py


from orchestrator.schemas import AnalysisRequest, AnalysisResponse
from orchestrator.controller import analyze_transaction
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agent-Based GenAI Financial Intelligence System",
    description="Fraud, Compliance & Credit Intelligence Backend",
    version="1.0.0",
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
