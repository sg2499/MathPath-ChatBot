from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="MathPath AI Chatbot Backend", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5.1-chat-latest", alias="OPENAI_MODEL")
    allowed_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000,https://www.mathpath.in,https://mathpath.in",
        alias="ALLOWED_ORIGINS",
    )

    # Local CSV storage
    leads_csv_path: str = Field(default="storage/leads.csv", alias="LEADS_CSV_PATH")
    chat_log_csv_path: str = Field(default="storage/chat_logs.csv", alias="CHAT_LOG_CSV_PATH")

    # Optional external lead forwarding
    # Use this for Make/Zapier/Pabbly/Google Apps Script webhook automation.
    lead_webhook_url: str | None = Field(default=None, alias="LEAD_WEBHOOK_URL")

    # Optional Supabase REST storage
    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_service_role_key: str | None = Field(default=None, alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_leads_table: str = Field(default="mathpath_leads", alias="SUPABASE_LEADS_TABLE")

    # Simple admin protection for lead export endpoints
    admin_api_key: str = Field(default="change_this_admin_key", alias="ADMIN_API_KEY")

    # Retrieval settings
    top_k: int = Field(default=5, alias="TOP_K")
    min_retrieval_score: float = Field(default=0.08, alias="MIN_RETRIEVAL_SCORE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def allowed_origin_list(self) -> list[str]:
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent

    @property
    def knowledge_base_dir(self) -> Path:
        return self.base_dir / "knowledge_base"


@lru_cache
def get_settings() -> Settings:
    return Settings()
