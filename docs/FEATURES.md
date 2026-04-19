# Feature Inventory

This inventory tracks user-visible and engineering-relevant capabilities.
Feature IDs are used lightly across roadmap, sprint, backlog, and test documents.

| ID | Feature | Status | Implementation Reference | Test Coverage | Description |
| --- | --- | --- | --- | --- | --- |
| `F-01` | CSV loading | Implemented | `src/loader.py` | Covered | Loads CSV files into pandas DataFrames with explicit file and empty-dataset handling. |
| `F-02` | Missing-value validation | Implemented | `src/validator.py` | Covered | Detects missing values by column and reports affected rows. |
| `F-03` | Duplicate-row validation | Implemented | `src/validator.py` | Covered | Detects duplicates based on selected key columns with case-insensitive column resolution. |
| `F-04` | Numeric outlier validation | Implemented | `src/validator.py` | Missing | Detects numeric outliers using z-score on a selected value column. |
| `F-05` | Time-series gap validation | Implemented | `src/validator.py` | Covered | Detects gaps in a selected date or period column. |
| `F-06` | Structured issue schema | Implemented | `src/schemas.py` | Covered | Uses a canonical issue format across validation, AI enrichment, and reporting. |
| `F-07` | JSON report generation | Implemented | `src/report.py` | Covered | Produces structured report sections for run, configuration, dataset, validation, summary, and issues. |
| `F-08` | AI explanation stub | Implemented | `src/ai_module.py` | Partial | Adds placeholder AI explanations without real LLM integration yet. |
| `F-09` | Sample data generation | Implemented | `scripts/generate_sample_data.py` | Manual | Generates synthetic CSV datasets covering clean and issue-focused scenarios. |
| `F-10` | Local engineering workflow | Implemented | `Makefile`, `pyproject.toml`, `.githooks/pre-commit` | Manual | Provides lint/test workflow, Git hooks, and contributor guidance. |
| `F-11` | CLI integration test coverage | Planned | Not yet implemented | Missing | End-to-end CLI validation tests are not yet implemented. |
| `F-12` | Configurable validation thresholds | Planned | Not yet implemented | Missing | Thresholds and rule parameters are still mostly hardcoded. |
| `F-13` | Real AI explanation integration | Planned | Not yet implemented | Missing | The AI module is currently a stub and not connected to an external model. |
| `F-14` | Batch processing | Planned | Not yet implemented | Missing | The CLI currently handles one input file per run. |
