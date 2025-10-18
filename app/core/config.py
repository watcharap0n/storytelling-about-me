"""Application configuration using environment variables."""

from functools import lru_cache
from typing import List, Optional
import os

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)

    app_name: str = "Kane Portfolio API"
    app_version: str = "1.0.0"
    environment: str = Field(default="development")

    # Provide a safe dev default; override via API_KEY env var in other environments
    api_key: str = Field(default="dev", alias="API_KEY")
    allowed_origins: List[str] = Field(default_factory=lambda: ["https://watcharapon.dev"], alias="ALLOWED_ORIGINS")

    n8n_contact_webhook: Optional[str] = Field(default=None, alias="N8N_WEBHOOK_URL")
    n8n_contact_timeout_seconds: int = Field(default=10)

    # Generic MCP forwarding webhook (optional)
    n8n_mcp_webhook: Optional[str] = Field(default=None, alias="N8N_MCP_WEBHOOK_URL")
    n8n_mcp_timeout_seconds: int = Field(default=15)

    calendar_source_url: Optional[str] = Field(default=None, alias="CALENDAR_SOURCE_URL")

    rag_endpoint: Optional[str] = Field(default=None, alias="RAG_ENDPOINT")

    rate_limit_per_minute: int = Field(default=60)

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    if os.getenv("API_KEY") is None and settings.environment.lower() in {"dev", "development", "local"}:
        print("[config] No API_KEY provided; using default 'dev' for development. Set API_KEY env var in production.")
    return settings
