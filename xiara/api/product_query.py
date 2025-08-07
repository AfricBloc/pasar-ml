from fastapi import APIRouter
from pydantic import BaseModel
from xiara.core.prompt_chain import handle_product_query
from shared.logging.logger import logger

router = APIRouter()

# Pydantic model for input
class ProductQueryRequest(BaseModel):
    userId: str
    prompt: str

# Route: Product query endpoint
@router.post("/chat", tags=["Xiara"])
def product_chat(request: ProductQueryRequest):
    logger.info(f"Xiara received product chat from {request.userId}: {request.prompt}")
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
