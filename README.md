# AIVeritas

AIVeritas is a lightweight validation and reporting engine for structured tabular datasets.
It is designed for local data-quality checks in operational reporting, statistical preparation, and repeatable validation workflows where a machine-readable report matters more than ad hoc spreadsheet inspection.

Example scenario:
before publishing a monthly reporting table, use AIVeritas to check for missing required values, duplicate entity rows, numeric anomalies, and broken date continuity, then keep the JSON report as a reviewable validation record.

The project currently supports:

- a Python CLI for scripted validation runs
- a local FastAPI backend
- a minimal React GUI for interactive use
- structured JSON reporting for downstream review or automation

## Why This Project Exists

Many data problems in reporting workflows are not model problems.
They are input-quality problems:

- missing values in required fields
- duplicate entity rows
- unexpected numeric anomalies
- missing dates or broken time continuity

AIVeritas exists to make those checks explicit, repeatable, and reviewable through a stable report format rather than one-off manual inspection.

## Current AI Status

The repository includes an AI explanation module, but it is currently a stub.
It exists to define the integration boundary for future LLM-based explanations.

The project should therefore be read primarily as:

- a validation and reporting engine today
- an AI-extendable validation workflow later

## What This Demonstrates

This repository is intended to show practical engineering skills rather than model hype.

- modular Python application structure
- deterministic validation design with explicit failure handling
- structured JSON report generation
- shared service orchestration across CLI and GUI interfaces
- FastAPI backend and React frontend integration
- automated tests, linting, and maintainable project documentation
- portfolio-relevant thinking around data quality, reporting workflows, and validation traceability

## Quality Signals

The current repository includes:

- direct validator tests for missing values, duplicates, numeric outliers, and time-series gaps
- CLI integration coverage for successful runs and generated failure reports
- shared-service and API tests for success, validation failure, load failure, and write failure flows
- frontend tests for validation submission, reopen flows, and recent-report failure handling
- `pylint`-based linting kept at `10.00/10`

## Architecture At A Glance

Core flow:

1. Load a CSV into a pandas DataFrame.
2. Run deterministic validation checks.
3. Normalize issues into a canonical schema.
4. Build a structured JSON report.
5. Surface the result through either the CLI or the local GUI.

Main components:

- `src/loader.py`
  CSV loading with explicit empty-file and empty-dataset handling
- `src/validator.py`
  missing values, duplicates, outliers, and time-series gap checks
- `src/services/validation_service.py`
  shared orchestration for CLI and GUI flows
- `src/report.py`
  final report construction and persistence
- `src/api/`
  local FastAPI interface for the GUI
- `frontend/`
  React + Vite interface for interactive local use

More detail:
- [Architecture](docs/ARCHITECTURE.md)
- [Feature Inventory](docs/FEATURES.md)
- [User Guide](docs/USER_GUIDE.md)

## Quick Start

### CLI

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt -r requirements-dev.txt

python3 -m src.main \
  --input data/synthetic/sample_missing.csv \
  --output reports/validation_report.json \
  --key-columns ID \
  --value-column VALUE \
  --time-column DATE
```

### GUI

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt -r requirements-dev.txt
make frontend-install

make api-dev
make gui-dev
```

Then open the local Vite URL shown in the terminal.

## Validation Scope

Implemented checks:

- missing values
- duplicate rows based on selected key columns
- numeric outliers using z-score
- time-series gaps based on a selected date column

Current limits:

- one file at a time in the GUI
- AI explanations are placeholders only
- validation thresholds are not yet broadly configurable
- the GUI is intentionally a compact summary interface, not a full report explorer

## Example Output

Each run produces a structured JSON report.

High-level structure:

```json
{
  "report_type": "validation_report",
  "run": {
    "status": "succeeded",
    "stage": "completed"
  },
  "configuration": {
    "key_columns": ["ID"],
    "value_column": "VALUE",
    "time_column": "DATE"
  },
  "dataset": {
    "loaded": true,
    "row_count": 10
  },
  "validation": {
    "status": "failed",
    "executed_checks": [
      "missing_values",
      "duplicate_rows",
      "numeric_outlier",
      "time_series_gap"
    ],
    "issue_count": 1
  },
  "summary": {
    "total_issues": 1
  },
  "issues": [
    {
      "issue_id": "ISSUE-0001",
      "code": "duplicate_rows"
    }
  ]
}
```

The full schema is documented through the codebase and user guide:
- [User Guide](docs/USER_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Decisions](docs/DECISIONS.md)

## Public Repository Notes

- License: [MIT](LICENSE)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- Sprints: [docs/SPRINTS.md](docs/SPRINTS.md)
- Backlog: [docs/BACKLOG.md](docs/BACKLOG.md)
- Test Matrix: [docs/TEST_MATRIX.md](docs/TEST_MATRIX.md)

## Future Direction

Near-term improvements:

- configurable validation thresholds
- richer API integration coverage across persisted-report flows
- direct tests for AI explanation stub output shape

Longer-term direction:

- real AI explanation integration behind the existing interface
- richer report exploration
- batch processing for multiple datasets
