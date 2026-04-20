"""FastAPI application factory for the local GUI backend."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from src.api.routes import create_router
from src.services.history_service import RecentReportStore
from src.services.validation_service import ValidationRunResult

DEFAULT_HISTORY_PATH = Path("data/app_state/recent_reports.json")
DEFAULT_REPORTS_DIR = Path("reports")


class LocalReportRepository:
    """Read and track locally persisted validation reports."""

    def __init__(
        self,
        *,
        history_store: RecentReportStore,
        reports_dir: Path,
    ) -> None:
        """Initialize the local report repository."""
        self._history_store = history_store
        self._reports_dir = reports_dir

    def build_report_path(self, report_id: str) -> Path:
        """Return the storage path for a generated report."""
        return self._reports_dir / f"{report_id}.json"

    def record_run(
        self,
        *,
        report_id: str,
        input_name: str,
        result: ValidationRunResult,
    ) -> None:
        """Track a validation run only when a report file exists."""
        if not result.output_path.exists():
            return

        self._history_store.add_entry(
            report_id=report_id,
            report_path=result.output_path,
            input_name=input_name,
            run_status=str(result.report["run"]["status"]),
        )

    def list_recent(self) -> list[dict[str, str]]:
        """Return the stored recent report metadata."""
        return self._history_store.list_entries()

    def load_report(self, report_id: str) -> dict[str, Any] | None:
        """Load a stored report by identifier."""
        entry = next(
            (item for item in self._history_store.list_entries() if item["report_id"] == report_id),
            None,
        )
        if entry is None:
            return None

        report_path = Path(entry["report_path"])
        if not report_path.exists():
            return None

        try:
            with report_path.open(encoding="utf-8") as file_handle:
                report = json.load(file_handle)
        except (JSONDecodeError, OSError, TypeError, ValueError):
            return None

        if not isinstance(report, dict):
            return None

        return dict(report)


def create_app(
    *,
    history_store: RecentReportStore | None = None,
    reports_dir: Path | None = None,
) -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title="AIVeritas API")
    repository = LocalReportRepository(
        history_store=history_store or RecentReportStore(DEFAULT_HISTORY_PATH),
        reports_dir=reports_dir or DEFAULT_REPORTS_DIR,
    )
    app.include_router(
        create_router(
            report_repository=repository,
        )
    )
    return app
