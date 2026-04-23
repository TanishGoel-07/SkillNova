# CareerLens AI

**An AI-powered career intelligence dashboard built with Streamlit**  
Analyze resumes, detect skill gaps, generate personalized learning roadmaps, and guide users toward better career decisions with interactive analytics and AI-driven insights.

---

## Overview

CareerLens AI is a smart career growth platform designed to function like a personal career mentor. It helps users understand their current profile, compare it against a target role, identify missing skills, and receive actionable recommendations to improve their employability.

This project is built as a **single-file Streamlit application** with a modern UI, strong visualizations, and deeply integrated AI features. It is ideal for students, job seekers, career switchers, and professionals who want a clear path toward their next role.

---

## Why This Project Exists

Many people have resumes, skills, and experience, but they do not know:

- how good their resume actually is
- what skills are missing for their dream role
- what they should learn next
- whether they are interview-ready
- how to structure a career roadmap

CareerLens AI solves this by combining:
- resume parsing
- AI analysis
- skill gap detection
- roadmap generation
- interview preparation
- dashboard-based progress tracking

---

## Key Features

### Resume Analyzer
Upload a resume in PDF or DOCX format and let the app extract meaningful information from it.

The analyzer can:
- parse resume text
- identify skills, experience, education, and projects
- score the resume
- estimate ATS compatibility
- highlight strengths and weaknesses
- suggest improvements in plain language

### Skill Gap Analysis
Compare the user’s current skills against a target job role.

The system can:
- detect missing skills
- show priority skills
- classify skills into categories such as must-have, good-to-have, and optional
- visualize gaps using charts and graphs

### Learning Roadmap Generator
Generate a personalized learning plan based on the user’s target role and current knowledge level.

The roadmap includes:
- weekly learning goals
- daily or task-based actions
- project suggestions
- progress tracking
- adaptive recommendations

### AI Career Coach
A built-in AI assistant helps users make career decisions.

It can answer questions like:
- What should I learn next?
- Am I ready for this role?
- How can I improve my resume?
- Which projects should I build?
- What should I focus on this week?

### Interview Preparation
The app generates interview practice content for the selected role.

It can create:
- technical questions
- behavioral questions
- situational questions
- role-specific practice prompts

### Interactive Dashboard
A visual dashboard brings everything together in one place.

It includes:
- resume score
- ATS score
- skill match score
- skill gap percentage
- roadmap progress
- charts and visual summaries

---

## Core Use Cases

CareerLens AI is useful for:

- students preparing for their first job
- fresh graduates trying to improve their resume
- professionals switching careers
- job seekers targeting a specific role
- learners planning upskilling journeys
- career coaches reviewing candidate progress

---

## Tech Stack

### Frontend / App Framework
- Streamlit

### AI Integration
- OpenAI API

### Data Handling
- Pandas

### Visualizations
- Plotly

### Resume Parsing
- PyPDF2 or pdfplumber
- python-docx

### Optional Utilities
- dotenv for environment variables
- JSON for structured AI responses

---

## Project Highlights

- Single-file Streamlit application
- Clean, modern, and visually rich UI
- Sidebar navigation
- AI-powered career insights
- Fully interactive dashboard
- Resume upload and parsing support
- Personalized career roadmap generation
- Skill gap visualization
- Interview preparation module
- Chat-based AI career assistant
- Designed for easy expansion into a larger platform

---

## UI / UX Design Goals

The app is designed to feel:
- modern
- premium
- clean
- friendly
- easy to understand
- visually informative

Design choices include:
- dark theme style
- gradient accents
- rounded cards
- glassmorphism-inspired containers
- strong spacing and hierarchy
- readable typography
- clear visual feedback
- responsive dashboard layouts

---

## Application Flow

1. The user opens the dashboard.
2. The user uploads a resume.
3. The app extracts resume content.
4. AI analyzes the resume and generates a score.
5. The app compares the profile with a target role.
6. Skill gaps are identified and visualized.
7. A personalized learning roadmap is generated.
8. The user can chat with the AI career coach.
9. The user can review interview questions and progress over time.

---

## Main Sections of the App

