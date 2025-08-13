from fastapi import APIRouter
from pydantic import BaseModel
from shared.logging.logger import logger
from xiara.core.prompt_chain import handle_product_query 
from fastapi import APIRouter
from xiara.core.memory_config import memory  # Make sure memory is imported
from xiara.core.memory_manager import get_memory  # Import get_memory

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
    




@router.get("/debug/history/{user_id}")
def get_user_chat_history(user_id: str):
    """Return chat history for the given user_id."""
    memory = get_memory(session_id=user_id)
    history_data = []

    if hasattr(memory, "chat_memory") and hasattr(memory.chat_memory, "messages"):
        for idx, msg in enumerate(memory.chat_memory.messages, start=1):
            role = getattr(msg, "type", "unknown").capitalize()
            content = getattr(msg, "content", "")
            history_data.append({"index": idx, "role": role, "content": content})
    
    return {"user_id": user_id, "chat_history": history_data}
    