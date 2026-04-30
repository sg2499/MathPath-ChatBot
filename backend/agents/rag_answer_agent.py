from __future__ import annotations

from openai import OpenAI

from agents.recommendation_agent import recommendation_note
from config import get_settings
from rag.vector_store import RetrievalResult

SYSTEM_PROMPT = """You are MathPath AI, the official website assistant for MathPath - Ace with Abacus.
Answer only using the provided MathPath context and safe organisational information.
Use warm, professional, parent-friendly language. Be concise, clear, and helpful.
Do not invent fees, batch timings, discounts, guarantees, medical claims, admission deadlines, or unavailable policies.
If information is unavailable, say the MathPath team can confirm it and share contact details.
Always guide interested parents toward a demo class or callback.
"""

CONTACT_BLOCK = """\n\nFor personalised guidance, parents may contact MathPath at 7980918759 / 9831684229 or email info@mathpath.in. Location: Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road, next to Urban Greens, above Vrindavan Sweets, Kolkata 700136."""


def _format_context(results: list[RetrievalResult]) -> str:
    return "\n\n---\n\n".join(f"Source: {r.source}\n{r.text}" for r in results)


def _fallback_answer(message: str, intent: str, results: list[RetrievalResult], recommended_program: str | None) -> str:
    if not results:
        return "I do not have enough MathPath information to answer that accurately." + CONTACT_BLOCK

    if intent == "fees":
        return "For fees, offers, or batch-specific charges, the MathPath team should confirm the latest details directly." + CONTACT_BLOCK

    if intent == "contact_location":
        return "MathPath can be contacted at **7980918759 / 9831684229** or **info@mathpath.in**. The centre is located at **Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road, next to Urban Greens, above Vrindavan Sweets, Kolkata 700136**."

    context = results[0].text.strip().replace("#", "").strip()
    intro = "Here is what MathPath offers based on your question:"
    if recommended_program:
        intro = f"Based on the details shared, the likely fit is **{recommended_program}**. {recommendation_note(recommended_program)}"

    if len(context) > 1100:
        context = context[:1100].rsplit(".", 1)[0] + "."

    add_contact = intent in {"demo_booking", "program_recommendation", "parent_concern", "bridge_course"}
    return f"{intro}\n\n{context}{CONTACT_BLOCK if add_contact else ''}"


def _build_user_prompt(message: str, intent: str, results: list[RetrievalResult], recommended_program: str | None) -> str:
    context = _format_context(results)
    return f"""
User question: {message}
Detected intent: {intent}
Recommended program: {recommended_program or "Not enough information"}

MathPath context:
{context}

Write a helpful answer for a parent or website visitor.
Use the recommended program only if it is relevant to the user's question.
"""


def _client() -> OpenAI | None:
    settings = get_settings()
    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
        return None
    return OpenAI(api_key=settings.openai_api_key)


def generate_answer(message: str, intent: str, results: list[RetrievalResult], recommended_program: str | None = None) -> str:
    settings = get_settings()
    client = _client()
    if client is None:
        return _fallback_answer(message, intent, results, recommended_program)

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(message, intent, results, recommended_program)},
            ],
            temperature=0.25,
        )
        return (response.choices[0].message.content or "").strip() or _fallback_answer(message, intent, results, recommended_program)
    except Exception:
        return _fallback_answer(message, intent, results, recommended_program)


def _stream_words(text: str):
    """Yield a fallback answer in small chunks so the UI still feels live without an LLM key."""
    for token in text.split(" "):
        yield token + " "


def generate_answer_stream(message: str, intent: str, results: list[RetrievalResult], recommended_program: str | None = None):
    settings = get_settings()
    client = _client()
    if client is None:
        yield from _stream_words(_fallback_answer(message, intent, results, recommended_program))
        return

    try:
        stream = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(message, intent, results, recommended_program)},
            ],
            temperature=0.25,
            stream=True,
        )
        for event in stream:
            if not event.choices:
                continue
            delta = event.choices[0].delta.content if event.choices[0].delta else None
            if delta:
                yield delta
    except Exception:
        yield from _stream_words(_fallback_answer(message, intent, results, recommended_program))
