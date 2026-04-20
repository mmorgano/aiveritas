# AIVeritas-Specific Rules

This file captures rules that are specific to AIVeritas and should not automatically be treated as universal defaults for every future project.

## Project-Specific Constraints

- Preserve the canonical issue schema used by `src/schemas.py`, `src/validator.py`, `src/report.py`, and `src/ai_module.py`.
- Keep deterministic validation logic separate from AI explanation logic.
- Keep the CLI supported as a first-class interface.
- Route local GUI behavior through shared service layers rather than duplicating validation flow in API handlers.
- Treat raw `SESSIONS/` files as private local workflow and never as public project history.
- Use durable documents such as `CHANGELOG.md`, `docs/SPRINTS.md`, and `docs/DECISIONS.md` for public engineering traceability.

## Project-Specific Documentation Expectations

- `docs/FEATURES.md` is the source of truth for feature status.
- `docs/TEST_MATRIX.md` is the source of truth for feature-to-test coverage mapping.
- `docs/DECISIONS.md` should be updated when architectural or workflow decisions materially change.
- `docs/ARCHITECTURE.md` should describe module responsibilities, not backlog plans.

## Project-Specific Workflow Defaults

- Use `make lint`, `make test`, and `make review-check` as the normal pre-commit workflow.
- Keep the synthetic dataset generator under `scripts/`.
- Keep project-management documentation lightweight and implementation-aware.
