# AGENTS

This file provides durable instructions for coding agents working in the AIVeritas repository.

## Project Intent

AIVeritas is an early-stage Python project focused on CSV validation, structured reporting, and future AI-assisted explanation.
Treat it as a serious engineering project with a small current scope.

Global reusable agent defaults live in [/home/morgmau/.codex/AGENTS.md](/home/morgmau/.codex/AGENTS.md).
Project-specific constraints live in [docs/AIVERITAS_RULES.md](/home/morgmau/projects/aiveritas/docs/AIVERITAS_RULES.md).

## Implementation Guidance

- Avoid mixing unrelated refactors into feature work.
- If you change behavior, update documentation that would become misleading.
- Preserve the canonical issue/report schema unless a change is intentional and documented.

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
- Keep the repository CLI-first unless a broader interface change is explicitly required.

## Documentation Guidance

- Update `docs/DECISIONS.md` when a significant technical choice changes the architecture or workflow.
- Keep `docs/FEATURES.md` as the source of truth for feature status.
- Keep `docs/TEST_MATRIX.md` as the source of truth for feature-to-test coverage.
- Treat raw `SESSIONS/` notes as private local workflow, not as public repository documentation.
- Promote durable outcomes from private work notes into `CHANGELOG.md`, `docs/SPRINTS.md`, or `docs/DECISIONS.md` when appropriate.
