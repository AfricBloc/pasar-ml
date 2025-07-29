from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Xena Agent", description="Smart wallet agent for Pasar", version="0.1")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xena", "env": os.getenv("ENVIRONMENT", "development")}

@app.post("/xena/command")
def handle_command(command: str):
    return {"agent": "Xena", "response": f"Command '{command}' received"}
