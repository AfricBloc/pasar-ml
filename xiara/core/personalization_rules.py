from typing import Tuple
from xiara.core.user_profile_manager import get_user_profile

def apply_personalization_filters(query: str, user_id: str) -> str:
    profile = get_user_profile(user_id)
    if not profile:
        return query  # No profile, return original query
    
    personalization_context = []

    if getattr(profile, "liked_categories", []):
        personalization_context.append(f"Focus on categories: {', '.join(profile.liked_categories)}.")
    
    if getattr(profile, "preferred_price_range", None):
        personalization_context.append(f"Filter by price range: {profile.preferred_price_range}.")
    
    if getattr(profile, "purchase_intent", None):
        personalization_context.append(f"User has {profile.purchase_intent} purchase intent.")

    # Combine personalization context with original query
    if personalization_context:
        query = f"{query}\n\n[Personalization: {' '.join(personalization_context)}]"

    return query
