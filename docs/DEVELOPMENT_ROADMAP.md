# Development Roadmap

## Current priority — measured print pagination

The next milestone is to stop student activities being clipped at the bottom of A4 pages.

Planned work:

1. Measure rendered activity height against the printable page area.
2. Keep headings and their first response item together.
3. Compact spacing only within safe readability limits.
4. Move a complete activity to the next page when it does not fit.
5. Split long repeatable item lists only at item boundaries.
6. Create an additional student page rather than truncating content.
7. Add regression fixtures for the current `do/does` overflow case.
8. Verify print preview and generated PDF output at A4 size.

## Near-term quality work

- strengthen printable-layout validation;
- improve support for generated or library visual assets;
- expand grammar and phonics regression cases;
- add clearer teacher-facing explanations when generation is blocked;
- record generation and repair diagnostics without exposing private learner data.

## Product work after print stability

- persistent projects and reusable learner profiles;
- user accounts and secure saved materials;
- reviewed contribution library;
- richer export options;
- deployment hardening and monitoring.

## Definition of done for a generation milestone

A feature is not considered complete merely because Gemini returns JSON. It must:

- satisfy the approved lesson contract;
- respect learner reading, writing, and pencil capabilities;
- survive semantic validation;
- render without hidden or clipped tasks;
- provide matching teacher guidance and answers;
- pass automated regression tests;
- fail safely without publishing when requirements are not met.
