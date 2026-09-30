from __future__ import annotations

from typing import TypeVar, Type

from google import genai
from google.genai import types
from pydantic import BaseModel

from config import settings

T = TypeVar("T", bound=BaseModel)


class GeminiService:
    """Small wrapper around the current Google GenAI Python SDK."""

    def __init__(self) -> None:
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not settings.gemini_configured:
                raise RuntimeError(
                    "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."
                )
            self._client = genai.Client(api_key=settings.gemini_api_key)
        return self._client

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        )
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: str | None = None,
    ) -> T:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=schema,
        )
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty structured response.")
        try:
            return schema.model_validate_json(text)
        except Exception as exc:
            raise RuntimeError(
                "Gemini returned invalid structured data. Please try again."
            ) from exc


gemini_service = GeminiService()
