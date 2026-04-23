# AIVeritas

AIVeritas is a local CSV validation tool with deterministic data-quality checks, CLI as the primary interface, JSON reporting, and a small local demo interface.

It is intended for local validation runs where a saved, machine-readable report is more useful than ad hoc spreadsheet inspection.

## Features

- CSV loading with explicit handling for missing files, empty files, and empty datasets
- Deterministic validation checks for:
  - missing values
  - duplicate rows
  - numeric outliers
  - time-series gaps
- Structured JSON report generation with stable top-level sections
- CLI exit codes for success and failure
- Sample CSV datasets for local demonstration
- Optional local API and browser demo interface built on the same validation core

## What v0.1 Includes

- A local Python CLI as the primary supported workflow
- JSON reports written to disk
- Automated Python tests for loader, validator, reporting, CLI, service, and API flows
- A small local demo interface kept in the repository as a secondary support surface

## What v0.1 Does Not Include

- No real AI features
- No external services or database
- No cloud or multi-user deployment model
- No batch processing
- No broadly configurable validation thresholds yet

The codebase still contains an `ai_explanation` placeholder field in reports for internal schema compatibility, but it is not part of the v0.1 product scope.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt -r requirements-dev.txt
```

Optional, only if you want to run the local demo interface:

```bash
make frontend-install
```

## Primary Workflow: CLI

Run a validation directly from the command line:

```bash
python3 -m src.main \
  --input data/synthetic/sample_missing.csv \
  --output reports/validation_report.json \
  --key-columns ID \
  --value-column VALUE \
  --time-column DATE
```
Example output:
```bash
Validation report saved to reports/validation_report.json
```

Expected behavior:

1. The CSV is loaded from `--input`.
2. Enabled deterministic checks are executed.
3. A JSON report is written to `--output`.
4. The process exits with `0` on a successful run and `1` when the run fails.

## Example Input and Output

Example input datasets are kept under [`data/synthetic/`](data/synthetic).

- Clean sample: [`data/synthetic/sample_clean.csv`](data/synthetic/sample_clean.csv)
- Missing values sample: [`data/synthetic/sample_missing.csv`](data/synthetic/sample_missing.csv)
- Duplicate rows sample: [`data/synthetic/sample_duplicates.csv`](data/synthetic/sample_duplicates.csv)
- Outliers sample: [`data/synthetic/sample_outliers.csv`](data/synthetic/sample_outliers.csv)
- Time-series gap sample: [`data/synthetic/sample_timeseries_gap.csv`](data/synthetic/sample_timeseries_gap.csv)

A committed example report using the current schema is available at [`examples/sample_validation_report.json`](examples/sample_validation_report.json).

High-level report structure:

```json
{
  "schema_version": "1.0.0",
  "report_type": "validation_report",
  "run": {
    "status": "succeeded",
    "stage": "completed",
    "input_path": "data/synthetic/sample_missing.csv"
  },
  "dataset": {
    "loaded": true,
    "row_count": 10,
    "column_count": 4
  },
  "validation": {
    "status": "failed",
    "executed_checks": [
      "missing_values",
      "duplicate_rows",
      "numeric_outlier",
      "time_series_gap"
    ],
    "issue_count": 2
  },
  "summary": {
    "total_issues": 2,
    "issues_by_severity": {
      "warning": 2
    }
  },
  "issues": [
    {
      "issue_id": "ISSUE-0001",
      "code": "missing_values",
      "severity": "warning",
      "message": "Column 'VALUE' contains missing values."
    }
  ]
}
```
Note:

The full report contains additional fields such as detailed scope, metrics, and contextual metadata.
The ai_explanation field may appear in the report as placeholder scaffolding, but it is not part of the v0.1 feature set.


## Secondary Demo Interface

The repository also includes:

- a local FastAPI backend under `src/api/`
- a small React + Vite browser interface under `frontend/`

These are secondary demo/support interfaces for local use. They are not the primary product surface for v0.1.

If you want to run them:

```bash
make api-dev
make gui-dev
```

More detail is available in [docs/USER_GUIDE.md](docs/USER_GUIDE.md).

## Project Structure

- `src/main.py`: CLI entry point
- `src/loader.py`: CSV loading
- `src/validator.py`: deterministic validation checks
- `src/schemas.py`: canonical issue/report helpers
- `src/report.py`: report assembly and persistence
- `src/services/validation_service.py`: shared execution flow
- `src/api/`: local API used by the demo interface
- `frontend/`: local browser demo interface
- `tests/`: Python test suite
- `data/synthetic/`: sample CSV inputs
- `examples/`: intentional example output artifacts

## Limitations

- CLI is the only primary workflow in v0.1.
- The browser interface is intentionally small and secondary.
- One dataset is processed per run.
- Validation thresholds are mostly hardcoded.
- The current checks are limited to missing values, duplicates, outliers, and time-series gaps.
- The project is local-only and has no remote execution model.

## Development and Verification

Useful commands from the repository root:

```bash
make lint
make test
make frontend-test
```

The CI workflow runs Python linting, Python tests, and frontend tests.

## Documentation

- [User Guide](docs/USER_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Feature Inventory](docs/FEATURES.md)
- [Test Matrix](docs/TEST_MATRIX.md)
- [Decisions](docs/DECISIONS.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)
