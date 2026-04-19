# Decisions

This file records lightweight architectural decision records for choices that materially shape the codebase.

## ADR-001: Keep the project as a local CLI first

Status: `Accepted`

Date: `2026-04-19`

Context:

- The repository is still early-stage and the main risk is validation correctness, not deployment topology.
- The current codebase already centers around a local CLI entry point in `src/main.py`.

Decision:

- Build AIVeritas first as a local Python CLI instead of starting with a service or web API.

Why:

- The core problem is validation correctness, not deployment complexity.
- A CLI keeps the feedback loop short and the architecture simple.
- It is easier to test and document at the current project stage.

Consequences:

- Operational scope stays small.
- Future API or service work remains possible but is not a current obligation.

Implications for development:

- New features should fit the CLI-first workflow unless a broader interface change is explicitly planned.
- Tests and documentation should continue to treat the CLI as the primary delivery surface.

## ADR-002: Use a canonical issue schema across modules

Status: `Accepted`

Date: `2026-04-19`

Context:

- Validation checks, failure handling, and reporting all need to exchange issue data.
- The current repository uses shared schema helpers in `src/schemas.py`.

Decision:

- Use a shared issue structure for validation issues, failure issues, AI enrichment, and report generation.

Why:

- Inconsistent dictionaries were difficult to extend safely.
- A stable issue contract makes reporting and test traceability easier.

Consequences:

- New checks should emit the canonical schema instead of ad hoc dictionaries.
- Schema changes should be documented and tested.

Implications for development:

- `src/validator.py`, `src/report.py`, and `src/ai_module.py` should evolve through the shared schema layer rather than diverging locally.
- Report changes should be reflected in `docs/ARCHITECTURE.md`, `docs/FEATURES.md`, and `docs/TEST_MATRIX.md` when relevant.

## ADR-003: Keep AI integration behind a stub module for now

Status: `Accepted`

Date: `2026-04-19`

Context:

- The repository already contains an AI explanation interface in `src/ai_module.py`, but it is intentionally a stub.
- Deterministic validation and report stability are still more important than model integration.

Decision:

- Keep `src/ai_module.py` as a placeholder instead of integrating a real external model now.

Why:

- Deterministic validation and report structure must stabilize first.
- External AI integration would add moving parts before the core validation path is mature.

Consequences:

- AI output is predictable but not yet useful beyond interface validation.
- A later AI integration should preserve the current explanation interface as much as practical.

Implications for development:

- AI-related tests should focus on output shape and interface stability before they focus on model behavior.
- Planned AI work should remain clearly marked as planned in roadmap and feature-tracking documents.

## ADR-004: Use pytest and pylint as default quality gates

Status: `Accepted`

Date: `2026-04-19`

Context:

- The project is intended to look and behave like a maintainable engineering repository.
- The current workflow already relies on `make test`, `make lint`, and a pre-commit hook.

Decision:

- Standardize on `pytest` for tests and `pylint` for linting.

Why:

- The project needs lightweight but explicit engineering discipline.
- These tools are already aligned with the repository workflow and contributor guidance.

Consequences:

- New work should include tests when behavior changes.
- Linting should run after coding and review cycles.

Implications for development:

- Contributor guidance and coding-agent guidance should remain aligned with `pytest` and `pylint`.
- When test or lint scope changes materially, update `CONTRIBUTING.md`, `AGENTS.md`, and `README.md`.

## ADR-005: Keep raw session logs private and use durable public artifacts instead

Status: `Accepted`

Date: `2026-04-19`

Context:

- Session-resume notes can help local execution, but raw working logs are noisy and often not suitable for a public repository.
- The repository already has stronger public artifacts for durable history, such as `CHANGELOG.md`, `docs/SPRINTS.md`, and `docs/DECISIONS.md`.

Decision:

- Keep raw session-tracking files private and ignored by Git.
- Use durable project artifacts, not session transcripts, to communicate repository history publicly.

Why:

- Public repository documentation should communicate decisions, progress, and scope without exposing ephemeral AI or personal workflow noise.
- Durable documents are easier to maintain and more useful to GitHub visitors.

Consequences:

- The `SESSIONS/` workflow may exist locally, but it is not part of the committed documentation system.
- Public progress should be reflected through roadmap, sprint, backlog, ADR, and changelog updates instead.

Implications for development:

- Do not commit raw `SESSIONS/` logs.
- If a session produces a meaningful architectural or planning outcome, promote that outcome into `CHANGELOG.md`, `docs/SPRINTS.md`, or `docs/DECISIONS.md` as appropriate.

## ADR-006: Defer typed domain models until schema pressure justifies them

Status: `Proposed`

Date: `2026-04-19`

Context:

- The current project uses plain dictionaries plus shared schema helpers to represent issues and reports.
- The codebase is still small, but schema growth could eventually justify stronger typed models.

Decision:

- Keep the current dictionary-based schema approach for now and revisit typed models only if maintainability pressure becomes real.

Why:

- The current scope does not yet justify the extra abstraction cost of formal domain-model classes.
- The shared helper layer already centralizes most schema handling.

Consequences:

- The project stays simple in the short term.
- The decision should be revisited if schema validation, mutation, or cross-module coupling grows significantly.

Implications for development:

- New work should continue using schema helpers consistently.
- If multiple modules start duplicating schema logic, revisit this ADR.
