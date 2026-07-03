# Architecture

## Design goal

Keep the generation workflow inspectable and testable. The system separates teacher input, compatibility rules, planning, generation, and validation rather than sending an unconstrained request directly to an AI model.

## Layers

### 1. Request models

`app/models.py` defines typed learner and lesson inputs. Pydantic rejects invalid ages, duplicate or missing vocabulary, unsupported durations, and malformed requests before generation begins.

### 2. Compatibility engine

`app/compatibility.py` maps reading, writing, pencil-control, age, and skill selections to allowed response modes and warnings.

Examples:

- a pre-reader receives oral and picture-based response modes;
- a learner with no Latin writing is not asked for written English;
- large-space pencil support removes dense written tasks;
- incompatible extended writing can block generation.

### 3. Planning and generation

`app/demo_generator.py` creates a quick review, a timed class flow, worksheet-page specifications, and an answer key. The public edition is deterministic so tests are stable and no external credentials are needed.

### 4. Validation

Generated packs are checked for:

- complete and contiguous timing;
- a flow ending at the requested duration;
- non-empty worksheet pages;
- activities on every page;
- answer coverage for every worksheet.

### 5. API and frontend

`app/main.py` exposes FastAPI endpoints. The browser interface is deliberately small and framework-free so the backend data flow remains easy to inspect.

## Private-product direction

The private product explores a provider layer for AI-assisted generation and repair. That adapter, proprietary prompts, pricing, and production configuration are not included in this public portfolio edition.
