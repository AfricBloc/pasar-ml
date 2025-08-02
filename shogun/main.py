import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.config.settings import settings
from shared.logging.logger import logger
from shogun.rules.checker import simple_fraud_check 


load_dotenv()

#Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Shogun Agent started in %s mode", settings.ENVIRONMENT)
    yield

#Initialize FastAPI app
app = FastAPI(
    title="Shogun Agent",
    description="Security & anomaly detection for Pasar",
    version="0.1",
    lifespan=lifespan
)

# 📦 Pydantic model for login event
class LoginEvent(BaseModel):
    username: str
    location: str

# 📦 Pydantic model for transaction check
class TransactionRequest(BaseModel):
    userId: str
    amount: float
    location: str
    country: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Shogun", "env": settings.ENVIRONMENT}

@app.get("/ping")
def ping():
    return {"status": "ok", "service": "Shogun"}

@app.post("/shogun/event/login")
def login_event(event: LoginEvent):
    logger.info("Shogun analyzing login for: %s from %s", event.username, event.location)
    # MVP placeholder: simple rule-based detection
    suspicious = "Nigeria" not in event.location
    return {"agent": "Shogun", "result": "suspicious" if suspicious else "normal"}
    # Future - connect anomaly detection model here

@app.post("/check")
def check_transaction(request: TransactionRequest):
    result = simple_fraud_check(request.model_dump())
    return {
        "fraud": result["fraud"],
        "reasons": result["reasons"]
    }