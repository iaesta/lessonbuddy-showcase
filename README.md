# LessonBuddy Showcase

A public, sanitised portfolio edition of **LessonBuddy**: an EdTech system that turns a teacher's learner profile and lesson focus into a structured ESL class plan and printable worksheet specification.

> This repository demonstrates architecture, validation, API design, automated testing, and product thinking. Proprietary prompts, credentials, commercial planning, private user data, and production-only logic remain in a private repository.

## Current milestone

As of **3 July 2026**, the private product has completed its first working end-to-end local generation flow:

1. A teacher submits the learner profile, lesson focus, target language, and duration.
2. Gemini proposes the lesson objective, timed class flow, and worksheet-page plan.
3. Buddy validates learner compatibility, timing, page density, activity variety, and requested practice modes.
4. Buddy repairs deterministic issues and allows one constrained Gemini repair attempt when needed.
5. Gemini generates the approved exercises.
6. Buddy normalises and validates every assembled activity before publication.
7. The app renders a teacher guide, page-by-page scripts and answers, and student worksheets.

The current private build is **Buddy 0.4.6.3** with **76 automated tests passing**.

The remaining high-priority issue is print pagination: an activity can currently exceed the printable A4 height and be clipped instead of flowing onto an additional page. This limitation is documented rather than hidden, and measured page fitting is the next engineering milestone.

## System workflow

```text
Teacher brief
      ↓
Gemini lesson planning
      ↓
Buddy plan validation + deterministic repair
      ↓
Teacher approval
      ↓
Gemini exercise generation
      ↓
Buddy semantic + learner-profile validation
      ↓
Teacher guide + answer key + student worksheets
```

## What the project demonstrates

- **Python + FastAPI** API design
- **Pydantic** request validation and typed domain models
- learner-profile compatibility rules that keep reading, writing, and pencil control separate
- two-stage AI generation with an approved plan locked before exercise generation
- deterministic repair before spending an additional model call
- semantic checks for instructions, word order, duplicate options, answers, and response demands
- page-density, practice-time, progression, variety, and reserve-work rules
- framework-free **HTML/CSS/JavaScript** frontend work
- automated regression tests and GitHub Actions CI
- QA-led development informed by real ESL classroom needs

## Public demo status

This public repository intentionally runs in **deterministic demo mode**. It remains usable without an API key and shows the request, compatibility, planning, generation, and validation boundaries in a safe and reproducible form.

The private product now contains a functioning Gemini-assisted flow. That provider adapter, its proprietary prompts, and the full commercial rule set are deliberately excluded from this public edition.

## API flow in this showcase

1. Submit a learner and lesson profile.
2. Receive a quick review with compatibility warnings.
3. Generate a deterministic sample pack.
4. Validate timing, worksheet activities, and answer coverage.

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
  main.py               FastAPI routes
  models.py             Typed request and output models
  compatibility.py      Learner-profile rules
  demo_generator.py     Deterministic generation and validation
  static/               Small browser interface
tests/                   API and compatibility tests
docs/                    Architecture, current status, and roadmap
examples/                Sample request and response
```

## Portfolio relevance

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
