"""Tests for validation utilities."""

from __future__ import annotations

import pandas as pd

from src.validator import (
    check_duplicate_rows,
    check_missing_values,
    check_numeric_outliers,
    check_time_series_gaps,
)


def test_check_missing_values_returns_structured_issue() -> None:
    """Missing-value validation should describe the affected column and rows."""
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "value": [10.0, None, 30.0],
        }
    )

    issues = check_missing_values(dataframe)

    assert len(issues) == 1
    assert issues[0]["code"] == "missing_values"
    assert issues[0]["category"] == "completeness"
    assert issues[0]["scope"]["columns"] == ["value"]
    assert issues[0]["scope"]["row_indices"] == [1]
    assert issues[0]["metrics"]["affected_row_count"] == 1


def test_check_duplicate_rows_returns_duplicate_group_issue() -> None:
    """Duplicate validation should report duplicate groups for the given keys."""
    dataframe = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "value": [10, 10, 30],
        }
    )

    issues = check_duplicate_rows(dataframe, key_columns=["id"])

    assert len(issues) == 1
    assert issues[0]["code"] == "duplicate_rows"
    assert issues[0]["scope"]["entity_keys"] == {"id": 1}
    assert issues[0]["metrics"]["affected_row_count"] == 2
    assert issues[0]["scope"]["row_indices"] == [0, 1]


def test_check_duplicate_rows_matches_key_column_case_insensitively() -> None:
    """Duplicate validation should resolve key columns case-insensitively."""
    dataframe = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "value": [10, 10, 30],
        }
    )

    issues = check_duplicate_rows(dataframe, key_columns=["ID"])

    assert len(issues) == 1
    assert issues[0]["scope"]["columns"] == ["id"]
    assert issues[0]["scope"]["entity_keys"] == {"id": 1}


def test_check_numeric_outliers_returns_structured_issue_for_flagged_row() -> None:
    """Outlier validation should report the flagged row and core metrics."""
    dataframe = pd.DataFrame(
        {
            "value": [10, 11, 12, 13, 100],
        }
    )

    issues = check_numeric_outliers(
        dataframe,
        value_column="value",
        z_score_threshold=1.5,
    )

    assert len(issues) == 1
    assert issues[0]["code"] == "numeric_outlier"
    assert issues[0]["scope"]["columns"] == ["value"]
    assert issues[0]["scope"]["row_indices"] == [4]
    assert "z_score" in issues[0]["metrics"]


def test_check_time_series_gaps_matches_unique_date_token() -> None:
    """Time-gap validation should resolve a unique date-like column token."""
    dataframe = pd.DataFrame(
        {
            "event_date": ["2026-01-01", "2026-01-02", "2026-01-04"],
            "value": [10, 11, 12],
        }
    )

    issues = check_time_series_gaps(dataframe, time_column="DATE")

    assert len(issues) == 1
    assert issues[0]["scope"]["columns"] == ["event_date"]
    assert issues[0]["metrics"]["affected_row_count"] == 1
