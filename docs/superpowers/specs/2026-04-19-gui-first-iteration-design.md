# AIVeritas GUI First Iteration Design

## Purpose

Add a first graphical interface to AIVeritas without replacing the existing CLI.
The GUI should make the current validation flow easier to use locally while preserving the existing deterministic validation core and report schema.

## Product Goal

The first GUI iteration should provide a local browser-based experience for a single CSV at a time.
It should let a user:

- select a CSV file
- provide the existing validation inputs
- run validation
- view an essential summary of the result
- reopen recent reports from a minimal local history

This iteration is not intended to become a full multi-user platform or a complex operational dashboard.

## Scope

### In Scope

- A local web app
- FastAPI backend as a new interface layer
- React + Vite frontend as a separate UI layer
- Single-file validation flow
- Minimal report summary view
- Minimal local recent-report history
- Reuse of the current validation core and report generation logic

### Out of Scope

- Multi-file validation in one run
- Rich issue exploration UI
- Authentication or user accounts
- Shared server deployment model
- Database-backed persistence
- Real AI integration changes
- Replacing the CLI

## Architectural Direction

The GUI should be implemented as a second interface on top of the current Python core.
The existing CLI remains supported.

### Backend

Use FastAPI as a thin application layer that:

- accepts validation requests from the frontend
- calls internal Python orchestration logic directly
- returns structured responses derived from the canonical report schema
- stores completed reports to disk
- maintains a minimal local history index for recent reports

The backend should not shell out to the CLI as a subprocess for normal operation.
It should reuse shared internal logic so that CLI and GUI stay behaviorally aligned.

### Frontend

Use React + Vite as a separate frontend application that:

- provides a single-page local UI
- sends validation requests to the FastAPI backend
- displays a compact summary of results
- lists recent reports and lets the user reopen them

The frontend should stay intentionally small in the first iteration.
No heavy design system or complex client-side state architecture is required yet.

## User Experience

### Main Screen

The first screen should include three functional areas:

1. Validation form
2. Current result summary
3. Recent reports list

### Validation Form

The form should support the current CLI-equivalent inputs:

- CSV file selection
- key columns
- value column
- time column

The form should remain minimal and readable.
It should not expose advanced validation configuration in this iteration.

### Result Summary

After a validation run, the UI should show only an essential summary, for example:

- run status
- validation status
- input file name
- total issue count
- summary counts by severity or category when available
- output report location or identifier

Detailed issue browsing can remain outside the first iteration.

### Recent Reports

The app should keep a minimal local history of recent reports.
For each recent report, store only:

- local identifier
- timestamp
- input file name
- report file path
- run status

A user should be able to reopen a recent report summary from that history.

## Data and Persistence

### Report Files

Continue saving generated reports as JSON files on disk.
The GUI should reuse the current report-building behavior as much as possible.

### Recent History Index

Store recent-report metadata in a small local JSON index.
A database is unnecessary for this iteration.

A practical direction is:

- keep reports under `reports/`
- keep the recent-history index in a small application state file under a local data directory

The exact path can be finalized during implementation.

## Backend Responsibilities

The FastAPI layer should provide endpoints for:

- running a validation from uploaded input and parameters
- listing recent reports
- reopening one saved report summary
- basic health or readiness information if useful for local development

The backend should also contain a small orchestration layer that adapts requests into existing loader, validator, AI stub, and report flows.

## Frontend Responsibilities

The React frontend should provide:

- a single-page layout
- upload and parameter form handling
- loading and error states
- essential result summary rendering
- recent-report list rendering
- reopen-report interaction

The frontend should be easy to replace or extend later without changing the validation core.

## Design Constraints

- Preserve the canonical issue and report schema.
- Keep deterministic validation logic separate from AI explanation logic.
- Keep the CLI working as a first-class interface.
- Do not duplicate validation rules in the frontend.
- Keep the first iteration smaller than a full dashboard product.
- Favor maintainable boundaries over fast but tangled glue code.

## Repository Direction

A likely repository structure after implementation is:

```text
src/            # existing validation core
src/api/        # FastAPI application layer
frontend/       # React + Vite application
reports/        # saved JSON reports
```

The exact path names can be adjusted if implementation reveals a cleaner fit.

## Testing Expectations

The new GUI architecture should introduce tests in layers:

- backend API tests for request/response behavior
- focused tests for recent-history persistence
- frontend tests only where they add real confidence
- existing core tests should remain valid

The first iteration should prioritize backend and integration confidence over UI test volume.

## Risks and Mitigations

### Risk: GUI logic drifts from CLI behavior

Mitigation:
Create a shared orchestration path used by both interfaces where practical.

### Risk: The GUI grows into a second product too early

Mitigation:
Limit the first release to single-file execution, minimal summary, and minimal recent history.

### Risk: Persistence becomes too complex too early

Mitigation:
Use report files plus a simple local JSON history index instead of a database.

### Risk: Frontend complexity outpaces product clarity

Mitigation:
Keep the UI to one main screen and avoid premature component abstraction.

## Traceability Impact

If this design is accepted and implemented, the project documentation should later be updated in:

- `docs/ROADMAP.md`
- `docs/SPRINTS.md`
- `docs/FEATURES.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `docs/TEST_MATRIX.md`

## Success Criteria

The first GUI iteration is successful if:

- a user can run AIVeritas locally through a browser UI
- the GUI validates one CSV at a time using the same core behavior as the CLI
- the GUI shows a minimal useful summary of the result
- the GUI lets the user reopen recent report summaries from local history
- the CLI and report schema remain intact
