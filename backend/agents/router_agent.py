import re


INTENT_KEYWORDS = {
    "demo_booking": ["book demo", "free demo", "schedule demo", "demo class", "trial class", "callback", "call me"],
    "fees": ["fee", "fees", "cost", "price", "charges", "payment"],
    "contact_location": ["contact", "phone", "email", "location", "address", "where", "near", "centre", "center", "branch"],
    "program_recommendation": ["age", "class", "grade", "which program", "which level", "suitable", "recommend", "right for my child"],
    "bridge_course": ["bridge", "late", "class 5", "class 6", "class 7", "class 8", "older child", "too late"],
    "school_math": ["school", "cbse", "icse", "state board", "wbseb", "syllabus", "exam", "homework"],
    "parent_concern": ["weak", "fear", "scared", "hate", "slow", "mistakes", "confidence", "basics", "struggle"],
    "program_details": ["program", "course", "curriculum", "level", "duration", "young learner", "preparatory", "intermediate", "master"],
    "assessment": ["assessment", "certificate", "certification", "promotion", "competition"],
}


def route_intent(message: str) -> str:
    text = message.lower()
    scores: dict[str, int] = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for keyword in keywords if keyword in text)

    best_intent, best_score = max(scores.items(), key=lambda item: item[1])
    if best_score > 0:
        return best_intent

    if re.search(r"\b[5-9]\s*(years|yrs|year old|yr old)\b", text):
        return "program_recommendation"
    if re.search(r"\b(class|grade|std|standard)\s*[1-8]\b", text):
        return "program_recommendation"
    return "general_query"
