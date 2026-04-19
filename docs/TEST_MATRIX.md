# Test Matrix

This matrix maps key capabilities to current automated coverage.
It should stay short enough to maintain during normal feature work.

| Capability | Status | Automated Coverage | Test Location | Notes |
| --- | --- | --- | --- | --- |
| Valid CSV loading | Implemented | Covered | `tests/test_loader.py` | Verifies successful DataFrame loading. |
| Empty dataset rejection | Implemented | Covered | `tests/test_loader.py` | Verifies header-only CSV failure path. |
| Missing-value issue generation | Implemented | Covered | `tests/test_validator.py` | Verifies canonical issue structure. |
| Duplicate-row issue generation | Implemented | Covered | `tests/test_validator.py` | Verifies duplicate scope and entity keys. |
| Case-insensitive key resolution | Implemented | Covered | `tests/test_validator.py` | Verifies relaxed column matching. |
| Time-series gap detection | Implemented | Covered | `tests/test_validator.py` | Verifies gap detection and resolved column name. |
| Numeric outlier detection | Implemented | Missing | Not yet added | Should verify threshold behavior and issue metrics. |
| Structured report sections | Implemented | Covered | `tests/test_report.py` | Verifies report envelope and issue IDs. |
| Failed-load report handling | Implemented | Covered | `tests/test_report.py` | Verifies stable report generation without a dataset. |
| Processing error normalization | Implemented | Covered | `tests/test_report.py` | Verifies error-to-issue mapping. |
| CLI success path | Implemented | Missing | Not yet added | Currently verified manually, not by automated tests. |
| CLI failure path | Implemented | Missing | Not yet added | Failure reports exist but should be covered by tests. |
| AI explanation stub structure | Implemented | Partial | Indirect via `tests/test_report.py` | Should eventually gain direct unit tests. |

## Coverage Priorities

- Add direct tests for numeric outlier detection.
- Add CLI integration tests for success and failure runs.
- Add direct tests for AI stub output shape once the interface stabilizes further.

