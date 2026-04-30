from __future__ import annotations

import re
from openai import OpenAI

from agents.recommendation_agent import recommendation_note
from config import get_settings
from rag.vector_store import RetrievalResult


OFFICIAL_PHONE = "7980918759 / 9831684229"
OFFICIAL_EMAIL = "info@mathpath.in"
OFFICIAL_LOCATION = (
    "Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road, "
    "next to Urban Greens, above Vrindavan Sweets, Kolkata 700136"
)

CONTACT_BLOCK = (
    f"\n\nFor accurate details, please contact the MathPath team directly.\n\n"
    f"Phone: {OFFICIAL_PHONE}\n"
    f"Email: {OFFICIAL_EMAIL}\n"
    f"Location: {OFFICIAL_LOCATION}"
)

SYSTEM_PROMPT = f"""You are MathPath AI, the official website assistant for MathPath - Ace with Abacus.

Your role:
- Help parents and website visitors understand MathPath.
- Explain MathPath programs, age-wise levels, abacus learning, visualisation, Bridge Course, daily practice, benefits, and contact details.
- Guide interested parents professionally toward a demo class or callback only when appropriate.

Official MathPath contact details:
Phone: {OFFICIAL_PHONE}
Email: {OFFICIAL_EMAIL}
Location: {OFFICIAL_LOCATION}

Strict rules:
1. Answer only using the provided MathPath context and safe organisational information.
2. Never invent fees, batch timings, discounts, guarantees, admission deadlines, teacher names, ownership details, management names, registration details, franchise details, or internal business details.
3. Never use placeholders such as [insert contact details here], [phone number], [email], [address], [owner name], or any unfinished placeholder text.
4. If ownership, management, fees, exact timings, offers, or internal business details are not available in the knowledge base, clearly say that the information is not publicly listed in your current knowledge base and share the official MathPath contact details.
5. Do not over-push demo booking. Suggest a demo only when the user is asking about admission, program selection, child suitability, callback, enrolment, or interest in joining.
6. For factual contact/location questions, give the exact official contact details.
7. Do not make medical, psychological, diagnostic, or guaranteed academic-result claims.
8. Keep answers warm, concise, professional, and parent-friendly.
9. If the user asks about owners or ownership, do not guess. Say that ownership details are not publicly listed in your current knowledge base and share the official contact details.
"""


def _format_context(results: list[RetrievalResult]) -> str:
    if not results:
        return "No matching MathPath context was retrieved."

    return "\n\n---\n\n".join(
        f"Source: {r.source}\n{r.text}" for r in results
    )


def _contains_owner_question(message: str) -> bool:
    text = message.lower()
    owner_terms = [
        "owner",
        "owners",
        "ownership",
        "founder",
        "founders",
        "director",
        "directors",
        "management",
        "who runs",
        "who owns",
        "proprietor",
        "partner",
        "partners",
    ]
    return any(term in text for term in owner_terms)


def _contains_contact_question(message: str) -> bool:
    text = message.lower()
    contact_terms = [
        "location",
        "located",
        "address",
        "centre",
        "center",
        "centres",
        "centers",
        "phone",
        "number",
        "contact",
        "email",
        "where are you",
        "where is",
    ]
    return any(term in text for term in contact_terms)


def _contains_demo_intent(message: str) -> bool:
    text = message.lower()
    demo_terms = [
        "book demo",
        "free demo",
        "schedule demo",
        "trial class",
        "callback",
        "call me",
        "admission",
        "enroll",
        "enrol",
        "join",
        "register",
        "start class",
    ]
    return any(term in text for term in demo_terms)


