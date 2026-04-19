"""Validation functions for AIVeritas datasets."""

from __future__ import annotations

from collections import Counter
from typing import Any, Sequence

import pandas as pd

from src.schemas import build_issue, to_serializable_value

ValidationIssue = dict[str, Any]


def check_missing_values(dataframe: pd.DataFrame) -> list[ValidationIssue]:
    """Detect missing values by column.

    Args:
        dataframe: Dataset to validate.

    Returns:
        A list of structured issues describing missing values.
    """
    issues: list[ValidationIssue] = []
    row_count = len(dataframe)

    for column_name in dataframe.columns:
        missing_mask = dataframe[column_name].isna()
        missing_count = int(missing_mask.sum())

        if missing_count == 0:
            continue

        affected_rows = [
            to_serializable_value(index)
            for index in dataframe.index[missing_mask].tolist()
        ]
        issues.append(
            build_issue(
                code="missing_values",
                category="completeness",
                severity="warning",
                message=f"Column '{column_name}' contains missing values.",
                columns=[str(column_name)],
                row_indices=affected_rows,
                metrics={
                    "affected_row_count": missing_count,
                    "missing_ratio": round(missing_count / row_count, 4),
                },
            )
        )

    return issues


def check_duplicate_rows(
    dataframe: pd.DataFrame,
    key_columns: Sequence[str],
) -> list[ValidationIssue]:
    """Detect duplicate rows using a selected set of key columns.

    Args:
        dataframe: Dataset to validate.
        key_columns: Columns that define uniqueness.

    Returns:
        A list of structured issues describing duplicate groups.

    Raises:
        ValueError: If one or more key columns are missing from the dataset.
    """
    if not key_columns:
        return []

    resolved_key_columns = _resolve_column_names(dataframe, key_columns)

    duplicate_mask = dataframe.duplicated(subset=resolved_key_columns, keep=False)
    if not duplicate_mask.any():
        return []

    duplicate_groups = dataframe.loc[duplicate_mask].groupby(
        resolved_key_columns,
        dropna=False,
        sort=False,
    )
    issues: list[ValidationIssue] = []

    for group_key, group_frame in duplicate_groups:
        normalized_key = group_key if isinstance(group_key, tuple) else (group_key,)
        issues.append(
            build_issue(
                code="duplicate_rows",
                category="uniqueness",
                severity="error",
                message="Duplicate rows detected for the selected key columns.",
                columns=[str(column) for column in resolved_key_columns],
                row_indices=[
                    to_serializable_value(index)
                    for index in group_frame.index.tolist()
                ],
                entity_keys={
                    str(column_name): _to_python_value(value)
                    for column_name, value in zip(resolved_key_columns, normalized_key)
                },
                metrics={
                    "affected_row_count": int(len(group_frame)),
                    "duplicate_count": int(len(group_frame)),
                },
                context={
                    "key_columns": [str(column) for column in resolved_key_columns],
                },
            )
        )

    return issues


def check_numeric_outliers(
    dataframe: pd.DataFrame,
    value_column: str | None,
    z_score_threshold: float = 3.0,
) -> list[ValidationIssue]:
    """Detect numeric outliers using z-score.

    Args:
        dataframe: Dataset to validate.
        value_column: Numeric column to analyze.
        z_score_threshold: Absolute z-score threshold for flagging outliers.

    Returns:
        A list of structured issues describing numeric outliers.

    Raises:
        ValueError: If the target column does not exist.
        TypeError: If the target column is not numeric.
    """
    if not value_column:
        return []

    resolved_value_column = _resolve_column_name(dataframe, value_column)

    series = dataframe[resolved_value_column]
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError(
            f"Column must be numeric for outlier detection: {resolved_value_column}"
        )

    numeric_series = series.dropna()
    if numeric_series.empty or len(numeric_series) < 2:
        return []

    standard_deviation = float(numeric_series.std(ddof=0))
    if standard_deviation == 0:
        return []

    mean_value = float(numeric_series.mean())
    z_scores = (numeric_series - mean_value) / standard_deviation
    outlier_mask = z_scores.abs() > z_score_threshold

    issues: list[ValidationIssue] = []
    for row_index, z_score in z_scores[outlier_mask].items():
        issues.append(
            build_issue(
                code="numeric_outlier",
                category="anomaly_detection",
                severity="warning",
                message=f"Potential numeric outlier detected in column '{resolved_value_column}'.",
                columns=[str(resolved_value_column)],
                row_indices=[to_serializable_value(row_index)],
                metrics={
                    "affected_row_count": 1,
                    "value": to_serializable_value(
                        dataframe.at[row_index, resolved_value_column]
                    ),
                    "z_score": round(float(z_score), 4),
                    "threshold": z_score_threshold,
                    "mean": round(mean_value, 4),
                    "stddev": round(standard_deviation, 4),
                },
            )
        )

    return issues


