from __future__ import annotations

import os
import requests

API_BASE = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000").rstrip("/")

checks = [
    ("GET /", "GET", "/", None),
    ("GET /health", "GET", "/health", None),
    ("POST /chat", "POST", "/chat", {"message": "What is the Bridge Course?"}),
]

for name, method, path, body in checks:
    url = f"{API_BASE}{path}"
    response = requests.request(method, url, json=body, timeout=45)
    print(f"{name}: {response.status_code}")
    print(response.text[:800])
    print("-" * 80)
    response.raise_for_status()

print("Deployment smoke test completed successfully.")
