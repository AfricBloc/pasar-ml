from fastapi.testclient import TestClient
from shogun.main import app

client = TestClient(app)


def test_root_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ping():
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.json()["service"] == "Shogun"


def test_login_event_normal():
    payload = {"username": "john", "location": "Lagos, Nigeria"}
    res = client.post("/shogun/event/login", json=payload)
    assert res.status_code == 200
    assert res.json()["result"] == "normal"


def test_login_event_suspicious():
    payload = {"username": "john", "location": "New York, USA"}
    res = client.post("/shogun/event/login", json=payload)
    assert res.status_code == 200
    assert res.json()["result"] == "suspicious"


def test_check_transaction_normal():
    payload = {
        "userId": "moses",
        "amount": 499.99,
        "location": "Lagos",
        "country": "Nigeria"
    }
    res = client.post("/check", json=payload)
    assert res.status_code == 200
    assert res.json()["fraud"] is False


def test_check_transaction_fraud():
    payload = {
        "userId": "moses",
        "amount": 15000,
        "location": "Abuja",
        "country": "Ghana"
    }
    res = client.post("/check", json=payload)
    assert res.status_code == 200
    assert res.json()["fraud"] is True
    reasons = res.json()["reasons"]
    assert "Amount exceeds $1000" in reasons
    assert "Transaction outside Nigeria" in reasons


def test_check_missing_fields():
    payload = {
        "userId": "moses",
        "amount": 15000
        # Missing location and country
    }
    res = client.post("/check", json=payload)
    assert res.status_code == 422


def test_check_empty_body():
    res = client.post("/check", json={})
    assert res.status_code == 422


def test_invalid_endpoint():
    res = client.get("/invalid")
    assert res.status_code == 404
