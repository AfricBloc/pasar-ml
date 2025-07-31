from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import sys
import os
from contextlib import asynccontextmanager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.config.settings import settings
from shared.logging.logger import logger
from api.endpoints import router as extra_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Xiara Agent started in %s mode", settings.ENVIRONMENT)
    yield

app = FastAPI(
    title="Xiara Agent",
    description="Conversational agent for Pasar",
    version="0.1",
    lifespan=lifespan
)

# 📦 Pydantic model for chat endpoint
class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xiara", "env": settings.ENVIRONMENT}

@app.post("/xiara/chat")
def chat(request: ChatRequest):
    logger.info("Xiara received chat prompt: %s", request.prompt)
    # MVP placeholder: Future - connect LangChain LLM here
    response_text = f"(Xiara MVP) You said: {request.prompt}"
    return {"agent": "Xiara", "response": response_text}

app.include_router(extra_router, prefix="/xiara")