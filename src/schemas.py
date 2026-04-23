"""Shared schema helpers for AIVeritas issues and reports."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd

Issue = dict[str, Any]
Report = dict[str, Any]


def build_issue(
    *,
    code: str,
    category: str,
    severity: str,
    message: str,
    stage: str = "validation",
    columns: Sequence[str] | None = None,
    row_indices: Sequence[Any] | None = None,
    entity_keys: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
    context: dict[str, Any] | None = None,
    ai_explanation: dict[str, Any] | None = None,
) -> Issue:
    """Build a canonical issue payload.

    Args:
        code: Stable machine-readable issue code.
        category: Issue category such as completeness or uniqueness.
        severity: Severity level.
        message: Human-readable issue summary.
        stage: Pipeline stage that produced the issue.
        columns: Columns in scope for the issue.
        row_indices: Row indices related to the issue.
        entity_keys: Entity or business keys related to the issue.
        metrics: Numeric or structured metrics for the issue.
        context: Additional context that does not fit the reserved sections.
        ai_explanation: Optional placeholder explanation payload.

    Returns:
        A normalized issue dictionary.
    """
    return {
        "issue_id": None,
        "stage": stage,
        "code": code,
        "category": category,
        "severity": severity,
        "message": message,
        "scope": {
            "columns": [str(column_name) for column_name in columns or []],
            "row_indices": [to_serializable_value(value) for value in row_indices or []],
            "entity_keys": {
                str(key): to_serializable_value(value) for key, value in (entity_keys or {}).items()
            },
        },
        "metrics": normalize_mapping(metrics),
        "context": normalize_mapping(context),
        "ai_explanation": normalize_mapping(ai_explanation) if ai_explanation else None,
    }


def assign_issue_ids(issues: Sequence[Issue]) -> list[Issue]:
    """Assign stable sequential identifiers to issues.

    Args:
        issues: Issue list to normalize.

    Returns:
        A new issue list with assigned identifiers.
    """
    normalized_issues: list[Issue] = []

    for index, issue in enumerate(issues, start=1):
        normalized_issue = build_issue(
            code=str(issue.get("code", "unknown_issue")),
            category=str(issue.get("category", "uncategorized")),
            severity=str(issue.get("severity", "warning")),
            message=str(issue.get("message", "")),
            stage=str(issue.get("stage", "validation")),
            columns=issue.get("scope", {}).get("columns", []),
            row_indices=issue.get("scope", {}).get("row_indices", []),
            entity_keys=issue.get("scope", {}).get("entity_keys", {}),
            metrics=issue.get("metrics", {}),
            context=issue.get("context", {}),
            ai_explanation=issue.get("ai_explanation"),
        )
        normalized_issue["issue_id"] = str(issue.get("issue_id") or f"ISSUE-{index:04d}")
        normalized_issues.append(normalized_issue)

    return normalized_issues


def build_dataset_snapshot(dataframe: pd.DataFrame | None) -> dict[str, Any]:
    """Build dataset metadata for the report.

    Args:
        dataframe: Loaded dataset or None if loading failed.

    Returns:
        Dataset metadata dictionary.
    """
    if dataframe is None:
        return {
            "loaded": False,
            "row_count": None,
            "column_count": None,
            "columns": [],
        }

    return {
        "loaded": True,
        "row_count": int(len(dataframe)),
        "column_count": int(len(dataframe.columns)),
        "columns": [str(column_name) for column_name in dataframe.columns.tolist()],
    }


def build_processing_issue(
    error: Exception,
    *,
    input_path: str | Path,
    stage: str,
) -> Issue:
    """Convert a runtime exception into the canonical issue schema.

    Args:
        error: Caught exception instance.
        input_path: Input file path related to the error.
        stage: Pipeline stage where the error happened.

    Returns:
        A canonical issue dictionary.
    """
    code, category = infer_issue_identity(error, stage)
    return build_issue(
        code=code,
        category=category,
        severity="error",
        message=str(error),
        stage=stage,
        metrics={},
        context={
            "input_path": str(input_path),
            "exception_type": type(error).__name__,
        },
    )


def infer_issue_identity(error: Exception, stage: str) -> tuple[str, str]:
    """Infer issue identity from an exception.

    Args:
        error: Exception instance.
        stage: Pipeline stage where the error occurred.

    Returns:
        Tuple of issue code and category.
    """
    message = str(error).casefold()

    if isinstance(error, FileNotFoundError):
        return "file_not_found", "pipeline"

    if "ambiguous column reference" in message or "missing required columns" in message:
        return "invalid_column_reference", "configuration"

    if "numeric for outlier detection" in message:
        return "invalid_numeric_column", "configuration"

    if "parseable date values" in message:
        return "invalid_time_column", "configuration"

    if "csv file is empty" in message:
        return "empty_file", "pipeline"

    if "csv dataset is empty" in message:
        return "empty_dataset", "pipeline"

    if stage == "load":
        return "load_failure", "pipeline"

    return "validation_failure", "pipeline"


def normalize_mapping(mapping: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize a dictionary into JSON-serializable values.

    Args:
        mapping: Mapping to normalize.

    Returns:
        Normalized mapping.
    """
    normalized_mapping: dict[str, Any] = {}

    for key, value in (mapping or {}).items():
        normalized_mapping[str(key)] = to_serializable_value(value)

    return normalized_mapping


def to_serializable_value(value: Any) -> Any:
    """Convert common pandas and NumPy values into JSON-friendly Python types.

    Args:
        value: Value to convert.

    Returns:
        JSON-friendly Python value.
    """
    if isinstance(value, dict):
        return {str(key): to_serializable_value(item) for key, item in value.items()}

    if isinstance(value, (list, tuple, set)):
        return [to_serializable_value(item) for item in value]

    if value is None:
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, pd.Timedelta):
        return f"{int(value.total_seconds())}s"

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, np.generic):
        return value.item()

    if pd.isna(value):
        return None

    return value


def utc_timestamp() -> str:
    """Build a UTC ISO timestamp string."""
    return datetime.now(timezone.utc).isoformat()


def listify(values: Iterable[str] | None) -> list[str]:
    """Convert a string iterable into a list of strings."""
    return [str(value) for value in values or []]
