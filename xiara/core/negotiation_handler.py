from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class NegotiationState:
    original_price: float
    target_price: float
    current_offer: float
    attempts: int
    last_update: datetime
    product_id: str

class NegotiationHandler:
    def __init__(self):
        self.negotiation_keywords = {
            'discount': ['discount', 'cheaper', 'lower price', 'better price', 'deal', 'offer'],
            'bargain': ['negotiate', 'bargain', 'reduce', 'cut price', 'best price'],
            'inquiry': ['how much', 'price', 'cost', 'pricing']
        }
        
        self.active_negotiations: Dict[str, NegotiationState] = {}
        self.MIN_DISCOUNT = 0.05  # 5% minimum discount
        self.MAX_DISCOUNT = 0.30  # 30% maximum discount
        
    def detect_negotiation_intent(self, message: str) -> Tuple[bool, Optional[str]]:
        message = message.lower()
        for intent, keywords in self.negotiation_keywords.items():
            if any(keyword in message for keyword in keywords):
                return True, intent
        return False, None

    def generate_response(self, 
                         user_id: str, 
                         product_id: str, 
                         original_price: float, 
                         intent: str) -> str:
        
        # Get or create negotiation state
        neg_state = self.active_negotiations.get(user_id)
        if not neg_state:
            neg_state = NegotiationState(
                original_price=original_price,
                target_price=original_price * 0.85,  # Initial 15% discount target
                current_offer=original_price,
                attempts=0,
                last_update=datetime.now(),
                product_id=product_id
            )
            self.active_negotiations[user_id] = neg_state

        # Handle different intents
        if intent == 'inquiry':
            return f"The current price is ${neg_state.current_offer:.2f}. Would you like to discuss a better price?"
            
        if intent == 'discount':
            if neg_state.attempts >= 3:
                return "I'll need to check with the seller for any additional discounts. Would you like me to do that?"
            
            # Calculate new offer based on attempts
            discount = min(0.05 * (neg_state.attempts + 1), self.MAX_DISCOUNT)
            new_offer = neg_state.original_price * (1 - discount)
            neg_state.current_offer = new_offer
            neg_state.attempts += 1
            
            return (f"I can offer you a special price of ${new_offer:.2f}. "
                   f"That's a {discount*100:.0f}% discount!")
                   
        if intent == 'bargain':
            if neg_state.current_offer <= neg_state.target_price:
                return ("This is already our best possible price. "
                       "Would you like to proceed with the purchase?")
            
            # Calculate counter-offer
            discount = min(0.07 * (neg_state.attempts + 1), self.MAX_DISCOUNT)
            new_offer = neg_state.original_price * (1 - discount)
            neg_state.current_offer = new_offer
            neg_state.attempts += 1
            
            return (f"I understand you're looking for a better deal. "
                   f"I can offer it at ${new_offer:.2f}. How does that sound?")

    def reset_negotiation(self, user_id: str):
        """Reset negotiation state for a user"""
        if user_id in self.active_negotiations:
            del self.active_negotiations[user_id]