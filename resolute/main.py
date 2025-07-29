from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Resolute Engine", description="Dispute resolution agent for Pasar", version="0.1")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Resolute", "env": os.getenv("ENVIRONMENT", "development")}

@app.post("/resolute/analyze")
def analyze_dispute(dispute_id: str):
    return {"agent": "Resolute", "result": f"Dispute {dispute_id} analysis placeholder"}
