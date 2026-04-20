# Architecture

## Overview

AIVeritas is currently a small local validation application with two local interfaces:

- a CLI entry point for scriptable usage
- a browser-based GUI backed by a local FastAPI service

The design keeps deterministic validation logic separate from interface layers, report generation, and future AI integration.

Related ADRs:

- `ADR-001` local CLI first
- `ADR-002` canonical issue schema
- `ADR-003` AI stub before real integration
- `ADR-004` pytest and pylint as quality gates
- `ADR-005` private session logs, public durable artifacts
- `ADR-007` local GUI as a secondary interface over the shared validation core

## Main Components

### `src/main.py`

- Parses CLI arguments.
- Delegates execution to the shared validation service.
- Preserves the scriptable local CLI interface.

### `src/services/validation_service.py`

- Provides shared orchestration for deterministic validation, AI stub enrichment, and report persistence.
- Returns structured run results that can be consumed by both CLI and API layers.
- Centralizes error-to-report behavior so interfaces do not reimplement validation flow.

### `src/services/history_service.py`

- Persists a lightweight recent-report index under local application state.
- Keeps GUI history concerns separate from report generation and validation logic.

### `src/api/`

- Exposes the local FastAPI application used by the GUI.
- Accepts file uploads and validation parameters.
- Returns report payloads, recent-report metadata, and reopenable stored reports.
- Keeps HTTP-specific request and response handling outside the validation core.

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

### `frontend/`

- Provides the React + Vite single-page GUI.
- Calls the local API for validation and recent-report actions.
- Keeps presentation logic, form state, and lightweight client-side error handling outside the Python core.

## Data Flow

### CLI flow

1. The CLI receives file path and validation options.
2. `src/main.py` calls the shared validation service.
3. The loader reads the CSV into a DataFrame.
4. The validator runs enabled checks and returns structured issues.
5. The AI stub enriches each issue with placeholder explanation data.
6. The report module builds a structured JSON report and writes it to disk.

### GUI flow

1. The React frontend submits a CSV file and validation options to the local FastAPI backend.
2. The API layer stores the upload temporarily and calls the shared validation service.
3. The validation service builds and persists the report through the same core flow used by the CLI.
4. The API records the run in recent-report history when persistence succeeds.
5. The frontend displays a minimal summary or reopens a stored recent report.

## Design Constraints

- Modules should stay small and focused.
- Readability is preferred over clever abstractions.
- The report schema should remain stable as features are added.
- AI integration must remain optional and isolated from deterministic validation logic.
- The CLI must remain usable even as the local GUI grows.
- GUI-specific state should stay out of deterministic validation modules.

## Traceability Notes

- Architecture changes should be reflected in `docs/DECISIONS.md`.
- Feature-level implementation status belongs in `docs/FEATURES.md`, not here.
- Test coverage expectations for architectural behavior belong in `docs/TEST_MATRIX.md`.
