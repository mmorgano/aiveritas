# Project Summary

## 1. One-sentence description

AIVeritas is a local CSV validation and JSON reporting tool with a Python CLI, a local FastAPI backend, and a minimal React GUI for running deterministic data-quality checks.

## 2. Intended purpose
- Validate tabular CSV datasets before they are used in reporting or operational workflows.
- Catch a small fixed set of data-quality problems: missing values, duplicate rows, numeric outliers, and time-series gaps.
- Persist a machine-readable JSON report instead of relying on ad hoc spreadsheet inspection.
- Demonstrate disciplined engineering around validation, reporting, test coverage, and interface separation.
- Likely target user: a solo developer, analyst, or technically comfortable operator validating local datasets on one machine.

## 3. Current shape of the project
- Project type: local application, not a deployable SaaS or reusable library.
- Entry points: `src/main.py` for CLI, `src/api/app.py` for FastAPI app creation, `frontend/src/main.tsx` and `frontend/src/App.tsx` for the browser UI.
- Main modules: `src/loader.py`, `src/validator.py`, `src/schemas.py`, `src/report.py`, `src/ai_module.py`, `src/services/validation_service.py`, `src/services/history_service.py`, `src/api/routes.py`.
- Interfaces: CLI, local HTTP API, local React GUI.
- Persistence: JSON reports under `reports/`; recent-report index under `data/app_state/recent_reports.json`.
- External dependencies: Python uses `pandas`, `numpy`, `fastapi`, `uvicorn`, `python-multipart`; frontend uses React, Vite, Vitest; dev tooling uses `pytest`, `pylint`, `httpx`.

## 4. What already works
- The Python validation core exists and is concrete, not aspirational: `src/validator.py` implements missing-value, duplicate-row, numeric outlier, and time-series-gap checks.
- The report model is real and reasonably consistent: `src/report.py` builds a structured report with run, configuration, dataset, validation, summary, and issues sections.
- The shared service layer is real: `src/services/validation_service.py` runs load -> validate -> AI stub enrichment -> report persistence and is used by both CLI and API paths.
- The CLI is functional: `src/main.py` parses arguments, runs validation, prints success to stdout, and returns non-zero on failure.
- The local API is functional: `src/api/routes.py` exposes health, validate, reopen recent report, recent report list, and report download endpoints.
- The GUI is functional at a basic level: `frontend/src/App.tsx` supports file upload, validation submission, recent report refresh, and reopening saved reports.
- Automated tests provide real evidence, not just claims:
- `make test` passed locally with `29 passed`.
- `make frontend-test` passed locally with `8 passed`.
- The repository contains realistic sample data generation in `scripts/generate_sample_data.py`.

## 5. What is incomplete or unclear
- The AI layer is explicitly fake. `src/ai_module.py` is a stub that always returns placeholder explanations. This is not a feature yet; it is scaffolding.
- The project positions itself as “AI-extendable”, but the current value is entirely deterministic validation. The AI story is branding, not capability.
- Validation configurability is thin. The outlier threshold is hardcoded in code paths and not exposed through CLI/API/GUI configuration.
- The GUI is intentionally narrow: one file at a time, summary view only, no real report exploration, no advanced validation controls.
- CI is incomplete relative to the project shape. `.github/workflows/ci.yml` runs only Python tests, not frontend tests, not frontend build, and not lint.
- There are stale or inconsistent artifacts in the root:
- `report.json` and `report_import.json` use an older report schema than the current `src/report.py` output.
- `reports/` contains generated sample reports that look more like local artifacts than durable project assets.
- `templates/` exists but appears empty, which makes it look abandoned or vestigial.
- `docs/` is thorough, but some of the planning/documentation volume is heavier than the implementation complexity and risks overstating maturity.

## 6. Architecture reconstruction
### Components
- `src/loader.py`: CSV ingestion with explicit handling for missing files, empty files, and empty datasets.
- `src/validator.py`: deterministic validation checks plus column-resolution helpers.
- `src/schemas.py`: canonical issue/report helper layer and serialization normalization.
- `src/report.py`: report assembly and JSON persistence.
- `src/ai_module.py`: placeholder issue enrichment only.
- `src/services/validation_service.py`: orchestration layer shared by CLI and API.
- `src/services/history_service.py`: local recent-report metadata store for GUI reopen flows.
- `src/api/`: HTTP transport layer for the local frontend.
- `frontend/src/`: minimal SPA for upload, run, summary, and reopen actions.

