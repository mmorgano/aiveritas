# Architecture

## Overview

AIVeritas is a small local validation application.

For v0.1, the intended product shape is:

- CLI as the primary interface
- deterministic validation logic in the Python core
- JSON report generation as the main output
- a local API and browser UI kept as secondary demo/support interfaces

The design keeps validation logic separate from interface layers and report persistence.

## Main Components

### `src/main.py`

- Parses CLI arguments.
- Calls the shared validation service.
- Defines the primary supported workflow for v0.1.

### `src/services/validation_service.py`

- Provides shared orchestration for loading, validation, placeholder explanation enrichment, and report persistence.
- Returns structured run results to the CLI and local API.
- Keeps the core execution path in one place.

### `src/loader.py`

- Loads CSV files into pandas DataFrames.
- Handles file-not-found, empty-file, and empty-dataset conditions explicitly.

### `src/validator.py`

- Contains the deterministic validation checks.
- Produces canonical issue dictionaries through shared schema helpers.
- Resolves requested column names against dataset columns.

### `src/schemas.py`

- Defines shared issue and report helper logic.
- Normalizes values for JSON serialization.
- Converts runtime exceptions into the canonical issue structure.

### `src/report.py`

- Builds the final report envelope.
- Separates runtime metadata from validation results.
- Assigns stable issue identifiers and serializes output to JSON.

### `src/ai_module.py`

- Provides non-core placeholder explanation scaffolding.
- Exists to preserve a stable internal issue shape.
- Is not part of the primary v0.1 product story.

### `src/api/`

- Exposes the local FastAPI application used by the browser demo interface.
- Accepts file uploads and validation parameters.
- Returns report payloads and recent-report metadata.

### `src/services/history_service.py`

- Persists a lightweight recent-report index under local application state.
- Supports reopening reports from the secondary demo interface.

### `frontend/`

- Provides the React + Vite browser demo interface.
- Calls the local API for validation and report reopening.
- Is intentionally secondary to the CLI.

## Data Flow

### Primary CLI flow

1. The user runs `src.main` with an input CSV path and output report path.
2. `src/main.py` calls the shared validation service.
3. The loader reads the CSV into a DataFrame.
4. The validator runs the enabled deterministic checks.
5. The report module builds a structured JSON report and writes it to disk.
6. The CLI prints a success or error message and exits with the appropriate code.

### Secondary demo flow

1. The browser demo submits a CSV file and options to the local FastAPI backend.
2. The API layer stores the upload temporarily and calls the same shared validation service.
3. The service writes a report to disk.
4. The API stores recent-report metadata and returns the report payload.

## Design Constraints

- The CLI must remain the primary supported interface.
- Deterministic validation logic should stay independent from interface-specific code.
- The report schema should remain stable as features are added.
- The local API and browser UI should remain optional support surfaces.
- Placeholder explanation scaffolding should not drive product scope.
