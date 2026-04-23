# AIVeritas Development Guidelines

## Purpose

This document defines the coding rules and development workflow for AIVeritas.
Use it as the reference during implementation, review, and maintenance.

Global coding defaults live in [/home/morgmau/.codex/AGENTS.md](/home/morgmau/.codex/AGENTS.md).
Project-specific constraints are summarized in [docs/AIVERITAS_RULES.md](/home/morgmau/projects/aiveritas/docs/AIVERITAS_RULES.md).

## Project Rules

- Use Python 3.12+ features only when they improve clarity in this codebase.
- Keep JSON report schemas consistent across modules.
- Prefer deterministic outputs over smart but unclear behavior.
- Do not introduce hidden side effects in helper functions.
- Keep validation logic modular and easy to extend.
- Preserve the AIVeritas issue/report schema unless a change is intentional and documented.
- Keep deterministic validation responsibilities separate from non-core placeholder explanation scaffolding.
- Keep the CLI supported as a first-class interface.
- Route local GUI behavior through shared service layers rather than duplicating validation flow in interface code.

## Repository Workflow

- Use `make lint`, `make test`, and `make review-check` as the normal local quality workflow.
- Install the versioned `pre-commit` hook with `make install-hooks`.
- Keep the synthetic dataset generator under `scripts/`.
- Avoid broad refactors unless they are required to support the change safely.

## Validation and Quality Gates

Run these checks before committing:

```bash
make lint
make test
make check
```

Quality gates:

- Schema changes must preserve report consistency.
- Review changes with `make review-check` before opening or updating a PR.

## Documentation Ownership

- Update `docs/DECISIONS.md` when architectural or workflow choices materially change.
- Keep `docs/FEATURES.md` as the source of truth for feature status.
- Keep `docs/TEST_MATRIX.md` as the source of truth for feature-to-test coverage.
- Treat raw `SESSIONS/` notes as private local workflow, not public repository history.
- Promote durable outcomes into `CHANGELOG.md`, `docs/SPRINTS.md`, or `docs/DECISIONS.md`.
