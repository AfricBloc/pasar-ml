from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from xiara.core.prompt_chain import handle_product_query
from xiara.core.ambiguity_detector import AmbiguityDetector
from xiara.core.negotiation_handler import NegotiationHandler
from shared.logging.logger import logger

router = APIRouter()
ambiguity_detector = AmbiguityDetector()
negotiation_handler = NegotiationHandler()

clarification_attempts = {}

class ProductContext(BaseModel):
    product_id: Optional[str] = None
    price: Optional[float] = None
    name: Optional[str] = None

class ProductQueryRequest(BaseModel):
    userId: str
    prompt: str
    context: Optional[ProductContext] = None

@router.post("/chat", tags=["Xiara"])
def product_chat(request: ProductQueryRequest):
    """
    Handle product chat requests with ambiguity detection and price negotiation.
    """
    logger.info(f"Xiara received product chat from {request.userId}: {request.prompt}")

    try:
        # If context has product info, check for negotiation
        if request.context and request.context.product_id and request.context.price:
            is_negotiating, intent = negotiation_handler.detect_negotiation_intent(request.prompt)
            if is_negotiating:
                response = negotiation_handler.generate_response(
                    user_id=request.userId,
                    product_id=request.context.product_id,
                    original_price=request.context.price,
                    intent=intent
                )
                return {
                    "agent": "Xiara",
                    "response": response,
                    "needs_clarification": False,
                    "is_negotiating": True,
                    "context": request.context
                }

        # Ambiguity detection
        attempts = clarification_attempts.get(request.userId, 0)
        is_ambiguous, ambiguity_type = ambiguity_detector.is_ambiguous(
            request.prompt,
            user_id=request.userId
        )

        if is_ambiguous:
            if attempts < 2:
                clarification = ambiguity_detector.generate_clarification(
                    ambiguity_type,
                    attempt=attempts
                )
                clarification_attempts[request.userId] = attempts + 1
                return {
                    "agent": "Xiara",
                    "response": clarification,
                    "needs_clarification": True,
                    "is_negotiating": False,
                    "context": request.context
                }
            else:
                clarification_attempts[request.userId] = 0
                return {
                    "agent": "Xiara",
                    "response": ambiguity_detector.get_fallback_response(),
                    "needs_clarification": True,
                    "is_negotiating": False,
                    "context": request.context
                }

        # Clear input - reset attempts and process normally
        clarification_attempts[request.userId] = 0
        answer = handle_product_query(request.prompt, user_id=request.userId)

        # Try to extract product context from the answer (simple pattern matching)
        new_context = extract_product_context(answer)
        context = ProductContext(**new_context) if new_context else request.context

        return {
            "agent": "Xiara",
            "response": answer,
            "needs_clarification": False,
            "is_negotiating": False,
            "context": context
        }

    except Exception as e:
        logger.error(f"Xiara failed to respond: {e}")
        return {
            "agent": "Xiara",
            "response": "Sorry, I encountered an error trying to respond to your request.",
            "needs_clarification": False,
            "is_negotiating": False,
            "context": None
        }

def extract_product_context(text: str) -> Optional[dict]:
    """
    Extract product information from response text.
    Looks for lines like:
    Name: ...
    Product ID: ...
    Price: $...
    """
    import re
    try:
        price_match = re.search(r'Price:?\s*\$?([\d,]+\.?\d*)', text)
        id_match = re.search(r'(?:Product\s*ID|ID):\s*([A-Za-z0-9-]+)', text)
        name_match = re.search(r'(?:Product\s*Name|Name):\s*([^\n]+)', text)

        if price_match and id_match and name_match:
            return {
                "product_id": id_match.group(1),
                "price": float(price_match.group(1).replace(',', '')),
                "name": name_match.group(1).strip()
            }
    except Exception as e:
        logger.error(f"Error extracting product context: {e}")
    return None

@router.delete("/reset/{user_id}", tags=["Xiara"])
def reset_conversation(user_id: str):
    """Reset both clarification and negotiation state for a user."""
    if user_id in clarification_attempts:
        del clarification_attempts[user_id]
    negotiation_handler.reset_negotiation(user_id)
    return {"status": "success"}