### Data flow
- CLI path:
- CSV path and options enter `src/main.py`.
- `run_validation()` in `src/services/validation_service.py` loads the file, runs validations, enriches issues with stub AI data, builds a report, and writes JSON to disk.
- API path:
- Uploaded CSV is temporarily written to disk in `src/api/routes.py`.
- The same `run_validation()` service is called with a generated report path.
- Successful persisted runs are indexed in `data/app_state/recent_reports.json`.
- GUI path:
- `frontend/src/api.ts` sends multipart form data to `/api/validate`, fetches recent reports from `/api/reports/recent`, and reopens saved reports via `/api/reports/{id}`.

### Execution flow
- Runtime model is local and single-user.
- CLI usage is direct Python execution via `src.main`.
- API usage is local FastAPI via `uvicorn`.
- GUI usage depends on a separately running Vite dev server plus the local API server.
- There is no evidence of packaging as a distributable CLI app, no deployment config, no database, and no remote service model.

## 7. Code quality and maintainability review
- Strengths:
- The core modules are small and mostly single-purpose.
- The validation/reporting boundary is cleaner than average for a small project.
- The shared service layer avoids duplicating validation logic across CLI and API.
- Error handling is explicit and converted into reportable issues instead of silently failing.
- Test coverage is broad enough to support the current small scope.
- Weaknesses:
- The project has three interfaces for a still-small validation engine, which increases surface area faster than it increases core value.
- The AI stub adds conceptual weight without delivering user value.
- The frontend has no linting, no typed backend client generation, and no real end-to-end integration coverage.
- CI does not reflect the full project anymore now that frontend code exists.
- Technical debt:
- Root-level old report artifacts (`report.json`, `report_import.json`) conflict with the canonical current schema.
- Documentation and planning apparatus are comparatively large for the amount of implemented domain logic.
- The report schema is dictionary-based everywhere; acceptable at this size, but future growth will become brittle if the schema expands much further.
- Red flags:
- The repository risks becoming a “portfolio architecture project” rather than a sharper product if AI, GUI, API, CLI, ADRs, backlog, and roadmap all keep growing together.
- The strongest working part is the deterministic validator, but the repo narrative still spends attention on future AI integration.
- Some generated/local-state directories exist in-tree (`reports/`, `data/app_state/`), which is fine for local work but weakens the signal if the repo is presented as a polished product.

## 8. Publishability assessment
- Current maturity: close to a believable local v0.1 if framed honestly as a local CSV validation tool, not as an AI product.
- Closest possible v0.1: a local validator with CLI as primary interface, optional local GUI, four deterministic checks, structured JSON report output, sample datasets, and passing Python/frontend tests.
- Estimated missing pieces:
- Remove or clearly quarantine stale generated artifacts.
- Tighten the release story so the README, sample outputs, CI, and actual supported workflow match.
- Decide whether the GUI is part of v0.1 or just an optional demo interface.
- Main blockers:
- Scope ambiguity more than code failure.
- The project already runs, but its narrative is split between validation tool, local app, and future AI platform.
- If you keep all three ambitions alive at once, completion will keep drifting.

## 9. Scope reduction proposal
List only the minimum features needed to reach a demonstrable v0.1.

- CSV loading with explicit failure handling.
- Deterministic checks for missing values, duplicates, outliers, and time-series gaps.
- Canonical JSON report generation.
- A single supported execution path: CLI first.
- Sample CSV datasets and one or two canonical example reports.
- Automated Python tests covering success and failure flows.
- Optional: keep the local GUI only if it is explicitly framed as secondary and demo-grade.
- Cut from v0.1 scope: real AI integration, batch processing, richer report explorer, configurable rule presets, multi-interface expansion beyond local use.

## 10. Final recommendation
Choose one:
- Finish now

## Appendix: Key files to read first
- `README.md`: best high-level statement of the intended product and current scope.
- `src/services/validation_service.py`: the actual center of gravity of the application.
- `src/validator.py`: the real product logic lives here.
- `src/report.py`: defines the actual output contract.
- `src/api/routes.py`: shows what the GUI/API surface really supports.
- `frontend/src/App.tsx`: shows how thin or substantial the GUI actually is.
- `tests/test_validation_service.py`: best evidence that the shared flow works across success and failure cases.
- `.github/workflows/ci.yml`: shows the mismatch between current project scope and what CI actually verifies.
