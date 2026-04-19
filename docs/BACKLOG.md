# Backlog

This backlog is intentionally lightweight.
It should capture real next work without pretending the project has a large delivery organization behind it.

## Priority Legend

- `P1`: important next work
- `P2`: useful follow-up work
- `P3`: later or opportunistic work

## Features

### P1

- Add configurable outlier threshold support in the CLI and report output.
- Add configurable duplicate-check profiles for multiple key combinations.
- Add CLI integration tests covering happy path and failure path execution.

### P2

- Add batch processing for validating multiple CSV files in one run.
- Add report output options for per-run metadata enrichment.
- Add optional validation presets for common dataset profiles.

### P3

- Explore support for additional tabular input formats.
- Explore rule plugin hooks for custom validations.

## Technical Debt

### P1

- Reduce duplicated report and workflow descriptions across documentation files.
- Review helper boundaries in schema/report handling to keep responsibilities small.

### P2

- Revisit how validation configuration is passed across CLI, validator, and report modules.
- Decide whether issue dictionaries should remain plain dicts or move toward typed models later.

## Quality Improvements

### P1

- Add tests for numeric outlier detection.
- Add tests for time-series gap detection.
- Add CLI tests for generated failure reports.

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

