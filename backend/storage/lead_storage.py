from __future__ import annotations

import csv
from pathlib import Path
from typing import Any
import httpx


LEAD_COLUMNS = [
    "lead_id",
    "created_at",
    "parent_name",
    "child_name",
    "child_age",
    "child_class",
    "phone",
    "email",
    "preferred_mode",
    "preferred_callback_time",
    "main_concern",
    "message",
    "session_id",
    "source",
    "recommended_program",
    "lead_score",
    "lead_priority",
    "status",
    "consent_to_contact",
]


class LocalCSVLeadStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, record: dict[str, Any]) -> None:
        file_exists = self.path.exists()
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LEAD_COLUMNS)
            if not file_exists:
                writer.writeheader()
            writer.writerow({col: record.get(col, "") for col in LEAD_COLUMNS})

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        return list(reversed(rows))[:limit]


class SupabaseLeadStore:
    def __init__(self, supabase_url: str, service_role_key: str, table: str):
        self.url = supabase_url.rstrip("/")
        self.key = service_role_key
        self.table = table

    def save(self, record: dict[str, Any]) -> None:
        endpoint = f"{self.url}/rest/v1/{self.table}"
        headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
        # Supabase/PostgREST accepts JSON array for insert.
        response = httpx.post(endpoint, headers=headers, json=[record], timeout=10)
        response.raise_for_status()


def forward_to_webhook(webhook_url: str | None, record: dict[str, Any]) -> None:
    if not webhook_url:
        return
    try:
        httpx.post(webhook_url, json=record, timeout=10)
    except Exception:
        # Never fail lead capture if the external automation is down.
        pass
