# CareerLens AI — Streamlit App

A production-quality, AI-powered career intelligence platform in a single Python file.

## Features

| Module | What it does |
|---|---|
| **Dashboard** | Score overview, radar chart, progress line chart, gap bar, skill pie |
| **Resume Analyzer** | Upload PDF/DOCX or paste text → AI scores resume + ATS + role match |
| **Skill Gap Analysis** | Enter skills + target role → AI returns must-haves, nice-to-haves, radar |
| **Learning Roadmap** | AI generates a week-by-week plan with checkable tasks |
| **AI Career Coach** | Context-aware chat using your resume + role profile |
| **Interview Prep** | AI generates technical/behavioral questions with hint & feedback |

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit openai plotly pandas pdfplumber python-docx
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Set your OpenAI API key

- Open the sidebar
- Expand **⚙ API Settings**
- Paste your OpenAI API key (`sk-...`)

---

## Usage Flow

1. **Resume Analyzer** — Upload your resume PDF/DOCX or paste text. Set your target role. Click *Analyze with AI*.
2. **Skill Gap** — Enter your current skills and target role. Click *Analyze Skill Gap*.
3. **Roadmap** — Set role + hours/week. Click *Generate AI Roadmap*. Check off tasks as you complete them.
4. **Career Coach** — Chat freely. Use quick-prompt buttons or type your own question.
5. **Interview Prep** — Generate questions, write answers, get instant AI feedback.
6. **Dashboard** — Review all scores and progress charts in one place.

---

## Environment Variables (optional)

Instead of entering the key in the sidebar, you can set:

```bash
export OPENAI_API_KEY=sk-your-key-here
```

Then add this line near the top of `app.py` (after imports):

```python
import os
if not st.session_state.api_key:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")
```

---

## Tech Stack

- **Streamlit** — UI framework
- **OpenAI GPT-4o-mini** — AI features (cost-efficient)
- **Plotly** — Interactive charts (radar, bar, line, pie)
- **pdfplumber** — PDF text extraction
- **python-docx** — DOCX text extraction

---

## Architecture Notes

- **Single file** (`app.py`) — all logic, UI, and AI in one place
- **Session state** — resume, analysis, roadmap, chat history all persisted during session
- **Structured JSON prompts** — every AI call returns typed JSON, parsed and rendered
- **Graceful fallbacks** — missing libraries degrade gracefully; app still runs without optional packages
- **Modular functions** — `page_*()` functions for each page, `call_openai()` for all AI, `make_*()` for charts
