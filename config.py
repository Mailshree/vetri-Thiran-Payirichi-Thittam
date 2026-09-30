from functools import lru_cache
import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = Field(default="EduGenie")
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-3.8-flash", validation_alias="GEMINI_MODEL")
    explanation_mode: str = Field(
        default="gemini",
        validation_alias="EXPLANATION_MODE",
        description="gemini or local",
    )
    local_explanation_model: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M",
        validation_alias="LOCAL_EXPLANATION_MODEL",
    )
    max_input_chars: int = Field(default=20000, validation_alias="MAX_INPUT_CHARS")
    cors_origins: str = Field(default="*", validation_alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key or os.getenv("GOOGLE_API_KEY"))

    @property
    def allowed_origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
