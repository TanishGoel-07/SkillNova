"""
Nexus — AI Career Operating System v4
Single-file Streamlit app | Multi-provider AI (Groq · OpenAI · Gemini)
Run: streamlit run Nexus_v4.py
"""

import streamlit as st
import json
import re
import io
import hashlib
import time
from datetime import datetime

# ── Optional imports ──────────────────────────────────────────────────────────
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

GROQ_AVAILABLE = OPENAI_AVAILABLE

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    pdfplumber = None

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import pytesseract
    from pdf2image import convert_from_bytes
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus — AI Career OS",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #05050f 0%, #0a0a18 50%, #060610 100%);
    color: #eeeeff;
}

[data-testid="stSidebar"] {
    background: rgba(8,8,18,0.99) !important;
    border-right: 1px solid rgba(108,99,255,0.18) !important;
}
[data-testid="stSidebar"] .stMarkdown { color: #9090b0; }

.main .block-container { padding: 2rem 2.5rem !important; max-width: 1400px; }

h1,h2,h3 { font-family:'Syne',sans-serif !important; color:#eeeeff !important; }

[data-testid="stMetric"] {
    background: rgba(16,16,30,0.95) !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    backdrop-filter: blur(12px);
    transition: border-color 0.2s;
}
[data-testid="stMetric"]:hover { border-color: rgba(108,99,255,0.4) !important; }
[data-testid="stMetricLabel"] { color:#9090b0 !important; font-size:0.72rem !important; letter-spacing:0.1em; text-transform:uppercase; }
[data-testid="stMetricValue"] { color:#a78bfa !important; font-family:'Syne',sans-serif !important; font-size:1.9rem !important; }
[data-testid="stMetricDelta"]  { font-size:0.72rem !important; }

.glass-card {
    background: rgba(16,16,30,0.8);
    border: 1px solid rgba(108,99,255,0.13);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    margin-bottom: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.glass-card:hover { border-color: rgba(108,99,255,0.25); box-shadow: 0 4px 24px rgba(108,99,255,0.06); }

.glass-card-accent {
    background: rgba(108,99,255,0.06);
    border: 1px solid rgba(108,99,255,0.26);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
    margin-bottom: 1rem;
}

.hero-score {
    background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(56,189,248,0.07));
    border: 1px solid rgba(108,99,255,0.28);
    border-radius: 22px;
    padding: 2rem;
    text-align:center;
    margin-bottom:1rem;
}

.section-title {
    font-family:'Syne',sans-serif;
    font-size:0.68rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:#5050a0;
    margin-bottom:0.6rem;
}

.tag-green  { display:inline-block; background:rgba(52,211,153,0.12); color:#34d399; border:1px solid rgba(52,211,153,0.3); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }
.tag-red    { display:inline-block; background:rgba(248,113,113,0.12); color:#f87171; border:1px solid rgba(248,113,113,0.3); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }
.tag-amber  { display:inline-block; background:rgba(251,191,36,0.12); color:#fbbf24; border:1px solid rgba(251,191,36,0.3); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }
.tag-purple { display:inline-block; background:rgba(108,99,255,0.12); color:#a78bfa; border:1px solid rgba(108,99,255,0.25); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }
.tag-teal   { display:inline-block; background:rgba(56,189,248,0.12); color:#38bdf8; border:1px solid rgba(56,189,248,0.25); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }
.tag-pink   { display:inline-block; background:rgba(244,114,182,0.12); color:#f472b6; border:1px solid rgba(244,114,182,0.25); border-radius:20px; padding:3px 11px; font-size:0.71rem; margin:2px; }

.chat-user  { background:rgba(108,99,255,0.18); border:1px solid rgba(108,99,255,0.28); border-radius:14px 14px 2px 14px; padding:0.85rem 1.1rem; margin:0.5rem 0; font-size:0.87rem; max-width:82%; margin-left:auto; }
.chat-ai    { background:rgba(16,16,38,0.95); border:1px solid rgba(255,255,255,0.07); border-radius:14px 14px 14px 2px; padding:0.85rem 1.1rem; margin:0.5rem 0; font-size:0.87rem; max-width:82%; }
.chat-label { font-size:0.63rem; color:#5050a0; letter-spacing:0.09em; text-transform:uppercase; margin-bottom:0.25rem; }

.prog-track { height:7px; background:rgba(255,255,255,0.06); border-radius:4px; overflow:hidden; margin-top:0.3rem; }
.prog-fill-purple { height:100%; background:linear-gradient(90deg,#6c63ff,#a78bfa); border-radius:4px; transition:width 0.6s ease; }
.prog-fill-teal   { height:100%; background:linear-gradient(90deg,#0ea5e9,#38bdf8); border-radius:4px; transition:width 0.6s ease; }
.prog-fill-green  { height:100%; background:linear-gradient(90deg,#059669,#34d399); border-radius:4px; transition:width 0.6s ease; }
.prog-fill-amber  { height:100%; background:linear-gradient(90deg,#d97706,#fbbf24); border-radius:4px; transition:width 0.6s ease; }
.prog-fill-red    { height:100%; background:linear-gradient(90deg,#dc2626,#f87171); border-radius:4px; transition:width 0.6s ease; }
.prog-fill-pink   { height:100%; background:linear-gradient(90deg,#be185d,#f472b6); border-radius:4px; transition:width 0.6s ease; }

hr { border-color:rgba(108,99,255,0.1) !important; }

.stButton > button {
    background: rgba(108,99,255,0.12) !important;
    color: #a78bfa !important;
    border: 1px solid rgba(108,99,255,0.28) !important;
    border-radius: 10px !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:0.85rem !important;
    font-weight:500 !important;
    transition:all 0.18s !important;
}
.stButton > button:hover {
    background: rgba(108,99,255,0.26) !important;
    border-color:#a78bfa !important;
    transform:translateY(-1px);
    box-shadow: 0 4px 16px rgba(108,99,255,0.2) !important;
}

.btn-primary > button {
    background: linear-gradient(135deg, rgba(108,99,255,0.5), rgba(56,189,248,0.3)) !important;
    color: #fff !important;
    border-color: rgba(108,99,255,0.6) !important;
    font-weight:600 !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox>div>div, .stNumberInput input {
    background:rgba(16,16,38,0.9) !important;
    border:1px solid rgba(108,99,255,0.2) !important;
    border-radius:10px !important;
    color:#eeeeff !important;
    font-family:'DM Sans',sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color:#6c63ff !important;
    box-shadow:0 0 0 3px rgba(108,99,255,0.12) !important;
}

[data-testid="stFileUploader"] {
    background:rgba(16,16,38,0.5);
    border:2px dashed rgba(108,99,255,0.3) !important;
    border-radius:14px !important;
}

.streamlit-expanderHeader {
    background:rgba(16,16,38,0.7) !important;
    border-radius:10px !important;
    color:#a78bfa !important;
    font-family:'Syne',sans-serif !important;
}

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-thumb { background:rgba(108,99,255,0.3); border-radius:2px; }

.logo-text {
    font-family:'Syne',sans-serif;
    font-size:1.5rem;
    font-weight:800;
    background:linear-gradient(135deg,#a78bfa,#38bdf8,#f472b6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    letter-spacing:-0.02em;
}
.logo-sub { font-size:0.63rem; color:#5050a0; letter-spacing:0.16em; text-transform:uppercase; margin-top:-2px; }

.alert-info    { background:rgba(56,189,248,0.08);  border-left:3px solid #38bdf8; padding:0.8rem 1rem; border-radius:0 10px 10px 0; font-size:0.84rem; color:#bae6fd; margin:0.5rem 0; line-height:1.6; }
.alert-success { background:rgba(52,211,153,0.08);  border-left:3px solid #34d399; padding:0.8rem 1rem; border-radius:0 10px 10px 0; font-size:0.84rem; color:#a7f3d0; margin:0.5rem 0; line-height:1.6; }
.alert-warning { background:rgba(251,191,36,0.08);  border-left:3px solid #fbbf24; padding:0.8rem 1rem; border-radius:0 10px 10px 0; font-size:0.84rem; color:#fde68a; margin:0.5rem 0; line-height:1.6; }
.alert-error   { background:rgba(248,113,113,0.08); border-left:3px solid #f87171; padding:0.8rem 1rem; border-radius:0 10px 10px 0; font-size:0.84rem; color:#fecaca; margin:0.5rem 0; line-height:1.6; }

.score-big   { font-family:'Syne',sans-serif; font-size:3.2rem; font-weight:800; color:#a78bfa; line-height:1; }
.score-label { font-size:0.68rem; color:#5050a0; text-transform:uppercase; letter-spacing:0.12em; margin-top:0.3rem; }

.stTabs [data-baseweb="tab-list"] {
    background:rgba(10,10,22,0.95) !important;
    border-radius:12px;
    padding:4px;
    border:1px solid rgba(108,99,255,0.15);
}
.stTabs [data-baseweb="tab"] {
    color:#9090b0 !important;
    border-radius:8px !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:0.82rem !important;
}
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#6c63ff,#5a52e8) !important; color:#fff !important; }

.stCheckbox span { color:#9090b0 !important; font-size:0.85rem !important; }

.insight-card {
    background:rgba(16,16,30,0.85);
    border:1px solid rgba(108,99,255,0.14);
    border-radius:14px;
    padding:1.1rem 1.3rem;
    margin-bottom:0.6rem;
    transition: border-color 0.2s;
}
.insight-card:hover { border-color:rgba(108,99,255,0.3); }
.insight-icon { font-size:1.3rem; margin-bottom:0.4rem; }
.insight-label { font-size:0.65rem; color:#5050a0; letter-spacing:0.1em; text-transform:uppercase; }
.insight-value { font-size:0.88rem; color:#d0d0f0; line-height:1.5; margin-top:0.2rem; }

.sec-card {
    background:rgba(12,12,24,0.85);
    border:1px solid rgba(108,99,255,0.12);
    border-radius:14px;
    padding:1rem 1.2rem;
    margin-bottom:0.75rem;
}
.sec-score-badge {
    display:inline-block;
    padding:2px 10px;
    border-radius:20px;
    font-size:0.72rem;
    font-weight:600;
    font-family:'Syne',sans-serif;
}

.jd-match-bar {
    background: rgba(16,16,30,0.9);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
}

.pipeline-step {
    display:flex; align-items:center; gap:12px;
    padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04);
}
.pipeline-step-icon {
    width:28px; height:28px; border-radius:50%; display:flex;
    align-items:center; justify-content:center; font-size:0.75rem;
    flex-shrink:0; font-weight:700;
}
.step-done { background:rgba(52,211,153,0.2); color:#34d399; border:1px solid rgba(52,211,153,0.4); }
.step-active { background:rgba(108,99,255,0.2); color:#a78bfa; border:1px solid rgba(108,99,255,0.4); }
.step-pending { background:rgba(255,255,255,0.05); color:#5050a0; border:1px solid rgba(255,255,255,0.08); }

.linkedin-card {
    background: linear-gradient(135deg, rgba(10,102,194,0.12), rgba(10,102,194,0.06));
    border: 1px solid rgba(10,102,194,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.project-card {
    background: rgba(16,16,30,0.8);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.project-card:hover { border-color: rgba(56,189,248,0.4); }

.salary-card {
    background: linear-gradient(135deg, rgba(52,211,153,0.1), rgba(16,185,129,0.05));
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    text-align:center;
}

.debug-panel {
    background:rgba(5,5,12,0.9);
    border:1px solid rgba(108,99,255,0.15);
    border-radius:10px;
    padding:0.75rem 1rem;
    font-family:monospace;
    font-size:0.72rem;
    color:#5050a0;
    margin-top:0.5rem;
}

.extraction-step {
    display:flex; align-items:center; gap:8px;
    padding:4px 0; font-size:0.78rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "api_key": "",
        "groq_api_key": "",
        "gemini_api_key": "",
        "resume_text": "",
        "resume_hash": "",
        "resume_analysis": None,
        "structured_resume": None,
        "skill_gap": None,
        "roadmap": None,
        "roadmap_checks": {},
        "chat_history": [],
        "interview_questions": None,
        "target_role": "Senior Frontend Developer",
        "current_skills": "",
        "extraction_meta": None,
        "jd_analysis": None,
        "jd_text": "",
        "linkedin_profile": None,
        "projects_generated": None,
        "salary_data": None,
        "dashboard_scores": {
            "resume_score": 0, "ats_score": 0,
            "role_match": 0, "career_readiness": 0,
            "gap_pct": 0, "roadmap_pct": 0
        },
        "progress_history": [],
        "active_provider": "",
        "debug_log": [],
        "pipeline_stages": {},
        "ai_provider_pref": "auto",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ══════════════════════════════════════════════════════════════════════════════
# AI ENGINE — Multi-provider with fallback & debug
# ══════════════════════════════════════════════════════════════════════════════
def call_ai(system_prompt: str, user_prompt: str, max_tokens: int = 2500) -> str:
    errors = []
    pref = st.session_state.get("ai_provider_pref", "auto")
    t0 = time.time()

    def _log(provider, tokens_est, latency, ok, err=""):
        entry = {
            "ts": datetime.now().strftime("%H:%M:%S"),
            "provider": provider,
            "tokens_est": tokens_est,
            "latency_ms": int(latency * 1000),
            "ok": ok,
            "error": err,
        }
        st.session_state.debug_log = ([entry] + st.session_state.debug_log)[:20]

    def try_groq():
        groq_key = st.session_state.get("groq_api_key", "")
        if not groq_key or not GROQ_AVAILABLE:
            return None
        try:
            client = openai.OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_prompt}],
                max_tokens=min(max_tokens, 8000), temperature=0.35,
            )
            lat = time.time() - t0
            tokens = resp.usage.total_tokens if resp.usage else (len(user_prompt.split()) + len(system_prompt.split()))
            _log("Groq · llama-3.3-70b", tokens, lat, True)
            st.session_state.active_provider = "Groq · llama-3.3-70b"
            return resp.choices[0].message.content.strip()
        except Exception as e:
            errors.append(f"Groq: {e}")
            _log("Groq", 0, time.time() - t0, False, str(e))
            return None

    def try_openai():
        openai_key = st.session_state.get("api_key", "")
        if not openai_key or not OPENAI_AVAILABLE:
            return None
        try:
            client = openai.OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_prompt}],
                max_tokens=max_tokens, temperature=0.35,
            )
            lat = time.time() - t0
            tokens = resp.usage.total_tokens if resp.usage else 0
            _log("OpenAI · gpt-4o-mini", tokens, lat, True)
            st.session_state.active_provider = "OpenAI · gpt-4o-mini"
            return resp.choices[0].message.content.strip()
        except Exception as e:
            errors.append(f"OpenAI: {e}")
            _log("OpenAI", 0, time.time() - t0, False, str(e))
            return None

    def try_gemini():
        gemini_key = st.session_state.get("gemini_api_key", "")
        if not gemini_key or not GEMINI_AVAILABLE:
            return None
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                                          system_instruction=system_prompt)
            resp = model.generate_content(user_prompt)
            lat = time.time() - t0
            _log("Gemini · 2.0-flash", 0, lat, True)
            st.session_state.active_provider = "Gemini · 2.0-flash"
            return resp.text.strip()
        except Exception as e:
            errors.append(f"Gemini: {e}")
            _log("Gemini", 0, time.time() - t0, False, str(e))
            return None

    order = {
        "auto":   [try_groq, try_openai, try_gemini],
        "groq":   [try_groq, try_openai, try_gemini],
        "openai": [try_openai, try_groq, try_gemini],
        "gemini": [try_gemini, try_groq, try_openai],
    }.get(pref, [try_groq, try_openai, try_gemini])

    for fn in order:
        result = fn()
        if result:
            return result

    if not any([st.session_state.get("groq_api_key"),
                st.session_state.get("api_key"),
                st.session_state.get("gemini_api_key")]):
        raise ValueError("No API key configured. Add a Groq (free!), OpenAI, or Gemini key in the sidebar.")
    raise RuntimeError("All AI providers failed. Errors: " + " | ".join(errors))


def parse_json(raw: str):
    """Robust JSON parser with multiple fallback strategies."""
    # Remove markdown fences
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    # Try direct parse
    for pat in [r'\{[\s\S]*\}', r'\[[\s\S]*\]']:
        m = re.search(pat, clean)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    # Try after stripping common prefix garbage
    try:
        return json.loads(clean)
    except Exception:
        pass
    # Last resort: find first { or [ and parse from there
    for i, ch in enumerate(clean):
        if ch in '{[':
            try:
                return json.loads(clean[i:])
            except Exception:
                pass
    raise ValueError(f"Could not parse JSON from AI response. Raw: {raw[:300]}")


# ══════════════════════════════════════════════════════════════════════════════
# CHUNKED AI PIPELINE — Handles large resumes without truncation
# ══════════════════════════════════════════════════════════════════════════════
def chunk_text(text: str, chunk_size: int = 2500, overlap: int = 200) -> list:
    """Split text into overlapping chunks to preserve context."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Try to break at paragraph boundary
        if end < len(text):
            para_break = text.rfind('\n\n', start, end)
            line_break = text.rfind('\n', start, end)
            if para_break > start + chunk_size // 2:
                end = para_break
            elif line_break > start + chunk_size // 2:
                end = line_break
        chunks.append(text[start:end])
        start = end - overlap if end < len(text) else end
    return chunks


def analyze_resume_chunked(resume_text: str, target_role: str) -> dict:
    """
    Multi-stage pipeline with chunking for full resume coverage.
    Stage 1: Extract structured data per chunk
    Stage 2: Merge and deduplicate
    Stage 3: Deep analysis on merged data
    Stage 4: Generate actionable insights
    """
    chunks = chunk_text(resume_text, chunk_size=2800)
    num_chunks = len(chunks)

    # ── Stage 1: Extract structured data from each chunk ──
    stage1_results = []
    for i, chunk in enumerate(chunks):
        sys_p = """Extract structured resume data from this text chunk. Return ONLY valid JSON:
{
  "name": "candidate name or empty string",
  "contact": {"email":"","phone":"","linkedin":"","location":""},
  "summary_text": "summary/objective paragraph found",
  "skills_found": ["skill1","skill2"],
  "experience_entries": [{"title":"","company":"","duration":"","bullets":["",""],"metrics":["quantified achievement"]}],
  "education_entries": [{"degree":"","institution":"","year":""}],
  "projects_found": [{"name":"","tech":"","description":""}],
  "certifications": ["cert1"],
  "keywords": ["keyword1","keyword2","keyword3"]
}"""
        try:
            raw = call_ai(sys_p, f"Resume chunk {i+1}/{num_chunks}:\n{chunk}", max_tokens=1200)
            stage1_results.append(parse_json(raw))
        except Exception:
            stage1_results.append({})

    # ── Stage 2: Merge all extracted data ──
    merged = {
        "name": "",
        "contact": {},
        "summary_text": "",
        "skills_found": [],
        "experience_entries": [],
        "education_entries": [],
        "projects_found": [],
        "certifications": [],
        "keywords": [],
    }
    for r in stage1_results:
        if r.get("name") and not merged["name"]:
            merged["name"] = r["name"]
        if r.get("contact") and not merged["contact"].get("email"):
            merged["contact"] = r["contact"]
        if r.get("summary_text") and not merged["summary_text"]:
            merged["summary_text"] = r["summary_text"]
        for sk in r.get("skills_found", []):
            if sk and sk not in merged["skills_found"]:
                merged["skills_found"].append(sk)
        merged["experience_entries"].extend(r.get("experience_entries", []))
        merged["education_entries"].extend(r.get("education_entries", []))
        merged["projects_found"].extend(r.get("projects_found", []))
        for c in r.get("certifications", []):
            if c and c not in merged["certifications"]:
                merged["certifications"].append(c)
        for kw in r.get("keywords", []):
            if kw and kw not in merged["keywords"]:
                merged["keywords"].append(kw)

    # ── Stage 3 & 4: Deep analysis using merged structured data ──
    resume_summary = f"""
Candidate: {merged.get('name','Unknown')}
Skills ({len(merged['skills_found'])}): {', '.join(merged['skills_found'][:40])}
Experience entries: {len(merged['experience_entries'])} roles
Projects: {len(merged['projects_found'])}
Certifications: {', '.join(merged['certifications'][:10])}
Keywords: {', '.join(merged['keywords'][:30])}
Experience bullets sample: {'; '.join([b for e in merged['experience_entries'][:3] for b in e.get('bullets',[])[:2]][:10])}
""".strip()

    sys_p_deep = f"""You are a world-class resume expert, ATS specialist, and senior career coach.
Perform an EXTREMELY thorough resume analysis. Return ONLY valid JSON with ALL fields fully populated.
Be specific, detailed, and actionable. Do not use placeholder text.

Return exactly this structure:
{{
  "candidate_name": "extracted name",
  "executive_summary": "3 sentence professional assessment specific to this candidate",
  "resume_score": 0,
  "ats_score": 0,
  "role_match_score": 0,
  "career_readiness_score": 0,
  "clarity_score": 0,
  "impact_score": 0,
  "keyword_coverage_score": 0,
  "formatting_score": 0,
  "content_depth_score": 0,
  "strengths": ["specific strength 1","specific strength 2","specific strength 3","specific strength 4","specific strength 5"],
  "weaknesses": ["specific weakness 1","specific weakness 2","specific weakness 3","specific weakness 4"],
  "missing_keywords": ["keyword1","keyword2","keyword3","keyword4","keyword5","keyword6","keyword7","keyword8"],
  "missing_skills": ["skill1","skill2","skill3","skill4","skill5","skill6"],
  "quick_wins": ["actionable quick win 1","actionable quick win 2","actionable quick win 3"],
  "weak_sections": ["section1","section2"],
  "strong_sections": ["section1","section2"],
  "experience_gap": "specific assessment of experience gaps",
  "quantification_score": 0,
  "section_feedback": {{
    "summary": {{"score":0,"issues":[""],"strengths":[""],"improvements":["",""],"rewrite":"rewritten version"}},
    "skills": {{"score":0,"issues":[""],"strengths":[""],"improvements":["",""],"rewrite":"rewritten version"}},
    "experience": {{"score":0,"issues":["",""],"strengths":[""],"improvements":["",""],"rewrite":"improved bullet example"}},
    "projects": {{"score":0,"issues":[""],"strengths":[""],"improvements":["",""],"rewrite":"improved project description"}},
    "education": {{"score":0,"issues":[],"strengths":[""],"improvements":[""],"rewrite":""}},
    "certifications": {{"score":0,"issues":[""],"strengths":[],"improvements":[""],"rewrite":""}},
    "formatting": {{"score":0,"issues":[""],"strengths":[""],"improvements":[""],"rewrite":""}}
  }},
  "role_fit": {{
    "selected_role": "{target_role}",
    "match_reasoning": "detailed 3 sentence explanation",
    "match_percentage": 0,
    "alternate_roles": ["role1","role2","role3","role4"],
    "priority_gaps": ["gap1","gap2","gap3","gap4","gap5"]
  }},
  "skill_clusters": {{
    "core": ["core skill 1","core skill 2","core skill 3"],
    "advanced": ["advanced skill 1","advanced skill 2"],
    "missing_critical": ["missing critical skill 1","missing critical skill 2","missing critical skill 3"],
    "adjacent": ["adjacent skill 1","adjacent skill 2"]
  }},
  "career_insights": {{
    "biggest_strength": "specific strength sentence",
    "biggest_risk": "specific risk sentence",
    "quickest_win": "specific actionable sentence",
    "job_ready": false,
    "next_best_action": "specific next step",
    "one_line_diagnosis": "one-line career diagnosis",
    "highest_roi_skill": "most valuable skill to learn and why",
    "fix_this_week": "specific action for this week",
    "career_trajectory": "where this candidate is headed",
    "market_positioning": "their market position and competitive advantage",
    "salary_range": "realistic salary range for target role based on skills",
    "competition_level": "Low|Medium|High|Very High",
    "recommendations": ["rec 1","rec 2","rec 3","rec 4","rec 5"]
  }},
  "rewrite_suggestions": [
    {{"original":"weak bullet from resume","improved":"improved version with metrics and action verbs","why":"explanation","impact":"High|Medium|Low"}},
    {{"original":"weak bullet from resume","improved":"improved version with metrics and action verbs","why":"explanation","impact":"High|Medium|Low"}},
    {{"original":"weak bullet from resume","improved":"improved version with metrics and action verbs","why":"explanation","impact":"High|Medium|Low"}},
    {{"original":"weak bullet from resume","improved":"improved version with metrics and action verbs","why":"explanation","impact":"High|Medium|Low"}}
  ],
  "roadmap": {{
    "7_day_plan": ["Day 1: specific task","Day 2: specific task","Day 3: specific task","Day 4: specific task","Day 5: specific task","Day 6: specific task","Day 7: specific task"],
    "30_day_plan": ["Week 1: specific goal","Week 2: specific goal","Week 3: specific goal","Week 4: specific goal"],
    "recommended_projects": ["Project idea 1 with tech stack","Project idea 2","Project idea 3"],
    "recommended_resources": ["Resource 1","Resource 2","Resource 3","Resource 4"]
  }},
  "interview_prep": {{
    "technical_questions": ["question1","question2","question3"],
    "behavioral_questions": ["question1","question2","question3"],
    "answer_tips": ["tip1","tip2","tip3"]
  }},
  "ats_analysis": {{
    "ats_friendly": false,
    "formatting_issues": ["issue1","issue2"],
    "keyword_density": "low|medium|high",
    "recommended_keywords": ["kw1","kw2","kw3","kw4","kw5"]
  }},
  "confidence": 0.85
}}"""

    usr_p = f"""Target Role: {target_role}

Structured Resume Data:
{resume_summary}

Full Resume Text (first 3000 chars):
{resume_text[:3000]}"""

    raw = call_ai(sys_p_deep, usr_p, max_tokens=4000)
    result = parse_json(raw)

    # Attach structured resume model
    result["structured_resume"] = merged
    result["chunks_processed"] = num_chunks
    return result


# ══════════════════════════════════════════════════════════════════════════════
# PDF & FILE EXTRACTION — Robust pipeline with OCR fallback
# ══════════════════════════════════════════════════════════════════════════════
def clean_text(text: str) -> str:
    """Advanced text cleaning for resume extraction."""
    # Fix broken hyphenated words
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    # Normalize multiple newlines (preserve double newlines for paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Fix multiple spaces/tabs
    text = re.sub(r'[ \t]{2,}', ' ', text)
    # Remove bullet point characters that break parsing
    text = re.sub(r'^[•·▪▸◦‣⁃]\s*', '- ', text, flags=re.MULTILINE)
    # Fix common OCR artifacts
    text = re.sub(r'[|]{2,}', ' ', text)
    text = re.sub(r'_{3,}', '', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text.strip()


def detect_text_quality(text: str) -> dict:
    """Assess extraction quality and return confidence score."""
    if not text:
        return {"score": 0, "words": 0, "assessment": "empty"}
    words = len(text.split())
    has_common_sections = sum(1 for s in ["experience", "education", "skills", "project", "work"]
                              if s in text.lower())
    has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', text))
    has_phone = bool(re.search(r'[\+\d][\d\s\-\(\)]{8,}', text))

    score = min(100, (
        min(words / 5, 40) +          # up to 40pts for word count
        has_common_sections * 10 +     # up to 50pts for sections
        has_email * 5 +
        has_phone * 5
    ))
    return {
        "score": int(score),
        "words": words,
        "assessment": "good" if score >= 70 else ("moderate" if score >= 40 else "poor"),
        "sections_found": has_common_sections,
    }


def extract_pdf(file_bytes: bytes) -> tuple:
    """
    Robust PDF extraction pipeline:
    1. pdfplumber (handles most PDFs + tables)
    2. PyPDF2 fallback
    3. OCR fallback (pytesseract + pdf2image)
    """
    results = []

    # Method 1: pdfplumber
    if PDFPLUMBER_AVAILABLE:
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages_text = []
                for page in pdf.pages:
                    pt = page.extract_text()
                    if pt:
                        pages_text.append(pt)
                    # Also try extracting tables
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            row_text = ' | '.join(str(c) for c in row if c)
                            if row_text.strip():
                                pages_text.append(row_text)
                text = "\n".join(pages_text)
                q = detect_text_quality(text)
                if q["score"] >= 40:
                    return clean_text(text), "pdfplumber", q
                results.append(("pdfplumber", text, q))
        except Exception as e:
            results.append(("pdfplumber", "", {"score": 0, "words": 0, "assessment": "failed"}))

    # Method 2: PyPDF2
    if PYPDF2_AVAILABLE:
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            pages_text = []
            for page in reader.pages:
                pt = page.extract_text()
                if pt:
                    pages_text.append(pt)
            text = "\n".join(pages_text)
            q = detect_text_quality(text)
            if q["score"] >= 40:
                return clean_text(text), "PyPDF2", q
            results.append(("PyPDF2", text, q))
        except Exception:
            results.append(("PyPDF2", "", {"score": 0, "words": 0, "assessment": "failed"}))

    # Method 3: OCR with pytesseract
    if OCR_AVAILABLE:
        try:
            images = convert_from_bytes(file_bytes, dpi=200)
            pages_text = []
            for img in images:
                text_ocr = pytesseract.image_to_string(img, lang='eng')
                pages_text.append(text_ocr)
            text = "\n".join(pages_text)
            q = detect_text_quality(text)
            if q["words"] >= 50:
                return clean_text(text), "OCR (pytesseract)", q
            results.append(("OCR", text, q))
        except Exception:
            results.append(("OCR", "", {"score": 0, "words": 0, "assessment": "failed"}))

    # Return best result even if below threshold
    if results:
        best = max(results, key=lambda x: x[2].get("score", 0))
        if best[1]:
            return clean_text(best[1]), best[0] + " (low quality)", best[2]

    return "", "failed", {"score": 0, "words": 0, "assessment": "failed"}


def parse_uploaded_file(uploaded) -> tuple:
    """Parse uploaded file with comprehensive extraction pipeline."""
    raw = uploaded.read()
    name = uploaded.name.lower()
    meta = {
        "filename": uploaded.name,
        "size_kb": round(len(raw) / 1024, 1),
        "method": "direct",
        "quality": {},
    }

    if name.endswith(".pdf"):
        text, method, quality = extract_pdf(raw)
        meta["method"] = method
        meta["file_type"] = "PDF"
        meta["quality"] = quality
        if not text or quality.get("score", 0) < 20:
            meta["warning"] = "⚠ PDF extraction quality is low. Try uploading as DOCX or TXT for better results."
    elif name.endswith(".docx"):
        if DOCX_AVAILABLE:
            doc = DocxDocument(io.BytesIO(raw))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            # Also extract table content
            for table in doc.tables:
                for row in table.rows:
                    row_text = ' | '.join(c.text for c in row.cells if c.text.strip())
                    if row_text:
                        paragraphs.append(row_text)
            text = "\n".join(paragraphs)
            meta["file_type"] = "DOCX"
            meta["quality"] = detect_text_quality(text)
        else:
            text = ""
            meta["file_type"] = "DOCX"
            meta["warning"] = "python-docx not installed. Cannot read DOCX."
    else:  # TXT
        text = raw.decode("utf-8", errors="ignore")
        meta["file_type"] = "TXT"
        meta["quality"] = detect_text_quality(text)

    if text:
        text = clean_text(text)

    meta["word_count"] = len(text.split()) if text else 0
    meta["char_count"] = len(text)
    meta["quality_score"] = meta["quality"].get("score", 0)
    lower = text.lower()
    meta["detected_sections"] = [s.title() for s in
        ["experience", "education", "skills", "projects", "summary",
         "objective", "certifications", "achievements", "publications", "awards"]
        if s in lower]
    return text, meta


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
PLOT_BG = "rgba(0,0,0,0)"
GRID_COL = "rgba(255,255,255,0.05)"
TEXT_COL = "#9090b0"
FONT_FAM = "DM Sans, sans-serif"


def base_layout(title="", height=300):
    return dict(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COL, family=FONT_FAM, size=11),
        margin=dict(l=20, r=20, t=40 if title else 10, b=20),
        title=title, title_font=dict(family="Syne,sans-serif", size=13, color="#eeeeff"),
        height=height
    )


def make_radar(cats, vals, target=None, title=""):
    c = cats + [cats[0]]; v = vals + [vals[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v, theta=c, fill="toself", name="Current",
        fillcolor="rgba(108,99,255,0.15)",
        line=dict(color="#6c63ff", width=2.5)
    ))
    if target:
        t = target + [target[0]]
        fig.add_trace(go.Scatterpolar(
            r=t, theta=c, fill="toself", name="Target",
            fillcolor="rgba(56,189,248,0.06)",
            line=dict(color="#38bdf8", width=1.5, dash="dot")
        ))
    fig.update_layout(
        **base_layout(title, height=300),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_COL,
                            tickfont=dict(size=9, color=TEXT_COL)),
            angularaxis=dict(gridcolor=GRID_COL, tickfont=dict(size=10, color=TEXT_COL))
        ),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COL, size=10))
    )
    return fig


def make_bar(labels, values, colors=None, title="", height=260):
    dc = ["#f87171", "#fbbf24", "#a78bfa", "#38bdf8", "#34d399", "#f472b6"]
    bc = colors or [dc[i % len(dc)] for i in range(len(labels))]
    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker=dict(color=bc, cornerradius=5,
                    line=dict(color="rgba(255,255,255,0.05)", width=1)),
        text=[str(v) for v in values],
        textposition="outside",
        textfont=dict(color=TEXT_COL, size=10)
    ))
    fig.update_layout(
        **base_layout(title, height),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL)),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL), range=[0, 115])
    )
    return fig


def make_hbar(labels, values, colors=None, title="", height=260):
    dc = ["#6c63ff", "#38bdf8", "#34d399", "#fbbf24", "#f87171", "#f472b6"]
    bc = colors or [dc[i % len(dc)] for i in range(len(labels))]
    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation='h',
        marker=dict(color=bc, cornerradius=5),
        text=[str(v) for v in values],
        textposition="auto",
        textfont=dict(color="#eeeeff", size=10)
    ))
    fig.update_layout(
        **base_layout(title, height),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL), range=[0, 115]),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL))
    )
    return fig


def make_line(x, y, title="Score Over Time", height=240):
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color="#6c63ff", width=2.5),
        marker=dict(color="#a78bfa", size=8, line=dict(color="#6c63ff", width=2)),
        fill="tozeroy", fillcolor="rgba(108,99,255,0.07)"
    ))
    fig.update_layout(
        **base_layout(title, height),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL)),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TEXT_COL), range=[0, 105])
    )
    return fig


def make_pie(labels, values, title="", height=280):
    colors = ["#6c63ff", "#38bdf8", "#34d399", "#fbbf24", "#f87171", "#f472b6", "#a78bfa"]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors[:len(labels)],
                    line=dict(color="rgba(0,0,0,0.3)", width=2)),
        hole=0.5,
        textfont=dict(color="#eeeeff", size=10)
    ))
    fig.update_layout(
        **base_layout(title, height),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COL, size=10))
    )
    return fig


def make_gauge(value, title, color="#a78bfa", height=200):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(color=TEXT_COL, size=12)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=TEXT_COL),
            bar=dict(color=color, thickness=0.25),
            bgcolor="rgba(255,255,255,0.03)",
            bordercolor=GRID_COL,
            steps=[
                dict(range=[0, 40], color="rgba(248,113,113,0.1)"),
                dict(range=[40, 70], color="rgba(251,191,36,0.1)"),
                dict(range=[70, 100], color="rgba(52,211,153,0.1)"),
            ],
        ),
        number=dict(font=dict(color=color, size=24, family="Syne,sans-serif")),
    ))
    fig.update_layout(paper_bgcolor=PLOT_BG, height=height, margin=dict(l=20, r=20, t=40, b=10))
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def tag_html(items, cls):
    return " ".join(f'<span class="tag-{cls}">{i}</span>' for i in items)


def progress_bar(pct, color="purple"):
    return f'<div class="prog-track"><div class="prog-fill-{color}" style="width:{min(int(pct), 100)}%"></div></div>'


def alert(msg, kind="info"):
    st.markdown(f'<div class="alert-{kind}">{msg}</div>', unsafe_allow_html=True)


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def score_color(s):
    if s >= 80: return "#34d399"
    if s >= 60: return "#fbbf24"
    return "#f87171"


def score_badge(s):
    c = score_color(s)
    return f'<span class="sec-score-badge" style="background:rgba(0,0,0,0.3);color:{c};border:1px solid {c}">{s}/100</span>'


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="logo-text">◈ Nexus</div><div class="logo-sub">AI Career Operating System v4</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("⚙ AI Provider Settings",
                     expanded=not bool(st.session_state.groq_api_key or
                                       st.session_state.api_key or
                                       st.session_state.gemini_api_key)):
        st.markdown('<div style="font-size:0.72rem;color:#5050a0;margin-bottom:0.75rem">Add at least ONE key. <b style="color:#34d399">Groq is free!</b></div>', unsafe_allow_html=True)
        g = st.text_input("🟢 Groq API Key (Free)", value=st.session_state.groq_api_key,
                          type="password", placeholder="gsk_...", help="Free at console.groq.com")
        if g != st.session_state.groq_api_key: st.session_state.groq_api_key = g

        o = st.text_input("OpenAI API Key", value=st.session_state.api_key,
                          type="password", placeholder="sk-...")
        if o != st.session_state.api_key: st.session_state.api_key = o

        gm = st.text_input("Gemini API Key", value=st.session_state.gemini_api_key,
                           type="password", placeholder="AIza...")
        if gm != st.session_state.gemini_api_key: st.session_state.gemini_api_key = gm

        pref = st.selectbox("Provider Priority", ["auto", "groq", "openai", "gemini"],
                            index=["auto", "groq", "openai", "gemini"].index(
                                st.session_state.ai_provider_pref))
        if pref != st.session_state.ai_provider_pref:
            st.session_state.ai_provider_pref = pref

        any_key = bool(st.session_state.groq_api_key or st.session_state.api_key or
                       st.session_state.gemini_api_key)
        if any_key:
            active = []
            if st.session_state.groq_api_key: active.append("Groq ✓")
            if st.session_state.api_key: active.append("OpenAI ✓")
            if st.session_state.gemini_api_key: active.append("Gemini ✓")
            st.markdown(f'<div class="alert-success" style="font-size:0.78rem">Active: {" · ".join(active)}</div>', unsafe_allow_html=True)
            if st.session_state.active_provider:
                st.markdown(f'<div style="font-size:0.68rem;color:#5050a0;margin-top:4px">Last used: {st.session_state.active_provider}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-warning" style="font-size:0.78rem">⚠ Enter at least one key</div>', unsafe_allow_html=True)

    st.markdown("---")

    nav_options = [
        "◈  Dashboard",
        "◉  Resume Analyzer",
        "◐  Skill Gap Analysis",
        "◳  Learning Roadmap",
        "◫  AI Career Coach",
        "◬  Interview Prep",
        "◆  Career Insights",
        "◍  JD Matcher",
        "◑  LinkedIn Optimizer",
        "◒  Project Generator",
        "◓  Salary Intelligence",
        "⊞  Export & Reports",
        "⊟  Debug Panel",
    ]
    page = st.radio("Navigation", nav_options, label_visibility="collapsed")

    st.markdown("---")
    sc = st.session_state.dashboard_scores
    if sc["resume_score"] > 0:
        st.markdown(f"""
        <div class="glass-card" style="padding:1rem">
        <div class="section-title">Live Scores</div>
        <div style="font-size:0.78rem;color:#9090b0;margin-bottom:4px">Resume</div>
        {progress_bar(sc['resume_score'],'purple')}
        <div style="font-size:0.72rem;color:#a78bfa;text-align:right">{sc['resume_score']}/100</div>
        <div style="font-size:0.78rem;color:#9090b0;margin-top:4px;margin-bottom:4px">ATS</div>
        {progress_bar(sc['ats_score'],'teal')}
        <div style="font-size:0.72rem;color:#38bdf8;text-align:right">{sc['ats_score']}/100</div>
        <div style="font-size:0.78rem;color:#9090b0;margin-top:4px;margin-bottom:4px">Role Match</div>
        {progress_bar(sc.get('role_match',0),'green')}
        <div style="font-size:0.72rem;color:#34d399;text-align:right">{sc.get('role_match',0)}%</div>
        <div style="font-size:0.78rem;color:#9090b0;margin-top:4px;margin-bottom:4px">Career Readiness</div>
        {progress_bar(sc.get('career_readiness',0),'amber')}
        <div style="font-size:0.72rem;color:#fbbf24;text-align:right">{sc.get('career_readiness',0)}/100</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='font-size:0.7rem;color:#404060;line-height:1.9'>
        <strong style='color:#5050a0'>Quick start</strong><br>
        1. Set API key(s) above<br>
        2. Go to Resume Analyzer<br>
        3. Upload your resume<br>
        4. Click Analyze Resume<br>
        5. Explore 12+ modules
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    st.markdown("## ◈ Career Intelligence Dashboard")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Your complete career health at a glance — powered by multi-stage AI analysis</div>', unsafe_allow_html=True)

    sc = st.session_state.dashboard_scores
    an = st.session_state.resume_analysis

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Resume Score",     f"{sc['resume_score']}/100",
              delta=f"+{sc['resume_score']-50} vs avg" if sc['resume_score'] > 0 else None)
    c2.metric("ATS Score",        f"{sc['ats_score']}/100",
              delta="✓ Good" if sc['ats_score'] >= 70 else ("Needs work" if sc['ats_score'] > 0 else None))
    c3.metric("Role Match",       f"{sc.get('role_match',0)}%",
              delta="Strong" if sc.get('role_match', 0) >= 70 else None)
    c4.metric("Career Ready",     f"{sc.get('career_readiness',0)}/100", delta=None)
    c5.metric("Roadmap Done",     f"{sc['roadmap_pct']}%",
              delta="In progress" if sc['roadmap_pct'] > 0 else None)
    c6.metric("Analyses Run",     str(len(st.session_state.progress_history)), delta=None)

    st.markdown("<br>", unsafe_allow_html=True)

    if an and an.get("executive_summary"):
        cname = an.get("candidate_name", "")
        chunks = an.get("chunks_processed", 1)
        st.markdown(f"""
        <div class="glass-card-accent">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem">
          <div class="section-title">◈ Executive Summary{f" — {cname}" if cname else ""}</div>
          <div style="font-size:0.68rem;color:#5050a0">{chunks} chunk{"s" if chunks > 1 else ""} analyzed · {st.session_state.active_provider}</div>
        </div>
        <div style="font-size:0.9rem;color:#d0d0f0;line-height:1.7">{an.get('executive_summary','')}</div>
        </div>
        """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Resume Section Radar")
        if PLOTLY_AVAILABLE:
            if an and an.get("section_feedback"):
                sf = an["section_feedback"]
                cats = ["Summary", "Skills", "Experience", "Projects", "Education", "Formatting"]
                vals = [sf.get(k.lower(), {}).get("score", 50) for k in cats]
                st.plotly_chart(make_radar(cats, vals, [90] * 6),
                                use_container_width=True, config={"displayModeBar": False})
            else:
                st.plotly_chart(make_radar(
                    ["Summary", "Skills", "Experience", "Projects", "Education", "Formatting"],
                    [65, 70, 60, 55, 80, 72], [90] * 6),
                    use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Score Progress Over Time")
        if PLOTLY_AVAILABLE:
            hist = st.session_state.progress_history
            if len(hist) >= 2:
                st.plotly_chart(make_line([h["date"] for h in hist], [h["score"] for h in hist]),
                                use_container_width=True, config={"displayModeBar": False})
            else:
                st.plotly_chart(make_line(
                    ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5"], [52, 58, 64, 70, 75]),
                    use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Score Breakdown")
        if PLOTLY_AVAILABLE and an:
            labels = ["Resume", "ATS", "Role Match", "Career Ready", "Clarity", "Impact", "Content"]
            values = [an.get("resume_score", 0), an.get("ats_score", 0),
                      an.get("role_match_score", 0), an.get("career_readiness_score", 0),
                      an.get("clarity_score", 0), an.get("impact_score", 0),
                      an.get("content_depth_score", 0)]
            st.plotly_chart(make_hbar(labels, values, [score_color(v) for v in values], height=260),
                            use_container_width=True, config={"displayModeBar": False})
        elif PLOTLY_AVAILABLE:
            st.plotly_chart(make_pie(
                ["Frontend", "Backend", "DevOps", "Testing", "Soft Skills"],
                [72, 45, 30, 35, 68]), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Top Skill Gaps")
        if PLOTLY_AVAILABLE and an and an.get("missing_skills"):
            ms = an["missing_skills"][:8]
            vals = [max(30, 90 - i * 7) for i in range(len(ms))]
            st.plotly_chart(make_bar(ms, vals, ["#f87171"] * len(ms), height=260),
                            use_container_width=True, config={"displayModeBar": False})
        elif PLOTLY_AVAILABLE:
            st.plotly_chart(make_bar(
                ["TypeScript", "Testing", "Sys Design", "GraphQL", "Docker"],
                [85, 70, 75, 55, 50],
                ["#f87171", "#f87171", "#fbbf24", "#fbbf24", "#a78bfa"], height=260),
                use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    if an and an.get("career_insights"):
        ci = an["career_insights"]
        st.markdown("<br>", unsafe_allow_html=True)
        section_title("◆ Live Career Insights")
        ia, ib, ic_, id_ = st.columns(4)
        with ia:
            st.markdown(f'<div class="insight-card"><div class="insight-icon">💪</div><div class="insight-label">Biggest Strength</div><div class="insight-value">{ci.get("biggest_strength","—")}</div></div>', unsafe_allow_html=True)
        with ib:
            st.markdown(f'<div class="insight-card"><div class="insight-icon">⚠️</div><div class="insight-label">Biggest Risk</div><div class="insight-value">{ci.get("biggest_risk","—")}</div></div>', unsafe_allow_html=True)
        with ic_:
            st.markdown(f'<div class="insight-card"><div class="insight-icon">⚡</div><div class="insight-label">Quickest Win</div><div class="insight-value">{ci.get("quickest_win","—")}</div></div>', unsafe_allow_html=True)
        with id_:
            ready = ci.get("job_ready", False)
            rc = "#34d399" if ready else "#f87171"
            rl = "Job Ready ✓" if ready else "Not Yet Ready"
            st.markdown(f'<div class="insight-card"><div class="insight-icon">🎯</div><div class="insight-label">Job Readiness</div><div class="insight-value" style="color:{rc};font-weight:600">{rl}</div></div>', unsafe_allow_html=True)

        # Skill clusters quick view
        if an.get("skill_clusters"):
            st.markdown("<br>", unsafe_allow_html=True)
            sk = an["skill_clusters"]
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                st.markdown('<div class="glass-card" style="padding:1rem">', unsafe_allow_html=True)
                section_title("Core Skills")
                st.markdown(tag_html(sk.get("core", []), "green"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with s2:
                st.markdown('<div class="glass-card" style="padding:1rem">', unsafe_allow_html=True)
                section_title("Advanced Skills")
                st.markdown(tag_html(sk.get("advanced", []), "purple"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with s3:
                st.markdown('<div class="glass-card" style="padding:1rem">', unsafe_allow_html=True)
                section_title("Critical Gaps")
                st.markdown(tag_html(sk.get("missing_critical", []), "red"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with s4:
                st.markdown('<div class="glass-card" style="padding:1rem">', unsafe_allow_html=True)
                section_title("Adjacent Skills")
                st.markdown(tag_html(sk.get("adjacent", []), "teal"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESUME ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
def page_resume():
    st.markdown("## ◉ Resume Intelligence Analyzer")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">8-stage AI pipeline · Full resume coverage · Chunked processing · Deep actionable insights</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Upload or Paste Resume")
        uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"],
                                    label_visibility="collapsed")
        if uploaded:
            with st.spinner("🔍 Running extraction pipeline..."):
                text, meta = parse_uploaded_file(uploaded)
            if text:
                st.session_state.resume_text = text
                st.session_state.extraction_meta = meta
                st.session_state.resume_analysis = None
                q = meta.get("quality", {})
                q_color = "#34d399" if q.get("score", 0) >= 70 else ("#fbbf24" if q.get("score", 0) >= 40 else "#f87171")
                alert(f"✓ {meta['word_count']} words · {meta['char_count']} chars · via {meta['method']} · Quality: <span style='color:{q_color};font-weight:600'>{q.get('score',0)}%</span>", "success")
                if meta.get("warning"):
                    alert(meta["warning"], "warning")
                if meta.get("detected_sections"):
                    st.markdown(tag_html(meta["detected_sections"], "teal"), unsafe_allow_html=True)
            else:
                alert("Could not extract text from file. Try pasting manually below.", "error")

        st.markdown("<div style='margin:0.5rem 0;color:#5050a0;font-size:0.75rem;text-align:center'>— or paste below —</div>", unsafe_allow_html=True)
        paste = st.text_area("Resume Text", value=st.session_state.resume_text, height=200,
                             placeholder="Paste your full resume text here...",
                             label_visibility="collapsed")
        if paste != st.session_state.resume_text:
            st.session_state.resume_text = paste
            st.session_state.resume_analysis = None

        target = st.text_input("🎯 Target Role",
                               value=st.session_state.target_role,
                               placeholder="e.g. Senior Frontend Developer")
        if target:
            st.session_state.target_role = target

        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("✨ Smart Clean", use_container_width=True):
                if st.session_state.resume_text:
                    st.session_state.resume_text = clean_text(st.session_state.resume_text)
                    alert("Text cleaned and normalized.", "success")
        with cc2:
            if st.button("🗑 Clear", use_container_width=True):
                st.session_state.resume_text = ""
                st.session_state.resume_analysis = None
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Run Full AI Analysis Pipeline", use_container_width=True, type="primary"):
            if not st.session_state.resume_text.strip():
                alert("Please upload or paste your resume first.", "warning")
            elif not any([st.session_state.groq_api_key, st.session_state.api_key,
                          st.session_state.gemini_api_key]):
                alert("Please configure an API key in the sidebar first.", "error")
            else:
                txt_hash = hashlib.md5(
                    (st.session_state.resume_text + st.session_state.target_role).encode()
                ).hexdigest()
                if txt_hash == st.session_state.resume_hash and st.session_state.resume_analysis:
                    alert("Analysis is up to date. Modify resume or target role to re-analyze.", "info")
                else:
                    wc = len(st.session_state.resume_text.split())
                    chunks_est = max(1, wc // 400)
                    with st.spinner(f"🧠 Running {chunks_est}-chunk AI pipeline — this takes 20–60 seconds..."):
                        try:
                            result = analyze_resume_chunked(
                                st.session_state.resume_text,
                                st.session_state.target_role
                            )
                            st.session_state.resume_analysis = result
                            st.session_state.structured_resume = result.get("structured_resume")
                            st.session_state.resume_hash = txt_hash
                            sc = st.session_state.dashboard_scores
                            sc["resume_score"]     = result.get("resume_score", 0)
                            sc["ats_score"]        = result.get("ats_score", 0)
                            sc["role_match"]       = result.get("role_match_score", 0)
                            sc["career_readiness"] = result.get("career_readiness_score", 0)
                            st.session_state.progress_history.append({
                                "date": datetime.now().strftime("%b %d %H:%M"),
                                "score": result.get("resume_score", 0)
                            })
                            alert(f"✓ Full pipeline complete! {result.get('chunks_processed', 1)} chunk(s) analyzed.", "success")
                        except Exception as e:
                            alert(f"Analysis error: {e}", "error")

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.extraction_meta:
            meta = st.session_state.extraction_meta
            with st.expander("📄 Extraction Details"):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Words", meta.get("word_count", 0))
                m2.metric("Quality", f"{meta.get('quality_score',0)}%")
                m3.metric("Type", meta.get("file_type", "—"))
                m4.metric("Size", f"{meta.get('size_kb',0)} KB")

        if st.session_state.resume_text:
            with st.expander("📋 Resume Preview"):
                preview = st.session_state.resume_text[:3000]
                if len(st.session_state.resume_text) > 3000:
                    preview += f"\n\n... [{len(st.session_state.resume_text)-3000} more chars]"
                st.text_area("", value=preview, height=200, label_visibility="collapsed", disabled=True)

    with col2:
        an = st.session_state.resume_analysis
        if an:
            # Score Hero
            st.markdown(f"""
            <div class="hero-score">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-bottom:1rem">
              <div><div class="score-big" style="color:#a78bfa">{an.get('resume_score',0)}</div><div class="score-label">Resume</div>{progress_bar(an.get('resume_score',0),'purple')}</div>
              <div><div class="score-big" style="color:#38bdf8">{an.get('ats_score',0)}</div><div class="score-label">ATS</div>{progress_bar(an.get('ats_score',0),'teal')}</div>
              <div><div class="score-big" style="color:#34d399">{an.get('role_match_score',0)}</div><div class="score-label">Role Match</div>{progress_bar(an.get('role_match_score',0),'green')}</div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem">
              <div><div style="font-size:1.4rem;font-weight:700;color:#fbbf24">{an.get('career_readiness_score',0)}</div><div class="score-label">Career Ready</div>{progress_bar(an.get('career_readiness_score',0),'amber')}</div>
              <div><div style="font-size:1.4rem;font-weight:700;color:#a78bfa">{an.get('clarity_score',0)}</div><div class="score-label">Clarity</div>{progress_bar(an.get('clarity_score',0),'purple')}</div>
              <div><div style="font-size:1.4rem;font-weight:700;color:#38bdf8">{an.get('impact_score',0)}</div><div class="score-label">Impact</div>{progress_bar(an.get('impact_score',0),'teal')}</div>
              <div><div style="font-size:1.4rem;font-weight:700;color:#f472b6">{an.get('content_depth_score',0)}</div><div class="score-label">Depth</div>{progress_bar(an.get('content_depth_score',0),'pink')}</div>
            </div>
            <div style="margin-top:0.75rem;font-size:0.72rem;color:#5050a0">
              Confidence: {int(an.get('confidence',0.85)*100)}% · {st.session_state.active_provider} · {an.get('chunks_processed',1)} chunk(s)
            </div>
            </div>
            """, unsafe_allow_html=True)

            t1, t2, t3, t4, t5, t6 = st.tabs(["Overview", "Sections", "Rewrites", "Role Fit", "ATS", "Quick Wins"])

            with t1:
                col_s, col_w = st.columns(2)
                with col_s:
                    section_title("Strengths")
                    for s in an.get("strengths", []):
                        st.markdown(f'<div style="display:flex;gap:8px;padding:5px 0;font-size:0.83rem;color:#9090b0;border-bottom:1px solid rgba(255,255,255,0.04)"><span style="color:#34d399;flex-shrink:0">✓</span>{s}</div>', unsafe_allow_html=True)
                with col_w:
                    section_title("Weaknesses")
                    for w in an.get("weaknesses", []):
                        st.markdown(f'<div style="display:flex;gap:8px;padding:5px 0;font-size:0.83rem;color:#9090b0;border-bottom:1px solid rgba(255,255,255,0.04)"><span style="color:#f87171;flex-shrink:0">✗</span>{w}</div>', unsafe_allow_html=True)
                st.markdown("---")
                section_title("Missing Keywords")
                st.markdown(tag_html(an.get("missing_keywords", []), "amber"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                section_title("Missing Skills")
                st.markdown(tag_html(an.get("missing_skills", []), "red"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if an.get("experience_gap"):
                    alert(f"🔍 Experience Gap: {an['experience_gap']}", "warning")
                ca, cb = st.columns(2)
                with ca:
                    section_title("Strong Sections")
                    st.markdown(tag_html(an.get("strong_sections", []), "green"), unsafe_allow_html=True)
                with cb:
                    section_title("Weak Sections")
                    st.markdown(tag_html(an.get("weak_sections", []), "red"), unsafe_allow_html=True)

            with t2:
                sf = an.get("section_feedback", {})
                icons = {"summary": "📝", "skills": "🛠", "experience": "💼", "projects": "🚀",
                         "education": "🎓", "certifications": "📜", "formatting": "🎨"}
                for sec_name, sec_data in sf.items():
                    if not isinstance(sec_data, dict):
                        continue
                    score = sec_data.get("score", 50)
                    with st.expander(f"{icons.get(sec_name,'◎')} {sec_name.title()} — {score}/100", expanded=False):
                        st.markdown(score_badge(score), unsafe_allow_html=True)
                        if PLOTLY_AVAILABLE:
                            st.plotly_chart(make_gauge(score, sec_name.title(), score_color(score), height=140),
                                            use_container_width=True, config={"displayModeBar": False})
                        ci2, cs2 = st.columns(2)
                        with ci2:
                            section_title("Issues")
                            for issue in sec_data.get("issues", []):
                                st.markdown(f'<div style="font-size:0.82rem;color:#f87171;padding:3px 0">▲ {issue}</div>', unsafe_allow_html=True)
                        with cs2:
                            section_title("What's Working")
                            for strength in sec_data.get("strengths", []):
                                st.markdown(f'<div style="font-size:0.82rem;color:#34d399;padding:3px 0">✓ {strength}</div>', unsafe_allow_html=True)
                        section_title("How to Improve")
                        for imp in sec_data.get("improvements", []):
                            st.markdown(f'<div style="font-size:0.82rem;color:#9090b0;padding:3px 0">◎ {imp}</div>', unsafe_allow_html=True)
                        if sec_data.get("rewrite"):
                            st.markdown("---")
                            section_title("✨ AI Rewrite Suggestion")
                            st.markdown(f'<div class="alert-info" style="font-style:italic">{sec_data["rewrite"]}</div>', unsafe_allow_html=True)

            with t3:
                rewrites = an.get("rewrite_suggestions", [])
                if rewrites:
                    for i, rw in enumerate(rewrites):
                        impact = rw.get("impact", "Medium")
                        ic_cls = {"High": "red", "Medium": "amber", "Low": "green"}.get(impact, "amber")
                        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
                        st.markdown(f'<div style="display:flex;justify-content:space-between"><div class="section-title">Suggestion {i+1}</div><span class="tag-{ic_cls}">Impact: {impact}</span></div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:0.82rem;color:#f87171;margin-bottom:0.5rem;padding:0.6rem;background:rgba(248,113,113,0.07);border-radius:8px;border-left:3px solid #f87171">❌ <b>Before:</b> {rw.get("original","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:0.82rem;color:#34d399;margin-bottom:0.5rem;padding:0.6rem;background:rgba(52,211,153,0.07);border-radius:8px;border-left:3px solid #34d399">✅ <b>After:</b> {rw.get("improved","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:0.78rem;color:#9090b0"><b style="color:#a78bfa">Why this works:</b> {rw.get("why","")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    alert("No rewrite suggestions in this analysis.", "info")

            with t4:
                rf = an.get("role_fit", {})
                if rf:
                    match_pct = rf.get("match_percentage", an.get("role_match_score", 0))
                    mc = score_color(match_pct)
                    st.markdown(f"""
                    <div class="glass-card-accent">
                    <div style="display:flex;align-items:center;gap:1.5rem">
                      <div style="text-align:center;flex-shrink:0">
                        <div style="font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;color:{mc}">{match_pct}%</div>
                        <div class="score-label">Role Match</div>
                      </div>
                      <div>
                        <div class="section-title">Role Fit: {rf.get('selected_role','—')}</div>
                        <div style="font-size:0.87rem;color:#d0d0f0;line-height:1.7">{rf.get('match_reasoning','')}</div>
                      </div>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                    ra, rb = st.columns(2)
                    with ra:
                        section_title("Priority Skill Gaps")
                        for g in rf.get("priority_gaps", []):
                            st.markdown(f'<span class="tag-red">{g}</span>', unsafe_allow_html=True)
                    with rb:
                        section_title("Alternate Role Suggestions")
                        for r in rf.get("alternate_roles", []):
                            st.markdown(f'<span class="tag-purple">{r}</span>', unsafe_allow_html=True)

            with t5:
                ats = an.get("ats_analysis", {})
                if ats:
                    ats_ok = ats.get("ats_friendly", False)
                    alert(f"{'✓ ATS Friendly' if ats_ok else '✗ ATS Issues Detected'}", "success" if ats_ok else "error")
                    kd = ats.get("keyword_density", "medium")
                    kd_color = {"high": "#34d399", "medium": "#fbbf24", "low": "#f87171"}.get(kd, "#fbbf24")
                    st.markdown(f'<div style="font-size:0.85rem;color:{kd_color};margin:0.5rem 0">Keyword Density: <b>{kd.upper()}</b></div>', unsafe_allow_html=True)
                    if ats.get("formatting_issues"):
                        section_title("Formatting Issues")
                        for fi in ats["formatting_issues"]:
                            st.markdown(f'<div class="alert-warning" style="font-size:0.8rem">⚠ {fi}</div>', unsafe_allow_html=True)
                    if ats.get("recommended_keywords"):
                        st.markdown("<br>", unsafe_allow_html=True)
                        section_title("Add These Keywords")
                        st.markdown(tag_html(ats["recommended_keywords"], "amber"), unsafe_allow_html=True)
                else:
                    alert("ATS analysis will appear here after resume analysis.", "info")

            with t6:
                qw = an.get("quick_wins", [])
                if qw:
                    for i, win in enumerate(qw):
                        st.markdown(f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)"><span style="background:rgba(251,191,36,0.2);color:#fbbf24;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;font-weight:700">⚡</span><div style="font-size:0.85rem;color:#d0d0f0">{win}</div></div>', unsafe_allow_html=True)
                # Roadmap quick view
                rm = an.get("roadmap", {})
                if rm:
                    st.markdown("<br>", unsafe_allow_html=True)
                    r1, r2 = st.columns(2)
                    with r1:
                        section_title("7-Day Sprint Plan")
                        for i, task in enumerate(rm.get("7_day_plan", [])):
                            st.markdown(f'<div style="font-size:0.8rem;color:#9090b0;padding:4px 0"><span style="color:#a78bfa">Day {i+1}</span> — {task}</div>', unsafe_allow_html=True)
                    with r2:
                        section_title("30-Day Goals")
                        for i, goal in enumerate(rm.get("30_day_plan", [])):
                            st.markdown(f'<div style="font-size:0.8rem;color:#9090b0;padding:4px 0"><span style="color:#38bdf8">Wk {i+1}</span> — {goal}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:4rem 1.5rem">
            <div style="font-size:4rem;opacity:0.1;margin-bottom:1.5rem">◉</div>
            <div style="color:#5050a0;font-size:0.95rem;line-height:2">
              Upload or paste your resume<br>
              Set your target role<br>
              Click <b style="color:#a78bfa">Run Full AI Analysis Pipeline</b><br><br>
              <span style="font-size:0.8rem">Multi-stage AI · Full resume coverage · 20+ insight dimensions</span>
            </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SKILL GAP
# ══════════════════════════════════════════════════════════════════════════════
def page_skillgap():
    st.markdown("## ◐ Skill Gap Analysis")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Identify exactly what stands between you and your target role</div>', unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1.2])

    with col_in:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Your Input")

        # Pre-fill from structured resume if available
        sr = st.session_state.structured_resume
        default_skills = st.session_state.current_skills
        if sr and not default_skills:
            default_skills = ", ".join(sr.get("skills_found", [])[:20])

        current_skills = st.text_area("Current Skills (comma-separated)",
                                      value=default_skills, height=100,
                                      placeholder="React, JavaScript, CSS, Python, SQL...")
        if current_skills != st.session_state.current_skills:
            st.session_state.current_skills = current_skills
        target = st.text_input("Target Role", value=st.session_state.target_role, key="sg_role")
        if target:
            st.session_state.target_role = target
        exp_level = st.selectbox("Experience Level",
                                 ["Student/Fresher", "0-1 years", "1-3 years", "3-5 years", "5+ years"])
        industry = st.selectbox("Industry Focus",
                                ["Tech/Software", "Fintech", "Healthcare", "E-commerce",
                                 "Startup", "Enterprise", "Consulting", "AI/ML"])

        if st.button("🔍 Analyze Skill Gap", use_container_width=True):
            if not current_skills.strip():
                alert("Please enter your current skills.", "warning")
            else:
                with st.spinner("Analyzing skill gaps..."):
                    sys_p = """You are a senior tech recruiter and career gap analyst with 15 years of experience.
Return ONLY valid JSON, no markdown, no explanation:
{
  "gap_percentage": 45,
  "priority_skill": "most important missing skill",
  "insight": "2-3 sentence practical insight about the gap and what it means for job search",
  "missing_skills": ["skill1","skill2","skill3","skill4","skill5","skill6"],
  "important_skills": ["skill1","skill2","skill3","skill4"],
  "optional_skills": ["skill1","skill2","skill3"],
  "adjacent_skills": ["skill1","skill2"],
  "radar_skills": ["s1","s2","s3","s4","s5","s6"],
  "radar_current": [70,40,35,60,50,25],
  "radar_target":  [90,85,80,75,70,60],
  "learning_order": ["learn this first — why","then this — why","then this","then this"],
  "time_estimate": "3-4 months with 10 hrs/week",
  "seniority_gap": "1-2 levels below target",
  "experience_gaps": ["missing X years in Y","no production experience in Z"],
  "alternate_roles": ["easier role 1","easier role 2","easier role 3"],
  "market_demand": "High|Medium|Low",
  "industry_specific_gaps": ["gap1","gap2"]
}"""
                    usr_p = f"Current skills: {current_skills}\nTarget: {target}\nExperience: {exp_level}\nIndustry: {industry}"
                    try:
                        raw = call_ai(sys_p, usr_p, max_tokens=1200)
                        result = parse_json(raw)
                        st.session_state.skill_gap = result
                        st.session_state.dashboard_scores["gap_pct"] = result.get("gap_percentage", 0)
                        alert("✓ Skill gap analysis complete!", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_out:
        sg = st.session_state.skill_gap
        if sg:
            gap_pct = sg.get("gap_percentage", 0)
            gap_color = "#f87171" if gap_pct > 60 else ("#fbbf24" if gap_pct > 35 else "#34d399")
            demand = sg.get("market_demand", "Medium")
            dc2 = {"High": "#34d399", "Medium": "#fbbf24", "Low": "#f87171"}.get(demand, "#fbbf24")
            st.markdown(f"""
            <div class="glass-card-accent">
            <div style="display:flex;align-items:center;gap:1.5rem">
              <div style="text-align:center;flex-shrink:0">
                <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:{gap_color}">{gap_pct}%</div>
                <div class="score-label">Skill Gap</div>
              </div>
              <div style="flex:1">
                <div style="font-size:0.9rem;font-weight:600;color:#eeeeff;margin-bottom:4px">Priority: <span style="color:#fbbf24">{sg.get('priority_skill','—')}</span></div>
                <div style="font-size:0.82rem;color:#9090b0;line-height:1.6">{sg.get('insight','')}</div>
                <div style="margin-top:8px;font-size:0.78rem;color:#5050a0">
                  ⏱ {sg.get('time_estimate','—')} · {sg.get('seniority_gap','—')} · Market Demand: <span style="color:{dc2}">{demand}</span>
                </div>
              </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Must-Have (Critical)")
                st.markdown(tag_html(sg.get("missing_skills", []), "red"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("High-Value")
                st.markdown(tag_html(sg.get("important_skills", []), "amber"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Good to Have")
                st.markdown(tag_html(sg.get("optional_skills", []), "purple"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c4:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Adjacent Skills")
                st.markdown(tag_html(sg.get("adjacent_skills", []), "teal"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if PLOTLY_AVAILABLE and sg.get("radar_skills"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Skill Radar — Current vs Target")
                st.plotly_chart(
                    make_radar(sg["radar_skills"], sg.get("radar_current", [50] * 6),
                               sg.get("radar_target", [90] * 6)),
                    use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Learning Order (Recommended Path)")
            for i, step in enumerate(sg.get("learning_order", [])):
                st.markdown(f'<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;font-size:0.83rem;color:#9090b0;border-bottom:1px solid rgba(255,255,255,0.04)"><span style="background:#6c63ff;color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.65rem;flex-shrink:0;margin-top:2px">{i+1}</span>{step}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if sg.get("experience_gaps"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Experience Gaps")
                for gap in sg["experience_gaps"]:
                    alert(f"⚠ {gap}", "warning")
                st.markdown('</div>', unsafe_allow_html=True)

            if sg.get("alternate_roles"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Easier Entry Roles")
                st.markdown(tag_html(sg.get("alternate_roles", []), "purple"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 1.5rem">
            <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◐</div>
            <div style="color:#5050a0;font-size:0.9rem">Enter your skills and target role,<br>then run the analysis.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEARNING ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
def page_roadmap():
    st.markdown("## ◳ Learning Roadmap")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Personalized week-by-week plan with tasks, mini-projects, resources, and checkpoints</div>', unsafe_allow_html=True)

    col_ctrl, col_stat = st.columns([2, 1])
    with col_ctrl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Configure Your Roadmap")
        c1, c2 = st.columns(2)
        with c1: target = st.text_input("Target Role", value=st.session_state.target_role, key="rm_role")
        with c2: hours = st.number_input("Hours/week available", min_value=2, max_value=40, value=10, step=1)
        skills_known = st.text_input("Skills you already know",
                                     value=st.session_state.current_skills,
                                     placeholder="React, JavaScript...")
        c3, c4 = st.columns(2)
        with c3: weeks_n = st.slider("Roadmap length (weeks)", 4, 16, 8)
        with c4: level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

        if st.button("🗺 Generate AI Roadmap", use_container_width=True):
            with st.spinner("Building your personalized roadmap..."):
                sys_p = f"""You are a world-class career mentor, learning path designer, and curriculum expert.
Generate a detailed {weeks_n}-week learning roadmap. Return ONLY a valid JSON array, no markdown:
[
  {{
    "week": 1,
    "title": "Topic Name",
    "objective": "Specific measurable goal for this week",
    "tasks": ["very specific task 1","very specific task 2","very specific task 3","very specific task 4"],
    "daily_focus": "One sentence daily focus theme",
    "resources": ["Real resource 1 (book/course/docs)","Real resource 2"],
    "project": "Specific mini project to build with tech stack",
    "checkpoint": "Specific measurable success criteria",
    "effort_hours": 10,
    "concepts": ["core concept 1","core concept 2","core concept 3"]
  }}
]
Make tasks extremely specific with action verbs. Include real resource names (e.g., 'MDN Web Docs', 'Eloquent JavaScript', 'CS50').
Each week should build on the previous."""
                usr_p = f"Target: {target}\nCurrent skills: {skills_known}\nHours/week: {hours}\nWeeks: {weeks_n}\nLevel: {level}"
                try:
                    raw = call_ai(sys_p, usr_p, max_tokens=3000)
                    result = parse_json(raw)
                    st.session_state.roadmap = result
                    st.session_state.roadmap_checks = {}
                    alert(f"✓ {len(result)}-week roadmap generated!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_stat:
        rm = st.session_state.roadmap
        if rm:
            total_tasks = sum(len(w.get("tasks", [])) for w in rm)
            checks = st.session_state.roadmap_checks
            done = sum(1 for k, v in checks.items() if v)
            pct = int(done / total_tasks * 100) if total_tasks else 0
            st.session_state.dashboard_scores["roadmap_pct"] = pct
            total_hours = sum(w.get("effort_hours", 0) for w in rm)
            st.markdown(f"""
            <div class="glass-card" style="text-align:center">
            <div class="score-big" style="color:#34d399">{pct}%</div>
            <div class="score-label">Complete</div>
            {progress_bar(pct,'green')}
            <div style="margin-top:0.75rem;font-size:0.82rem;color:#5050a0">{done} / {total_tasks} tasks</div>
            <div style="font-size:0.78rem;color:#5050a0">{len(rm)} weeks · ~{total_hours}h total</div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.roadmap:
        st.markdown("<br>", unsafe_allow_html=True)
        checks = st.session_state.roadmap_checks
        for wi, week in enumerate(st.session_state.roadmap):
            tasks = week.get("tasks", [])
            week_done = sum(1 for i in range(len(tasks)) if checks.get(f"{wi}_{i}", False))
            is_done = week_done == len(tasks) and len(tasks) > 0
            title_str = ("✓ " if is_done else "") + f"Week {week.get('week', wi+1)} — {week.get('title','')}"

            with st.expander(title_str, expanded=(wi == 0)):
                if week.get("objective"):
                    alert(f"🎯 Goal: {week['objective']}", "info")
                tc, rc = st.columns([2, 1])
                with tc:
                    section_title("Tasks")
                    for ti, task in enumerate(tasks):
                        key = f"{wi}_{ti}"
                        current = checks.get(key, False)
                        checked = st.checkbox(task, value=current, key=f"chk_{wi}_{ti}")
                        if checked != current:
                            st.session_state.roadmap_checks[key] = checked
                            st.rerun()
                    if week.get("concepts"):
                        st.markdown("<br>", unsafe_allow_html=True)
                        section_title("Core Concepts")
                        st.markdown(tag_html(week["concepts"], "teal"), unsafe_allow_html=True)
                with rc:
                    for r in week.get("resources", []):
                        st.markdown(f'<div style="font-size:0.79rem;color:#9090b0;padding:3px 0">📚 {r}</div>', unsafe_allow_html=True)
                    if week.get("project"):
                        st.markdown(f'<br><div style="font-size:0.8rem;color:#a78bfa;padding:8px;background:rgba(108,99,255,0.1);border-radius:8px;border:1px solid rgba(108,99,255,0.2)">🚀 {week["project"]}</div>', unsafe_allow_html=True)
                    if week.get("checkpoint"):
                        st.markdown(f'<br><div style="font-size:0.79rem;color:#34d399;padding:6px;background:rgba(52,211,153,0.07);border-radius:6px">✓ {week["checkpoint"]}</div>', unsafe_allow_html=True)
                    if week.get("effort_hours"):
                        st.markdown(f'<div style="font-size:0.75rem;color:#5050a0;margin-top:8px">⏱ ~{week["effort_hours"]}h this week</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 1.5rem;margin-top:1rem">
        <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◳</div>
        <div style="color:#5050a0;font-size:0.9rem">Configure your roadmap above<br>and generate a personalized learning plan.</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AI CAREER COACH
# ══════════════════════════════════════════════════════════════════════════════
def page_chat():
    st.markdown("## ◫ AI Career Coach")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1rem">Context-aware AI coach with full knowledge of your resume, scores, and career profile</div>', unsafe_allow_html=True)

    quick_prompts = [
        "How can I improve my resume score?", "What skill should I learn first?",
        "Give me salary negotiation tips", "How do I prepare for system design?",
        "Review my resume executive summary", "What are my top 3 career risks?",
        "How do I stand out for this role?", "What projects should I build?",
        "How do I handle interview nerves?", "What's my quickest path to a job?",
        "How should I rewrite my LinkedIn?", "What companies should I target?",
    ]
    qcols = st.columns(4)
    for i, prompt in enumerate(quick_prompts):
        with qcols[i % 4]:
            if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                _chat_get_reply(prompt)
                st.rerun()

    st.markdown("---")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><div class="chat-label">You</div>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai"><div class="chat-label">◈ Nexus AI Coach</div>{msg["content"]}</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown('<div style="text-align:center;padding:3rem;color:#404060"><div style="font-size:2.5rem;margin-bottom:0.5rem">◫</div><div style="font-size:0.87rem">Start a conversation or tap a quick prompt above.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ic, bc = st.columns([5, 1])
    with ic:
        user_input = st.text_input("Message", placeholder="Ask your career coach anything...",
                                   label_visibility="collapsed", key="chat_input_box")
    with bc:
        send = st.button("Send ↗", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        _chat_get_reply(user_input)
        st.rerun()

    if st.button("Clear conversation", key="clr_chat"):
        st.session_state.chat_history = []
        st.rerun()


def _chat_get_reply(user_msg: str):
    an = st.session_state.resume_analysis or {}
    ci = an.get("career_insights", {})
    sr = st.session_state.structured_resume or {}
    sys_p = f"""You are Nexus AI, an expert career coach specializing in tech hiring, resume optimization, and career strategy.
You have deep knowledge of this candidate's profile:

- Target role: {st.session_state.target_role}
- Current skills: {st.session_state.current_skills or sr.get('skills_found', ['not specified'])[:10]}
- Resume score: {an.get('resume_score', 'not analyzed')}/100
- ATS score: {an.get('ats_score', 'not analyzed')}/100
- Role match: {an.get('role_match_score', 'not analyzed')}%
- Career readiness: {an.get('career_readiness_score', 'not analyzed')}/100
- Biggest strength: {ci.get('biggest_strength', 'unknown')}
- Biggest risk: {ci.get('biggest_risk', 'unknown')}
- Job ready: {ci.get('job_ready', 'unknown')}
- Missing skills: {', '.join(an.get('missing_skills', [])[:6]) or 'unknown'}
- Salary range: {ci.get('salary_range', 'not estimated')}
- One-line diagnosis: {ci.get('one_line_diagnosis', 'not analyzed')}

Be specific, encouraging, and highly actionable. Use bullet points only for 3+ items.
Reference their actual data when relevant. Give concrete next steps, not vague advice.
Aim for 3-6 sentences or bullet points."""
    history = st.session_state.chat_history[-10:]
    try:
        any_key = bool(st.session_state.get("groq_api_key") or
                       st.session_state.get("api_key") or
                       st.session_state.get("gemini_api_key"))
        if not any_key:
            reply = "Please set at least one API key in ⚙ AI Provider Settings in the sidebar (Groq is free!)."
        else:
            user_context = "\n".join(f"{m['role']}: {m['content']}" for m in history[-8:])
            reply = call_ai(sys_p, user_context, max_tokens=600)
    except Exception as e:
        reply = f"Error: {e}"
    st.session_state.chat_history.append({"role": "assistant", "content": reply})


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW PREP
# ══════════════════════════════════════════════════════════════════════════════
def page_interview():
    st.markdown("## ◬ Interview Intelligence System")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">AI-generated questions with answer strategies, common mistakes, and instant AI feedback</div>', unsafe_allow_html=True)

    ctrl_col, _ = st.columns([2, 1])
    with ctrl_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: role = st.text_input("Role", value=st.session_state.target_role, key="iv_role")
        with c2: q_type = st.selectbox("Type", ["Mixed", "Technical", "Behavioral", "Senior-Level", "System Design"])
        with c3: q_count = st.selectbox("Count", [3, 5, 7, 10], index=1)
        with c4: difficulty = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])

        if st.button("⚡ Generate Intelligence Questions", use_container_width=True):
            with st.spinner("Generating tailored interview questions..."):
                resume_ctx = f"\nCandidate resume context: {st.session_state.resume_text[:1800]}" if st.session_state.resume_text else ""
                an = st.session_state.resume_analysis
                strengths_ctx = f"\nCandidate strengths: {', '.join(an.get('strengths', [])[:3])}" if an else ""
                sys_p = f"""You are a principal engineer and senior interviewer at a FAANG company.
Generate {q_count} {q_type.lower()} questions for: {role}. Difficulty: {difficulty}.
Tailor questions to the candidate's specific background when resume context is provided.
Return ONLY valid JSON array, no markdown:
[{{
  "type": "{q_type}",
  "question": "full, specific question text",
  "difficulty": "Easy|Medium|Hard",
  "hint": "strategic one-line hint for approaching this question",
  "good_answer_points": ["point 1 — what to say","point 2 — what to include","point 3"],
  "common_mistake": "what most candidates get wrong and how to avoid it",
  "time_to_answer": "X minutes",
  "answer_strategy": "STAR|Technical deep-dive|Problem decomposition|etc",
  "follow_up": "likely follow-up question"
}}]"""
                try:
                    raw = call_ai(sys_p, f"Role: {role}{resume_ctx}{strengths_ctx}", max_tokens=2000)
                    questions = parse_json(raw)
                    st.session_state.interview_questions = questions
                    alert(f"✓ {len(questions)} questions generated!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.interview_questions:
        st.markdown("<br>", unsafe_allow_html=True)
        for qi, q in enumerate(st.session_state.interview_questions):
            diff = q.get("difficulty", "Medium")
            dc = {"Easy": "green", "Medium": "amber", "Hard": "red"}.get(diff, "amber")
            question_preview = q.get('question', '')[:80]
            with st.expander(f"Q{qi+1} [{diff}]: {question_preview}...", expanded=(qi == 0)):
                st.markdown(f"""
                <div style="margin-bottom:0.75rem">
                  <span class="tag-{dc}">{diff}</span>
                  <span class="tag-purple">{q.get("type","Technical")}</span>
                  {"<span class='tag-teal'>⏱ "+q.get('time_to_answer','')+"</span>" if q.get("time_to_answer") else ""}
                  {"<span class='tag-amber'>Strategy: "+q.get('answer_strategy','')+"</span>" if q.get("answer_strategy") else ""}
                </div>
                <div style="font-size:1rem;color:#eeeeff;margin-bottom:1rem;line-height:1.7;padding:1rem;background:rgba(108,99,255,0.06);border-radius:10px;border-left:3px solid #6c63ff">
                  {q.get("question","")}
                </div>
                """, unsafe_allow_html=True)

                if q.get("follow_up"):
                    st.markdown(f'<div style="font-size:0.78rem;color:#5050a0;margin-bottom:0.75rem">🔄 Likely follow-up: <i>{q["follow_up"]}</i></div>', unsafe_allow_html=True)

                answer = st.text_area("Your answer", key=f"ta_{qi}", height=130,
                                      placeholder="Type your answer here... aim for the STAR method for behavioral questions")
                h_col, e_col, _ = st.columns([1, 1, 2])
                with h_col:
                    if st.button("Show Hint", key=f"hint_{qi}"):
                        alert(q.get("hint", "No hint available."), "info")
                with e_col:
                    if st.button("🤖 AI Feedback", key=f"eval_{qi}"):
                        if not answer.strip():
                            alert("Write an answer first.", "warning")
                        else:
                            with st.spinner("Evaluating your answer..."):
                                try:
                                    fb = call_ai(
                                        f"""You are a senior tech interviewer at a top company. 
Give specific, actionable feedback on this interview answer.
Score it out of 10. Be encouraging but honest.
Structure: Score | What worked well | What to improve | One concrete suggestion.
4-6 sentences total.""",
                                        f"Question: {q.get('question','')}\nAnswer: {answer}\nRole: {st.session_state.target_role}",
                                        max_tokens=400)
                                    alert(fb, "success")
                                except Exception as e:
                                    alert(f"Error: {e}", "error")

                gpa = q.get("good_answer_points", [])
                cm = q.get("common_mistake", "")
                if gpa or cm:
                    st.markdown("---")
                    cg, cc = st.columns(2)
                    with cg:
                        if gpa:
                            section_title("Key Points to Cover")
                            for p in gpa:
                                st.markdown(f'<div style="font-size:0.8rem;color:#9090b0;padding:3px 0">◎ {p}</div>', unsafe_allow_html=True)
                    with cc:
                        if cm:
                            section_title("Common Mistake")
                            st.markdown(f'<div class="alert-warning" style="font-size:0.8rem">{cm}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 1.5rem;margin-top:1rem">
        <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◬</div>
        <div style="color:#5050a0;font-size:0.9rem">Set a role and generate AI interview questions.<br>Practice answers and get instant AI feedback.</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAREER INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
def page_insights():
    st.markdown("## ◆ Career Insights")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Deep AI diagnosis of your career profile, trajectory, risks, and highest-ROI actions</div>', unsafe_allow_html=True)

    an = st.session_state.resume_analysis
    ci = an.get("career_insights", {}) if an else {}

    if not ci:
        col_a, _ = st.columns([2, 1])
        with col_a:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Generate Standalone Career Insights")
            role = st.text_input("Target Role", value=st.session_state.target_role, key="ci_role")
            skills = st.text_area("Your Skills & Experience Summary",
                                  value=st.session_state.current_skills, height=100,
                                  placeholder="Describe your background, years of experience, key skills...")
            exp_years = st.selectbox("Years of Experience",
                                     ["<1 year", "1-2 years", "2-4 years", "4-7 years", "7+ years"])

            if st.button("◆ Generate Career Insights", use_container_width=True):
                with st.spinner("Analyzing your career profile..."):
                    sys_p = """You are a world-class career strategist with 20 years of experience placing senior tech professionals.
Return ONLY valid JSON, no markdown:
{
  "one_line_diagnosis": "one crisp sentence career diagnosis",
  "biggest_strength": "specific sentence about standout strength",
  "biggest_risk": "specific sentence about main career risk",
  "quickest_win": "one very actionable sentence for immediate improvement",
  "job_ready": false,
  "next_best_action": "specific, concrete next step",
  "highest_roi_skill": "skill name — why it matters and expected impact",
  "fix_this_week": "one very specific action to take this week",
  "career_trajectory": "where they are headed based on current profile",
  "market_positioning": "their competitive position and unique angle",
  "salary_range": "realistic salary range: $X - $Y (city/remote)",
  "competition_level": "Low|Medium|High|Very High",
  "growth_potential": "High|Medium|Low",
  "time_to_job_ready": "e.g. 3-6 months with consistent effort",
  "recommendations": ["specific rec 1","specific rec 2","specific rec 3","specific rec 4","specific rec 5"]
}"""
                    try:
                        raw = call_ai(sys_p,
                                      f"Target: {role}\nBackground: {skills}\nExperience: {exp_years}",
                                      max_tokens=1000)
                        result = parse_json(raw)
                        if not st.session_state.resume_analysis:
                            st.session_state.resume_analysis = {"career_insights": result}
                        else:
                            st.session_state.resume_analysis["career_insights"] = result
                        ci = result
                        alert("✓ Career insights generated!", "success")
                        st.rerun()
                    except Exception as e:
                        alert(f"Error: {e}", "error")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        alert("✓ Insights loaded from your resume analysis.", "info")

    if ci:
        st.markdown(f"""
        <div class="glass-card-accent" style="text-align:center;padding:1.5rem">
        <div class="section-title">◆ Career Diagnosis</div>
        <div style="font-size:1.05rem;color:#d0d0f0;font-style:italic;line-height:1.7">"{ci.get('one_line_diagnosis','')}"</div>
        {"<div style='margin-top:0.5rem;font-size:0.78rem;color:#5050a0'>Est. time to job-ready: "+ci.get('time_to_job_ready','')+"</div>" if ci.get('time_to_job_ready') else ""}
        </div>
        """, unsafe_allow_html=True)

        ia, ib, ic_ = st.columns(3)
        with ia:
            st.markdown(f'<div class="insight-card"><div class="insight-icon">💪</div><div class="insight-label">Biggest Strength</div><div class="insight-value">{ci.get("biggest_strength","—")}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card"><div class="insight-icon">📈</div><div class="insight-label">Career Trajectory</div><div class="insight-value">{ci.get("career_trajectory","—")}</div></div>', unsafe_allow_html=True)
        with ib:
            st.markdown(f'<div class="insight-card"><div class="insight-icon">⚠️</div><div class="insight-label">Biggest Risk</div><div class="insight-value">{ci.get("biggest_risk","—")}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card"><div class="insight-icon">💰</div><div class="insight-label">Estimated Salary Range</div><div class="insight-value">{ci.get("salary_range","—")}</div></div>', unsafe_allow_html=True)
        with ic_:
            ready = ci.get("job_ready", False)
            rc = "#34d399" if ready else "#f87171"
            rl = "Job Ready ✓" if ready else "Not Yet Ready"
            st.markdown(f'<div class="insight-card"><div class="insight-icon">🎯</div><div class="insight-label">Job Readiness</div><div class="insight-value" style="color:{rc};font-weight:600">{rl}</div></div>', unsafe_allow_html=True)
            comp = ci.get("competition_level", "Medium")
            cc2 = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171", "Very High": "#f87171"}.get(comp, "#fbbf24")
            st.markdown(f'<div class="insight-card"><div class="insight-icon">🏆</div><div class="insight-label">Competition Level</div><div class="insight-value" style="color:{cc2}">{comp}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        aa, ab = st.columns(2)
        with aa:
            st.markdown(f'<div class="glass-card" style="border-color:rgba(251,191,36,0.3)"><div class="section-title">⚡ Quickest Win</div><div style="font-size:0.9rem;color:#fbbf24;font-weight:600">{ci.get("quickest_win","—")}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card" style="border-color:rgba(108,99,255,0.3)"><div class="section-title">🎓 Highest ROI Skill</div><div style="font-size:0.9rem;color:#a78bfa;font-weight:600">{ci.get("highest_roi_skill","—")}</div></div>', unsafe_allow_html=True)
        with ab:
            st.markdown(f'<div class="glass-card" style="border-color:rgba(52,211,153,0.3)"><div class="section-title">🚀 Next Best Action</div><div style="font-size:0.9rem;color:#34d399;font-weight:600">{ci.get("next_best_action","—")}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card" style="border-color:rgba(56,189,248,0.3)"><div class="section-title">📅 Fix This Week</div><div style="font-size:0.9rem;color:#38bdf8;font-weight:600">{ci.get("fix_this_week","—")}</div></div>', unsafe_allow_html=True)

        if ci.get("recommendations"):
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Top Strategic Recommendations")
            for i, rec in enumerate(ci.get("recommendations", [])):
                st.markdown(f'<div style="display:flex;gap:12px;padding:8px 0;font-size:0.85rem;color:#9090b0;border-bottom:1px solid rgba(255,255,255,0.04)"><span style="color:#a78bfa;font-weight:600;flex-shrink:0">#{i+1}</span>{rec}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if ci.get("market_positioning"):
            alert(f"🌐 Market Positioning: {ci.get('market_positioning','')}", "info")


# ══════════════════════════════════════════════════════════════════════════════
# JD MATCHER (NEW)
# ══════════════════════════════════════════════════════════════════════════════
def page_jd_matcher():
    st.markdown("## ◍ Job Description Matcher")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Compare your resume against any job description — find gaps, match %, and tailoring suggestions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Job Description")
        jd_text = st.text_area("Paste Job Description", value=st.session_state.jd_text,
                               height=300, placeholder="Paste the full job description here...",
                               label_visibility="collapsed")
        if jd_text != st.session_state.jd_text:
            st.session_state.jd_text = jd_text
            st.session_state.jd_analysis = None

        if not st.session_state.resume_text:
            alert("⚠ Upload/paste your resume in the Resume Analyzer first.", "warning")

        if st.button("🔍 Analyze JD Match", use_container_width=True):
            if not jd_text.strip():
                alert("Please paste a job description.", "warning")
            elif not st.session_state.resume_text:
                alert("Please add your resume in the Resume Analyzer first.", "warning")
            else:
                with st.spinner("Comparing resume vs job description..."):
                    sys_p = """You are an ATS system and senior HR tech specialist.
Compare the resume against the job description and return ONLY valid JSON:
{
  "match_percentage": 65,
  "match_level": "Strong|Good|Moderate|Weak",
  "match_summary": "2 sentence summary of fit",
  "keywords_present": ["kw1","kw2","kw3","kw4","kw5"],
  "keywords_missing": ["kw1","kw2","kw3","kw4","kw5","kw6"],
  "skills_match": [{"skill":"skill name","status":"present|missing|partial","importance":"must-have|nice-to-have"}],
  "experience_match": "detailed assessment of experience alignment",
  "education_match": "education requirement match assessment",
  "tailoring_suggestions": ["specific suggestion 1","specific suggestion 2","specific suggestion 3","specific suggestion 4"],
  "headline_suggestion": "tailored resume headline for this JD",
  "summary_rewrite": "rewritten resume summary tailored to this job",
  "cover_letter_angle": "best angle/hook for cover letter",
  "red_flags": ["potential concern 1","potential concern 2"],
  "strengths_for_role": ["strength 1","strength 2","strength 3"],
  "ats_score_for_jd": 0
}"""
                    usr_p = f"Resume:\n{st.session_state.resume_text[:3000]}\n\nJob Description:\n{jd_text[:2000]}"
                    try:
                        raw = call_ai(sys_p, usr_p, max_tokens=2000)
                        result = parse_json(raw)
                        st.session_state.jd_analysis = result
                        alert("✓ JD match analysis complete!", "success")
                    except Exception as e:
                        alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        jd = st.session_state.jd_analysis
        if jd:
            match_pct = jd.get("match_percentage", 0)
            match_color = score_color(match_pct)
            match_level = jd.get("match_level", "Moderate")

            st.markdown(f"""
            <div class="hero-score">
            <div style="font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;color:{match_color}">{match_pct}%</div>
            <div class="score-label">Resume–JD Match</div>
            {progress_bar(match_pct, 'green' if match_pct >= 70 else ('amber' if match_pct >= 50 else 'red'))}
            <div style="margin-top:0.5rem;font-size:0.85rem;color:{match_color};font-weight:600">{match_level} Match</div>
            {"<div style='margin-top:0.5rem;font-size:0.82rem;color:#9090b0;line-height:1.5'>"+jd.get('match_summary','')+"</div>" if jd.get('match_summary') else ""}
            </div>
            """, unsafe_allow_html=True)

            t1, t2, t3 = st.tabs(["Keywords", "Suggestions", "Cover Letter"])

            with t1:
                kp_col, km_col = st.columns(2)
                with kp_col:
                    section_title("Keywords Present ✓")
                    st.markdown(tag_html(jd.get("keywords_present", []), "green"), unsafe_allow_html=True)
                with km_col:
                    section_title("Keywords Missing ✗")
                    st.markdown(tag_html(jd.get("keywords_missing", []), "red"), unsafe_allow_html=True)

                if jd.get("skills_match"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    section_title("Skills Breakdown")
                    for sm in jd["skills_match"]:
                        status = sm.get("status", "missing")
                        s_cls = {"present": "green", "missing": "red", "partial": "amber"}.get(status, "amber")
                        importance = sm.get("importance", "nice-to-have")
                        st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)"><span class="tag-{s_cls}">{status}</span><span style="font-size:0.83rem;color:#d0d0f0">{sm.get("skill","")}</span><span style="font-size:0.7rem;color:#5050a0;margin-left:auto">{importance}</span></div>', unsafe_allow_html=True)

                if jd.get("red_flags"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    section_title("⚠ Potential Concerns")
                    for flag in jd["red_flags"]:
                        alert(flag, "warning")

            with t2:
                if jd.get("headline_suggestion"):
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    section_title("✨ Tailored Resume Headline")
                    st.markdown(f'<div style="font-size:0.9rem;color:#a78bfa;font-style:italic;font-weight:500">{jd["headline_suggestion"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                if jd.get("summary_rewrite"):
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    section_title("✨ Rewritten Summary (JD-Tailored)")
                    st.markdown(f'<div class="alert-info" style="font-style:italic">{jd["summary_rewrite"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                section_title("Tailoring Suggestions")
                for i, sug in enumerate(jd.get("tailoring_suggestions", [])):
                    st.markdown(f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)"><span style="color:#38bdf8;font-weight:700;flex-shrink:0">{i+1}</span><div style="font-size:0.85rem;color:#d0d0f0">{sug}</div></div>', unsafe_allow_html=True)

                if jd.get("strengths_for_role"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    section_title("Your Strengths for This Role")
                    for s in jd["strengths_for_role"]:
                        st.markdown(f'<div style="font-size:0.83rem;color:#34d399;padding:4px 0">✓ {s}</div>', unsafe_allow_html=True)

            with t3:
                if jd.get("cover_letter_angle"):
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    section_title("Cover Letter Angle / Hook")
                    st.markdown(f'<div style="font-size:0.9rem;color:#d0d0f0;line-height:1.7">{jd["cover_letter_angle"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                if st.button("✉ Generate Full Cover Letter", use_container_width=True):
                    with st.spinner("Generating cover letter..."):
                        try:
                            cl = call_ai(
                                "You are an expert cover letter writer. Write a compelling, specific, professional cover letter. 3-4 paragraphs. Do NOT use placeholders like [Company Name] - use 'the company' if needed.",
                                f"Role: {st.session_state.target_role}\nJD angle: {jd.get('cover_letter_angle','')}\nCandidate strengths: {', '.join(jd.get('strengths_for_role',[]))}\nResume summary: {st.session_state.resume_text[:1000]}",
                                max_tokens=800
                            )
                            st.text_area("Generated Cover Letter", value=cl, height=350, key="cl_output")
                        except Exception as e:
                            alert(f"Error: {e}", "error")
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 1.5rem">
            <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◍</div>
            <div style="color:#5050a0;font-size:0.9rem">Paste a job description and click Analyze<br>to see your resume match score and tailoring suggestions.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LINKEDIN OPTIMIZER (NEW)
# ══════════════════════════════════════════════════════════════════════════════
def page_linkedin():
    st.markdown("## ◑ LinkedIn Profile Optimizer")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">AI-generated LinkedIn headline, about section, experience bullets, and profile summary</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Your Profile Context")
        role = st.text_input("Target Role / Headline", value=st.session_state.target_role, key="li_role")
        skills_input = st.text_input("Top Skills (comma-separated)",
                                     value=st.session_state.current_skills[:100] if st.session_state.current_skills else "",
                                     placeholder="Python, ML, React, Product Management...")
        tone = st.selectbox("Profile Tone", ["Professional & Authoritative", "Approachable & Collaborative",
                                              "Technical & Data-driven", "Creative & Innovative",
                                              "Entrepreneurial & Ambitious"])
        years_exp = st.text_input("Years of experience", placeholder="e.g. 4 years")
        top_achievement = st.text_area("Top career achievement",
                                       placeholder="e.g. Led migration to microservices, reducing latency by 60%...",
                                       height=80)

        if st.button("✨ Generate LinkedIn Profile", use_container_width=True):
            with st.spinner("Crafting your LinkedIn profile..."):
                resume_ctx = f"\nResume context:\n{st.session_state.resume_text[:2000]}" if st.session_state.resume_text else ""
                sys_p = """You are a LinkedIn optimization expert who has helped 500+ professionals land jobs at top companies.
Return ONLY valid JSON, no markdown:
{
  "headline_options": ["headline 1 (max 220 chars)","headline 2 — different angle","headline 3 — keyword-focused"],
  "about_section": "Full LinkedIn About section — 3-4 paragraphs, engaging, keyword-rich, first-person, ends with call to action",
  "open_to_work": "Recommended Open to Work settings text",
  "experience_bullets": ["improved bullet 1 with metrics","improved bullet 2 with impact","improved bullet 3"],
  "skills_to_add": ["skill1","skill2","skill3","skill4","skill5"],
  "featured_section_idea": "What to put in the Featured section",
  "connection_request_template": "Short personalized connection request template",
  "optimization_tips": ["tip 1","tip 2","tip 3","tip 4"]
}"""
                usr_p = f"Role: {role}\nSkills: {skills_input}\nTone: {tone}\nExperience: {years_exp}\nTop achievement: {top_achievement}{resume_ctx}"
                try:
                    raw = call_ai(sys_p, usr_p, max_tokens=1800)
                    result = parse_json(raw)
                    st.session_state.linkedin_profile = result
                    alert("✓ LinkedIn profile generated!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        lp = st.session_state.linkedin_profile
        if lp:
            st.markdown('<div class="linkedin-card">', unsafe_allow_html=True)
            section_title("✨ Headline Options")
            for i, h in enumerate(lp.get("headline_options", [])):
                st.markdown(f'<div style="padding:8px 12px;margin-bottom:6px;background:rgba(10,102,194,0.1);border:1px solid rgba(10,102,194,0.2);border-radius:8px;font-size:0.88rem;color:#eeeeff"><span style="color:#5050a0;font-size:0.7rem">Option {i+1}:</span><br>{h}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if lp.get("about_section"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("About Section")
                st.text_area("Copy this to LinkedIn", value=lp["about_section"],
                             height=250, key="li_about")
                st.markdown('</div>', unsafe_allow_html=True)

            if lp.get("skills_to_add"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Skills to Add to Profile")
                st.markdown(tag_html(lp["skills_to_add"], "teal"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if lp.get("experience_bullets"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Improved Experience Bullets")
                for b in lp["experience_bullets"]:
                    st.markdown(f'<div style="font-size:0.83rem;color:#34d399;padding:4px 0">✓ {b}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if lp.get("featured_section_idea") or lp.get("connection_request_template"):
                fa, fb = st.columns(2)
                with fa:
                    if lp.get("featured_section_idea"):
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        section_title("Featured Section")
                        st.markdown(f'<div style="font-size:0.85rem;color:#d0d0f0">{lp["featured_section_idea"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                with fb:
                    if lp.get("connection_request_template"):
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        section_title("Connection Request Template")
                        st.markdown(f'<div style="font-size:0.82rem;color:#9090b0;font-style:italic">{lp["connection_request_template"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

            if lp.get("optimization_tips"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Optimization Tips")
                for tip in lp["optimization_tips"]:
                    alert(f"💡 {tip}", "info")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 1.5rem">
            <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◑</div>
            <div style="color:#5050a0;font-size:0.9rem">Fill in your profile context<br>and generate AI-optimized LinkedIn content.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT GENERATOR (NEW)
# ══════════════════════════════════════════════════════════════════════════════
def page_projects():
    st.markdown("## ◒ AI Project Generator")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Generate real-world portfolio projects based on your skill gaps and target role</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Project Preferences")
        role = st.text_input("Target Role", value=st.session_state.target_role, key="pj_role")
        current_skills = st.text_input("Your Current Skills",
                                       value=st.session_state.current_skills or "",
                                       placeholder="React, JavaScript, Python...")
        an = st.session_state.resume_analysis
        missing_skills_default = ", ".join(an.get("missing_skills", [])[:6]) if an else ""
        missing_skills = st.text_input("Skills to Practice (from gap analysis)",
                                       value=missing_skills_default,
                                       placeholder="TypeScript, Testing, Docker...")
        proj_count = st.selectbox("Number of Projects", [3, 5, 7])
        difficulty = st.selectbox("Project Difficulty", ["Beginner", "Intermediate", "Advanced", "Mixed"])
        proj_type = st.multiselect("Project Types",
                                   ["Web App", "API", "CLI Tool", "Data Pipeline", "ML Project",
                                    "Mobile App", "DevOps/Infrastructure", "Open Source Contribution"],
                                   default=["Web App", "API"])

        if st.button("🚀 Generate Project Ideas", use_container_width=True):
            with st.spinner("Generating portfolio-worthy project ideas..."):
                sys_p = f"""You are a senior software engineer and career coach who helps candidates build impressive portfolios.
Generate {proj_count} {difficulty} project ideas for someone targeting: {role}.
Return ONLY valid JSON array, no markdown:
[{{
  "title": "Project Name",
  "tagline": "one sentence elevator pitch",
  "description": "2-3 sentence detailed description of what to build",
  "skills_practiced": ["skill1","skill2","skill3"],
  "tech_stack": ["tech1","tech2","tech3"],
  "difficulty": "Beginner|Intermediate|Advanced",
  "estimated_hours": 20,
  "key_features": ["feature 1","feature 2","feature 3","feature 4"],
  "stretch_goals": ["stretch 1","stretch 2"],
  "resume_bullet": "How to describe this on a resume with metrics",
  "interview_talking_points": ["point 1","point 2"],
  "github_readme_hook": "First paragraph of README to attract attention",
  "employer_appeal": "Why employers in target role will be impressed by this"
}}]"""
                usr_p = f"Role: {role}\nCurrent skills: {current_skills}\nSkills to practice: {missing_skills}\nProject types: {', '.join(proj_type)}"
                try:
                    raw = call_ai(sys_p, usr_p, max_tokens=2500)
                    result = parse_json(raw)
                    st.session_state.projects_generated = result
                    alert(f"✓ {len(result)} project ideas generated!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        projects = st.session_state.projects_generated
        if projects:
            for i, proj in enumerate(projects):
                diff = proj.get("difficulty", "Intermediate")
                dc = {"Beginner": "green", "Intermediate": "amber", "Advanced": "red"}.get(diff, "amber")
                st.markdown(f'<div class="project-card">', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem">
                  <div>
                    <div style="font-size:1rem;font-weight:600;color:#eeeeff;font-family:'Syne',sans-serif">{proj.get("title","Project")}</div>
                    <div style="font-size:0.8rem;color:#5050a0;font-style:italic;margin-top:2px">{proj.get("tagline","")}</div>
                  </div>
                  <div style="display:flex;gap:6px;flex-shrink:0">
                    <span class="tag-{dc}">{diff}</span>
                    <span class="tag-teal">~{proj.get("estimated_hours",20)}h</span>
                  </div>
                </div>
                <div style="font-size:0.83rem;color:#9090b0;line-height:1.6;margin-bottom:0.75rem">{proj.get("description","")}</div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    section_title("Tech Stack")
                    st.markdown(tag_html(proj.get("tech_stack", []), "purple"), unsafe_allow_html=True)
                with c2:
                    section_title("Skills Practiced")
                    st.markdown(tag_html(proj.get("skills_practiced", []), "teal"), unsafe_allow_html=True)

                with st.expander(f"📋 Full Details — {proj.get('title','')}"):
                    if proj.get("key_features"):
                        section_title("Key Features to Build")
                        for f in proj["key_features"]:
                            st.markdown(f'<div style="font-size:0.82rem;color:#9090b0;padding:3px 0">◎ {f}</div>', unsafe_allow_html=True)
                    if proj.get("stretch_goals"):
                        st.markdown("<br>", unsafe_allow_html=True)
                        section_title("Stretch Goals")
                        for sg in proj["stretch_goals"]:
                            st.markdown(f'<div style="font-size:0.82rem;color:#5050a0;padding:3px 0">⊕ {sg}</div>', unsafe_allow_html=True)
                    if proj.get("resume_bullet"):
                        st.markdown("<br>", unsafe_allow_html=True)
                        section_title("Resume Bullet")
                        st.markdown(f'<div class="alert-success" style="font-size:0.82rem">{proj["resume_bullet"]}</div>', unsafe_allow_html=True)
                    if proj.get("employer_appeal"):
                        alert(f"💼 Employer Appeal: {proj['employer_appeal']}", "info")
                    if proj.get("github_readme_hook"):
                        section_title("GitHub README Hook")
                        st.markdown(f'<div style="font-size:0.82rem;color:#9090b0;font-style:italic;padding:0.5rem;background:rgba(0,0,0,0.2);border-radius:6px">{proj["github_readme_hook"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 1.5rem">
            <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◒</div>
            <div style="color:#5050a0;font-size:0.9rem">Set your preferences and generate<br>portfolio-worthy project ideas.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SALARY INTELLIGENCE (NEW)
# ══════════════════════════════════════════════════════════════════════════════
def page_salary():
    st.markdown("## ◓ Salary Intelligence Engine")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">AI-powered salary estimation, negotiation strategies, and market intelligence</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Your Profile")
        role = st.text_input("Target Role", value=st.session_state.target_role, key="sal_role")
        skills = st.text_input("Top Skills", value=st.session_state.current_skills or "", placeholder="Python, React, ML...")
        years_exp = st.selectbox("Years of Experience",
                                 ["0-1 year", "1-2 years", "2-4 years", "4-6 years", "6-10 years", "10+ years"])
        location = st.text_input("Location (City/Remote)", placeholder="San Francisco, CA / Remote / London, UK")
        company_size = st.selectbox("Target Company Size",
                                    ["Startup (<50)", "Mid-size (50-500)", "Large (500-5000)", "Enterprise (5000+)", "FAANG/Big Tech"])
        education = st.selectbox("Highest Education",
                                 ["High School", "Associate's", "Bachelor's", "Master's", "PhD", "Self-taught/Bootcamp"])

        if st.button("💰 Estimate My Salary", use_container_width=True):
            with st.spinner("Analyzing market data..."):
                sys_p = """You are a senior compensation analyst with access to market data from Levels.fyi, Glassdoor, and LinkedIn Salary.
Return ONLY valid JSON, no markdown:
{
  "base_salary_range": {"min": 80000, "max": 120000, "median": 95000, "currency": "USD"},
  "total_comp_range": {"min": 90000, "max": 150000, "median": 115000},
  "equity_typical": "description of typical equity package",
  "signing_bonus": "typical signing bonus range",
  "confidence": "High|Medium|Low",
  "factors_positive": ["factor boosting pay 1","factor 2","factor 3"],
  "factors_negative": ["factor lowering pay 1","factor 2"],
  "negotiation_strategy": "3-4 sentence negotiation approach",
  "negotiation_tips": ["tip 1","tip 2","tip 3","tip 4"],
  "market_demand": "High|Medium|Low",
  "growth_trajectory": "expected salary growth in 2-3 years",
  "top_paying_companies": ["company 1","company 2","company 3","company 4"],
  "alternative_roles_salary": [{"role":"role name","range":"$X-$Y"}],
  "skills_for_premium": ["skill that adds $X","skill 2","skill 3"]
}"""
                usr_p = f"Role: {role}\nSkills: {skills}\nExperience: {years_exp}\nLocation: {location}\nCompany size: {company_size}\nEducation: {education}"
                try:
                    raw = call_ai(sys_p, usr_p, max_tokens=1200)
                    result = parse_json(raw)
                    st.session_state.salary_data = result
                    alert("✓ Salary analysis complete!", "success")
                except Exception as e:
                    alert(f"Error: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        sd = st.session_state.salary_data
        if sd:
            base = sd.get("base_salary_range", {})
            total = sd.get("total_comp_range", {})

            # Salary cards
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="salary-card">
                <div class="section-title">Base Salary Range</div>
                <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#34d399">${base.get('min',0):,} – ${base.get('max',0):,}</div>
                <div style="font-size:0.8rem;color:#5050a0;margin-top:0.3rem">Median: ${base.get('median',0):,} {base.get('currency','USD')}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="salary-card" style="border-color:rgba(108,99,255,0.3);background:linear-gradient(135deg,rgba(108,99,255,0.08),rgba(108,99,255,0.04))">
                <div class="section-title">Total Compensation</div>
                <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#a78bfa">${total.get('min',0):,} – ${total.get('max',0):,}</div>
                <div style="font-size:0.8rem;color:#5050a0;margin-top:0.3rem">Incl. equity, bonuses</div>
                </div>
                """, unsafe_allow_html=True)

            if sd.get("equity_typical") or sd.get("signing_bonus"):
                e1, e2 = st.columns(2)
                with e1:
                    if sd.get("equity_typical"):
                        st.markdown(f'<div class="glass-card" style="padding:0.9rem"><div class="section-title">Equity Package</div><div style="font-size:0.83rem;color:#d0d0f0">{sd["equity_typical"]}</div></div>', unsafe_allow_html=True)
                with e2:
                    if sd.get("signing_bonus"):
                        st.markdown(f'<div class="glass-card" style="padding:0.9rem"><div class="section-title">Signing Bonus</div><div style="font-size:0.83rem;color:#d0d0f0">{sd["signing_bonus"]}</div></div>', unsafe_allow_html=True)

            if sd.get("factors_positive") or sd.get("factors_negative"):
                fp, fn = st.columns(2)
                with fp:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    section_title("Factors Boosting Pay")
                    for f in sd.get("factors_positive", []):
                        st.markdown(f'<div style="font-size:0.82rem;color:#34d399;padding:3px 0">↑ {f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with fn:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    section_title("Factors Lowering Pay")
                    for f in sd.get("factors_negative", []):
                        st.markdown(f'<div style="font-size:0.82rem;color:#f87171;padding:3px 0">↓ {f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            if sd.get("negotiation_strategy"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("💬 Negotiation Strategy")
                st.markdown(f'<div style="font-size:0.87rem;color:#d0d0f0;line-height:1.7;margin-bottom:0.75rem">{sd["negotiation_strategy"]}</div>', unsafe_allow_html=True)
                for tip in sd.get("negotiation_tips", []):
                    st.markdown(f'<div style="font-size:0.82rem;color:#fbbf24;padding:4px 0">⚡ {tip}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if sd.get("skills_for_premium"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Skills That Command Premium Salary")
                st.markdown(tag_html(sd["skills_for_premium"], "amber"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if sd.get("top_paying_companies"):
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Top-Paying Companies to Target")
                st.markdown(tag_html(sd["top_paying_companies"], "green"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:3rem 1.5rem">
            <div style="font-size:3rem;opacity:0.15;margin-bottom:1rem">◓</div>
            <div style="color:#5050a0;font-size:0.9rem">Fill in your profile and estimate<br>your market salary range.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT & REPORTS
# ══════════════════════════════════════════════════════════════════════════════
def page_export():
    st.markdown("## ⊞ Export & Reports")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">Download your full analysis, roadmap, interview prep, and career report</div>', unsafe_allow_html=True)

    an = st.session_state.resume_analysis
    rm = st.session_state.roadmap
    iq = st.session_state.interview_questions
    jd = st.session_state.jd_analysis
    lp = st.session_state.linkedin_profile
    sd = st.session_state.salary_data

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Full Analysis Package (JSON)")
        full_package = {
            "generated": datetime.now().isoformat(),
            "target_role": st.session_state.target_role,
            "resume_analysis": an,
            "skill_gap": st.session_state.skill_gap,
            "roadmap": rm,
            "interview_questions": iq,
            "jd_analysis": jd,
            "linkedin_profile": lp,
            "salary_data": sd,
        }
        st.download_button(
            "⬇ Download Full Package (JSON)",
            data=json.dumps(full_package, indent=2, default=str),
            file_name=f"nexus_career_package_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json", use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if rm:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Roadmap Export (TXT)")
            lines = [f"Nexus AI — Learning Roadmap\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\nTarget: {st.session_state.target_role}\n{'='*50}"]
            for w in rm:
                lines.append(f"\nWeek {w.get('week','')} — {w.get('title','')}")
                if w.get("objective"): lines.append(f"Goal: {w['objective']}")
                for t in w.get("tasks", []): lines.append(f"  - {t}")
                if w.get("resources"):
                    for r in w.get("resources", []): lines.append(f"  📚 {r}")
                if w.get("project"): lines.append(f"  🚀 Project: {w['project']}")
                if w.get("checkpoint"): lines.append(f"  ✓ Checkpoint: {w['checkpoint']}")
            st.download_button(
                "⬇ Download Roadmap (TXT)",
                data="\n".join(lines),
                file_name=f"nexus_roadmap_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if an:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Career Intelligence Report (TXT)")
            sc = st.session_state.dashboard_scores
            ci = an.get("career_insights", {})
            lines = [
                "Nexus AI — Career Intelligence Report",
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                f"Candidate: {an.get('candidate_name', 'Unknown')}",
                f"Target Role: {st.session_state.target_role}",
                f"Analyzed by: {st.session_state.active_provider}",
                "=" * 60,
                f"\nSCORES",
                f"Resume Score: {sc['resume_score']}/100",
                f"ATS Score: {sc['ats_score']}/100",
                f"Role Match: {sc.get('role_match', 0)}%",
                f"Career Readiness: {sc.get('career_readiness', 0)}/100",
                f"\nEXECUTIVE SUMMARY\n{an.get('executive_summary', '')}",
                "\nSTRENGTHS",
            ]
            for s in an.get("strengths", []): lines.append(f"  + {s}")
            lines.append("\nWEAKNESSES")
            for w in an.get("weaknesses", []): lines.append(f"  - {w}")
            lines.append(f"\nMISSING SKILLS\n  " + ", ".join(an.get("missing_skills", [])))
            if ci:
                lines += ["\nCAREER INSIGHTS",
                          f"  Diagnosis: {ci.get('one_line_diagnosis', '')}",
                          f"  Biggest Strength: {ci.get('biggest_strength', '')}",
                          f"  Biggest Risk: {ci.get('biggest_risk', '')}",
                          f"  Quickest Win: {ci.get('quickest_win', '')}",
                          f"  Next Best Action: {ci.get('next_best_action', '')}",
                          f"  Salary Range: {ci.get('salary_range', '')}",
                          f"  Job Ready: {ci.get('job_ready', False)}"]
            if sd:
                base = sd.get("base_salary_range", {})
                lines += [f"\nSALARY ESTIMATE",
                          f"  Base: ${base.get('min',0):,} - ${base.get('max',0):,}",
                          f"  Negotiation: {sd.get('negotiation_strategy','')}"]
            st.download_button(
                "⬇ Download Career Report (TXT)",
                data="\n".join(lines),
                file_name=f"nexus_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if iq:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Interview Prep Export (TXT)")
            lines = [f"Nexus AI — Interview Prep\nRole: {st.session_state.target_role}\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n{'='*50}"]
            for i, q in enumerate(iq):
                lines.append(f"\nQ{i+1} [{q.get('difficulty','')}] [{q.get('type','')}]")
                lines.append(f"Question: {q.get('question','')}")
                lines.append(f"Strategy: {q.get('answer_strategy','')}")
                lines.append(f"Hint: {q.get('hint','')}")
                if q.get("good_answer_points"):
                    lines.append("Key Points:")
                    for p in q["good_answer_points"]: lines.append(f"  - {p}")
                if q.get("common_mistake"): lines.append(f"Common Mistake: {q['common_mistake']}")
            st.download_button(
                "⬇ Download Interview Prep (TXT)",
                data="\n".join(lines),
                file_name=f"nexus_interview_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    if an:
        with st.expander("🔍 View Raw Analysis JSON"):
            st.json(an)


# ══════════════════════════════════════════════════════════════════════════════
# DEBUG PANEL
# ══════════════════════════════════════════════════════════════════════════════
def page_debug():
    st.markdown("## ⊟ Debug Panel")
    st.markdown('<div style="color:#5050a0;font-size:0.85rem;margin-bottom:1.5rem">System diagnostics, API call log, token usage, and session state inspector</div>', unsafe_allow_html=True)

    # System status
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("pdfplumber", "✓" if PDFPLUMBER_AVAILABLE else "✗")
    c2.metric("PyPDF2", "✓" if PYPDF2_AVAILABLE else "✗")
    c3.metric("OCR (tesseract)", "✓" if OCR_AVAILABLE else "✗")
    c4.metric("Plotly", "✓" if PLOTLY_AVAILABLE else "✗")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("OpenAI/Groq SDK", "✓" if OPENAI_AVAILABLE else "✗")
    c6.metric("Gemini SDK", "✓" if GEMINI_AVAILABLE else "✗")
    c7.metric("python-docx", "✓" if DOCX_AVAILABLE else "✗")
    c8.metric("Active Provider", st.session_state.active_provider or "None")

    st.markdown("---")
    section_title("API Call Log (Last 20)")
    debug_log = st.session_state.debug_log
    if debug_log:
        for entry in debug_log:
            ok_icon = "✓" if entry.get("ok") else "✗"
            ok_color = "#34d399" if entry.get("ok") else "#f87171"
            st.markdown(f"""
            <div class="debug-panel">
              <span style="color:{ok_color}">{ok_icon}</span>
              <span style="color:#a78bfa">[{entry.get('ts','')}]</span>
              <span style="color:#eeeeff"> {entry.get('provider','')}</span>
              <span style="color:#5050a0"> · {entry.get('latency_ms',0)}ms</span>
              <span style="color:#5050a0"> · ~{entry.get('tokens_est',0)} tokens</span>
              {f'<span style="color:#f87171"> · {entry.get("error","")[:80]}</span>' if entry.get('error') else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        alert("No API calls logged yet. Run an analysis to see logs.", "info")

    st.markdown("---")
    section_title("Session State Inspector")
    with st.expander("Resume Analysis Data"):
        if st.session_state.resume_analysis:
            st.json(st.session_state.resume_analysis)
        else:
            st.write("No analysis yet.")

    with st.expander("Structured Resume Model"):
        if st.session_state.structured_resume:
            st.json(st.session_state.structured_resume)
        else:
            st.write("No structured resume yet.")

    with st.expander("Dashboard Scores"):
        st.json(st.session_state.dashboard_scores)

    with st.expander("Extraction Meta"):
        if st.session_state.extraction_meta:
            st.json(st.session_state.extraction_meta)

    if st.button("🗑 Clear All Session Data", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page_map = {
    "◈  Dashboard":              page_dashboard,
    "◉  Resume Analyzer":        page_resume,
    "◐  Skill Gap Analysis":     page_skillgap,
    "◳  Learning Roadmap":       page_roadmap,
    "◫  AI Career Coach":        page_chat,
    "◬  Interview Prep":         page_interview,
    "◆  Career Insights":        page_insights,
    "◍  JD Matcher":             page_jd_matcher,
    "◑  LinkedIn Optimizer":     page_linkedin,
    "◒  Project Generator":      page_projects,
    "◓  Salary Intelligence":    page_salary,
    "⊞  Export & Reports":       page_export,
    "⊟  Debug Panel":            page_debug,
}

page_map[page]()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#252540;font-size:0.7rem;padding:1rem 0;border-top:1px solid rgba(108,99,255,0.08)">
  Nexus AI Career OS v4 · Multi-stage AI pipeline · Groq · OpenAI · Gemini · Built with Streamlit
</div>
""", unsafe_allow_html=True)