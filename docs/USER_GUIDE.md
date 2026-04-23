# User Guide

## Overview

AIVeritas is a local CSV validation tool.

For v0.1, the primary workflow is the CLI:

- run validation locally
- save a structured JSON report
- use the process exit code to detect success or failure

The repository also includes a small local API and browser demo interface, but they are secondary support surfaces, not the primary product workflow.

## Primary Workflow: CLI

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt -r requirements-dev.txt
```

### Run a validation

```bash
python3 -m src.main \
  --input data/synthetic/sample_missing.csv \
  --output reports/validation_report.json \
  --key-columns ID \
  --value-column VALUE \
  --time-column DATE
```

### CLI arguments

- `--input`
  Path to the input CSV file.
- `--output`
  Path where the JSON report will be written.
- `--key-columns`
  One or more columns used for duplicate detection.
- `--value-column`
  Numeric column used for outlier detection.
- `--time-column`
  Date or period column used for time-series gap detection.

### Validation rules

- Missing-value validation always runs.
- Duplicate validation runs when `--key-columns` is provided.
- Outlier validation runs when `--value-column` is provided.
- Time-series-gap validation runs when `--time-column` is provided.

### Exit codes

- `0`: the validation run completed and a report was written
- `1`: the run failed and a failure report was written when possible

Note:
- A completed run can still contain validation issues.
- In that case, the JSON report will show `validation.status = failed` even though the CLI process itself completed successfully.

## Example Inputs

Sample CSV inputs are kept under `data/synthetic/`:

- `sample_clean.csv`
- `sample_missing.csv`
- `sample_duplicates.csv`
- `sample_outliers.csv`
- `sample_timeseries_gap.csv`

These files are intended for local testing and demonstration.

## JSON Report

Each run produces a JSON report.

Typical output location:

```text
reports/<name>.json
```

The current report structure includes:

- `run`
- `configuration`
- `dataset`
- `validation`
- `summary`
- `issues`

An example report using the current schema is committed at `examples/sample_validation_report.json`.

## Interpreting Results

### Run section

- `run.status`
  Whether the application flow succeeded or failed.
- `run.stage`
  The last completed or failed stage.
- `run.input_path`
  Input path used for the run.

### Validation section

- `validation.status`
  Whether validation passed or failed based on detected issues.
- `validation.executed_checks`
  Which checks actually ran.
- `validation.issue_count`
  Number of issue objects generated for the run.

### Summary section

- `summary.total_issues`
  Total number of issue objects in the report.

### Issues section

Each issue includes:

- a stable issue identifier
- a machine-readable issue code
- a severity
- a message
- scope data such as columns and row indices

The current schema still contains an `ai_explanation` placeholder object on issues. This is non-core scaffolding and should not be treated as a real v0.1 feature.

## Secondary Demo Interface

The repository also includes:

- a local FastAPI backend
- a small React + Vite browser interface

This interface is useful for local demonstration, but it is intentionally secondary in v0.1.

### Run the local demo interface

Install frontend dependencies:

```bash
make frontend-install
```

Start the local API:

```bash
make api-dev
```

In a second terminal, start the frontend:

```bash
make gui-dev
```

Open the local Vite URL shown in the terminal.

### Demo interface limits

- One CSV file at a time
- Minimal summary view
- Lightweight recent-report reopening
- No full report explorer

## Troubleshooting

### The CLI exits with an error

Check:

- the input path exists
- the output path is writable
- the selected columns exist in the CSV
- the value column is numeric if outlier detection is enabled
- the time column contains parseable date values if time-gap detection is enabled

### The report file is missing

Check:

- the `--output` path is valid
- the destination directory is writable
- the process did not fail during the write stage

### The local demo interface cannot connect

Check that both processes are running:

```bash
make api-dev
make gui-dev
```

If the local API is not reachable, the demo interface should show an explicit error message.
