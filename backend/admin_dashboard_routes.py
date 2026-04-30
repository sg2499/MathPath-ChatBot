"""
Optional Step 7 backend patch for the MathPath Chatbot backend.

Add this file to the existing backend folder and include the router in main.py:

    from admin_dashboard_routes import router as admin_dashboard_router
    app.include_router(admin_dashboard_router)

This patch adds:
- /admin/analytics
- /admin/chat-logs
- /admin/leads/{lead_id}/status

It works with the CSV storage paths already configured in Step 4.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from admin_auth import require_admin
from config import get_settings
from agents.lead_agent import list_leads

settings = get_settings()
router = APIRouter(prefix="/admin", tags=["admin-dashboard"])


class LeadStatusUpdate(BaseModel):
    status: Literal["new", "contacted", "demo_booked", "converted", "not_interested"]


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


@router.get("/analytics")
def admin_analytics(_: None = Depends(require_admin)) -> dict[str, Any]:
    leads = list_leads(limit=5000)
    total = len(leads)
    priorities = Counter(str(lead.get("lead_priority", "new")).lower() for lead in leads)
    modes = Counter(str(lead.get("preferred_mode", "not_sure")).lower() for lead in leads)
    statuses = Counter(str(lead.get("status", "new")).lower() for lead in leads)
    programs = Counter(str(lead.get("recommended_program", "not_available") or "not_available") for lead in leads)
    consented = sum(1 for lead in leads if str(lead.get("consent_to_contact", "true")).lower() == "true")

    return {
        "total_leads": total,
        "hot_leads": priorities.get("hot", 0),
        "warm_leads": priorities.get("warm", 0),
        "new_leads": priorities.get("new", 0),
        "consented_contacts": consented,
        "by_priority": dict(priorities),
        "by_mode": dict(modes),
        "by_status": dict(statuses),
        "by_recommended_program": dict(programs),
    }


@router.get("/chat-logs")
def admin_chat_logs(limit: int = 200, _: None = Depends(require_admin)) -> dict[str, Any]:
    path = settings.base_dir / settings.chat_log_csv_path
    rows = _read_csv(path)
    rows = rows[-limit:]
    rows.reverse()
    return {"count": len(rows), "chat_logs": rows}


@router.patch("/leads/{lead_id}/status")
def update_lead_status(lead_id: str, payload: LeadStatusUpdate, _: None = Depends(require_admin)) -> dict[str, Any]:
    path = settings.base_dir / settings.leads_csv_path
    rows = _read_csv(path)
    if not rows:
        raise HTTPException(status_code=404, detail="No leads found.")

    updated = None
    for row in rows:
        if row.get("lead_id") == lead_id:
            row["status"] = payload.status
            updated = row
            break

    if updated is None:
        raise HTTPException(status_code=404, detail=f"Lead not found: {lead_id}")

    _write_csv(path, rows)
    return {"status": "success", "lead": updated}
