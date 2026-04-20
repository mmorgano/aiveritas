"""Tests for the recent report history store."""

from __future__ import annotations

from pathlib import Path

from src.services.history_service import RecentReportStore


def test_recent_report_store_appends_entry(tmp_path: Path) -> None:
    """A stored report should be returned by the history list."""
    store = RecentReportStore(tmp_path / "recent_reports.json")

    store.add_entry(
        report_id="r1",
        report_path=tmp_path / "report.json",
        input_name="input.csv",
        run_status="success",
    )

    entries = store.list_entries()

    assert len(entries) == 1
    assert entries[0]["report_id"] == "r1"
    assert entries[0]["input_name"] == "input.csv"
    assert entries[0]["report_path"] == str(tmp_path / "report.json")
    assert entries[0]["run_status"] == "success"
    assert "timestamp" in entries[0]


def test_recent_report_store_keeps_newest_entries_only(tmp_path: Path) -> None:
    """The history store should trim older entries beyond the limit."""
    store = RecentReportStore(tmp_path / "recent_reports.json", limit=2)

    for index in range(3):
        store.add_entry(
            report_id=f"r{index}",
            report_path=tmp_path / f"report-{index}.json",
            input_name=f"input-{index}.csv",
            run_status="success",
        )

    entries = store.list_entries()

    assert [entry["report_id"] for entry in entries] == ["r2", "r1"]


def test_recent_report_store_recovers_from_malformed_json(tmp_path: Path) -> None:
    """The history store should fall back to empty history for invalid JSON."""
    index_path = tmp_path / "recent_reports.json"
    index_path.write_text("{not valid json", encoding="utf-8")

    store = RecentReportStore(index_path)

    assert not store.list_entries()


def test_recent_report_store_add_entry_recovers_from_malformed_json(
    tmp_path: Path,
) -> None:
    """Adding an entry should replace malformed history with valid JSON."""
    index_path = tmp_path / "recent_reports.json"
    index_path.write_text("{not valid json", encoding="utf-8")

    store = RecentReportStore(index_path)

    store.add_entry(
        report_id="r1",
        report_path=tmp_path / "report.json",
        input_name="input.csv",
        run_status="success",
    )

    entries = store.list_entries()

    assert len(entries) == 1
    assert entries[0]["report_id"] == "r1"
    assert entries[0]["input_name"] == "input.csv"
    assert entries[0]["report_path"] == str(tmp_path / "report.json")
    assert entries[0]["run_status"] == "success"
    assert "timestamp" in entries[0]
