import json
from pydantic import BaseModel
from typing import List, Optional
import redis
import os

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:10920")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class UserProfile(BaseModel):
    user_id: str
    liked_categories: List[str] = []
    disliked_categories: List[str] = []
    preferred_price_range: Optional[str] = None
    purchase_intent: Optional[str] = None
    history: List[str] = []

def get_user_profile(user_id: str) -> Optional[UserProfile]:
    """Retrieve user profile from Redis"""
    data = redis_client.get(f"user_profile:{user_id}")
    if data:
        # Explicitly cast to str for type checkers
        return UserProfile(**json.loads(str(data)))
    return None

def save_user_profile(profile: UserProfile):
    """Save user profile to Redis"""
    redis_client.set(f"user_profile:{profile.user_id}", profile.json())

def add_to_history(user_id: str, query: str):
    """Append a query to user's history in Redis"""
    profile = get_user_profile(user_id)
    if not profile:
        profile = UserProfile(user_id=user_id)
    profile.history.append(query)
    save_user_profile(profile)
