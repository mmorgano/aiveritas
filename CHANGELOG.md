# Changelog

All meaningful changes to AIVeritas should be recorded in this file.

The format is intentionally lightweight and closer to Keep a Changelog than to release-note prose.

## [Unreleased]

### Added

- Initial AIVeritas CLI workflow for CSV validation and JSON report generation.
- CSV loader with explicit handling for missing files, empty files, and empty datasets.
- Validation checks for missing values, duplicate rows, numeric outliers, and time-series gaps.
- Canonical issue schema shared across validation, failure handling, AI enrichment, and reporting.
- Placeholder AI explanation module for future model integration.
- Synthetic sample dataset generator.
- Automated tests for loader, validator, and report behavior.
- Developer workflow support through `Makefile`, `pyproject.toml`, lint/test commands, and Git hooks.
- Project-management and architecture documentation set under `docs/`.
- Lightweight traceability between roadmap, sprint planning, feature inventory, test coverage, and ADRs.
- Shared validation orchestration used by both CLI and GUI-oriented flows.
- Local FastAPI backend for validation runs, recent reports, and report reopening.
- React + Vite frontend for local CSV validation and minimal report review.
- Lightweight recent-report history persisted under local application state.
- Automated tests for validation service, history persistence, local API routes, and frontend behavior.

### Changed

- Report output was structured into explicit `run`, `configuration`, `dataset`, `validation`, `summary`, and `issues` sections.
- Contributor workflow was formalized through repository-level documentation and quality gates.
- Public repository documentation was aligned to keep raw session logs private while preserving durable engineering history.
- The architecture evolved from CLI-only delivery to a dual local-interface model while keeping the CLI supported.
