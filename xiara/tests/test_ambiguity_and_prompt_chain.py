import pytest
from unittest.mock import patch
from xiara.core.ambiguity_detector import is_ambiguous
from xiara.core.prompt_chain import handle_product_query

@pytest.mark.parametrize("query,expected", [
    ("I want something cheap", True),   # Rule-based hit
    ("I want a watch", True),           # Rule-based hit
    ("Recommend some to me", True),     # Rule-based hit
    ("I am looking for waterproof hiking boots", False),  # Should be clear
])
def test_rule_based_ambiguity(query, expected):
    """Test the rule-based path in ambiguity detection."""
    assert is_ambiguous(query, user_id="test_user") == expected

@patch("xiara.core.ambiguity_detector.llm")  # Patch LLM for fallback test
def test_llm_fallback_ambiguity(mock_llm):
    """Simulate LLM fallback when query not in rule-based dict."""
    mock_llm.predict.return_value = "Yes"
    result = is_ambiguous("Tell me something interesting", user_id="test_user_llm")
    assert result is True
    mock_llm.predict.assert_called_once()

@patch("xiara.core.prompt_chain.build_user_chain")
def test_handle_product_query_ambiguous(mock_chain):
    """Ensure ambiguous queries return clarification message."""
    query = "I want something cheap"
    response = handle_product_query(query, user_id="test_user_pc")
    assert "clarify" in response.lower() or "could you" in response.lower()

@patch("xiara.core.prompt_chain.build_user_chain")
def test_handle_product_query_non_ambiguous(mock_chain):
    """Ensure non-ambiguous queries call the QA chain."""
    mock_chain.return_value.invoke.return_value = {
        "answer": "Here are some waterproof hiking boots",
        "source_documents": []
    }
    query = "I am looking for waterproof hiking boots"
    response = handle_product_query(query, user_id="test_user_pc2")
    assert "waterproof hiking boots" in response.lower()
