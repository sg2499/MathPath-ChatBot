from __future__ import annotations

import re
from openai import OpenAI

from agents.recommendation_agent import recommendation_note
from config import get_settings
from rag.vector_store import RetrievalResult


OFFICIAL_PHONE = "7980918759 / 9831684229"
OFFICIAL_EMAIL = "info@mathpath.in"
LAKE_TOWN_CENTRE = "240, Block A, 1st Floor, Laketown, Kolkata - 700089"
RAJARHAT_CENTRE = (
    "Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road, "
    "next to Urban Greens, above Vrindavan Sweets, Kolkata 700136"
)
OFFICIAL_LOCATION = (
    f"Lake Town Centre: {LAKE_TOWN_CENTRE}\n"
    f"Rajarhat Centre: {RAJARHAT_CENTRE}"
)

CONTACT_BLOCK = (
    f"\n\nFor accurate details, please contact the MathPath team directly.\n\n"
    f"Phone: {OFFICIAL_PHONE}\n"
    f"Email: {OFFICIAL_EMAIL}\n"
    f"Centres:\n{OFFICIAL_LOCATION}"
)

PROGRAM_ENTRY_ANSWER = """In MathPath, children are enrolled into one of three entry programs based on their class group:

- **Young Learner** – For UKG, Class 1, and Class 2. Duration: 10 months. Focus: foundational operations in abacus. After completion, the child is promoted to Preparatory Level 2.
- **Preparatory Level 1** – For Class 3 and Class 4. Duration: 4 months. Focus: visual and operational fluency. After completion, the child is promoted to Preparatory Level 2.
- **Bridge Course** – For Class 5 to Class 8 late joiners. Duration: 10–12 months. Four levels are clubbed into one compact level. After completion, the child is promoted to Intermediate Level 1.
""".strip()

SYSTEM_PROMPT = f"""You are MathPath AI, the official website assistant for MathPath - Ace with Abacus.

Your role:
- Help parents and website visitors understand MathPath.
- Explain MathPath programs, age-wise levels, abacus learning, visualisation, Bridge Course, daily practice, benefits, class process, assessment, certification, competitions, and contact details.
- Guide interested parents professionally toward a demo class or callback only when appropriate.

Official MathPath contact details:
Phone: {OFFICIAL_PHONE}
Email: {OFFICIAL_EMAIL}
Centres:
{OFFICIAL_LOCATION}

Core professional style:
1. Be crisp, clear, and professional.
2. Default response length must be 2 to 5 short sentences.
3. Use bullet points only when the user asks a multi-part question or asks for comparison.
4. Answer the exact question first. Add only one useful next step when needed.
5. Do not bore users with long explanations unless they ask for details.
6. Do not repeatedly push demo booking.
7. Suggest demo/callback only when the user asks about admission, joining, program selection, child suitability, callback, enrolment, or trial class.
8. For questions like "what programs do you offer", "different programs", "age-wise programs", "how do you cater to age groups", or "which program for which class", mention only the three entry programs: Young Learner, Preparatory Level 1, and Bridge Course. Do not mention Intermediate Level or Master Module unless the user specifically asks about full progression, intermediate level, master module, advanced levels, or complete curriculum.

Strict accuracy rules:
1. Answer only using the provided MathPath context and safe organisational information.
2. Never invent fees, exact batch availability, discounts, guarantees, admission deadlines, teacher names, ownership details, management names, registration details, franchise details, or internal business details.
3. Never use placeholders such as [insert contact details here], [phone number], [email], [address], [owner name], or any unfinished placeholder text.
4. If ownership, management, fees, exact timings, offers, or internal business details are not available in the knowledge base, clearly say so and share the official MathPath contact details.
5. For factual contact/location questions, always show both MathPath centres: Lake Town Centre and Rajarhat Centre, along with phone and email.
6. Do not make medical, psychological, diagnostic, or guaranteed academic-result claims.
7. If asked about fees, say that the latest fee structure should be confirmed with MathPath and share the phone numbers.
8. If asked about batch timings, mention available broad options only: weekdays from 5 PM and weekend morning/afternoon/evening batches. Ask them to confirm exact availability with MathPath.
"""


def _format_context(results: list[RetrievalResult]) -> str:
    if not results:
        return "No matching MathPath context was retrieved."

    return "\n\n---\n\n".join(
        f"Source: {r.source}\n{r.text}" for r in results
    )


def _contains_any(message: str, terms: list[str]) -> bool:
    text = message.lower()
    return any(term in text for term in terms)


def _contains_owner_question(message: str) -> bool:
    return _contains_any(
        message,
        [
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
        ],
    )


def _contains_contact_question(message: str) -> bool:
    return _contains_any(
        message,
        [
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
        ],
    )


def _contains_demo_intent(message: str) -> bool:
    return _contains_any(
        message,
        [
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
        ],
    )


