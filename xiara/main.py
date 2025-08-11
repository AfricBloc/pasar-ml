import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local modules
from shared.config.settings import settings
from shared.logging.logger import logger
from xiara.api.endpoints import router as extra_router  # Optional extra Xiara endpoints
from xiara.api.product_query import router as product_query_router              # The actual product query route
from xiara.core.prompt_chain import handle_product_query
<<<<<<< HEAD
from xiara.api import user_profile


=======
>>>>>>> a31d99d0b062efdb674c9e318c9236551a31e903

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
<<<<<<< HEAD
    logger.info(" Xiara Agent started in %s mode", settings.ENVIRONMENT)
=======
    logger.info("🚀 Xiara Agent started in %s mode", settings.ENVIRONMENT)
>>>>>>> a31d99d0b062efdb674c9e318c9236551a31e903
    yield

app = FastAPI(
    title="Xiara Agent",
    description="Conversational agent for Pasar",
    version="0.1.0",
    lifespan=lifespan
)

# Health check
@app.get("/")
def health_check():
    return {"status": "ok", "service": "Xiara", "env": settings.ENVIRONMENT}
<<<<<<< HEAD

# Temporary direct chat endpoint (can be removed once router is used exclusively)
class ChatRequest(BaseModel):
    userId: str
    prompt: str

@app.post("/xiara/chat")
def chat(request: ChatRequest):
    logger.info(f"Xiara received chat from {request.userId}: {request.prompt}")
    try:
        answer = handle_product_query(request.prompt, user_id=request.userId)
        return {
            "agent": "Xiara",
            "response": answer
        }
    except Exception as e:
        logger.error(f"Xiara failed to respond: {e}")
        return {
            "agent": "Xiara",
            "response": "Sorry, I encountered an error trying to respond to your request."
        }

# Include route(s) from product_query.py and extra_router (if used)
app.include_router(product_query_router)
app.include_router(extra_router, prefix="/xiara")
app.include_router(user_profile.router, prefix="/xiara")

=======

# Temporary direct chat endpoint (can be removed once router is used exclusively)
class ChatRequest(BaseModel):
    userId: str
    prompt: str

@app.post("/xiara/chat")
def chat(request: ChatRequest):
    logger.info("Xiara received chat from %s: %s", request.userId, request.prompt)
    response_text = handle_product_query(request.prompt, user_id=request.userId)
    return {"agent": "Xiara", "response": response_text}

# Include route(s) from product_query.py and extra_router (if used)
app.include_router(product_query_router)
app.include_router(extra_router, prefix="/xiara")
>>>>>>> a31d99d0b062efdb674c9e318c9236551a31e903
