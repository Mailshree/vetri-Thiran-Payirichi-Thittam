from fastapi.testclient import TestClient

import main
import qna
import explanation_module
import quiz_module
import summary_module
import learning_path
from models import QuizResponse, QuizQuestion


class FakeGemini:
    def generate_text(self, prompt, system_instruction=None):
        if "summarize" in prompt.lower():
            return "This is a short summary of the supplied material."
        if "learning path" in prompt.lower():
            return "# Week 1\nLearn the fundamentals.\n\n# Week 2\nPractice core concepts."
        if "explain" in prompt.lower():
            return "A simple explanation with an example."
        return "The largest ocean is the Pacific Ocean."

    def generate_structured(self, prompt, schema, system_instruction=None):
        return QuizResponse(
            title="Practice Quiz",
            questions=[
                QuizQuestion(
                    question="Which ocean is the largest?",
                    options=["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
                    correct_answer="Pacific Ocean",
                    explanation="The Pacific Ocean is the largest ocean on Earth.",
                ),
                QuizQuestion(
                    question="How many options are in this question?",
                    options=["One", "Two", "Three", "Four"],
                    correct_answer="Four",
                    explanation="The quiz requires four options per question.",
                ),
                QuizQuestion(
                    question="What is EduGenie designed to support?",
                    options=["Learning", "Driving", "Banking", "Shopping"],
                    correct_answer="Learning",
                    explanation="EduGenie is an educational learning assistant.",
                ),
            ],
        )


fake = FakeGemini()
qna.gemini_service = fake
explanation_module.gemini_service = fake
quiz_module.gemini_service = fake
summary_module.gemini_service = fake
learning_path.gemini_service = fake

client = TestClient(main.app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_qa():
    response = client.post("/qa", json={"text": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert "Pacific" in response.json()["answer"]


def test_explain():
    response = client.post(
        "/explain",
        json={"text": "Recursion", "level": "beginner"},
    )
    assert response.status_code == 200
    assert "explanation" in response.json()


def test_quiz():
    response = client.post(
        "/quiz",
        json={"text": "Oceans are large bodies of salt water.", "question_count": 3},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 3
    assert all(len(q["options"]) == 4 for q in data["questions"])


def test_summary():
    response = client.post(
        "/summarize",
        json={"text": "A long educational passage.", "max_sentences": 5},
    )
    assert response.status_code == 200
    assert "summary" in response.json()


def test_learning_path():
    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "SQL",
            "level": "beginner",
            "hours_per_week": 5,
            "weeks": 6,
        },
    )
    assert response.status_code == 200
    assert response.json()["topic"] == "SQL"


def test_validation_rejects_empty_text():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422