def check_time_series_gaps(
    dataframe: pd.DataFrame,
    time_column: str | None,
) -> list[ValidationIssue]:
    """Detect gaps in a time series column.

    Args:
        dataframe: Dataset to validate.
        time_column: Date or period column to analyze.

    Returns:
        A list of structured issues describing time series gaps.

    Raises:
        ValueError: If the target column is missing or cannot be parsed as dates.
    """
    if not time_column:
        return []

    resolved_time_column = _resolve_column_name(dataframe, time_column)

    try:
        timestamp_series = pd.to_datetime(dataframe[resolved_time_column], errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Column must contain parseable date values: {resolved_time_column}"
        ) from error

    unique_timestamps = pd.Series(
        timestamp_series.dropna().drop_duplicates().sort_values().tolist()
    )
    if len(unique_timestamps) < 2:
        return []

    time_deltas = unique_timestamps.diff().dropna()
    if time_deltas.empty:
        return []

    expected_delta = time_deltas.mode().iloc[0]
    if expected_delta <= pd.Timedelta(0):
        return []

    issues: list[ValidationIssue] = []
    for previous_value, current_value in zip(unique_timestamps[:-1], unique_timestamps[1:]):
        gap_delta = current_value - previous_value
        if gap_delta <= expected_delta:
            continue

        missing_points = pd.date_range(
            start=previous_value + expected_delta,
            end=current_value - expected_delta,
            freq=expected_delta,
        )
        issues.append(
            build_issue(
                code="time_series_gap",
                category="timeliness",
                severity="warning",
                message=f"Gap detected in time series column '{resolved_time_column}'.",
                columns=[str(resolved_time_column)],
                metrics={
                    "affected_row_count": int(len(missing_points)),
                    "expected_interval": _timedelta_to_string(expected_delta),
                },
                context={
                    "gap_start": previous_value.isoformat(),
                    "gap_end": current_value.isoformat(),
                    "missing_points": [timestamp.isoformat() for timestamp in missing_points],
                },
            )
        )

    return issues


def run_validations(
    dataframe: pd.DataFrame,
    key_columns: Sequence[str] | None = None,
    value_column: str | None = None,
    time_column: str | None = None,
) -> list[ValidationIssue]:
    """Run all configured validations and collect issues.

    Args:
        dataframe: Dataset to validate.
        key_columns: Columns used for duplicate detection.
        value_column: Numeric column used for outlier detection.
        time_column: Date or period column used for gap detection.

    Returns:
        A flat list of structured validation issues.
    """
    issues: list[ValidationIssue] = []
    issues.extend(check_missing_values(dataframe))
    issues.extend(check_duplicate_rows(dataframe, key_columns or []))
    issues.extend(check_numeric_outliers(dataframe, value_column))
    issues.extend(check_time_series_gaps(dataframe, time_column))
    return issues


def summarize_issues(issues: Sequence[ValidationIssue]) -> dict[str, int]:
    """Build a summary of issues by type.

    Args:
        issues: Validation issues to summarize.

    Returns:
        A dictionary keyed by issue type.
    """
    counts = Counter(issue["code"] for issue in issues)
    return {issue_type: int(count) for issue_type, count in counts.items()}


def _resolve_column_names(dataframe: pd.DataFrame, column_names: Sequence[str]) -> list[str]:
    """Resolve a list of requested column names against the dataset columns."""
    return [_resolve_column_name(dataframe, column_name) for column_name in column_names]


def _resolve_column_name(dataframe: pd.DataFrame, column_name: str) -> str:
    """Resolve a requested column name using strict and relaxed matching rules."""
    available_columns = [str(candidate) for candidate in dataframe.columns.tolist()]

    if column_name in available_columns:
        return column_name

    matching_strategies = [
        lambda candidate: candidate.casefold() == column_name.casefold(),
        lambda candidate: _normalize_column_name(candidate) == _normalize_column_name(column_name),
        lambda candidate: _requested_tokens_match(column_name, candidate),
    ]

    for matcher in matching_strategies:
        matches = [candidate for candidate in available_columns if matcher(candidate)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            formatted_matches = ", ".join(matches)
            raise ValueError(
                f"Ambiguous column reference '{column_name}'. Matching columns: {formatted_matches}"
            )

    formatted_columns = ", ".join(available_columns)
    raise ValueError(
        f"Missing required columns: {column_name}. "
        f"Available columns: {formatted_columns}"
    )


def _to_python_value(value: Any) -> Any:
    """Convert pandas and NumPy scalar values to JSON-friendly Python types."""
    return to_serializable_value(value)


def _timedelta_to_string(time_delta: pd.Timedelta) -> str:
    """Convert a pandas Timedelta to a readable string."""
    total_seconds = int(time_delta.total_seconds())
    return f"{total_seconds}s"


def _normalize_column_name(column_name: str) -> str:
    """Normalize a column name for relaxed comparisons."""
    return "".join(character for character in column_name.casefold() if character.isalnum())


def _requested_tokens_match(requested_name: str, candidate_name: str) -> bool:
    """Check whether requested name tokens uniquely describe a candidate column."""
    requested_tokens = _split_column_tokens(requested_name)
    candidate_tokens = _split_column_tokens(candidate_name)

    if not requested_tokens or not candidate_tokens:
        return False

    return requested_tokens.issubset(candidate_tokens)


def _split_column_tokens(column_name: str) -> set[str]:
    """Split a column name into normalized alphanumeric tokens."""
    token = []
    tokens: set[str] = set()

    for character in column_name.casefold():
        if character.isalnum():
            token.append(character)
            continue

        if token:
            tokens.add("".join(token))
            token = []

    if token:
        tokens.add("".join(token))

    return tokens
