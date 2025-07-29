from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from shared.config.settings import settings
from shared.logging.logger import logger

load_dotenv()

app = FastAPI(title="Shogun Agent", description="Security & anomaly detection for Pasar", version="0.1")

# 📦 Pydantic model for login event
class LoginEvent(BaseModel):
    username: str
    location: str

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Shogun Agent started in %s mode", settings.ENVIRONMENT)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Shogun", "env": settings.ENVIRONMENT}

@app.post("/shogun/event/login")
def login_event(event: LoginEvent):
    logger.info("Shogun analyzing login for: %s from %s", event.username, event.location)
    # MVP placeholder: simple rule-based detection
    suspicious = "Nigeria" not in event.location
    return {"agent": "Shogun", "result": "suspicious" if suspicious else "normal"}
    # Future - connect anomaly detection model here