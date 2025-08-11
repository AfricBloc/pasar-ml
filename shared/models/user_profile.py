# shared/models/user_profile.py
from pydantic import BaseModel
from typing import List, Optional, Tuple

class UserProfile(BaseModel):
    user_id: str
    liked_categories: List[str] = []
    price_range: Optional[Tuple[int, int]] = None  # (min_price, max_price)
    purchase_intent: Optional[str] = None
    last_queries: List[str] = []
