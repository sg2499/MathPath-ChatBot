from datetime import datetime, timezone
from uuid import uuid4
from schemas import LeadRequest
from config import get_settings
from storage.lead_storage import SupabaseLeadStore, forward_to_webhook
from agents.lead_qualification_agent import qualify_lead

def should_capture_lead(intent: str, message: str) -> bool:
    text = message.lower()
    explicit_triggers = [
        "book demo", "free demo", "schedule demo", "demo class", "trial class",
        "book a trial", "arrange demo", "want a demo", "need a demo", "callback",
        "call me", "contact me for demo",
    ]
    return intent == "demo_booking" and any(trigger in text for trigger in explicit_triggers)

def build_lead_record(lead: LeadRequest) -> dict:
    base = lead.model_dump()
    qualification = qualify_lead(base)
    return {
        "lead_id": f"MP-{uuid4().hex[:10].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "parent_name": lead.parent_name,
        "child_name": lead.child_name or "",
        "child_age": lead.child_age or "",
        "child_class": lead.child_class or "",
        "phone": lead.phone,
        "email": lead.email or "",
        "preferred_mode": lead.preferred_mode,
        "preferred_callback_time": lead.preferred_callback_time or "",
        "main_concern": lead.main_concern or "",
        "message": lead.message or "",
        "session_id": lead.session_id or "",
        "source": lead.source or "mathpath_chatbot_widget",
        "recommended_program": qualification["recommended_program"] or "",
        "lead_score": qualification["lead_score"],
        "lead_priority": qualification["lead_priority"],
        "status": "new",
        "consent_to_contact": lead.consent_to_contact,
    }

def save_lead(lead: LeadRequest) -> dict:
    settings = get_settings()
    record = build_lead_record(lead)
    
    supabase_store = SupabaseLeadStore()
    supabase_store.save(record)

    forward_to_webhook(settings.lead_webhook_url, record)
    return record

def list_leads(limit: int = 100) -> list[dict]:
    supabase_store = SupabaseLeadStore()
    return supabase_store.list(limit=limit)
