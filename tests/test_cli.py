"""CLI integration tests for AIVeritas."""

from __future__ import annotations

import json

from src.main import main


def test_main_returns_zero_and_writes_report_for_valid_input(
    tmp_path,
    capsys,
) -> None:
    """The CLI should save a report and exit successfully for valid input."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "report.json"
    input_path.write_text(
        "ID,VALUE,DATE\n1,10,2026-01-01\n2,20,2026-01-02\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--key-columns",
            "ID",
            "--value-column",
            "VALUE",
            "--time-column",
            "DATE",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Validation report saved to" in captured.out
    assert captured.err == ""
    assert report["run"]["status"] == "succeeded"
    assert report["validation"]["status"] == "passed"


def test_main_returns_one_and_writes_failure_report_for_missing_input(
    tmp_path,
    capsys,
) -> None:
    """The CLI should emit an error and save a failure report for missing input."""
    input_path = tmp_path / "missing.csv"
    output_path = tmp_path / "report.json"

    exit_code = main(
        [
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 1
    assert captured.out == ""
    assert "Error: CSV file not found:" in captured.err
    assert report["run"]["status"] == "failed"
    assert report["run"]["stage"] == "load"
    assert report["issues"][0]["code"] == "file_not_found"
