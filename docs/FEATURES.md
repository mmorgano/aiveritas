# Feature Inventory

This inventory tracks user-visible and engineering-relevant capabilities.
Feature IDs are used lightly across roadmap, sprint, backlog, and test documents.

| ID | Feature | Status | Implementation Reference | Test Coverage | Description |
| --- | --- | --- | --- | --- | --- |
| `F-01` | CSV loading | Implemented | `src/loader.py` | Covered | Loads CSV files into pandas DataFrames with explicit file and empty-dataset handling. |
| `F-02` | Missing-value validation | Implemented | `src/validator.py` | Covered | Detects missing values by column and reports affected rows. |
| `F-03` | Duplicate-row validation | Implemented | `src/validator.py` | Covered | Detects duplicates based on selected key columns with case-insensitive column resolution. |
| `F-04` | Numeric outlier validation | Implemented | `src/validator.py` | Covered | Detects numeric outliers using z-score on a selected value column. |
| `F-05` | Time-series gap validation | Implemented | `src/validator.py` | Covered | Detects gaps in a selected date or period column. |
| `F-06` | Structured issue schema | Implemented | `src/schemas.py` | Covered | Uses a canonical issue format across validation, placeholder explanation scaffolding, and reporting. |
| `F-07` | JSON report generation | Implemented | `src/report.py` | Covered | Produces structured report sections for run, configuration, dataset, validation, summary, and issues. |
| `F-08` | Placeholder explanation scaffolding | Secondary | `src/ai_module.py` | Partial | Keeps a non-core placeholder `ai_explanation` field for internal schema compatibility. |
| `F-09` | Sample data generation | Implemented | `scripts/generate_sample_data.py` | Manual | Generates synthetic CSV datasets covering clean and issue-focused scenarios. |
| `F-10` | Local engineering workflow | Implemented | `Makefile`, `pyproject.toml`, `.githooks/pre-commit` | Manual | Provides lint/test workflow, Git hooks, and contributor guidance. |
| `F-11` | CLI integration test coverage | Implemented | `tests/test_cli.py` | Covered | Covers CLI success and missing-input failure flows through `src.main.main()`. |
| `F-12` | Configurable validation thresholds | Planned | Not yet implemented | Missing | Thresholds and rule parameters are still mostly hardcoded. |
| `F-14` | Batch processing | Planned | Not yet implemented | Missing | The CLI currently handles one input file per run. |
| `F-15` | Shared validation orchestration | Implemented | `src/services/validation_service.py`, `src/main.py` | Covered | Reuses one validation pipeline across the CLI and the secondary demo interface. |
| `F-16` | Local FastAPI backend | Secondary | `src/api/app.py`, `src/api/routes.py`, `src/api/schemas.py` | Covered | Supports the local demo interface and report reopening flows. |
| `F-17` | Local React GUI | Secondary | `frontend/src/` | Covered | Provides a small browser-based demo interface for local runs and report review. |
| `F-18` | Recent report history | Secondary | `src/services/history_service.py`, `src/api/app.py` | Covered | Persists a lightweight local index used by the demo interface. |
