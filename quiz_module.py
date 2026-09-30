from gemini_service import gemini_service
from models import QuizResponse


def generate_quiz(text: str, question_count: int = 3) -> QuizResponse:
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    prompt = f"""
Create exactly {question_count} multiple-choice questions from the study material below.

Study material:
{text}

Rules:
- Each question must have exactly four distinct options.
- The correct_answer must exactly match one option.
- Include a short explanation for why the answer is correct.
- Questions must test understanding of the supplied material.
- Do not introduce unrelated facts.
- Return only the requested structured JSON object.
""".strip()

    return gemini_service.generate_structured(
        prompt,
        QuizResponse,
        system_instruction=(
            "You are EduGenie's quiz generator. Produce reliable, educational MCQs "
            "with plausible distractors."
        ),
    )