def _contains_fee_question(message: str) -> bool:
    return _contains_any(
        message,
        ["fee", "fees", "price", "pricing", "cost", "charges", "payment"],
    )


def _contains_timing_question(message: str) -> bool:
    return _contains_any(
        message,
        ["timing", "timings", "class time", "batch", "batches", "schedule", "days"],
    )


def _contains_program_entry_question(message: str) -> bool:
    """Detect questions asking for MathPath's entry/enrolment programs."""
    text = message.lower()

    asks_about_programs = any(
        term in text
        for term in [
            "program", "programs", "programme", "programmes", "course", "courses",
            "level", "levels", "age group", "age groups", "class group", "class wise",
            "class-wise", "different age", "cater", "offer", "offered", "enroll",
            "enrol", "admission", "suitable", "which class", "what class", "entry"
        ]
    )

    asks_for_overview = any(
        phrase in text
        for phrase in [
            "different programs", "different programmes", "programs you offer",
            "programmes you offer", "what programs", "what programmes",
            "which programs", "which programmes", "program details", "program structure",
            "different courses", "courses you offer", "what courses", "age groups",
            "different age group", "different age groups", "cater to different",
            "cater different", "entry program", "entry programs", "for different class",
            "for each class", "class wise program", "class-wise program",
            "how will mathpath cater", "explain about the different programs",
            "different programs you offer", "programs available"
        ]
    )

    specifically_asks_full_progression = any(
        phrase in text
        for phrase in [
            "full curriculum", "complete curriculum", "all levels", "entire program",
            "start to end", "full progression", "intermediate", "master module",
            "advanced level", "advanced levels", "after bridge", "after preparatory"
        ]
    )

    return asks_about_programs and asks_for_overview and not specifically_asks_full_progression


def _sanitize_answer(answer: str) -> str:
    """Remove AI placeholder text and keep answer compact."""
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
    if _contains_program_entry_question(message):
        return PROGRAM_ENTRY_ANSWER

    if _contains_owner_question(message):
        if _contains_contact_question(message):
            return (
                f"MathPath has two centres:\n{OFFICIAL_LOCATION}\n\n"
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

    if intent == "fees" or _contains_fee_question(message):
        return (
            "For the latest MathPath fee structure, please contact the helpline directly. "
            f"Phone: {OFFICIAL_PHONE}."
        )

    if _contains_timing_question(message):
        return (
            "MathPath offers weekday evening classes from 5 PM onward and weekend batches on Saturday and Sunday "
            "in morning, afternoon, and evening slots. Exact availability should be confirmed with the MathPath team. "
            f"Phone: {OFFICIAL_PHONE}."
        )

    if intent == "contact_location" or _contains_contact_question(message):
        return (
            f"MathPath has two centres:\n{OFFICIAL_LOCATION}\n\n"
            f"Phone: {OFFICIAL_PHONE}\n"
            f"Email: {OFFICIAL_EMAIL}"
        )

    if not results:
        return (
            "I do not have enough verified MathPath information to answer that accurately. "
            f"Please contact MathPath at {OFFICIAL_PHONE} or {OFFICIAL_EMAIL}."
        )

    context = results[0].text.strip().replace("#", "").strip()
    if len(context) > 700:
        context = context[:700].rsplit(".", 1)[0] + "."

    intro = "Here is the relevant MathPath information:"
    if recommended_program:
        intro = f"The likely fit is **{recommended_program}**. {recommendation_note(recommended_program)}"

    add_contact = intent in {"demo_booking", "program_recommendation"} or _contains_demo_intent(message)
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
Centres:
{OFFICIAL_LOCATION}

Response instructions:
- Write a crisp, professional answer for a parent or website visitor.
- Default to 2 to 5 short sentences.
- Do not write a long answer unless the user specifically asks for details.
- Answer the exact question first.
- Use bullets only when they make the answer easier to scan.
- Never use placeholders.
- Never write "[insert contact details here]" or similar placeholder text.
- If the user asks about owners, ownership, directors, management, or internal administrative details, say that this information is not publicly listed in your current MathPath knowledge base and share the official phone/email.
- If the user asks for centre/location/contact details, show both centres exactly: Lake Town Centre and Rajarhat Centre, plus phone and email.
- If the user asks about fees, do not mention any fee amount. Ask them to contact the helpline.
- If the user asks about timings, mention broad options only: weekdays from 5 PM and weekend morning/afternoon/evening batches.
- For program overview / age-wise program / programs offered questions, answer only with the three entry programs: Young Learner, Preparatory Level 1, and Bridge Course. Do not include Intermediate Level or Master Module unless the user specifically asks about advanced/full progression levels.
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
    if _contains_program_entry_question(message):
        return PROGRAM_ENTRY_ANSWER

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
            temperature=0.15,
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
    if _contains_program_entry_question(message):
        yield from _stream_words(PROGRAM_ENTRY_ANSWER)
        return

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
            temperature=0.15,
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
