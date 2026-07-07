from __future__ import annotations

from typing import Any
import httpx
import os
from supabase import create_client

class SupabaseLeadStore:
    def __init__(self):
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        self.table = os.environ.get("SUPABASE_LEADS_TABLE", "leads")
        
        self.supabase = None
        if supabase_url and supabase_key:
            self.supabase = create_client(supabase_url, supabase_key)

    def save(self, record: dict[str, Any]) -> None:
        if not self.supabase:
            print("No Supabase credentials found. Skipping lead save.")
            return
        self.supabase.table(self.table).insert(record).execute()

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.supabase:
            return []
        response = self.supabase.table(self.table).select("*").order("created_at", desc=True).limit(limit).execute()
        return response.data

def forward_to_webhook(webhook_url: str | None, record: dict[str, Any]) -> None:
    if not webhook_url:
        return
    try:
        httpx.post(webhook_url, json=record, timeout=10)
    except Exception:
        pass