### 1. Dashboard
A summary view with key scores, charts, and performance indicators.

### 2. Resume Analyzer
Uploads and analyzes resume content.

### 3. Skill Gap Analysis
Compares current skills with target role requirements.

### 4. Learning Roadmap
Shows a personalized learning journey.

### 5. AI Career Coach
A conversational assistant for career guidance.

### 6. Interview Prep
Generates role-specific interview practice content.

---

## Example AI Outputs

### Resume Analysis
```json
{
  "score": 82,
  "ats_score": 76,
  "strengths": [
    "Strong project section",
    "Clear education background"
  ],
  "weaknesses": [
    "Missing measurable achievements",
    "Some ATS keywords are absent"
  ],
  "improvements": [
    "Add impact-focused bullet points",
    "Include more role-specific keywords"
  ]
}
Skill Gap Analysis
{
  "missing_skills": [
    "Python",
    "SQL",
    "Data Visualization"
  ],
  "important_skills": [
    "Problem Solving",
    "Communication"
  ],
  "optional_skills": [
    "Cloud Basics",
    "Version Control"
  ]
}
Roadmap
{
  "weeks": [
    {
      "week": 1,
      "tasks": [
        "Learn fundamentals",
        "Review resume keywords",
        "Complete beginner project"
      ]
    }
  ]
}
Installation
1. Clone the Repository
git clone https://github.com/your-username/careerlens-ai.git
cd careerlens-ai
2. Create a Virtual Environment
python -m venv venv
3. Activate the Environment
On Windows
venv\Scripts\activate
On macOS/Linux
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key

If needed, you can also include additional configuration values such as:

MODEL_NAME=gpt-4.1
STREAMLIT_SERVER_PORT=8501
Running the App

Start the application with:

streamlit run app.py

Then open the local URL shown in the terminal, usually:

http://localhost:8501
Recommended File Structure
careerlens-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
└── assets/
    └── screenshots/

If the project later expands, you can organize it into:

careerlens-ai/
│
├── app.py
├── utils/
├── prompts/
├── components/
├── assets/
├── requirements.txt
└── README.md
Suggested Dependencies
streamlit
openai
pandas
plotly
PyPDF2
python-docx
python-dotenv

You may also use:

pdfplumber
numpy
matplotlib
How the AI Is Used

CareerLens AI uses AI across multiple parts of the product:

1. Resume Understanding

Extracts and structures information from uploaded resumes.

2. Resume Scoring

Evaluates quality, clarity, keyword strength, and ATS friendliness.

3. Skill Comparison

Compares extracted skills with the target role.

4. Roadmap Generation

Produces a tailored learning path based on gaps and goals.

5. Career Coaching

Provides contextual advice through chat.

6. Interview Preparation

Generates useful questions and guidance based on role.

Visualization Ideas Used in the Dashboard

The app can include:

radar charts for skill balance
bar charts for skill gaps
progress rings for roadmap completion
line charts for improvement over time
score cards for resume and ATS results
categorized charts for skill priorities

These visualizations make the app easier to understand and more engaging.

Future Enhancements

This project can be extended with:

user authentication
database persistence
profile history tracking
downloadable PDF reports
job recommendation engine
LinkedIn profile import
multi-user support
recruiter dashboard
deployment to Streamlit Cloud or AWS
mobile-friendly improvements
richer AI memory and user personalization
Development Goals

This project is meant to be:

useful
visually impressive
easy to demonstrate
AI-driven
portfolio-ready
expandable into a production product
Contribution Guidelines

Contributions are welcome.

To contribute:
Fork the repository
Create a feature branch
Make your changes
Test the app
Submit a pull request

Example:

git checkout -b feature-new-dashboard
git add .
git commit -m "Add new dashboard improvements"
git push origin feature-new-dashboard
License

This project is licensed under the MIT License.

Acknowledgements

This project was inspired by the need for smarter, more personalized career guidance tools that combine AI, analytics, and beautiful user interfaces in one place.

Final Vision

CareerLens AI is more than a dashboard. It is a career intelligence system that helps users discover where they stand, understand what they need to learn, and move forward with confidence.

It turns a resume into insight, insight into action, and action into career progress.
