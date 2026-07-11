# Public / private boundary

LessonBuddy is developed as a private product. This repository is a deliberately reduced portfolio edition.

## Included here

- small typed FastAPI contracts;
- basic learner-profile compatibility examples;
- deterministic sample planning and generation;
- a simplified teacher approval interaction;
- generic teacher and student renderers;
- public regression tests;
- CI and deployment-friendly project structure.

## Kept private

- provider credentials and provider SDK integration;
- proprietary planning and generation prompts;
- the private two-stage generation bridge;
- commercial blueprint construction;
- the complete pedagogical QC and repair system;
- private storage, history, and product analytics;
- production print-fitting and document assembly internals;
- real user, teacher, school, or student data.

## Design rule

A public feature may demonstrate a product concept, but it must be implemented independently and at a reduced level. Production modules must never be copied into this repository.

The automated public-boundary test searches the application source for known provider and production markers. This does not replace code review, but it adds a useful guardrail.
