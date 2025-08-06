import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.config.settings import settings
from shared.logging.logger import logger
from xiara.api.endpoints import router as extra_router
from xiara.core.prompt_chain import handle_product_query


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
    userId: str
    prompt: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xiara", "env": settings.ENVIRONMENT}

@app.post("/xiara/chat")
def chat(request: ChatRequest):
    logger.info("Xiara received chat from %s: %s", request.userId, request.prompt)
    # MVP placeholder: LangChain LLM connection
    # In a real implementation, this would connect to an LLM service
    response_text = handle_product_query(request.prompt, user_id=request.userId)
    return {"agent": "Xiara", "response": response_text}

app.include_router(extra_router, prefix="/xiara")