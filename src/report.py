"""Report creation and persistence utilities."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

from src.schemas import (
    assign_issue_ids,
    build_dataset_snapshot,
    listify,
    utc_timestamp,
)


def build_validation_report(
    input_path: str | Path,
    dataframe: pd.DataFrame | None,
    issues: Sequence[dict[str, Any]],
    *,
    run_status: str,
    validation_status: str,
    run_stage: str,
    configuration: dict[str, Any] | None = None,
    executed_checks: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Build the final validation report structure.

    Args:
        input_path: Source CSV path.
        dataframe: Loaded dataset if available.
        issues: Structured validation issues.
        run_status: Runtime status for the CLI execution.
        validation_status: Validation result status.
        run_stage: Last completed or failed stage.
        configuration: Validation configuration snapshot.
        executed_checks: Validation checks requested for the run.

    Returns:
        A JSON-serializable validation report.
    """
    normalized_issues = assign_issue_ids(issues)
    severity_counts = Counter(issue["severity"] for issue in normalized_issues)
    category_counts = Counter(issue["category"] for issue in normalized_issues)
    code_counts = Counter(issue["code"] for issue in normalized_issues)

    return {
        "schema_version": "1.0.0",
        "report_type": "validation_report",
        "project": {
            "name": "aiveritas",
        },
        "run": {
            "generated_at": utc_timestamp(),
            "status": run_status,
            "stage": run_stage,
            "input_path": str(input_path),
        },
        "configuration": {
            "key_columns": listify((configuration or {}).get("key_columns")),
            "value_column": (configuration or {}).get("value_column"),
            "time_column": (configuration or {}).get("time_column"),
        },
        "dataset": build_dataset_snapshot(dataframe),
        "validation": {
            "status": validation_status,
            "executed_checks": listify(executed_checks),
            "issue_count": int(len(normalized_issues)),
        },
        "summary": {
            "total_issues": int(len(normalized_issues)),
            "issues_by_severity": {severity: int(count) for severity, count in severity_counts.items()},
            "issues_by_category": {category: int(count) for category, count in category_counts.items()},
            "issues_by_code": {code: int(count) for code, count in code_counts.items()},
        },
        "issues": normalized_issues,
    }


def save_report(report: dict[str, Any], output_path: str | Path) -> Path:
    """Save the validation report as JSON.

    Args:
        report: Validation report payload.
        output_path: Destination JSON file path.

    Returns:
        The resolved output path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(report, file_handle, indent=2, ensure_ascii=False)

    return path
