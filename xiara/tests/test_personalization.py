# xiara/tests/test_personalization.py
import profile
from xiara.core.user_profile_manager import save_user_profile, get_user_profile, UserProfile
from xiara.core.personalization_rules import apply_personalization_filters

def test_personalization_rules():
    profile = UserProfile(
    user_id="u1",
    liked_categories=["laptops", "electronics"],
    preferred_price_range="₦20000 - ₦50000",
    purchase_intent="buy a new laptop"
)

    
    save_user_profile(profile)
    query = "Find a good budget laptop"
    result = apply_personalization_filters(query, "u1")
    assert "laptops" in result
    assert "₦20000" in result or "₦20,000" in result
    assert "₦50000" in result or "₦50,000" in result