def _sanitize_answer(answer: str) -> str:
    """
    Removes common AI placeholder patterns and replaces them with MathPath's
    official contact details so the bot never shows unfinished placeholder text.
    """
    if not answer:
        return ""

    placeholder_patterns = [
        r"\[insert contact details here\]",
        r"\[contact details\]",
        r"\[insert phone number\]",
        r"\[phone number\]",
        r"\[insert email\]",
        r"\[email\]",
        r"\[insert address\]",
        r"\[address\]",
        r"\[owner name\]",
        r"\[insert owner name\]",
        r"\[management details\]",
        r"\[insert management details\]",
    ]

    cleaned = answer
    had_placeholder = False

    for pattern in placeholder_patterns:
        if re.search(pattern, cleaned, flags=re.IGNORECASE):
            had_placeholder = True
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Remove awkward empty sentences caused by placeholder removal.
    cleaned = re.sub(r"\s+([,.!?])", r"\1", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    if had_placeholder:
        if OFFICIAL_PHONE not in cleaned and OFFICIAL_EMAIL not in cleaned:
            cleaned += CONTACT_BLOCK

    return cleaned.strip()


def _fallback_answer(
    message: str,
    intent: str,
    results: list[RetrievalResult],
    recommended_program: str | None,
) -> str:
    if _contains_owner_question(message):
        if _contains_contact_question(message):
            return (
                f"MathPath is located at {OFFICIAL_LOCATION}.\n\n"
                "Ownership or internal administrative details are not publicly listed in my current MathPath knowledge base. "
                "For official ownership, management, or administrative information, please contact the MathPath team directly.\n\n"
                f"Phone: {OFFICIAL_PHONE}\n"
                f"Email: {OFFICIAL_EMAIL}"
            )

        return (
            "Ownership or internal administrative details are not publicly listed in my current MathPath knowledge base. "
            "For official ownership, management, or administrative information, please contact the MathPath team directly.\n\n"
            f"Phone: {OFFICIAL_PHONE}\n"
            f"Email: {OFFICIAL_EMAIL}"
        )

    if intent == "fees":
        return (
            "For fees, offers, batch timings, and admission-related charges, the MathPath team should confirm the latest details directly."
            + CONTACT_BLOCK
        )

    if intent == "contact_location" or _contains_contact_question(message):
        return (
            f"You can contact MathPath at {OFFICIAL_PHONE} or email {OFFICIAL_EMAIL}.\n\n"
            f"The centre is located at {OFFICIAL_LOCATION}."
        )

    if not results:
        return (
            "I do not have enough verified MathPath information to answer that accurately."
            + CONTACT_BLOCK
        )

    context = results[0].text.strip().replace("#", "").strip()

    intro = "Here is what MathPath offers based on your question:"
    if recommended_program:
        intro = (
            f"Based on the details shared, the likely fit is **{recommended_program}**. "
            f"{recommendation_note(recommended_program)}"
        )

    if len(context) > 1100:
        context = context[:1100].rsplit(".", 1)[0] + "."

    add_contact = intent in {
        "demo_booking",
        "program_recommendation",
        "parent_concern",
        "bridge_course",
    } or _contains_demo_intent(message)

    return f"{intro}\n\n{context}{CONTACT_BLOCK if add_contact else ''}"


def _build_user_prompt(
    message: str,
    intent: str,
    results: list[RetrievalResult],
    recommended_program: str | None,
) -> str:
    context = _format_context(results)

    return f"""
User question:
{message}

Detected intent:
{intent}

Recommended program:
{recommended_program or "Not enough information"}

MathPath context:
{context}

Official MathPath contact details:
Phone: {OFFICIAL_PHONE}
Email: {OFFICIAL_EMAIL}
Location: {OFFICIAL_LOCATION}

Response instructions:
- Write a helpful answer for a parent or website visitor.
- Use the recommended program only if relevant.
- Never use placeholders.
- Never write "[insert contact details here]" or similar placeholder text.
- If the user asks about owners, ownership, directors, management, or internal administrative details, say that this information is not publicly listed in your current MathPath knowledge base and share the official phone/email.
- If the user asks for centre/location/contact details, provide the exact official MathPath contact details.
- Do not invent fees, timings, names, ownership details, guarantees, or offers.
- Do not push demo booking unless the user shows admission/joining/demo/callback intent.
"""


def _client() -> OpenAI | None:
    settings = get_settings()
    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
        return None
    return OpenAI(api_key=settings.openai_api_key)


def generate_answer(
    message: str,
    intent: str,
    results: list[RetrievalResult],
    recommended_program: str | None = None,
) -> str:
    settings = get_settings()
    client = _client()

    if client is None:
        return _sanitize_answer(
            _fallback_answer(message, intent, results, recommended_program)
        )

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": _build_user_prompt(
                        message, intent, results, recommended_program
                    ),
                },
            ],
            temperature=0.2,
        )

        answer = (response.choices[0].message.content or "").strip()
        if not answer:
            answer = _fallback_answer(message, intent, results, recommended_program)

        return _sanitize_answer(answer)

    except Exception:
        return _sanitize_answer(
            _fallback_answer(message, intent, results, recommended_program)
        )


def _stream_words(text: str):
    """Yield a fallback answer in small chunks so the UI still feels live without an LLM key."""
    for token in text.split(" "):
        yield token + " "


def generate_answer_stream(
    message: str,
    intent: str,
    results: list[RetrievalResult],
    recommended_program: str | None = None,
):
    settings = get_settings()
    client = _client()

    if client is None:
        fallback = _sanitize_answer(
            _fallback_answer(message, intent, results, recommended_program)
        )
        yield from _stream_words(fallback)
        return

    try:
        stream = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": _build_user_prompt(
                        message, intent, results, recommended_program
                    ),
                },
            ],
            temperature=0.2,
            stream=True,
        )

        for event in stream:
            if not event.choices:
                continue

            delta = event.choices[0].delta.content if event.choices[0].delta else None

            if delta:
                yield delta

    except Exception:
        fallback = _sanitize_answer(
            _fallback_answer(message, intent, results, recommended_program)
        )
        yield from _stream_words(fallback)
