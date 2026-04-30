import json
import os
from pathlib import Path
import requests

API_BASE = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000").rstrip("/")
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "lead_test_payloads.json"


def test_lead_capture_payloads():
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for case in cases:
        response = requests.post(f"{API_BASE}/lead", json=case["payload"], timeout=30)
        expected_status_code = case.get("expected_status_code", 200)
        assert response.status_code == expected_status_code, f"{case['id']} failed: {response.text}"
        if expected_status_code == 200:
            payload = response.json()
            assert payload.get("status") == case["expected_status"]
            assert payload.get("lead_id")
