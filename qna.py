from gemini_service import gemini_service

SYSTEM_PROMPT = """
You are EduGenie, a friendly academic question-answering assistant.
Answer students accurately and clearly.
Prefer concise explanations, simple language, and examples when useful.
Do not pretend to know uncertain facts. If a question is ambiguous, state the
assumption you are making.
""".strip()


def answer_question(question: str) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = f"""
Answer the following student question.

Question:
{question}

Requirements:
- Give the direct answer first.
- Then give a short explanation.
- Use bullets when they improve readability.
- Keep the response educational and age-appropriate.
""".strip()

    return gemini_service.generate_text(prompt, SYSTEM_PROMPT)
