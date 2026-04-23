# Roadmap

## Product Positioning

AIVeritas is a local CSV validation tool with deterministic data-quality checks, CLI as the primary interface, JSON reporting, and a small local demo interface.

## v0.1 Scope

Status: `Current release target`

Primary goals:

- keep the CLI as the only primary workflow
- keep JSON report output stable and reviewable
- keep validation behavior deterministic and local
- keep the demo interface clearly secondary

Included in v0.1:

- CSV loading with explicit failure handling
- missing-value validation
- duplicate-row validation
- numeric outlier validation
- time-series-gap validation
- structured JSON report generation
- CLI success and failure exit behavior
- sample CSV inputs
- local API and GUI as secondary demo/support interfaces

Not included in v0.1:

- real AI features
- external services or database persistence
- cloud deployment
- batch processing
- broad runtime configurability for validation rules

## Near-Term Follow-Up

Candidate work after v0.1:

- configurable validation thresholds
- tighter CLI ergonomics
- broader failure-path coverage where useful
- small improvements to the secondary demo interface without changing product scope

## Traceability

- Feature-level implementation status: `docs/FEATURES.md`
- Test coverage alignment: `docs/TEST_MATRIX.md`
- Architectural decisions: `docs/DECISIONS.md`
- Candidate follow-up work: `docs/BACKLOG.md`
