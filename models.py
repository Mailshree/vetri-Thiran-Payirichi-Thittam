from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=20000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value


class ExplainRequest(TextRequest):
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"


class SummaryRequest(TextRequest):
    max_sentences: int = Field(default=5, ge=1, le=10)


class QuizRequest(TextRequest):
    question_count: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    hours_per_week: float = Field(default=5, ge=1, le=40)
    weeks: int = Field(default=6, ge=1, le=52)

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Topic cannot be empty.")
        return value


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    title: str
    questions: list[QuizQuestion] = Field(min_length=1, max_length=10)


class ErrorResponse(BaseModel):
    detail: str
