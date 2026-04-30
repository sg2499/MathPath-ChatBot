import os
import pytest
import requests

API_BASE = os.getenv("MATHPATH_API_BASE_URL", "http://localhost:8000").rstrip("/")
ADMIN_TOKEN = os.getenv("MATHPATH_ADMIN_TOKEN")


@pytest.mark.skipif(not ADMIN_TOKEN, reason="MATHPATH_ADMIN_TOKEN not set")
def test_admin_list_leads_authorized():
    response = requests.get(
        f"{API_BASE}/admin/leads",
        headers={"X-Admin-Token": ADMIN_TOKEN},
        timeout=30,
    )
    assert response.status_code == 200
    payload = response.json()
    assert "count" in payload
    assert "leads" in payload


def test_admin_list_leads_rejects_without_token():
    response = requests.get(f"{API_BASE}/admin/leads", timeout=30)
    assert response.status_code in (401, 403)
