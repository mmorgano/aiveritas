"""Tests for report generation utilities."""

from __future__ import annotations

import pandas as pd

from src.ai_module import explain_issue
from src.report import build_validation_report
from src.schemas import build_issue, build_processing_issue


def test_build_validation_report_uses_structured_sections() -> None:
    """The report should separate run, dataset, validation, and summary sections."""
    dataframe = pd.DataFrame({"ID": [1, 2], "VALUE": [10.0, None]})
    issue = build_issue(
        code="missing_values",
        category="completeness",
        severity="warning",
        message="Column 'VALUE' contains missing values.",
        columns=["VALUE"],
        row_indices=[1],
        metrics={"affected_row_count": 1},
    )
    issue["ai_explanation"] = explain_issue(issue)

    report = build_validation_report(
        "data/sample.csv",
        dataframe,
        [issue],
        run_status="succeeded",
        validation_status="failed",
        run_stage="completed",
        configuration={
            "key_columns": ["ID"],
            "value_column": "VALUE",
            "time_column": None,
        },
        executed_checks=["missing_values", "duplicate_rows", "numeric_outlier"],
    )

    assert report["schema_version"] == "1.0.0"
    assert report["run"]["status"] == "succeeded"
    assert report["dataset"]["loaded"] is True
    assert report["validation"]["status"] == "failed"
    assert report["summary"]["issues_by_code"] == {"missing_values": 1}
    assert report["issues"][0]["issue_id"] == "ISSUE-0001"
    assert report["issues"][0]["ai_explanation"]["status"] == "placeholder"


def test_build_validation_report_handles_failed_loads() -> None:
    """The report should remain valid when dataset loading fails."""
    issue = build_issue(
        code="file_not_found",
        category="pipeline",
        severity="error",
        message="CSV file not found: missing.csv",
        stage="load",
        context={"input_path": "missing.csv"},
    )

    report = build_validation_report(
        "missing.csv",
        None,
        [issue],
        run_status="failed",
        validation_status="not_run",
        run_stage="load",
        configuration={},
        executed_checks=["missing_values"],
    )

    assert report["run"]["status"] == "failed"
    assert report["dataset"]["loaded"] is False
    assert report["validation"]["status"] == "not_run"
    assert report["summary"]["issues_by_category"] == {"pipeline": 1}


def test_build_processing_issue_maps_loader_errors_consistently() -> None:
    """Runtime exceptions should map into the canonical issue contract."""
    issue = build_processing_issue(
        FileNotFoundError("CSV file not found: missing.csv"),
        input_path="missing.csv",
        stage="load",
    )

    assert issue["code"] == "file_not_found"
    assert issue["category"] == "pipeline"
    assert issue["stage"] == "load"
    assert issue["context"]["input_path"] == "missing.csv"
