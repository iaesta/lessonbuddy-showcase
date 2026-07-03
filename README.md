# LessonBuddy Showcase

A public, sanitised portfolio edition of **LessonBuddy**: an EdTech prototype that turns a teacher's learner profile and lesson goal into a structured ESL class plan and printable worksheet specification.

> This repository is a portfolio snapshot. Proprietary prompts, commercial planning, credentials, private user data, and production-only logic are intentionally excluded.

## What this project demonstrates

- **Python + FastAPI** API design
- **Pydantic** request validation and typed domain models
- learner-profile compatibility rules
- deterministic demo generation for reliable testing
- output validation before presenting generated material
- a small **HTML/CSS/JavaScript** frontend
- automated tests and GitHub Actions CI
- product thinking informed by real ESL teaching experience

## Why I built it

Teachers often spend significant unpaid time adapting materials for age, reading ability, writing ability, pencil control, class duration, and support needs. LessonBuddy explores how structured software and AI-assisted generation can reduce that preparation time without ignoring pedagogical constraints.

## Current public-demo status

The public edition runs in **deterministic demo mode** and is fully testable without an API key. The private product repository also explores Gemini-assisted generation; that integration is still being stabilised and is deliberately not presented here as production-ready.

## API flow

1. Submit a learner and lesson profile.
2. Receive a quick review with the interpreted plan and compatibility warnings.
3. Generate a deterministic sample pack.
4. Validate the flow, worksheet activities, and answer coverage.

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

## Example request

```json
{
  "topic": "Phonics: sh and ch",
  "primary_skill": "phonics",
  "target_words": ["ship", "shoe", "chair", "cheese"],
  "age_min": 6,
  "age_max": 8,
  "level_label": "Pre-A1",
  "reading_stage": "pre_reader",
  "latin_writing_stage": "no_latin_writing",
  "pencil_control": "age_appropriate",
  "session_duration_minutes": 40,
  "student_count": 8,
  "teacher_request": "Create a visual sound-discrimination lesson with no independent reading."
}
```

## Repository map

```text
app/
  main.py              FastAPI routes
  models.py            Typed request and output models
  compatibility.py     Learner-profile rules
  demo_generator.py    Deterministic generation and validation
  static/               Small browser interface
tests/                  API and rule tests
docs/                   Architecture and project-status notes
examples/               Sample request and response
```

## Roles this project supports

This project is relevant to junior or hybrid roles involving:

- QA and test automation
- Python backend development
- AI-output evaluation
- EdTech product development
- product operations
- prompt and workflow design

## Author

**Jessica Ariza Gomez** — ESL educator, former QA professional, and independent developer.

## Copyright and permitted use

**Copyright © 2026 Jessica Ariza Gomez. All rights reserved.**

This repository is provided solely for portfolio review, recruitment, and professional evaluation. No permission is granted to reproduce, redistribute, publish, sublicense, create derivative commercial products from, or use this code or its materials commercially without prior written permission from the copyright holder.
