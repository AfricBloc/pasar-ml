from fastapi import APIRouter
from pydantic import BaseModel
from shared.logging.logger import logger

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok", "message": "Xiara is running!"}

class QueryRequest(BaseModel):
    userId: str
    prompt: str

@router.post("/query")
def query(request: QueryRequest):
    logger.info("Query from user %s: %s", request.userId, request.prompt)

    user_input = request.prompt.lower()
    if "hello" in user_input:
        reply = f"Hi {request.userId}, how can I help you today?"
    elif "product" in user_input:
        reply = "You can search for products by describing them."
    else:
        reply = f"I'm not sure how to respond to: '{request.prompt}'"

    return {
        "agent": "Xiara",
        "reply": reply,
        "userId": request.userId
    }
