from agents.recommendation_agent import recommend_program


def qualify_lead(data: dict) -> dict:
    """Basic deterministic lead scoring for admissions follow-up.

    This helps the MathPath team quickly identify urgent demo/admission leads.
    It does not replace human counselling.
    """
    text = " ".join(str(data.get(k, "")) for k in [
        "main_concern", "message", "preferred_callback_time", "child_age", "child_class", "preferred_mode"
    ]).lower()

    score = 40
    if data.get("phone"):
        score += 15
    if data.get("child_age") or data.get("child_class"):
        score += 10
    if data.get("preferred_callback_time"):
        score += 10
    if any(word in text for word in ["demo", "admission", "join", "enroll", "enrol", "callback", "call"]):
        score += 15
    if any(word in text for word in ["weak", "struggle", "fear", "slow", "mistake", "school", "exam", "late"]):
        score += 10
    if data.get("preferred_mode") in {"offline", "online", "hybrid"}:
        score += 5

    score = min(score, 100)
    if score >= 80:
        priority = "hot"
    elif score >= 60:
        priority = "warm"
    else:
        priority = "new"

    recommended_program = recommend_program(
        data.get("message", "") or data.get("main_concern", "") or "",
        child_age=data.get("child_age"),
        child_class=data.get("child_class"),
    )

    return {
        "lead_score": score,
        "lead_priority": priority,
        "recommended_program": recommended_program,
    }
