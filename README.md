# AIVeritas

AIVeritas is an AI-assisted data validation and anomaly explanation engine for CSV datasets.
It runs rule-based quality checks, builds a structured JSON report, and prepares each issue for future LLM-based explanations through a stub AI module.

## Features

- Load CSV files into pandas DataFrames with explicit error handling.
- Detect missing values by column.
- Detect duplicate rows based on selected key columns.
- Detect numeric outliers using z-score.
- Detect time series gaps for a date or period column.
- Produce a consistent JSON validation report.
- Enrich issues with a placeholder AI explanation payload.
- Generate synthetic sample datasets for local testing.
- Separate runtime status from validation status in the report output.

## Project Documentation

The repository includes a lightweight but maintainable engineering documentation set:

- [docs/ROADMAP.md](/home/morgmau/projects/aiveritas/docs/ROADMAP.md) for project direction and phased evolution
- [docs/SPRINTS.md](/home/morgmau/projects/aiveritas/docs/SPRINTS.md) for completed and planned execution slices
- [docs/BACKLOG.md](/home/morgmau/projects/aiveritas/docs/BACKLOG.md) for prioritized future work
- [docs/FEATURES.md](/home/morgmau/projects/aiveritas/docs/FEATURES.md) for feature inventory and implementation status
- [docs/TEST_MATRIX.md](/home/morgmau/projects/aiveritas/docs/TEST_MATRIX.md) for feature-to-test traceability
- [docs/ARCHITECTURE.md](/home/morgmau/projects/aiveritas/docs/ARCHITECTURE.md) for module responsibilities and data flow
- [docs/DECISIONS.md](/home/morgmau/projects/aiveritas/docs/DECISIONS.md) for lightweight ADRs
- [CHANGELOG.md](/home/morgmau/projects/aiveritas/CHANGELOG.md) for meaningful repository changes

## Folder Structure

```text
aiveritas/
├── data/
│   └── synthetic/
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── BACKLOG.md
│   ├── DECISIONS.md
│   ├── FEATURES.md
│   ├── ROADMAP.md
│   ├── SPRINTS.md
│   ├── TEST_MATRIX.md
│   └── development-guidelines.md
├── .githooks/
│   └── pre-commit
├── scripts/
│   ├── generate_sample_data.py
│   └── install_git_hooks.sh
├── src/
│   ├── __init__.py
│   ├── ai_module.py
│   ├── loader.py
│   ├── main.py
│   ├── report.py
│   ├── schemas.py
│   └── validator.py
├── tests/
│   ├── test_loader.py
│   ├── test_report.py
│   └── test_validator.py
├── README.md
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
python3 -m pip install -r requirements.txt -r requirements-dev.txt
```

3. Install the repository Git hooks.

```bash
make install-hooks
```

4. Generate sample datasets.

```bash
python3 scripts/generate_sample_data.py
```

5. Run tests.

```bash
python3 -m pytest
```

## Development Workflow

Project rules are documented in [docs/development-guidelines.md](/home/morgmau/projects/aiveritas/docs/development-guidelines.md).

Recommended commands:

```bash
make help
make bootstrap
make generate-samples
make lint
make test
make review-check
make check
make ci
```

Workflow expectations:

- After each code writing session, run `make lint` and improve the `pylint` result.
- After each code review pass, run `make lint` again and reduce warnings unless an exception is justified.
- Use `make review-check` when you want one command for lint plus test validation.
- Install the versioned `pre-commit` hook with `make install-hooks` so `make lint` runs automatically before each commit.
- Use [CONTRIBUTING.md](/home/morgmau/projects/aiveritas/CONTRIBUTING.md) as the default contributor workflow.

## CLI Usage

Run the validator with:

```bash
python3 -m src.main \
  --input data/synthetic/sample_missing.csv \
  --output reports/validation_report.json \
  --key-columns ID \
  --value-column VALUE \
  --time-column DATE
```

### Arguments

- `--input`: Path to the input CSV file.
- `--output`: Path to the output JSON report.
- `--key-columns`: One or more columns used for duplicate detection.
- `--value-column`: Numeric column used for z-score outlier detection.
- `--time-column`: Date or period column used for time series gap detection.

## Report Overview

The generated report includes:

- `run`: execution metadata such as status, stage, timestamp, and input path.
- `configuration`: CLI validation settings used for the run.
- `dataset`: dataset metadata, or a safe empty snapshot if loading fails.
- `validation`: validation result state and enabled checks.
- `summary`: counts by severity, category, and issue code.
- `issues`: a canonical issue list with `scope`, `metrics`, `context`, and `ai_explanation`.

## Future Roadmap

- Replace the AI stub with an actual LLM integration layer.
- Add configurable validation thresholds and rule profiles.
- Support batch directory processing.
- Add richer CLI output and logging.
- Expand test coverage for edge cases and integration flows.
