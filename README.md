# GapForge

> **AI-powered career gap analysis and project roadmap generator.**
> Upload your resume (or enter your profile manually), pick a target company, and get a personalized shortlist of portfolio projects that close your skill gaps, complete with a step-by-step execution roadmap.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)

---

## Overview

GapForge is a full-stack AI agent that takes your resume and a target company, then runs a multi-stage LangGraph pipeline to:

1. Parse your profile
2. Research the target company's benchmark skills
3. Identify your skill gaps
4. Generate, filter, and rank portfolio project ideas
5. Produce a deep execution roadmap for your chosen project

The user can refine the shortlist with natural-language feedback before committing to a final project.

---

## Features

- **Resume Upload** - Supports PDF parsing directly from your resume
- **Manual Profile Entry** - No resume? Enter your skills and experience manually
- **Target Company Research** - Benchmarks against real company skill expectations
- **Skill Gap Analysis** - Identifies missing skills ranked by impact
- **AI Idea Generation** - Creates tailored portfolio project ideas to fill those gaps
- **Feedback Loop** - Refine the shortlist with natural-language feedback
- **Deep Roadmap** - Step-by-step execution plan with resume bullets for your chosen project
- **Progress Tracker** - Visual stage tracker UI throughout the experience

---

## How It Works

The backend is built as a **LangGraph state machine** with two compiled graphs:

```
[Parse Profile] --> [Target Research] --> [Gap Analysis] --> [Idea Generation]
      --> [Filtering] --> [Shortlist] ----+--> [Deep Plan] --> END
                                         |
                              (feedback) +--> [Idea Generation] (loop)
```

| Stage | Description |
|---|---|
| **Parse Profile** | Extracts skills, experience, and projects from a PDF resume or manual input |
| **Target Research** | Fetches benchmark skills expected at the target company |
| **Gap Analysis** | Compares your profile against the benchmark to surface skill gaps |
| **Idea Generation** | LLM generates project ideas aligned with the gaps |
| **Filtering** | Removes ideas that overlap with existing projects |
| **Shortlist** | Ranks and returns the top 5 ideas |
| **Deep Plan** | Generates a full execution roadmap for the selected idea |

---

## Tech Stack

### Backend

| Tool | Purpose |
|---|---|
| **FastAPI** | REST API server |
| **LangGraph** | Stateful multi-step AI agent pipeline |
| **LangChain** | LLM integration utilities |
| **Google Generative AI** | Gemini LLM for analysis and generation |
| **PyPDF / python-docx** | Resume parsing |
| **Pydantic** | Data validation and schemas |
| **Uvicorn** | ASGI server |

### Frontend

| Tool | Purpose |
|---|---|
| **React 18** | UI framework |
| **Vite** | Build tool and dev server |
| **Tailwind CSS** | Utility-first styling |

---

## Project Structure

```
Resume-gap/
|-- backend/
|   |-- main.py                  # FastAPI app and API routes
|   |-- agent.py                 # LangGraph state machine and node definitions
|   |-- requirements.txt         # Python dependencies
|   |-- .env                     # Environment variables (not committed)
|   |-- stages/
|   |   |-- profile_parser.py    # PDF and manual profile parsing
|   |   |-- target_research.py   # Company benchmark research
|   |   |-- gap_analysis.py      # Skill gap identification
|   |   |-- idea_generation.py   # LLM project idea generation
|   |   |-- filtering.py         # Idea deduplication and filtering
|   |   |-- shortlist.py         # Ranking and shortlist creation
|   |   `-- deep_plan.py         # Execution roadmap generation
|   `-- utils/                   # Shared helper utilities
|
`-- frontend/
    |-- index.html
    |-- package.json
    |-- vite.config.js
    `-- src/
        |-- App.jsx              # Main app state and routing
        |-- api.js               # API client functions
        `-- components/
            |-- StartScreen.jsx      # Resume upload and manual entry form
            |-- GapsScreen.jsx       # Skill gap display
            |-- ShortlistScreen.jsx  # Project idea shortlist and feedback
            |-- RoadmapScreen.jsx    # Deep execution roadmap display
            |-- StageTracker.jsx     # Step progress indicator
            `-- PipelineLoader.jsx   # Loading state with step messages
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A **Google Gemini API key**

---

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file and fill in your API key
# (see Environment Variables below)

# 5. Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

---

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Set VITE_API_URL in frontend/.env
# VITE_API_URL=http://localhost:8000

# 4. Start the dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/start` | Start the pipeline with a resume file upload |
| `POST` | `/api/start-manual` | Start the pipeline with a manual profile JSON |
| `POST` | `/api/feedback` | Refine the shortlist with natural-language feedback |
| `POST` | `/api/select` | Select an idea and generate the deep roadmap |
| `GET` | `/api/session/{session_id}` | Retrieve full session state |
| `GET` | `/health` | Health check |

### POST /api/start

```
Form Data:
  resume          file     PDF resume file
  target_company  string   e.g. "Google" (optional, defaults to "default")

Response:
  session_id, user_profile, skill_gaps, shortlist, iteration
```

### POST /api/start-manual

```json
{
  "target_company": "Google",
  "name": "Jane Doe",
  "technical_skills": ["Python", "React"],
  "soft_skills": ["Communication"],
  "past_projects": [{ "name": "Portfolio Site" }],
  "languages": ["English"],
  "years_experience": 2.0,
  "target_roles": ["Software Engineer"]
}
```

### POST /api/feedback

```
Query Params:
  session_id   string
  feedback     string   e.g. "I prefer backend-focused projects"
```

### POST /api/select

```
Query Params:
  session_id   string
  idea_index   int      0-based index from the returned shortlist
```

---

## Environment Variables

### Backend - `backend/.env`

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |

### Frontend - `frontend/.env`

| Variable | Required | Description |
|---|---|---|
| `VITE_API_URL` | Yes | Base URL of the backend API (e.g. `http://localhost:8000`) |

---

> Built with LangGraph, FastAPI, and React.
