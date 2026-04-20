"""Tests for shared validation orchestration."""

from __future__ import annotations

import json

import pandas as pd

from src.services.validation_service import run_validation


def test_run_validation_success_writes_report(tmp_path) -> None:
    """Successful validation runs should save a succeeded report."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "report.json"
    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10.0, 20.0],
        }
    )
    dataframe.to_csv(input_path, index=False)

    result = run_validation(
        input_path=input_path,
        output_path=output_path,
        key_columns=["id"],
        value_column="value",
    )

    assert result.success is True
    assert result.error is None
    assert result.output_path == output_path
    assert output_path.exists()

    with output_path.open(encoding="utf-8") as file_handle:
        report = json.load(file_handle)

    assert report["run"]["status"] == "succeeded"
    assert report["validation"]["status"] == "passed"
    assert report["validation"]["executed_checks"] == [
        "missing_values",
        "duplicate_rows",
        "numeric_outlier",
    ]
    assert report["summary"]["total_issues"] == 0


def test_run_validation_missing_input_creates_failure_report(tmp_path) -> None:
    """Missing input files should still produce a failure report."""
    input_path = tmp_path / "missing.csv"
    output_path = tmp_path / "report.json"

    result = run_validation(
        input_path=input_path,
        output_path=output_path,
    )

    assert result.success is False
    assert isinstance(result.error, FileNotFoundError)
    assert result.output_path == output_path
    assert output_path.exists()

    with output_path.open(encoding="utf-8") as file_handle:
        report = json.load(file_handle)

    assert report["run"]["status"] == "failed"
    assert report["run"]["stage"] == "load"
    assert report["validation"]["status"] == "not_run"
    assert report["issues"][0]["code"] == "file_not_found"


def test_run_validation_validation_failure_creates_failure_report(tmp_path) -> None:
    """Validation-stage errors should be reported without hiding the failure."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "report.json"
    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "value": ["bad", "data"],
        }
    )
    dataframe.to_csv(input_path, index=False)

    result = run_validation(
        input_path=input_path,
        output_path=output_path,
        value_column="value",
    )

    assert result.success is False
    assert isinstance(result.error, TypeError)
    assert result.output_path == output_path
    assert output_path.exists()

    with output_path.open(encoding="utf-8") as file_handle:
        report = json.load(file_handle)

    assert report["run"]["status"] == "failed"
    assert report["run"]["stage"] == "validation"
    assert report["validation"]["status"] == "failed"
    assert report["issues"][0]["code"] == "invalid_numeric_column"


def test_run_validation_save_failure_returns_one_report_attempt(
    tmp_path,
    monkeypatch,
) -> None:
    """Write failures should not retry saving a failure report to the same path."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "report.json"
    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10.0, 20.0],
        }
    )
    dataframe.to_csv(input_path, index=False)

    save_calls = {"count": 0}

    def failing_save_report(_report, _destination):
        """Fail report persistence after the first attempted write."""
        save_calls["count"] += 1
        raise OSError("permission denied")

    monkeypatch.setattr(
        "src.services.validation_service.save_report",
        failing_save_report,
    )

    result = run_validation(
        input_path=input_path,
        output_path=output_path,
    )

    assert result.success is False
    assert isinstance(result.error, OSError)
    assert result.output_path == output_path
    assert not output_path.exists()
    assert save_calls["count"] == 1

    report = result.report
    assert report["run"]["status"] == "failed"
    assert report["run"]["stage"] == "write"
    assert report["validation"]["status"] == "passed"
    assert report["issues"][0]["code"] == "report_write_failure"
