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
| `F-04` | Numeric outlier detection | Implemented | Missing | Not yet added | Should verify threshold behavior and issue metrics. |
| `F-07` | Structured report sections | Implemented | Covered | `tests/test_report.py` | Verifies report envelope and issue IDs. |
| `F-07` | Failed-load report handling | Implemented | Covered | `tests/test_report.py` | Verifies stable report generation without a dataset. |
| `F-06` | Processing error normalization | Implemented | Covered | `tests/test_report.py` | Verifies error-to-issue mapping. |
| `F-15` | Shared validation orchestration success and failure paths | Implemented | Covered | `tests/test_validation_service.py` | Verifies shared execution for success, load failure, validation failure, and write failure. |
| `F-16` | Local API validation and reopen endpoints | Implemented | Covered | `tests/test_api.py` | Verifies health, validate, recent-report, and reopen flows. |
| `F-18` | Recent report history persistence | Implemented | Covered | `tests/test_history_service.py` | Verifies append, trim, malformed-index fallback, and recovery. |
| `F-17` | GUI summary and recent-report interactions | Implemented | Covered | `frontend/src/__tests__/App.test.tsx` | Verifies recent-report loading, validation submit, refresh, reopen, and error handling. |
| `F-11` | CLI success path | Planned | Missing | Not yet added | Currently verified manually, not by automated tests. |
| `F-11` | CLI failure path | Planned | Missing | Not yet added | Failure reports exist but should be covered by tests. |
| `F-08` | AI explanation stub structure | Implemented | Partial | Indirect via `tests/test_report.py` | Should eventually gain direct unit tests. |

## Coverage Priorities

- Add direct tests for numeric outlier detection.
- Add CLI integration tests for success and failure runs.
- Add integration coverage spanning frontend request shape through backend validation execution once the local app surface stabilizes.
- Add direct tests for AI stub output shape once the interface stabilizes further.
