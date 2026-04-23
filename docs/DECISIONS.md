# Decisions

This file records lightweight architectural decisions that materially shape the repository.

## ADR-001: Keep the project as a local CLI first

Status: `Accepted`

Date: `2026-04-19`

Context:

- The core problem is local CSV validation correctness.
- The most reliable product path is a direct local CLI.

Decision:

- Keep the CLI as the primary interface.

Consequences:

- The CLI remains the reference workflow for documentation and release scope.
- Other interfaces must not redefine the core validation flow.

## ADR-002: Use a canonical issue schema across modules

Status: `Accepted`

Date: `2026-04-19`

Context:

- Validation checks, failure handling, and reporting need a shared structure.

Decision:

- Use shared schema helpers for issues and report-adjacent payloads.

Consequences:

- Validation and reporting stay aligned through one issue shape.
- Schema changes should be intentional and documented.

## ADR-003: Keep placeholder explanation scaffolding out of v0.1 scope

Status: `Accepted`

Date: `2026-04-19`

Context:

- The codebase contains `src/ai_module.py` and an `ai_explanation` field in issue payloads.
- These placeholders do not provide real user value in v0.1.

Decision:

- Keep the placeholder scaffolding in code for internal schema continuity.
- Do not position it as a core product capability.

Consequences:

- v0.1 documentation should describe AIVeritas as a deterministic CSV validation tool.
- The placeholder explanation field remains secondary and non-core.

## ADR-004: Use pytest and pylint as default quality gates

Status: `Accepted`

Date: `2026-04-19`

Context:

- The project needs lightweight, explicit engineering discipline.

Decision:

- Standardize on `pytest` for tests and `pylint` for linting.

Consequences:

- New behavior should be covered by tests.
- Local and CI workflows should reflect these checks.

## ADR-005: Keep raw session logs private and use durable public artifacts instead

Status: `Accepted`

Date: `2026-04-19`

Context:

- Local session notes are useful for workflow continuity but are not public project artifacts.

Decision:

- Keep raw session-tracking files private and ignored by Git.
- Use repository documents such as README, changelog, roadmap, and ADRs for durable public context.

Consequences:

- `SESSIONS/` stays out of committed project history.

## ADR-006: Defer typed domain models until schema pressure justifies them

Status: `Proposed`

Date: `2026-04-19`

Context:

- The current project uses dictionaries plus shared helpers to represent issues and reports.
- The codebase is still small.

Decision:

- Keep the current dictionary-based approach for now.

Consequences:

- The code stays simple at current size.
- Revisit only if schema growth creates real maintenance pressure.

## ADR-007: Keep the local API and GUI as secondary interfaces

Status: `Accepted`

Date: `2026-04-20`

Context:

- A browser interface exists and works locally.
- The CLI remains the cleanest primary release surface for v0.1.

Decision:

- Keep the FastAPI backend and React GUI in the repository.
- Treat them as secondary local demo/support interfaces over the shared validation core.

Consequences:

- README and user guidance should present the CLI first.
- Validation behavior should continue to flow through shared service code rather than interface-specific implementations.
