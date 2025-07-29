from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from shared.config.settings import settings
from shared.logging.logger import logger

load_dotenv()

app = FastAPI(title="Resolute Engine", description="Dispute resolution agent for Pasar", version="0.1")

# 📦 Pydantic model for dispute analysis
class DisputeRequest(BaseModel):
    dispute_id: str
    buyer_claim: str
    seller_response: str

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Resolute Engine started in %s mode", settings.ENVIRONMENT)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Resolute", "env": settings.ENVIRONMENT}

@app.post("/resolute/analyze")
def analyze_dispute(request: DisputeRequest):
    logger.info("Resolute analyzing dispute %s", request.dispute_id)
    # MVP placeholder: dummy verdict logic
    verdict = "escalate" if "damage" in request.buyer_claim.lower() else "reject"
    return {"agent": "Resolute", "dispute_id": request.dispute_id, "verdict": verdict}
