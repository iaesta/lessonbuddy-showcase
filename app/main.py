from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.demo_generator import build_demo_pack, build_quick_review
from app.models import (
    ApprovedGenerationRequest,
    GenerationResponse,
    QuickReview,
    WorksheetRequest,
)

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "app" / "static"
APP_VERSION = "1.1.0-showcase"

app = FastAPI(
    title="LessonBuddy Showcase",
    version=APP_VERSION,
    description=(
        "Sanitised portfolio edition of a structured ESL "
        "lesson-planning and worksheet-validation system."
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
        "engine": "deterministic-portfolio-demo-v2",
        "externalAIConfigured": False,
        "publicBoundary": "No production prompts, provider adapter, or commercial rules.",
    }


@app.post("/api/quick-review", response_model=QuickReview)
def quick_review(request: WorksheetRequest) -> QuickReview:
    return build_quick_review(request)


@app.post("/api/generate", response_model=GenerationResponse)
def generate(request: WorksheetRequest) -> GenerationResponse:
    try:
        return build_demo_pack(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/generate-approved", response_model=GenerationResponse)
def generate_approved(payload: ApprovedGenerationRequest) -> GenerationResponse:
    try:
        return build_demo_pack(
            payload.request,
            approved_flow=payload.approved_flow,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
