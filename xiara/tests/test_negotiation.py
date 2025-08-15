import pytest
from datetime import datetime
from xiara.core.negotiation_handler import NegotiationHandler, NegotiationState

@pytest.fixture
def negotiation_handler():
    return NegotiationHandler()

def test_detect_negotiation_intent(negotiation_handler):
    # Test discount intent
    is_negotiating, intent = negotiation_handler.detect_negotiation_intent("Can I get this cheaper?")
    assert is_negotiating == True
    assert intent == 'discount'

    # Test bargain intent
    is_negotiating, intent = negotiation_handler.detect_negotiation_intent("Let's negotiate the price")
    assert is_negotiating == True
    assert intent == 'bargain'

    # Test inquiry intent
    is_negotiating, intent = negotiation_handler.detect_negotiation_intent("How much does it cost?")
    assert is_negotiating == True
    assert intent == 'inquiry'

    # Test non-negotiation message
    is_negotiating, intent = negotiation_handler.detect_negotiation_intent("I love this product")
    assert is_negotiating == False
    assert intent is None

def test_generate_response_inquiry(negotiation_handler):
    response = negotiation_handler.generate_response(
        user_id="test_user",
        product_id="test_product",
        original_price=100.0,
        intent="inquiry"
    )
    assert "current price is $100.00" in response
    assert "discuss a better price" in response

def test_generate_response_discount(negotiation_handler):
    # First attempt
    response = negotiation_handler.generate_response(
        user_id="test_user",
        product_id="test_product",
        original_price=100.0,
        intent="discount"
    )
    assert "$95.00" in response  # 5% discount
    assert "5% discount" in response

    # Second attempt - should offer bigger discount
    response = negotiation_handler.generate_response(
        user_id="test_user",
        product_id="test_product",
        original_price=100.0,
        intent="discount"
    )
    assert "$90.00" in response  # 10% discount
    assert "10% discount" in response

    # Test max attempts
    for _ in range(3):  # Push it over the limit
        response = negotiation_handler.generate_response(
            user_id="test_user",
            product_id="test_product",
            original_price=100.0,
            intent="discount"
        )
    assert "check with the seller" in response

def test_generate_response_bargain(negotiation_handler):
    response = negotiation_handler.generate_response(
        user_id="test_user2",
        product_id="test_product",
        original_price=100.0,
        intent="bargain"
    )
    assert "$93.00" in response  # 7% discount
    assert "better deal" in response

def test_reset_negotiation(negotiation_handler):
    # Start a negotiation
    negotiation_handler.generate_response(
        user_id="test_user",
        product_id="test_product",
        original_price=100.0,
        intent="discount"
    )
    assert "test_user" in negotiation_handler.active_negotiations

    # Reset it
    negotiation_handler.reset_negotiation("test_user")
    assert "test_user" not in negotiation_handler.active_negotiations