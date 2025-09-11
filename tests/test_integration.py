import pytest
from fastapi.testclient import TestClient
from resolute.main import app

client = TestClient(app)

def test_analyze_missing_files():
    payload = {
        "orderId": "ORD_TEST",
        "productId": "PROD_TEST",
        "disputeDetails": {
            "buyer_image_paths": ["tests/fixtures/buyer/missing.png"],
            "seller_image_paths": ["tests/fixtures/seller/missing.png"],
            "claim_text": "The phone is cracked",
            "product_description": "Black iPhone 12, mint condition",
            "buyer_submitted_at": "2025-09-01T12:00:00Z",
            "seller_listed_at": "2025-08-30T08:00:00Z"
        }
    }
    response = client.post(
        "/resolute/analyze",
        headers={"Authorization": "Bearer test-token"},
        json=payload
    )
    assert response.status_code == 400
    assert "Missing evidence files" in response.json()["detail"]
