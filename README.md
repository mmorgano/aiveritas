# AIVeritas

AIVeritas is an AI-assisted data validation and anomaly explanation engine for CSV datasets.
It runs rule-based quality checks, builds a structured JSON report, and prepares each issue for future LLM-based explanations through a stub AI module.
The repository now supports both a scriptable CLI and a first-iteration local GUI backed by FastAPI and React.

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
- Run the same validation workflow through either the CLI or the local GUI.
- Reopen a lightweight history of recent reports in the GUI.

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
│   ├── AIVERITAS_RULES.md
│   ├── BACKLOG.md
│   ├── DECISIONS.md
│   ├── FEATURES.md
│   ├── ROADMAP.md
│   ├── SPRINTS.md
│   ├── TEST_MATRIX.md
│   └── development-guidelines.md
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── .githooks/
│   └── pre-commit
├── scripts/
│   ├── generate_sample_data.py
│   └── install_git_hooks.sh
├── src/
│   ├── __init__.py
│   ├── ai_module.py
│   ├── api/
│   ├── loader.py
│   ├── main.py
│   ├── report.py
│   ├── schemas.py
│   ├── services/
│   └── validator.py
├── tests/
│   ├── test_api.py
│   ├── test_history_service.py
│   ├── test_loader.py
│   ├── test_report.py
│   ├── test_validation_service.py
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

2. Install Python dependencies.

```bash
python3 -m pip install -r requirements.txt -r requirements-dev.txt
```

3. Install frontend dependencies.

```bash
make frontend-install
```

4. Install the repository Git hooks.

```bash
make install-hooks
```

5. Generate sample datasets.

```bash
python3 scripts/generate_sample_data.py
```

6. Run tests.

```bash
python3 -m pytest
```

## Development Workflow

Global coding defaults for agents live in [/home/morgmau/.codex/AGENTS.md](/home/morgmau/.codex/AGENTS.md).
Project-specific rules and workflow live in [docs/AIVERITAS_RULES.md](/home/morgmau/projects/aiveritas/docs/AIVERITAS_RULES.md) and [docs/development-guidelines.md](/home/morgmau/projects/aiveritas/docs/development-guidelines.md).

Recommended commands:

```bash
make help
make bootstrap
make generate-samples
make lint
make test
make frontend-test
make api-dev
make gui-dev
make review-check
make check
make ci
```

Workflow expectations:

- Use `make review-check` when you want one command for lint plus test validation.
- Install the versioned `pre-commit` hook with `make install-hooks` so `make lint` runs automatically before each commit.
- Use `make api-dev` and `make gui-dev` in separate terminals for local GUI development.
- Use [CONTRIBUTING.md](/home/morgmau/projects/aiveritas/CONTRIBUTING.md) as the default contributor workflow.
- Treat raw `SESSIONS/` notes as private local workflow rather than public project history.

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

## Local GUI Usage

Start the backend:

```bash
make api-dev
```

In a second terminal, start the frontend:

```bash
make gui-dev
```

Then open the Vite local URL shown in the terminal.
The first iteration supports one CSV file at a time, a minimal summary view, and reopening recent reports stored locally.

## Report Overview

The generated report includes:

- `run`: execution metadata such as status, stage, timestamp, and input path.
- `configuration`: CLI validation settings used for the run.
- `dataset`: dataset metadata, or a safe empty snapshot if loading fails.
- `validation`: validation result state and enabled checks.
- `summary`: counts by severity, category, and issue code.
- `issues`: a canonical issue list with `scope`, `metrics`, `context`, and `ai_explanation`.

Keep the issue and report schema stable unless a deliberate change is documented.

## Future Roadmap

- Replace the AI stub with an actual LLM integration layer.
- Add configurable validation thresholds and rule profiles.
- Support batch directory processing.
- Add richer report review and operational ergonomics across the local interfaces.
- Expand test coverage for edge cases and integration flows.
