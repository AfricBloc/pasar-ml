import re
from typing import Optional, Tuple, Dict, List
from xiara.core.memory_manager import get_memory
from xiara.core.llm_config import llm

class AmbiguityDetector:
    def __init__(self):
        # Common generic terms that usually mean "needs clarification"
        self.GENERIC_TERMS = {
            "something", "anything", "cheap", "affordable", "some", "recommend some",
            "nice one", "good one", "suggest some", "give me something"
        }

        # Words that often indicate a product request
        self.PRODUCT_HINTS = {
            "watch", "boots", "phone", "bag", "shoes", "laptop", "tv", "television",
            "earphones", "headphones", "jacket", "shirt", "dress", "fridge", "refrigerator",
            # Add beauty/personal care products
            "cream", "lotion", "moisturizer", "soap", "shampoo", "deodorant",
            # Add common brands
            "nivea", "samsung", "apple", "nike", "adidas","apple","dell","hp","lenovo"

        }

        # Attributes / descriptors that reduce ambiguity
        self.DESCRIPTORS = {
            "waterproof", "wireless", "durable", "lightweight", "compact", "leather",
            "wooden", "budget", "under", "brand", "luxury", "smart", "digital", 
            "moisturizing", "hydrating", "anti-aging",
        }

        # Clarification templates for different types of ambiguity
        self.clarification_templates = {
            'price': [
                "What type of product are you looking for in your budget?",
                "Could you specify what kind of items you want within your price range?",
                "I can help you find affordable options. What category interests you?"
            ],
            'quality': [
                "What specific type of product do you want the best quality in?",
                "Which category of products would you like to explore for high quality items?",
                "I can help find top-rated items. What exactly are you looking for?"
            ],
            'generic': [
                "Could you be more specific about what type of product you're looking for?",
                "What category of items interests you?",
                "To help you better, could you tell me what kind of product you need?"
            ]
        }

    def is_ambiguous(self, query: str, user_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Detects if query is ambiguous using hybrid approach (rules → LLM → memory context).
        Returns tuple of (is_ambiguous, ambiguity_type)
        """
        query_lower = query.strip().lower()

        # If query contains both a brand and a product type, it's specific enough
        words = set(query_lower.split())
        has_brand = any(brand in words for brand in {"nivea", "samsung", "apple", "nike", "adidas", "dell", "hp", "lenovo"})
        has_product = any(prod in words for prod in self.PRODUCT_HINTS)
        
        if has_brand and has_product:
            return False, None

        # Check session memory for product intent
        if user_id:
            memory = get_memory(session_id=user_id)
            if hasattr(memory, "chat_memory") and memory.chat_memory.messages:
                for msg in reversed(memory.chat_memory.messages):
                    if msg.type == "human":
                        content_str = str(msg.content)
                        if any(prod in content_str.lower() for prod in self.PRODUCT_HINTS):
                            return False, None

        # Price-related ambiguity
        if any(term in query_lower for term in ["cheap", "affordable", "budget", "cost", "price"]):
            return True, 'price'

        # Quality-related ambiguity
        if any(term in query_lower for term in ["best", "good", "quality", "top"]):
            return True, 'quality'

        # Generic ambiguity
        if any(term in query_lower for term in self.GENERIC_TERMS):
            return True, 'generic'

        # Clear query with product + descriptor
        if any(prod in query_lower for prod in self.PRODUCT_HINTS) and \
           any(desc in query_lower for desc in self.DESCRIPTORS):
            return False, None

        # Product without descriptor - check with LLM
        if any(prod in query_lower for prod in self.PRODUCT_HINTS):
            is_ambiguous = self.llm_check(query_lower)
            return is_ambiguous, 'generic' if is_ambiguous else None

        # No product hints - ambiguous
        return True, 'generic'

    def llm_check(self, query: str) -> bool:
        """LLM-based ambiguity detection for borderline cases."""
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

    def generate_clarification(self, ambiguity_type: str, attempt: int = 0) -> str:
        """
        Generates appropriate clarifying question based on ambiguity type and attempt count.
        """
        templates = self.clarification_templates.get(ambiguity_type, self.clarification_templates['generic'])
        index = min(attempt, len(templates) - 1)
        return templates[index]

    def get_fallback_response(self) -> str:
        """Returns a fallback response when multiple clarification attempts fail."""
        return ("I want to help you find exactly what you need. "
                "Please try rephrasing your request with specific details about "
                "the type of product you're interested in.")

    def get_context_prompt(self, user_input: str, previous_context: Optional[str] = None) -> str:
        """Generates a context-aware prompt combining previous context and current input."""
        if previous_context:
            return f"Previous context: {previous_context}\nCurrent request: {user_input}"
        return user_input