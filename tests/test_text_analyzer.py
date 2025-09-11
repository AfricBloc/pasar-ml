import pytest
from resolute.analyzers.text_checker import analyze_claim_vs_description

def test_exact_match_text():
    res = analyze_claim_vs_description("Black iPhone 12", "Black iPhone 12 in mint condition")
    assert res.similarity > 0.7
    assert res.discrepancy is False

def test_color_mismatch_text():
    res = analyze_claim_vs_description("I got a red phone", "Black iPhone 12 in mint condition")
    assert res.discrepancy is True

def test_empty_claim_text():
    res = analyze_claim_vs_description("", "Black iPhone 12")
    assert res.similarity < 0.5
