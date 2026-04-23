# RELEASE_NOTES_v0.1

## What the project is

AIVeritas v0.1 is a local CSV validation tool with deterministic data-quality checks, a CLI-first workflow, structured JSON reporting, and a small local demo interface kept as a secondary support surface.

## What is included

- Local CLI execution through `src.main`
- CSV loading with explicit failure handling
- Deterministic checks for:
  - missing values
  - duplicate rows
  - numeric outliers
  - time-series gaps
- Structured JSON report generation
- Sample CSV inputs under `data/synthetic/`
- A committed example report under `examples/`
- Python tests for the validation core, reporting, CLI, service layer, and API
- Frontend tests for the local demo interface
- Local FastAPI backend and React GUI retained as secondary demo/support interfaces

## What is intentionally NOT included

- Real AI functionality
- External services, database, or cloud deployment
- Batch validation across multiple files
- Broad runtime configuration for validation thresholds
- A full report explorer in the browser interface
- Multi-user or remote execution workflows

## Known limitations

- The CLI is the only primary workflow in v0.1.
- The local API and browser interface are secondary and intentionally minimal.
- Validation thresholds are mostly hardcoded.
- The report schema still contains a placeholder `ai_explanation` field for schema continuity, but it is not part of the core product scope.
- The tool is designed for local usage on one machine.
