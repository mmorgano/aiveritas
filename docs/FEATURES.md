# Feature Inventory

This inventory tracks user-visible and engineering-relevant capabilities at a level that is easy to maintain.

| Feature | Status | Description |
| --- | --- | --- |
| CSV loading | Implemented | Loads CSV files into pandas DataFrames with explicit file and empty-dataset handling. |
| Missing-value validation | Implemented | Detects missing values by column and reports affected rows. |
| Duplicate-row validation | Implemented | Detects duplicates based on selected key columns with case-insensitive column resolution. |
| Numeric outlier validation | Implemented | Detects numeric outliers using z-score on a selected value column. |
| Time-series gap validation | Implemented | Detects gaps in a selected date or period column. |
| Structured issue schema | Implemented | Uses a canonical issue format across validation, AI enrichment, and reporting. |
| JSON report generation | Implemented | Produces structured report sections for run, configuration, dataset, validation, summary, and issues. |
| AI explanation stub | Implemented | Adds placeholder AI explanations without real LLM integration yet. |
| Sample data generation | Implemented | Generates synthetic CSV datasets covering clean and issue-focused scenarios. |
| Local engineering workflow | Implemented | Provides `make` commands, lint/test workflow, and a versioned pre-commit hook. |
| CLI integration test coverage | Planned | End-to-end CLI validation tests are not yet implemented. |
| Configurable validation thresholds | Planned | Thresholds and rule parameters are still mostly hardcoded. |
| Real AI explanation integration | Planned | The AI module is currently a stub and not connected to an external model. |
| Batch processing | Planned | The CLI currently handles one input file per run. |

