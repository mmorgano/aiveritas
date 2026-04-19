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
| `F-11` | CLI success path | Planned | Missing | Not yet added | Currently verified manually, not by automated tests. |
| `F-11` | CLI failure path | Planned | Missing | Not yet added | Failure reports exist but should be covered by tests. |
| `F-08` | AI explanation stub structure | Implemented | Partial | Indirect via `tests/test_report.py` | Should eventually gain direct unit tests. |

## Coverage Priorities

- Add direct tests for numeric outlier detection.
- Add CLI integration tests for success and failure runs.
- Add direct tests for AI stub output shape once the interface stabilizes further.
