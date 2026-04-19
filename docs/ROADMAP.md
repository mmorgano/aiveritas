# Roadmap

## Vision

AIVeritas aims to become a practical validation engine for tabular datasets that combines deterministic data-quality checks with explainable, AI-assisted issue interpretation.

The near-term goal is a reliable local CLI for CSV validation.
The longer-term goal is a maintainable validation platform with configurable rules, stronger reporting, and production-ready AI integration.

## Planning Principles

- Build a small but trustworthy validation core first.
- Prefer readable, testable modules over broad feature scope.
- Keep report schemas stable before adding integrations.
- Introduce AI only after the deterministic validation pipeline is dependable.

## Traceability

- Feature-level implementation status is tracked in `docs/FEATURES.md`.
- Sprint execution is tracked in `docs/SPRINTS.md`.
- Near-term and future candidate work is tracked in `docs/BACKLOG.md`.
- Test coverage alignment is tracked in `docs/TEST_MATRIX.md`.

## Phase 1: MVP Baseline

Status: `Implemented`

Primary feature focus:

- `F-01` CSV loading
- `F-02` Missing-value validation
- `F-03` Duplicate-row validation
- `F-04` Numeric outlier validation
- `F-05` Time-series gap validation
- `F-06` Structured issue schema
- `F-07` JSON report generation
- `F-08` AI explanation stub
- `F-09` Sample data generation
- `F-10` Local engineering workflow

Scope:

- CSV loading with explicit error handling.
- Rule-based validation for missing values.
- Rule-based validation for duplicate rows.
- Rule-based validation for numeric outliers.
- Rule-based validation for time-series gaps.
- Structured JSON report generation.
- CLI execution flow.
- Placeholder AI explanation stub.
- Synthetic sample dataset generation.
- Initial automated tests with `pytest`.

Exit criteria:

- A user can run the CLI locally against a CSV file and receive a structured report.
- Core validation paths are covered by basic tests.
- Contributor workflow and engineering rules are documented.

## Phase 2: Near-Term Improvements

Status: `Planned`

Primary feature focus:

- `F-11` CLI integration coverage
- `F-12` Configurable validation thresholds

Scope:

- Expand test coverage for CLI flows and failure cases.
- Add configurable validation thresholds and rule parameters.
- Add richer dataset metadata to reports.
- Improve validation summaries and issue grouping.
- Add logging suitable for local debugging and CI usage.
- Improve documentation traceability between features, tests, and backlog items.

Exit criteria:

- Validation behavior is configurable without code edits.
- The report format remains stable and better supports downstream tooling.
- The project can be maintained confidently through tests and documented decisions.

## Phase 3: Production-Oriented Core

Status: `Planned`

Primary feature focus:

- `F-13` Real AI explanation integration
- `F-14` Batch processing

Scope:

- Introduce a real AI explanation integration behind a stable interface.
- Add support for multiple input profiles or validation presets.
- Add batch processing for multiple files.
- Improve CLI ergonomics for operational use.
- Add release discipline and versioned change management.

Exit criteria:

- AI integration is isolated from deterministic validation logic.
- Multiple datasets can be processed predictably.
- Operational workflows are documented and testable.

## Phase 4: Long-Term Goals

Status: `Aspirational`

Scope:

- Support additional tabular formats beyond CSV.
- Add pluggable validation rules.
- Add stronger observability and auditability for validation runs.
- Explore service or API-based execution models.

Exit criteria:

- The project evolves from a local validation CLI into a reusable validation platform.
