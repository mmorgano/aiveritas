# User Guide

## Overview

AIVeritas validates structured tabular datasets through:

- a local CLI for scriptable runs
- a local browser-based GUI for interactive runs

It runs deterministic data-quality checks, builds a structured JSON report, and adds placeholder AI explanations to each issue.

Current validation checks:

- missing values
- duplicate rows based on selected key columns
- numeric outliers based on a selected numeric column
- time-series gaps based on a selected date column

## Quick Start

### GUI

Start the local API:

```bash
make api-dev
```

In a second terminal, start the frontend:

```bash
make gui-dev
```

Open the local Vite URL shown in the terminal.

### CLI

Run a validation directly from the command line:

```bash
python3 -m src.main \
  --input data/synthetic/sample_missing.csv \
  --output reports/validation_report.json \
  --key-columns ID \
  --value-column VALUE \
  --time-column DATE
```

## Using The GUI

### 1. Choose a CSV file

- Use the `CSV file` picker to select one local CSV file.
- The selected filename appears below the picker.

### 2. Set validation inputs

- `Key columns`
  Use one or more columns for duplicate detection.
  Example: `ID`
- `Value column`
  Use a numeric column for outlier detection.
  Example: `VALUE`
- `Time column`
  Use a date or period column for time-series gap detection.
  Example: `DATE`

Notes:

- Missing-value validation always runs.
- Duplicate validation runs when `Key columns` is provided.
- Outlier validation runs when `Value column` is provided.
- Time-series-gap validation runs when `Time column` is provided.

### 3. Run validation

- Click `Run validation`.
- The status banner reports whether validation is running, completed, or failed.

## How To Read Results

### Summary section

- `Report ID`
  Unique identifier for the generated report.
- `Input file`
  Name of the CSV file used for the run.
- `Generated at`
  UTC timestamp for report generation.
- `Run status`
  Whether the application flow succeeded or failed.
- `Validation status`
  Whether validation passed or failed based on detected issues.
- `Rows`
  Number of dataset rows loaded into the run.
- `Total issues`
  Number of structured issues found in the report.
- `Saved report`
  Download link for the generated JSON report.

### Executed checks

This section shows which validations actually ran for the current result.

Example:

- `missing_values`
- `duplicate_rows`
- `numeric_outlier`
- `time_series_gap`

### Issues found

Each issue entry shows:

- issue identifier
- human-readable message
- severity and issue code
- columns involved
- row indices when available

If `Total issues` is `1`, it means one structured issue object was produced in the report.
That issue may refer to one or more rows, columns, or entities depending on the validation.

### Recent reports

The right-hand panel keeps a small local history of recent validation runs.

Use `Reopen <filename>` to reopen a previously saved report summary.

## JSON Report

Each run produces a JSON report under the local reports directory.

Typical location:

```text
reports/<report_id>.json
```

The report includes:

- `run`
- `configuration`
- `dataset`
- `validation`
- `summary`
- `issues`

Use the `Download JSON report` link in the GUI if you want the saved file directly.

## Common Scenarios

### Duplicate check

If you select `sample_duplicates.csv` and set:

- `Key columns = ID`
- `Value column = VALUE`
- `Time column = DATE`

then AIVeritas will run:

- missing-value validation
- duplicate detection
- numeric outlier detection
- time-series gap detection

If the summary shows:

- `Validation status = failed`
- `Rows = 10`
- `Total issues = 1`

that means one issue object was created in the final report for that run.

## Current Limits

- The GUI handles one CSV file at a time.
- The GUI is still intentionally minimal.
- The AI module is a stub, not a real model integration.
- Validation thresholds are not yet broadly configurable from the UI.
- The GUI shows a useful summary, not yet a full report explorer.

## Troubleshooting

### Clicking `Run validation` does nothing

Check that both services are running:

```bash
make api-dev
make gui-dev
```

If the local API is not reachable, the GUI should show an explicit error message.

### The report download link is missing

- Make sure the validation actually completed.
- Make sure the backend was able to save the report.
- Check the status banner for write or backend errors.

### A validation does not run

Check whether the related input was provided:

- no `Key columns` -> no duplicate check
- no `Value column` -> no outlier check
- no `Time column` -> no time-series-gap check
