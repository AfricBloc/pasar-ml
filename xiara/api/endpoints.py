from fastapi import APIRouter
from pydantic import BaseModel
from shared.logging.logger import logger
from xiara.core.prompt_chain import handle_product_query 

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
    response_text = handle_product_query(request.prompt, user_id=request.userId)
    return {
        "agent": "Xiara",
        "reply": response_text,
        "userId": request.userId
    }