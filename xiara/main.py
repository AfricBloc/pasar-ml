# main.py – Base template for all Pasar ML agent microservices

from fastapi import FastAPI
from dotenv import load_dotenv
import os

# ✅ Load .env variables
load_dotenv()

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Pasar ML Agent",
    description="Base FastAPI service for Xiara/Shogun/Resolute/Xena",
    version="0.1.0"
)

# ✅ Root healthcheck endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "service": os.getenv("ENVIRONMENT", "development")}

# ✅ Example placeholder endpoint (update per agent)
@app.post("/ping")
def ping_service():
    return {"message": "Service is up and running!"}
