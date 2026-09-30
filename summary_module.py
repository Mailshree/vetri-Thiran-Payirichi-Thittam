from gemini_service import gemini_service


def summarize_text(text: str, max_sentences: int = 5) -> str:
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    prompt = f"""
Summarize the following educational passage in no more than {max_sentences} sentences.

Passage:
{text}

Requirements:
- Preserve the main ideas and important facts.
- Remove repetition and minor details.
- Use simple, clear language.
- Do not add information that is not in the passage.
""".strip()

    return gemini_service.generate_text(
        prompt,
        "You are EduGenie's study-notes summarizer.",
    )
