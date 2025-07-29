from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Shogun Agent", description="Security & anomaly detection for Pasar", version="0.1")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Shogun", "env": os.getenv("ENVIRONMENT", "development")}

@app.post("/shogun/event/login")
def login_event(username: str):
    return {"agent": "Shogun", "message": f"Login event received for {username}"}
