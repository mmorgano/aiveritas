# AGENTS

This file provides durable instructions for coding agents working in the AIVeritas repository.

## Project Intent

AIVeritas is an early-stage Python project focused on CSV validation, structured reporting, and future AI-assisted explanation.
Treat it as a serious engineering project with a small current scope.

## Engineering Rules

- Follow the Zen of Python pragmatically.
- Prefer readability over cleverness.
- Keep modules small and responsibilities clear.
- Use type hints throughout the codebase.
- Use Google-style docstrings for public modules, functions, and classes.
- Keep comments in English.
- Preserve the canonical issue/report schema unless a change is intentional and documented.

## Implementation Guidance

- Prefer the smallest change that solves the task cleanly.
- Apply TDD for new features and bug fixes when practical.
- Add or update `pytest` coverage when behavior changes.
- Run `pylint` after each writing or review cycle and improve the result when possible.
- Avoid mixing unrelated refactors into feature work.
- If you change behavior, update documentation that would become misleading.

## Review Guidance

When reviewing code, prioritize:

- correctness
- regressions
- missing tests
- schema consistency
- error handling clarity
- maintainability

Keep summaries brief.
Findings should be concrete and reference affected files or behaviors.

## Architecture Guidance

- Keep deterministic validation logic separate from AI explanation logic.
- Keep report-building responsibilities out of validation modules.
- Use shared schema helpers rather than ad hoc issue dictionaries.
- Preserve CLI simplicity unless a broader interface change is explicitly required.

## Documentation Guidance

- Keep planning and status files realistic.
- Mark planned work clearly as planned.
- Do not document features as implemented unless they exist in the codebase.
- Update `docs/DECISIONS.md` when a significant technical choice changes the architecture or workflow.

