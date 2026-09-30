from gemini_service import gemini_service


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    hours_per_week: float = 5,
    weeks: int = 6,
) -> dict:
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    prompt = f"""
Create a personalized learning path for the topic "{topic}".

Learner level: {level}
Available study time: {hours_per_week} hours per week
Duration: {weeks} weeks

Return a practical plan from foundational concepts toward more advanced material.

Include:
1. A short learning goal.
2. A week-by-week plan.
3. For every week: topics, suggested activities, and a small practice task.
4. A list of recommended resource types (for example: official documentation,
   textbooks, tutorials, or practice sites). Do not invent exact URLs.
5. A final mini-project or assessment idea.
6. Tips for staying consistent.

Format the response with Markdown headings and bullet points.
""".strip()

    text = gemini_service.generate_text(
        prompt,
        "You are EduGenie's personalized learning-path coach.",
    )
    return {"topic": topic, "level": level, "plan": text}
