# Architecture

## Design goal

Keep AI-assisted generation inspectable, constrained, and testable. LessonBuddy does not send an unconstrained teacher request directly to a model and trust the result. It separates teacher input, compatibility rules, planning, approval, generation, normalisation, and validation.

## Public showcase layers

### 1. Request models

`app/models.py` defines typed learner and lesson inputs. Pydantic rejects invalid ages, missing target language, unsupported durations, and malformed requests before generation begins.

### 2. Compatibility engine

`app/compatibility.py` maps reading, Latin-writing, pencil-control, age, and skill selections to allowed response modes and warnings.

Examples:

- a pre-reader receives oral and picture-based response modes;
- a learner with no Latin writing is not asked for written English;
- large-space pencil support removes dense written tasks;
- incompatible extended writing can block generation.

### 3. Deterministic demo generator

`app/demo_generator.py` creates a quick review, timed class flow, worksheet-page specifications, and an answer key. The public edition is deterministic so tests remain stable and no external credentials are needed.

### 4. Validation

Generated demo packs are checked for:

- complete and contiguous timing;
- a flow ending at the requested duration;
- non-empty worksheet pages;
- activities on every page;
- answer coverage for every worksheet.

### 5. API and frontend

`app/main.py` exposes FastAPI endpoints. The browser interface is deliberately small and framework-free so the backend data flow remains easy to inspect.

## Private product architecture

The current private product extends these boundaries into a two-stage AI workflow:

```text
Teacher brief
  → Gemini planning
  → Buddy plan validation
  → deterministic plan repair
  → optional constrained Gemini repair
  → teacher approval
  → Gemini exercise generation
  → Buddy normalisation
  → semantic and learner-profile validation
  → printable pack
```

### Planning contract

Gemini creates the objective, timed class flow, and page-level worksheet plan. Buddy converts broad ideas into measurable constraints, including exact activity counts, item budgets, classroom practice time, reserve work, progression, and page variety. The approved plan is then locked before exercise generation.

### Generation contract

Gemini may generate only activity types approved by the plan. Buddy then checks concrete exercise semantics rather than merely checking JSON shape.

Examples of current private checks include:

- vague instructions are replaced or rejected;
- word-order tokens must match the accepted answer exactly;
- already-solved or trivially rearranged word-order items are rejected;
- multiple-choice options must be distinct and unambiguous;
- requested dialogue, gap-fill, or sentence production must actually appear in the printed work;
- reading, writing, and pencil demands cannot exceed the learner profile;
- teacher-read-aloud support is recorded explicitly for word-level readers;
- underfilled pages and insufficient real response actions are rejected.

### Repair strategy

Deterministic problems are repaired locally first. This saves model calls and ensures reproducible behaviour. A single constrained Gemini repair attempt is available for creative problems. If the repaired result still fails, Buddy publishes nothing and reports the validation details.

## Security and repository separation

The public showcase excludes:

- API keys and secrets;
- proprietary prompts;
- the production Gemini adapter;
- commercial and pricing logic;
- private test data;
- unfinished production features presented as complete.

The private repository remains the source of truth for the full product.
