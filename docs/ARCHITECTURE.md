# Architecture

## Overview

AIVeritas is currently a small local CLI application with a modular validation pipeline.
The design keeps deterministic validation logic separate from report generation and future AI integration.

## Main Components

### `src/main.py`

- Parses CLI arguments.
- Orchestrates loading, validation, AI enrichment, and report saving.
- Handles runtime failures and converts them into structured failure reports.

### `src/loader.py`

- Loads CSV files into pandas DataFrames.
- Handles file-not-found, empty-file, and empty-dataset conditions explicitly.

### `src/validator.py`

- Contains modular validation checks.
- Produces canonical issue dictionaries through shared schema helpers.
- Resolves requested column names against dataset columns using strict and relaxed matching rules.

### `src/ai_module.py`

- Provides a placeholder explanation layer.
- Enriches issues with a predictable AI explanation shape.
- Deliberately avoids coupling validation behavior to an external AI provider at this stage.

### `src/report.py`

- Builds the final report envelope.
- Separates runtime metadata from validation results.
- Assigns stable issue identifiers and serializes output to JSON.

### `src/schemas.py`

- Defines the shared issue and report helper logic.
- Normalizes values for JSON serialization.
- Converts runtime exceptions into the same canonical issue format used by validation logic.

## Data Flow

1. The CLI receives file path and validation options.
2. The loader reads the CSV into a DataFrame.
3. The validator runs enabled checks and returns structured issues.
4. The AI stub enriches each issue with placeholder explanation data.
5. The report module builds a structured JSON report and writes it to disk.
6. If loading or validation fails, the failure is converted into a canonical issue and still reported.

## Design Constraints

- Modules should stay small and focused.
- Readability is preferred over clever abstractions.
- The report schema should remain stable as features are added.
- AI integration must remain optional and isolated from deterministic validation logic.

