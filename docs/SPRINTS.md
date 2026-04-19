# Sprints

This file tracks execution in a lightweight format suitable for an early-stage personal engineering project.

## Sprint Cadence

- Sprint length: 1 to 2 weeks as available.
- Focus: one clear improvement theme per sprint.
- Rule: each sprint should end with working code, updated tests, and updated documentation when behavior changes.

## Sprint 0: Project Bootstrap

Status: `Completed`

Objective:

- Establish the initial repository structure and working validation flow.

Delivered:

- `src/` package with loader, validator, report, AI stub, and CLI entry point.
- Synthetic datasets under `data/synthetic/`.
- Initial tests for loader, validator, and report behavior.
- Base workflow files such as `Makefile`, `pyproject.toml`, and development guidelines.

Notes:

- This sprint established the baseline needed for disciplined iteration.

## Sprint 1: Engineering Discipline and Documentation

Status: `Completed`

Objective:

- Make the repository look and behave like a maintainable engineering project.

Delivered:

- Shared issue/report schema alignment.
- Contributor workflow and lint/test process.
- Git hook installation flow.
- Project-management and architecture documentation set.

Notes:

- The project is still small, but now has explicit planning, decision tracking, and traceability documents.

## Sprint 2: Validation Hardening

Status: `Planned`

Objective:

- Improve correctness confidence and reduce fragile validation behavior.

Planned work:

- Add CLI integration tests.
- Expand failure-path coverage.
- Add tests for outlier and time-series-gap scenarios.
- Review error messages and report consistency.

Exit criteria:

- Higher-confidence validation behavior with broader automated coverage.

## Sprint 3: Configurable Validation Rules

Status: `Planned`

Objective:

- Move key validation parameters from code defaults to user-configurable inputs.

Planned work:

- Configurable z-score threshold.
- Configurable time-series frequency assumptions where practical.
- Cleaner report metadata for effective validation configuration.

Exit criteria:

- Users can tune validation behavior without editing source files.

