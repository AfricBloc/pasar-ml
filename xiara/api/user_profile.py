from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from xiara.core.user_profile_manager import get_user_profile, save_user_profile

router = APIRouter(tags=["User Profile"])

# Request model for creating/updating user profile
class UserProfileRequest(BaseModel):
    user_id: str
    liked_categories: List[str] = []
    disliked_categories: List[str] = []
    price_range: Optional[str] = None  # legacy field
    preferred_price_range: Optional[str] = None
    purchase_intent: Optional[str] = None
    history: List[str] = []

    def __init__(self, **data):
        # If only price_range is provided, map it to preferred_price_range
        if "price_range" in data and "preferred_price_range" not in data:
            data["preferred_price_range"] = data["price_range"]
        super().__init__(**data)


@router.get("/user/{user_id}")
def get_profile(user_id: str):
    """Fetch a user's saved profile."""
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return dict(profile)

@router.post("/user/{user_id}")
def update_profile(user_id: str, request: UserProfileRequest):
    """Update or create a user's profile."""
    profile = get_user_profile(user_id)
    if not profile:
        from xiara.core.user_profile_manager import UserProfile
        profile = UserProfile(user_id=user_id)

    # Apply updates if provided
    if request.liked_categories is not None:
        profile.liked_categories = request.liked_categories
    if request.disliked_categories is not None:
        profile.disliked_categories = request.disliked_categories
    if request.preferred_price_range is not None:
        profile.preferred_price_range = request.preferred_price_range
    if request.purchase_intent is not None:
        profile.purchase_intent = request.purchase_intent

    save_user_profile(profile)
    return {"message": "Profile updated successfully", "profile": dict(profile)}
