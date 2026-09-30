from __future__ import annotations

from config import settings
from gemini_service import gemini_service


def _gemini_explanation(concept: str, level: str) -> str:
    prompt = f"""
Explain the following educational concept for a {level}-level learner.

Concept:
{concept}

Requirements:
- Start with a one-sentence definition.
- Explain the idea using simple language.
- Give one practical or everyday example.
- If appropriate, finish with 2-3 key points to remember.
- Avoid unnecessary jargon.
""".strip()

    return gemini_service.generate_text(
        prompt,
        "You are EduGenie's concept-explanation tutor. Focus on clarity and understanding.",
    )


def _local_explanation(concept: str, level: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires the optional transformers dependency. "
            "Install requirements-local.txt or use EXPLANATION_MODE=gemini."
        ) from exc

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
    )
    prompt = (
        f"Explain {concept} to a {level} student in simple language. "
        "Give a definition, short explanation, and one example."
    )
    result = generator(prompt, max_new_tokens=180, do_sample=False)
    if not result or "generated_text" not in result[0]:
        raise RuntimeError("The local explanation model returned no text.")
    return result[0]["generated_text"].strip()


def explain_concept(concept: str, level: str = "beginner") -> str:
    if not concept.strip():
        raise ValueError("Concept cannot be empty.")

    if settings.explanation_mode.lower() == "local":
        return _local_explanation(concept, level)

    return _gemini_explanation(concept, level)
