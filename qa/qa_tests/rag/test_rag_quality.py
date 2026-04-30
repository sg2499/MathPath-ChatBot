import json
import os
from pathlib import Path
import requests

API_BASE = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000").rstrip("/")
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "parent_prompt_test_cases.json"


def _normalise(text: str) -> str:
    return text.lower().replace("–", "-").replace("—", "-")


def test_parent_prompt_answer_quality():
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    failures = []

    for case in cases:
        request_payload = {
            "message": case["message"],
            "child_age": case.get("child_age"),
            "child_class": case.get("child_class"),
            "session_id": f"qa-{case['id']}",
        }
        response = requests.post(f"{API_BASE}/chat", json=request_payload, timeout=45)
        if response.status_code != 200:
            failures.append(f"{case['id']}: HTTP {response.status_code} {response.text}")
            continue

        payload = response.json()
        answer = _normalise(payload.get("answer", ""))

        for keyword in case.get("expected_keywords", []):
            if keyword.lower() not in answer:
                failures.append(f"{case['id']}: missing expected keyword '{keyword}' in answer")

        for forbidden in case.get("must_not_include", []):
            if forbidden.lower() in answer:
                failures.append(f"{case['id']}: included forbidden phrase '{forbidden}'")

        expected_program = case.get("expected_recommended_program")
        if expected_program and payload.get("recommended_program") != expected_program:
            failures.append(
                f"{case['id']}: expected recommended_program='{expected_program}', got '{payload.get('recommended_program')}'"
            )

        if "expected_should_capture_lead" in case:
            if payload.get("should_capture_lead") != case["expected_should_capture_lead"]:
                failures.append(
                    f"{case['id']}: expected should_capture_lead={case['expected_should_capture_lead']}, got {payload.get('should_capture_lead')}"
                )

    assert not failures, "\n".join(failures)
