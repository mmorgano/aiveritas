# Sprints

This file tracks execution in a lightweight format suitable for an early-stage personal engineering project.

## Sprint Cadence

- Sprint length: 1 to 2 weeks as available.
- Focus: one clear improvement theme per sprint.
- Rule: each sprint should end with working code, updated tests, and updated documentation when behavior changes.

## Sprint 0: Project Bootstrap

Status: `Completed`

Related roadmap phase:

- Phase 1: MVP Baseline

Feature focus:

- `F-01` through `F-09`

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

Related roadmap phase:

- Phase 1: MVP Baseline

Feature focus:

- `F-06`
- `F-07`
- `F-10`

Objective:

- Make the repository look and behave like a maintainable engineering project.

Delivered:

- Shared issue/report schema alignment.
- Contributor workflow and lint/test process.
- Git hook installation flow.
- Project-management and architecture documentation set.

Notes:

- The project is still small, but now has explicit planning, decision tracking, and traceability documents.

## Sprint 2: Local GUI Foundation

Status: `Completed`

Related roadmap phase:

- Phase 2: Local Application Foundations

Feature focus:

- `F-15`
- `F-16`
- `F-17`
- `F-18`

Objective:

- Add a second local interface without rewriting the validation core.

Delivered:

- Shared validation orchestration for CLI and GUI entry points.
- Local FastAPI backend for validation execution and report reopening.
- Minimal React + Vite frontend for upload, run, summary, and recent reports.
- Lightweight recent-report history persisted under local application state.
- Automated tests for validation service, history store, API routes, and frontend behavior.

Notes:

- The CLI remains supported, but the repository now has a realistic local application path.

## Sprint 3: Validation Hardening

Status: `Planned`

Related roadmap phase:

- Phase 2: Local Application Foundations

Feature focus:

- `F-04`
- `F-05`
- `F-11`

Objective:

- Improve correctness confidence and reduce fragile validation behavior across both interfaces.

Planned work:

- Add CLI integration tests.
- Expand failure-path coverage.
- Add tests for outlier and time-series-gap scenarios.
- Review error messages and report consistency.

Exit criteria:

- Higher-confidence validation behavior with broader automated coverage.

## Sprint 4: Configurable Validation Rules

Status: `Planned`

Related roadmap phase:

- Phase 2: Local Application Foundations

Feature focus:

- `F-12`

Objective:

- Move key validation parameters from code defaults to user-configurable inputs.

Planned work:

- Configurable z-score threshold.
- Configurable time-series frequency assumptions where practical.
- Cleaner report metadata for effective validation configuration.

Exit criteria:

- Users can tune validation behavior without editing source files.
