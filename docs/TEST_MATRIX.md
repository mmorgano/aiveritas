# Test Matrix

This matrix maps key capabilities to current automated coverage.
It should stay short enough to maintain during normal feature work.

| Feature ID | Capability | Status | Automated Coverage | Test Location | Notes |
| --- | --- | --- | --- | --- | --- |
| `F-01` | Valid CSV loading | Implemented | Covered | `tests/test_loader.py` | Verifies successful DataFrame loading. |
| `F-01` | Empty dataset rejection | Implemented | Covered | `tests/test_loader.py` | Verifies header-only CSV failure path. |
| `F-02` | Missing-value issue generation | Implemented | Covered | `tests/test_validator.py` | Verifies canonical issue structure. |
| `F-03` | Duplicate-row issue generation | Implemented | Covered | `tests/test_validator.py` | Verifies duplicate scope and entity keys. |
| `F-03` | Case-insensitive key resolution | Implemented | Covered | `tests/test_validator.py` | Verifies relaxed column matching. |
| `F-05` | Time-series gap detection | Implemented | Covered | `tests/test_validator.py` | Verifies gap detection and resolved column name. |
| `F-04` | Numeric outlier detection | Implemented | Covered | `tests/test_validator.py` | Verifies flagged-row issue generation with core outlier metrics. |
| `F-07` | Structured report sections | Implemented | Covered | `tests/test_report.py` | Verifies report envelope and issue IDs. |
| `F-07` | Failed-load report handling | Implemented | Covered | `tests/test_report.py` | Verifies stable report generation without a dataset. |
| `F-06` | Processing error normalization | Implemented | Covered | `tests/test_report.py` | Verifies error-to-issue mapping. |
| `F-15` | Shared validation orchestration success and failure paths | Implemented | Covered | `tests/test_validation_service.py` | Verifies shared execution for the CLI path and the secondary demo interface. |
| `F-16` | Local API validation and reopen endpoints | Secondary | Covered | `tests/test_api.py` | Verifies the local backend used by the browser demo interface. |
| `F-18` | Recent report history persistence | Secondary | Covered | `tests/test_history_service.py` | Verifies the local history index used by the demo interface. |
| `F-17` | GUI summary and recent-report interactions | Secondary | Covered | `frontend/src/__tests__/App.test.tsx` | Verifies recent-report loading, validation submit, refresh, reopen, and error handling in the demo interface. |
| `F-11` | CLI success path | Implemented | Covered | `tests/test_cli.py` | Verifies exit code, stdout, and saved success report generation. |
| `F-11` | CLI failure path | Implemented | Covered | `tests/test_cli.py` | Verifies exit code, stderr, and saved failure report generation for missing input. |
| `F-08` | Placeholder explanation scaffolding | Secondary | Partial | Indirect via `tests/test_report.py` | Kept for schema continuity and not treated as a core v0.1 feature. |

## Coverage Priorities

- Preserve CLI-path coverage as the primary quality signal for v0.1.
- Keep frontend and API tests in CI because those secondary surfaces are still committed and supported locally.
