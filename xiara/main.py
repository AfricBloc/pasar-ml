from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from shared.config.settings import settings
from shared.logging.logger import logger

load_dotenv()

app = FastAPI(title="Xiara Agent", description="Conversational agent for Pasar", version="0.1")

# 📦 Pydantic model for chat endpoint
class ChatRequest(BaseModel):
    prompt: str

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Xiara Agent started in %s mode", settings.ENVIRONMENT)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xiara", "env": settings.ENVIRONMENT}

@app.post("/xiara/chat")
def chat(request: ChatRequest):
    logger.info("Xiara received chat prompt: %s", request.prompt)
    # MVP placeholder: Future - connect LangChain LLM here
    response_text = f"(Xiara MVP) You said: {request.prompt}"
    return {"agent": "Xiara", "response": response_text}
