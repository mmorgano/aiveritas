"""Tests for the local FastAPI backend."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from src.api.app import create_app
from src.services.history_service import RecentReportStore
from src.services.validation_service import ValidationRunResult


async def _build_client(
    *,
    tmp_path: Path,
    history_store: RecentReportStore | None = None,
    reports_dir: Path | None = None,
) -> httpx.AsyncClient:
    """Build an HTTP client bound to the local ASGI app."""
    app = create_app(
        history_store=history_store or RecentReportStore(tmp_path / "recent_reports.json"),
        reports_dir=reports_dir or tmp_path / "reports",
    )
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")


@pytest.mark.anyio
async def test_health_endpoint_returns_ok(tmp_path: Path) -> None:
    """The health endpoint should return a minimal OK payload."""
    async with await _build_client(tmp_path=tmp_path) as client:
        response = await client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_validate_endpoint_returns_report_and_tracks_history(tmp_path: Path) -> None:
    """Validation should return the shared report payload and persist history."""
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("ID,DATE,VALUE\n1,2026-01-01,10\n", encoding="utf-8")
    reports_dir = tmp_path / "reports"
    history_store = RecentReportStore(tmp_path / "recent_reports.json")
    async with await _build_client(
        tmp_path=tmp_path,
        history_store=history_store,
        reports_dir=reports_dir,
    ) as client:
        with csv_path.open("rb") as input_file:
            response = await client.post(
                "/api/validate",
                files={"file": ("input.csv", input_file, "text/csv")},
                data={
                    "key_columns": "ID",
                    "value_column": "VALUE",
                    "time_column": "DATE",
                },
            )

        body = response.json()

        assert response.status_code == 200
        assert body["report"]["run"]["status"] == "succeeded"
        assert body["report"]["validation"]["status"] == "passed"

    entries = history_store.list_entries()
    assert len(entries) == 1
    assert entries[0]["report_id"] == body["report_id"]
    assert entries[0]["input_name"] == "input.csv"
    assert entries[0]["run_status"] == "succeeded"
    assert Path(entries[0]["report_path"]).exists()


@pytest.mark.anyio
async def test_validate_endpoint_skips_history_when_report_was_not_persisted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """History should stay empty when validation finishes without a saved report."""
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("ID,VALUE\n1,10\n", encoding="utf-8")
    history_store = RecentReportStore(tmp_path / "recent_reports.json")
    failed_report = {
        "run": {"status": "failed", "stage": "write"},
        "validation": {"status": "passed"},
        "issues": [{"code": "report_write_failure"}],
    }

    def fake_run_validation(**_: object) -> ValidationRunResult:
        """Return a failed validation result without a persisted file."""
        return ValidationRunResult(
            success=False,
            output_path=tmp_path / "reports" / "missing.json",
            report=failed_report,
            error=OSError("permission denied"),
        )

    monkeypatch.setattr("src.api.routes.run_validation", fake_run_validation)

    async with await _build_client(
        tmp_path=tmp_path,
        history_store=history_store,
        reports_dir=tmp_path / "reports",
    ) as client:
        with csv_path.open("rb") as input_file:
            response = await client.post(
                "/api/validate",
                files={"file": ("input.csv", input_file, "text/csv")},
            )

        assert response.status_code == 200
        assert response.json()["report"]["run"]["status"] == "failed"

    assert not history_store.list_entries()


@pytest.mark.anyio
async def test_recent_reports_endpoint_returns_entries(tmp_path: Path) -> None:
    """Recent reports should expose the stored report metadata."""
    history_store = RecentReportStore(tmp_path / "recent_reports.json")
    history_store.add_entry(
        report_id="r1",
        report_path=tmp_path / "reports" / "r1.json",
        input_name="input.csv",
        run_status="succeeded",
    )
    async with await _build_client(
        tmp_path=tmp_path,
        history_store=history_store,
        reports_dir=tmp_path / "reports",
    ) as client:
        response = await client.get("/api/reports/recent")

        assert response.status_code == 200
        assert response.json()["entries"][0]["report_id"] == "r1"
        assert "report_path" not in response.json()["entries"][0]


@pytest.mark.anyio
async def test_reopen_report_endpoint_returns_report_payload(tmp_path: Path) -> None:
    """Stored report entries should be reopenable by report identifier."""
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    report_path = reports_dir / "r1.json"
    report_path.write_text(
        (
            '{"report_type": "validation_report", "run": {"status": "succeeded"}, '
            '"validation": {"status": "passed"}}'
        ),
        encoding="utf-8",
    )
    history_store = RecentReportStore(tmp_path / "recent_reports.json")
    history_store.add_entry(
        report_id="r1",
        report_path=report_path,
        input_name="input.csv",
        run_status="succeeded",
    )
    async with await _build_client(
        tmp_path=tmp_path,
        history_store=history_store,
        reports_dir=reports_dir,
    ) as client:
        response = await client.get("/api/reports/r1")

        assert response.status_code == 200
        assert response.json()["report_id"] == "r1"
        assert response.json()["report"]["run"]["status"] == "succeeded"


@pytest.mark.anyio
async def test_reopen_report_endpoint_returns_not_found_for_unknown_report(
    tmp_path: Path,
) -> None:
    """Unknown report identifiers should return a 404."""
    async with await _build_client(tmp_path=tmp_path) as client:
        response = await client.get("/api/reports/missing")

        assert response.status_code == 404
        assert response.json()["detail"] == "Report not found."


@pytest.mark.anyio
async def test_reopen_report_endpoint_returns_not_found_for_malformed_report_json(
    tmp_path: Path,
) -> None:
    """Malformed stored report files should be treated as missing."""
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    report_path = reports_dir / "r1.json"
    report_path.write_text("{not valid json", encoding="utf-8")
    history_store = RecentReportStore(tmp_path / "recent_reports.json")
    history_store.add_entry(
        report_id="r1",
        report_path=report_path,
        input_name="input.csv",
        run_status="succeeded",
    )

    async with await _build_client(
        tmp_path=tmp_path,
        history_store=history_store,
        reports_dir=reports_dir,
    ) as client:
        response = await client.get("/api/reports/r1")

        assert response.status_code == 404
        assert response.json()["detail"] == "Report not found."
