# Backlog

This backlog is intentionally lightweight.
It should capture real next work without pretending the project has a large delivery organization behind it.

## Priority Legend

- `P1`: important next work
- `P2`: useful follow-up work
- `P3`: later or opportunistic work

## Maintenance Rules

- Keep backlog items short and implementation-aware.
- If an item becomes implemented, move the status to `docs/FEATURES.md` and adjust `docs/SPRINTS.md` or `CHANGELOG.md` as needed.
- If an item changes architecture or workflow materially, reflect it in `docs/DECISIONS.md`.

## Features

### P1

- Add configurable outlier threshold support in the CLI and report output.
  Related feature: `F-12`
- Add configurable duplicate-check profiles for multiple key combinations.
  Related feature: `F-12`
- Add CLI integration tests covering happy path and failure path execution.
  Related feature: `F-11`
- Add API integration tests that exercise the shared validation service with persisted reports.
  Related features: `F-15`, `F-16`

### P2

- Add batch processing for validating multiple CSV files in one run.
  Related feature: `F-14`
- Add report output options for per-run metadata enrichment.
- Add optional validation presets for common dataset profiles.
- Add a richer report-detail view in the GUI once report sections stabilize.
  Related feature: `F-17`

### P3

- Explore support for additional tabular input formats.
- Explore rule plugin hooks for custom validations.

## Technical Debt

### P1

- Reduce duplicated report and workflow descriptions across documentation files.
- Review helper boundaries in schema/report handling to keep responsibilities small.
- Decide whether local app-state paths should become configurable once the GUI grows beyond a single-machine workflow.
  Related feature: `F-18`

### P2

- Revisit how validation configuration is passed across CLI, validator, and report modules.
- Decide whether issue dictionaries should remain plain dicts or move toward typed models later.
- Review whether frontend API types should be generated or remain hand-maintained once the API surface grows.

## Quality Improvements

### P1

- Add tests for numeric outlier detection.
  Related feature: `F-04`
- Add tests for time-series gap detection.
  Related feature: `F-05`
- Add CLI tests for generated failure reports.
  Related feature: `F-11`
- Add frontend smoke coverage for recent-report loading failures and empty-state behavior.
  Related feature: `F-17`

### P2

- Add lint-driven cleanup for any new warnings introduced by future work.
- Add regression tests for case-insensitive column resolution edge cases.

## Documentation Tasks

### P1

- Keep `TEST_MATRIX.md` aligned with every new feature and test file.
- Update `DECISIONS.md` when a design choice changes behavior or maintainability.

### P2

- Add release notes discipline once the first tagged version exists.
- Add example report snippets to the README after the report schema stabilizes further.
