from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None
    parent_name: str | None = None
    child_name: str | None = None
    child_age: str | None = None
    child_class: str | None = None


class SourceChunk(BaseModel):
    source: str
    score: float
    text: str


class ChatResponse(BaseModel):
    answer: str
    intent: str
    recommended_program: str | None = None
    sources: list[SourceChunk] = Field(default_factory=list)
    should_capture_lead: bool = False
    suggested_questions: list[str] = Field(default_factory=list)
    session_id: str


class LeadRequest(BaseModel):
    parent_name: str = Field(..., min_length=2, max_length=120)
    child_name: str | None = Field(default=None, max_length=120)
    child_age: str | None = Field(default=None, max_length=20)
    child_class: str | None = Field(default=None, max_length=40)
    phone: str = Field(..., min_length=7, max_length=20)
    email: str | None = Field(default=None, max_length=160)
    preferred_mode: Literal["offline", "online", "hybrid", "not_sure"] = "not_sure"
    preferred_callback_time: str | None = Field(default=None, max_length=120)
    main_concern: str | None = Field(default=None, max_length=300)
    message: str | None = Field(default=None, max_length=1000)
    session_id: str | None = None
    source: str = "mathpath_chatbot_widget"
    consent_to_contact: bool = True

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str) -> str:
        cleaned = value.strip().replace(" ", "").replace("-", "")
        allowed = set("+0123456789")
        if not cleaned or any(ch not in allowed for ch in cleaned):
            raise ValueError("Phone number should contain only digits and an optional + sign.")
        if cleaned.count("+") > 1 or ("+" in cleaned and not cleaned.startswith("+")):
            raise ValueError("Phone number should contain an optional + sign only at the beginning.")
        if len(cleaned.replace("+", "")) < 7:
            raise ValueError("Phone number is too short.")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None or value.strip() == "":
            return None
        value = value.strip()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Please enter a valid email address.")
        return value


class LeadResponse(BaseModel):
    status: str
    message: str
    lead_id: str | None = None


class LeadRecord(BaseModel):
    lead_id: str
    created_at: str
    parent_name: str
    child_name: str | None = None
    child_age: str | None = None
    child_class: str | None = None
    phone: str
    email: str | None = None
    preferred_mode: str
    preferred_callback_time: str | None = None
    main_concern: str | None = None
    message: str | None = None
    session_id: str | None = None
    source: str
    recommended_program: str | None = None
    lead_score: int
    lead_priority: str
    status: str
    consent_to_contact: bool
