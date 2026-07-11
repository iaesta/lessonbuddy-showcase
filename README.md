# LessonBuddy Portfolio Showcase

A polished, sanitised portfolio presentation of **LessonBuddy**, an EdTech project designed to help teachers turn learner profiles and lesson goals into structured ESL materials.

This repository is intentionally a **showcase, not the product**.

It presents the problem, product thinking, engineering approach, QA mindset, and selected interface concepts without publishing the private generation system, prompts, provider integration, validation rules, storage, or production document logic.

## What this portfolio demonstrates

- product thinking grounded in real classroom needs;
- FastAPI project structure;
- typed public metadata with Pydantic;
- a responsive HTML/CSS/JavaScript interface;
- accessibility-conscious UI decisions;
- clear separation between teacher and student views;
- automated tests and GitHub Actions;
- explicit protection of private product logic.

## Portfolio experience

The public site shows:

- the classroom problem LessonBuddy addresses;
- a high-level workflow;
- selected interface mock-ups;
- engineering highlights;
- QA and validation principles;
- the public/private architecture boundary;
- project status and transferable skills.

It does **not** accept lesson briefs or generate real materials.

## Public boundary

The following remain private:

- AI provider code and credentials;
- production prompts;
- planning and generation bridges;
- commercial blueprints;
- detailed pedagogical QC rules;
- repair strategies;
- private storage and history;
- production print assembly;
- user and student data.

The public app exposes only a small read-only project metadata endpoint for portfolio inspection.

## Run locally

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

## Public API

- `GET /api/health`
- `GET /api/project-snapshot`

Both endpoints return portfolio metadata only.

## Repository map

```text
app/
  main.py               Read-only FastAPI portfolio routes
  models.py             Public metadata model
  static/               Portfolio interface
tests/
  test_app.py           Route tests
  test_public_boundary.py
                        Safety guardrails
docs/
  PUBLIC-BOUNDARY.md     Public/private separation
```

## Author

**Jessica Ariza Gomez** — ESL educator, former QA professional, and independent developer.

## Copyright and permitted use

**Copyright © 2026 Jessica Ariza Gomez. All rights reserved.**

This repository is provided solely for portfolio review, recruitment, and professional evaluation. No permission is granted to reproduce, redistribute, publish, sublicense, create derivative commercial products from, or use this code or its materials commercially without prior written permission from the copyright holder.
