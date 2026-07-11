# LessonBuddy Showcase

A public, sanitised portfolio edition of **LessonBuddy**: an EdTech system that turns a teacher's learner profile and lesson focus into a structured ESL class plan and printable worksheet demonstration.

> This repository demonstrates architecture, validation, API design, automated testing, frontend work, and product thinking. Production prompts, credentials, provider adapters, commercial rules, private storage, and user data remain private.

## Current public milestone

The public showcase is now **v1.1.0-showcase**.

It demonstrates a safe, deterministic version of the current product workflow:

1. A teacher submits a learner profile, lesson focus, target language, and duration.
2. The API creates a typed review plan with stable demo stage IDs.
3. The teacher can edit, reorder, add, or remove non-required stages in the browser.
4. The required **Student pages** stage remains protected.
5. The approved demo flow is submitted to a separate generation endpoint.
6. The API produces a deterministic teacher guide, answer key, and student pages.
7. Validation checks timing continuity, unique IDs, worksheet coverage, and activity variety.
8. Student sheets omit internal `Core` / `Extra` labels while the teacher guide retains them.
9. A print-specific A4 view is included without exposing the private production renderer.

The private product contains the real AI provider integration, proprietary prompts, production planning bridges, full pedagogical QC, storage, and commercial document assembly. Those components are not copied into this repository.

## Safe public boundary

This showcase intentionally excludes:

- AI credentials and provider SDK integration
- production prompt text
- private two-stage planning and repair logic
- commercial blueprint generation
- the complete pedagogical validation rule set
- private persistence and history
- production document assembly internals
- user or student data

A regression test scans the public application for provider and production markers so those components are not added accidentally.

## Public demo workflow

```text
Teacher brief
      ↓
Deterministic review plan
      ↓
Teacher edits and approves the demo flow
      ↓
Deterministic sample generation
      ↓
Public validation boundary
      ↓
Teacher guide + student print view + structured JSON
```

## What the project demonstrates

- **Python + FastAPI** API design
- **Pydantic** request validation and typed domain models
- learner-profile compatibility rules that keep reading, writing, and pencil control separate
- a teacher-in-the-loop review step
- stable public demo IDs and approved-flow validation
- deterministic generation for reliable testing
- separate teacher and student rendering concerns
- A4 print styling
- framework-free **HTML/CSS/JavaScript**
- automated regression tests and GitHub Actions CI
- QA-led development informed by real ESL classroom needs

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Run tests:

```bash
pytest -q
```

## API endpoints

- `GET /api/health` — public version and safety boundary
- `POST /api/quick-review` — deterministic typed review plan
- `POST /api/generate` — backward-compatible deterministic generation
- `POST /api/generate-approved` — generation from a teacher-approved demo flow

## Example request

```json
{
  "topic": "Animals at the zoo",
  "primary_skill": "vocabulary",
  "target_words": ["lion", "monkey", "elephant", "giraffe"],
  "age_min": 6,
  "age_max": 8,
  "level_label": "A1",
  "reading_stage": "word",
  "latin_writing_stage": "write_words",
  "pencil_control": "age_appropriate",
  "session_duration_minutes": 40,
  "student_count": 8,
  "teacher_request": ""
}
```

## Repository map

```text
app/
  main.py               FastAPI routes
  models.py             Typed request, review, and output models
  compatibility.py      Learner-profile rules
  demo_generator.py     Deterministic public generation and validation
  static/               Browser interface and print view
tests/
  test_app.py           API and approved-flow tests
  test_compatibility.py Learner-profile tests
  test_public_boundary.py
docs/
  PUBLIC-BOUNDARY.md     Explicit private/public separation
```

## Portfolio relevance

This project is relevant to junior or hybrid roles involving:

- QA and test automation
- Python backend development
- AI-output evaluation
- EdTech product development
- product operations
- frontend implementation
- prompt and workflow design

## Author

**Jessica Ariza Gomez** — ESL educator, former QA professional, and independent developer.

## Copyright and permitted use

**Copyright © 2026 Jessica Ariza Gomez. All rights reserved.**

This repository is provided solely for portfolio review, recruitment, and professional evaluation. No permission is granted to reproduce, redistribute, publish, sublicense, create derivative commercial products from, or use this code or its materials commercially without prior written permission from the copyright holder.
