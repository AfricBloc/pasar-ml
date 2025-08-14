# xiara/core/ambiguity_detector.py
import re
from typing import Optional
from xiara.core.memory_manager import get_memory
from xiara.core.llm_config import llm

# Common generic terms that usually mean "needs clarification"
GENERIC_TERMS = {
    "something", "anything", "cheap", "affordable", "some", "recommend some",
    "nice one", "good one", "suggest some", "give me something"
}

# Words that often indicate a product request
PRODUCT_HINTS = {
    "watch", "boots", "phone", "bag", "shoes", "laptop", "tv", "television",
    "earphones", "headphones", "jacket", "shirt", "dress", "fridge", "refrigerator"
}

# Attributes / descriptors that reduce ambiguity
DESCRIPTORS = {
    "waterproof", "wireless", "durable", "lightweight", "compact", "leather",
    "wooden", "budget", "under", "brand", "luxury", "smart", "digital"
}


def is_ambiguous(query: str, user_id: Optional[str] = None) -> bool:
    """Hybrid ambiguity detection with rule-based → LLM fallback → memory context."""

    query_lower = query.strip().lower()

    #  Check session memory to see if prior turn has product intent
    if user_id:
        memory = get_memory(session_id=user_id)
        if hasattr(memory, "chat_memory") and memory.chat_memory.messages:
            for msg in reversed(memory.chat_memory.messages):
                if msg.type == "human":
                    content_str = str(msg.content)
                    if any(prod in content_str.lower() for prod in PRODUCT_HINTS):
                        # If last turn had product context and user is following up → not ambiguous
                        return False

    #  Rule-based: generic phrases are ambiguous
    if any(term in query_lower for term in GENERIC_TERMS):
        return True

    #  Rule-based: if we have product + descriptor → clear
    if any(prod in query_lower for prod in PRODUCT_HINTS) and any(desc in query_lower for desc in DESCRIPTORS):
        return False

    #  If product is mentioned without descriptor → might be vague
    if any(prod in query_lower for prod in PRODUCT_HINTS) and not any(desc in query_lower for desc in DESCRIPTORS):
        # Could be vague, check with LLM
        return llm_check(query_lower)

    #  No product hints → ambiguous
    if not any(prod in query_lower for prod in PRODUCT_HINTS):
        return True

    #  Fallback to LLM for borderline cases
    return llm_check(query_lower)


def llm_check(query: str) -> bool:
    """LLM-based ambiguity detection (safe fallback)."""
    try:
        prompt = (
            f"Is the following shopping-related query ambiguous (multiple possible interpretations)? "
            f"Answer only 'YES' or 'NO'. Query: '{query}'"
        )
        response = llm.invoke(prompt)
        answer = response.content.strip().upper()
        return answer.startswith("Y")
    except Exception:
        # If LLM fails, assume not ambiguous to avoid over-blocking
        return False
