# Project Status

Last updated: **3 July 2026**

## Public showcase

Completed:

- typed FastAPI endpoints;
- request validation;
- learner-profile compatibility rules;
- deterministic planning and generation;
- answer-key creation;
- output validation;
- responsive browser interface;
- automated API and rule tests;
- GitHub Actions continuous integration.

The public edition remains deterministic and sanitised so it can be reviewed safely without credentials or proprietary prompts.

## Private product: current working milestone

The private product has reached a functioning local end-to-end Gemini workflow:

- Gemini generates the lesson objective, flow, and worksheet plan;
- Buddy validates and repairs the plan before approval;
- Gemini generates only the approved exercise structure;
- Buddy assembles and validates the final teacher and student materials;
- failed validation prevents publication;
- the teacher can leave the desired class outcome blank and let Buddy propose one;
- teacher-led reading support allows word-level readers to use oral partner interviews safely;
- semantic checks reject vague instructions, solved word-order tasks, repeated options, and ambiguous answers;
- premium quality checks cover density, progression, timing, variety, reserve work, and real response actions;
- **76 automated tests pass** in Buddy **0.4.6.3**.

## Verified end-to-end output

A real `do/does` lesson successfully travelled through the full local pipeline and produced:

- a timed teacher guide;
- page-by-page scripts and answer keys;
- two student worksheet pages;
- genuine scrambled word-order work;
- a teacher-modelled partner interview.

This confirms the Gemini-to-Buddy connection and validation pipeline are operational.

## Known limitation

The current browser renderer does not yet measure the final printable height before invoking the print dialog. A dense activity can therefore be clipped at the bottom of an A4 page instead of moving to an additional page.

This is the next active engineering problem. It is a rendering and pagination issue, not a failure of the Gemini connection or validation architecture.

## Intentionally excluded from the public repository

- API keys and secrets;
- proprietary prompts;
- full private validation rules;
- private business and pricing documents;
- private test data;
- production deployment configuration;
- unfinished features presented as complete.

## Engineering approach

The project is developed incrementally with a QA mindset: reproduce failures, convert them into regression tests, repair the narrowest responsible layer, run the complete suite, and document known limitations honestly.
