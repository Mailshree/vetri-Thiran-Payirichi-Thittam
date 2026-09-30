from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    ErrorResponse,
    ExplainRequest,
    LearningPathRequest,
    QuizRequest,
    SummaryRequest,
    TextRequest,
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    description="Google Gemini powered educational learning assistant.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": settings.gemini_configured,
        "model": settings.gemini_model,
        "explanation_mode": settings.explanation_mode,
    }


@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        return {"answer": answer_question(payload.text)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to answer the question right now.",
        )


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        return {"explanation": explain_concept(payload.text, payload.level)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to explain the concept right now.",
        )


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        result = generate_quiz(payload.text, payload.question_count)
        return result.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate the quiz right now.",
        )


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    try:
        return {"summary": summarize_text(payload.text, payload.max_sentences)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to summarize the text right now.",
        )


@app.post("/learn/recommendations")
async def learning_recommendations(payload: LearningPathRequest):
    try:
        return get_learning_recommendations(
            topic=payload.topic,
            level=payload.level,
            hours_per_week=payload.hours_per_week,
            weeks=payload.weeks,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to create a learning path right now.",
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Keep FastAPI's default JSON format for API clients.
    from fastapi.exception_handlers import http_exception_handler as default_handler
    return await default_handler(request, exc)
