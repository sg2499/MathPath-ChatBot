import os
import requests

API_BASE = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000").rstrip("/")


def test_root_endpoint():
    response = requests.get(f"{API_BASE}/", timeout=20)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "ok"
    assert "MathPath" in payload.get("message", "")


def test_health_endpoint():
    response = requests.get(f"{API_BASE}/health", timeout=20)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "healthy"


def test_chat_endpoint_minimum_response():
    response = requests.post(
        f"{API_BASE}/chat",
        json={"message": "What is MathPath?"},
        timeout=30,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("answer")
    assert payload.get("session_id")
    assert isinstance(payload.get("sources"), list)
    assert isinstance(payload.get("suggested_questions"), list)
