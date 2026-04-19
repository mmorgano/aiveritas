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

## Folder Structure

```text
aiveritas/
├── data/
│   └── synthetic/
├── scripts/
│   └── generate_sample_data.py
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
python3 -m pip install -r requirements.txt
```

3. Generate sample datasets.

```bash
python3 scripts/generate_sample_data.py
```

4. Run tests.

```bash
python3 -m pytest
```

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
