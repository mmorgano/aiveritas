# Decisions

This file records lightweight architectural decision records for choices that materially shape the codebase.

## ADR-001: Keep the project as a local CLI first

Status: `Accepted`

Date: `2026-04-19`

Decision:

- Build AIVeritas first as a local Python CLI instead of starting with a service or web API.

Why:

- The core problem is validation correctness, not deployment complexity.
- A CLI keeps the feedback loop short and the architecture simple.
- It is easier to test and document at the current project stage.

Consequences:

- Operational scope stays small.
- Future API or service work remains possible but is not a current obligation.

## ADR-002: Use a canonical issue schema across modules

Status: `Accepted`

Date: `2026-04-19`

Decision:

- Use a shared issue structure for validation issues, failure issues, AI enrichment, and report generation.

Why:

- Inconsistent dictionaries were difficult to extend safely.
- A stable issue contract makes reporting and test traceability easier.

Consequences:

- New checks should emit the canonical schema instead of ad hoc dictionaries.
- Schema changes should be documented and tested.

## ADR-003: Keep AI integration behind a stub module for now

Status: `Accepted`

Date: `2026-04-19`

Decision:

- Keep `src/ai_module.py` as a placeholder instead of integrating a real external model now.

Why:

- Deterministic validation and report structure must stabilize first.
- External AI integration would add moving parts before the core validation path is mature.

Consequences:

- AI output is predictable but not yet useful beyond interface validation.
- A later AI integration should preserve the current explanation interface as much as practical.

## ADR-004: Use pytest and pylint as default quality gates

Status: `Accepted`

Date: `2026-04-19`

Decision:

- Standardize on `pytest` for tests and `pylint` for linting.

Why:

- The project needs lightweight but explicit engineering discipline.
- These tools are already aligned with the repository workflow and contributor guidance.

Consequences:

- New work should include tests when behavior changes.
- Linting should run after coding and review cycles.

