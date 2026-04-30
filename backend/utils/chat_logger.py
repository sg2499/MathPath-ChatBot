import csv
from datetime import datetime
from config import get_settings


def log_chat(session_id: str, message: str, answer: str, intent: str, recommended_program: str | None) -> None:
    settings = get_settings()
    path = settings.base_dir / settings.chat_log_csv_path
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()

    row = {
        "created_at": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "message": message,
        "answer": answer,
        "intent": intent,
        "recommended_program": recommended_program or "",
    }

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
