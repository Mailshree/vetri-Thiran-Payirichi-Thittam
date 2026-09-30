# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant built with **FastAPI**, **HTML/CSS/JavaScript**, and Google's **Gemini API**.

It supports:

- Question answering
- Simple concept explanations
- 3/5/10-question MCQ generation
- Educational text summarization
- Personalized learning paths

## Architecture

```text
Browser
   |
   | HTTP / JSON
   v
FastAPI (main.py)
   |
   +--> qna.py ----------------------+
   +--> explanation_module.py -------+
   +--> quiz_module.py --------------+--> gemini_service.py --> Google Gemini API
   +--> summary_module.py -----------+
   +--> learning_path.py ------------+
   |
   +--> templates/index.html
   +--> static/style.css
```

The original project document mentioned Gemini 1.5 Pro and LaMini-Flan-T5. This implementation uses the current Google GenAI SDK and a current Gemini model by default. The explanation module also contains an optional local LaMini mode.

## 1. Prerequisites

Install:

- Python 3.10 or newer
- VS Code
- A Gemini API key

Google recommends using `GEMINI_API_KEY` as an environment variable rather than hard-coding a key.

## 2. Open the project

Open the `EduGenie` folder in VS Code.

VS Code terminal:

```powershell
cd EduGenie
```

## 3. Create a virtual environment

Windows:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
```

If `py` is unavailable:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your real key.

Do not commit `.env` to Git. It is already included in `.gitignore`.

## 6. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## 7. Test the project

The test suite does not call Gemini. It uses a fake AI service, so you can run it without spending API quota.

```bash
pytest
```

You should see all tests passing.

## 8. Test the real Gemini integration

Make sure `.env` contains a valid API key, start the server, and use the web page.

Try:

### Q&A

```text
Which is the largest ocean?
```

### Explanation

```text
Recursion
```

### Quiz

```text
Paste a short chapter or paragraph.
```

### Summary

```text
Paste a long educational paragraph.
```

### Learning path

```text
SQL
```

## 9. Test the API directly

PowerShell example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Which is the largest ocean?"}'
```

Quiz:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/quiz `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"The Pacific Ocean is the largest ocean on Earth.","question_count":3}'
```

## 10. Optional local explanation model

The original document proposed LaMini-Flan-T5-783M for concept explanations.

The project supports it without making it a mandatory dependency.

Install the optional packages:

```bash
pip install -r requirements-local.txt
```

Then change `.env`:

```text
EXPLANATION_MODE=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local-model run may download model files and can require substantial disk space/RAM. For a simple college project setup, the default Gemini explanation mode is easier to run.

## 11. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/api/health` | Application/AI configuration status |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | MCQ generation |
| POST | `/summarize` | Text summarization |
| POST | `/learn/recommendations` | Personalized learning path |

## 12. Example request bodies

### `/qa`

```json
{
  "text": "What is photosynthesis?"
}
```

### `/explain`

```json
{
  "text": "Explain recursion",
  "level": "beginner"
}
```

### `/quiz`

```json
{
  "text": "Photosynthesis is the process by which green plants convert light energy into chemical energy.",
  "question_count": 3
}
```

### `/summarize`

```json
{
  "text": "Paste a long educational passage here.",
  "max_sentences": 5
}
```

### `/learn/recommendations`

```json
{
  "topic": "SQL",
  "level": "beginner",
  "hours_per_week": 5,
  "weeks": 6
}
```

## 13. Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is active:

```powershell
.venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

### Gemini API key error

Check `.env`:

```text
GEMINI_API_KEY=your_real_key
```

Restart Uvicorn after changing `.env`.

### Port already in use

Use another port:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Tests fail because dependencies are missing

Run:

```bash
pip install -r requirements.txt
pytest
```

## 14. Security notes

- Never put the Gemini API key in frontend JavaScript.
- Keep `.env` private.
- The browser talks to FastAPI; only the backend talks to Gemini.
- The quiz endpoint uses structured output validation with Pydantic.
- Input lengths and numeric settings are validated by FastAPI/Pydantic.

## 15. Future improvements

Possible extensions:

- Login and student profiles
- Learning progress dashboard
- Persistent quiz scores
- PDF/document upload
- Image-based doubt solving
- Voice input/output
- Multilingual responses
- Teacher/parent dashboards
- Database-backed learning history
