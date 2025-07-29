# main.py – Base template for all Pasar ML agent microservices

from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = FastAPI(title="Xiara Agent", description="Conversational agent for Pasar", version="0.1")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xiara", "env": os.getenv("ENVIRONMENT", "development")}

@app.post("/xiara/chat")
def chat(prompt: str):
    return {"agent": "Xiara", "response": f"Received prompt: {prompt}"}
