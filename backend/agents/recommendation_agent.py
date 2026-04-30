import re


def _extract_first_number(text: str) -> int | None:
    match = re.search(r"\b(\d{1,2})\b", text)
    return int(match.group(1)) if match else None


def recommend_program(message: str, child_age: str | None = None, child_class: str | None = None) -> str | None:
    combined = " ".join(x for x in [message, child_age or "", child_class or ""] if x).lower()

    class_match = re.search(r"(?:class|grade)\s*(\d{1,2})", combined)
    if class_match:
        grade = int(class_match.group(1))
        if grade <= 2:
            return "Young Learner Program"
        if grade in [3, 4]:
            return "Preparatory Level"
        if grade in [5, 6, 7]:
            if "late" in combined or "new" in combined or "beginner" in combined or "start" in combined:
                return "Bridge Course"
            return "Intermediate Level or Bridge Course after assessment"

    age = _extract_first_number(combined)
    if age is not None:
        if 5 <= age <= 7:
            return "Young Learner Program"
        if 8 <= age <= 9:
            return "Preparatory Level"
        if 10 <= age <= 11:
            return "Intermediate Level after basic assessment"
        if age >= 12:
            return "Master Module or Bridge Course after assessment"

    if "bridge" in combined or "late" in combined:
        return "Bridge Course"
    if "master" in combined:
        return "Master Module"
    return None


def recommendation_note(program: str | None) -> str:
    if not program:
        return "For the best recommendation, please share your child's age or class."

    notes = {
        "Young Learner Program": "This is suitable for young children who need strong number sense, abacus basics, and joyful early maths confidence.",
        "Preparatory Level": "This is suitable for children who are ready to build structured abacus skills, speed, accuracy, multiplication, division, decimals, and school-maths support.",
        "Intermediate Level after basic assessment": "This is suitable when the child already has basic number confidence and is ready for advanced operations and exam-oriented application.",
        "Intermediate Level or Bridge Course after assessment": "For Classes 5–7, MathPath should first assess whether the child needs a Bridge Course or can enter the Intermediate pathway directly.",
        "Master Module or Bridge Course after assessment": "For older children, MathPath can suggest either the compact Master Module or Bridge Course after checking the child's current calculation comfort.",
        "Bridge Course": "This is designed for late joiners who need a focused route to catch up without feeling misplaced among much younger beginners.",
        "Master Module": "This is the compact advanced module for higher application topics such as percentage, square roots, cube roots, profit and loss, decimals, and simple interest.",
    }
    return notes.get(program, "MathPath can recommend the correct level after a short assessment.")
