from fastapi import APIRouter
from pydantic import BaseModel
from xiara.core.prompt_chain import handle_product_query
from xiara.core.ambiguity_detector import AmbiguityDetector
from shared.logging.logger import logger

router = APIRouter()
ambiguity_detector = AmbiguityDetector()

# Track clarification attempts per user
clarification_attempts = {}

class ProductQueryRequest(BaseModel):
    userId: str
    prompt: str

@router.post("/chat", tags=["Xiara"])
def product_chat(request: ProductQueryRequest):
    """
    Handle product chat requests with ambiguity detection and clarification.
    """
    logger.info(f"Xiara received product chat from {request.userId}: {request.prompt}")
    
    try:
        # Get current clarification attempts for this user
        attempts = clarification_attempts.get(request.userId, 0)
        
        # Check for ambiguity
        is_ambiguous, ambiguity_type = ambiguity_detector.is_ambiguous(
            request.prompt, 
            user_id=request.userId
        )

        if is_ambiguous:
            if attempts < 2:
                # Generate clarifying question
                clarification = ambiguity_detector.generate_clarification(
                    ambiguity_type, 
                    attempt=attempts
                )
                # Increment attempts
                clarification_attempts[request.userId] = attempts + 1
                
                return {
                    "agent": "Xiara",
                    "response": clarification,
                    "needs_clarification": True
                }
            else:
                # Reset attempts and return fallback
                clarification_attempts[request.userId] = 0
                return {
                    "agent": "Xiara",
                    "response": ambiguity_detector.get_fallback_response(),
                    "needs_clarification": True
                }
        
        # Clear input - reset attempts and process normally
        clarification_attempts[request.userId] = 0
        answer = handle_product_query(request.prompt, user_id=request.userId)
        
        return {
            "agent": "Xiara",
            "response": answer,
            "needs_clarification": False
        }

    except Exception as e:
        logger.error(f"Xiara failed to respond: {e}")
        return {
            "agent": "Xiara",
            "response": "Sorry, I encountered an error trying to respond to your request.",
            "needs_clarification": False
        }

@router.delete("/reset-clarification/{user_id}", tags=["Xiara"])
def reset_clarification(user_id: str):
    """
    Reset clarification attempts for a user.
    """
    if user_id in clarification_attempts:
        del clarification_attempts[user_id]
    return {"status": "success"}