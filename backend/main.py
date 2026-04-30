from __future__ import annotations

import json
from uuid import uuid4

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from admin_auth import require_admin
from admin_dashboard_routes import router as admin_dashboard_router
from agents.lead_agent import list_leads, save_lead, should_capture_lead
from agents.rag_answer_agent import generate_answer, generate_answer_stream
from agents.recommendation_agent import recommend_program
from agents.router_agent import route_intent
from config import get_settings
from rag.retriever import get_vector_store, retrieve_context
from schemas import ChatRequest, ChatResponse, LeadRequest, LeadResponse, SourceChunk
from utils.chat_logger import log_chat

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.1.0")
app.include_router(admin_dashboard_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUGGESTED_QUESTIONS = [
    "Which MathPath program is right for my child?",
    "My child is weak in maths. Can MathPath help?",
    "What is the Bridge Course?",
    "How does daily app practice work?",
    "Can I book a demo class?",
]


def _prepare_chat(message: str, child_age: str | None = None, child_class: str | None = None):
    intent = route_intent(message)
    recommended_program = recommend_program(message, child_age=child_age, child_class=child_class)
    retrieval_query = message
    if recommended_program:
        retrieval_query += f" {recommended_program} program details age class MathPath"
    results = retrieve_context(retrieval_query, top_k=settings.top_k)
    filtered = [r for r in results if r.score >= settings.min_retrieval_score] or results[:2]
    return intent, recommended_program, filtered


@app.on_event("startup")
def startup_event() -> None:
    get_vector_store()


@app.get("/")
def root() -> dict:
    return {
        "status": "ok",
        "message": "MathPath AI Chatbot Backend is running.",
        "version": "1.1.0",
        "features": [
            "agentic_rag",
            "streaming_answers",
            "lead_capture",
            "local_csv",
            "optional_supabase",
            "optional_webhook",
            "admin_dashboard",
            "qa_suite",
            "website_embed",
        ],
    }


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "knowledge_base": "loaded", "streaming": "enabled"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid4())
    intent, recommended_program, filtered = _prepare_chat(
        request.message,
        child_age=request.child_age,
        child_class=request.child_class,
    )
    answer = generate_answer(request.message, intent, filtered, recommended_program)
    log_chat(session_id, request.message, answer, intent, recommended_program)

    return ChatResponse(
        answer=answer,
        intent=intent,
        recommended_program=recommended_program,
        sources=[SourceChunk(source=r.source, score=round(r.score, 4), text=r.text[:500]) for r in filtered],
        should_capture_lead=should_capture_lead(intent, request.message),
        suggested_questions=SUGGESTED_QUESTIONS,
        session_id=session_id,
    )


@app.post("/chat/stream")
def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Stream chatbot answers using Server-Sent Events.

    The frontend receives three event types:
    - metadata: intent, source references, lead signal, session_id
    - delta: progressive text chunks
    - done: completion marker
    """
    session_id = request.session_id or str(uuid4())
    intent, recommended_program, filtered = _prepare_chat(
        request.message,
        child_age=request.child_age,
        child_class=request.child_class,
    )

    metadata = {
        "type": "metadata",
        "intent": intent,
        "recommended_program": recommended_program,
        "sources": [
            {"source": r.source, "score": round(r.score, 4), "text": r.text[:500]}
            for r in filtered
        ],
        "should_capture_lead": should_capture_lead(intent, request.message),
        "suggested_questions": SUGGESTED_QUESTIONS,
        "session_id": session_id,
    }

    def event_stream():
        full_answer = ""
        yield f"data: {json.dumps(metadata, ensure_ascii=False)}\n\n"
        try:
            for chunk in generate_answer_stream(request.message, intent, filtered, recommended_program):
                if not chunk:
                    continue
                full_answer += chunk
                yield f"data: {json.dumps({'type': 'delta', 'content': chunk}, ensure_ascii=False)}\n\n"
            final_answer = full_answer.strip()
            log_chat(session_id, request.message, final_answer, intent, recommended_program)
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id}, ensure_ascii=False)}\n\n"
        except Exception:
            fallback = (
                "I’m having trouble generating a live response right now. "
                "Please contact MathPath at 7980918759 / 9831684229 or email info@mathpath.in."
            )
            full_answer += fallback
            yield f"data: {json.dumps({'type': 'delta', 'content': fallback}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'error', 'message': 'stream_failed'}, ensure_ascii=False)}\n\n"
            log_chat(session_id, request.message, full_answer.strip(), intent, recommended_program)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/lead", response_model=LeadResponse)
def create_lead(lead: LeadRequest) -> LeadResponse:
    record = save_lead(lead)
    return LeadResponse(
        status="success",
        lead_id=record["lead_id"],
        message="Thank you. The MathPath team will contact you shortly for demo/admission guidance.",
    )


@app.get("/admin/leads")
def admin_list_leads(limit: int = 100, _: None = Depends(require_admin)) -> dict:
    leads = list_leads(limit)
    return {"count": len(leads), "leads": leads}


@app.get("/admin/leads/export")
def admin_export_leads(_: None = Depends(require_admin)) -> FileResponse:
    path = settings.base_dir / settings.leads_csv_path
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    return FileResponse(path, filename="mathpath_leads.csv", media_type="text/csv")


@app.get("/admin/chat-logs/export")
def admin_export_chat_logs(_: None = Depends(require_admin)) -> FileResponse:
    path = settings.base_dir / settings.chat_log_csv_path
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    return FileResponse(path, filename="mathpath_chat_logs.csv", media_type="text/csv")
