from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import ProjectSnapshot

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "app" / "static"
APP_VERSION = "1.1.0-portfolio"

app = FastAPI(
    title="LessonBuddy Portfolio Showcase",
    version=APP_VERSION,
    description=(
        "Read-only portfolio presentation of an ESL planning product. "
        "Production logic is intentionally excluded."
    ),
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "appVersion": APP_VERSION,
        "mode": "portfolio-only",
        "writeOperations": False,
    }


@app.get("/api/project-snapshot", response_model=ProjectSnapshot)
def project_snapshot() -> ProjectSnapshot:
    return ProjectSnapshot(
        name="LessonBuddy",
        edition="Sanitised portfolio showcase",
        status="Private product under active development",
        summary=(
            "A teacher-support system for structuring ESL lesson plans and "
            "printable materials around learner profiles and classroom constraints."
        ),
        engineering_highlights=[
            "FastAPI and Pydantic architecture",
            "Teacher-in-the-loop approval workflow",
            "Separate teacher and student presentation layers",
            "Automated regression testing",
            "Responsive, accessible frontend design",
        ],
        qa_principles=[
            "Validate before publishing output",
            "Keep learner constraints explicit",
            "Prefer deterministic checks where possible",
            "Protect print and classroom usability",
        ],
        private_by_design=[
            "Provider integration and credentials",
            "Prompt and generation strategy",
            "Detailed pedagogical rule set",
            "Private storage and production document logic",
        ],
    )
