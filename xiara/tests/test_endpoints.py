from fastapi.testclient import TestClient
from xiara.main import app


client = TestClient(app)

def test_root_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_ping():
    res = client.get("/xiara/ping")
    assert res.status_code == 200
    assert "status" in res.json()

def test_invalid_endpoint():
    res = client.get("/invalid")
    assert res.status_code == 404

def test_chat_valid_prompt():
    res = client.post("/xiara/chat", json={"prompt": "Hello"})
    assert res.status_code == 200
    assert "response" in res.json()

def test_chat_missing_prompt():
    res = client.post("/xiara/chat", json={})
    assert res.status_code == 422  # Unprocessable Entity

def test_query_valid_prompt():
    res = client.post("/xiara/query", json={"userId": "moses", "prompt": "show me phones"})
    assert res.status_code == 200
    assert "reply" in res.json()

def test_query_missing_userId():
    res = client.post("/xiara/query", json={"prompt": "what's available?"})
    assert res.status_code == 422

def test_query_missing_prompt():
    res = client.post("/xiara/query", json={"userId": "sam"})
    assert res.status_code == 422

def test_query_empty_prompt():
    res = client.post("/xiara/query", json={"userId": "sam", "prompt": ""})
    assert res.status_code == 200  # Still valid, handled by chain

def test_chat_invalid_method():
    res = client.get("/xiara/chat")
    assert res.status_code == 405

def test_query_invalid_method():
    res = client.get("/xiara/query")
    assert res.status_code == 405

def test_ping_invalid_method():
    res = client.post("/xiara/ping")
    assert res.status_code == 405
