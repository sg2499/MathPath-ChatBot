import os
from datetime import datetime
from supabase import create_client

def log_chat(session_id: str, message: str, answer: str, intent: str, recommended_program: str | None) -> None:
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not supabase_url or not supabase_key:
        print("No Supabase credentials found. Skipping chat log.")
        return

    try:
        supabase = create_client(supabase_url, supabase_key)
        supabase.table('chat_logs').insert({
            "created_at": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "message": message,
            "answer": answer,
            "intent": intent,
            "recommended_program": recommended_program or "",
        }).execute()
    except Exception as e:
        print(f"Failed to log chat to Supabase: {e}")
