from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from shared.config.settings import settings
from shared.logging.logger import logger

load_dotenv()

app = FastAPI(title="Xena Agent", description="Smart wallet agent for Pasar", version="0.1")

# 📦 Pydantic model for wallet command
class WalletCommand(BaseModel):
    command: str

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Xena Agent started in %s mode", settings.ENVIRONMENT)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xena", "env": settings.ENVIRONMENT}

@app.post("/xena/command")
def handle_command(request: WalletCommand):
    logger.info("Xena processing wallet command: %s", request.command)
    # MVP placeholder: dummy blockchain response
    action = f"(Xena MVP) Executed command: {request.command}"
    return {"agent": "Xena", "result": action}
