"""Routes for the local FastAPI backend."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Protocol
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from src.api.schemas import (
    HealthResponse,
    RecentReportEntryResponse,
    RecentReportsResponse,
    ReopenReportResponse,
    ValidationResponse,
)
from src.services.validation_service import ValidationRunResult, run_validation


class ReportRepository(Protocol):
    """Repository contract used by the local API routes."""

    def build_report_path(self, report_id: str) -> Path:
        """Return the storage path for a generated report."""

    def record_run(
        self,
        *,
        report_id: str,
        input_name: str,
        result: ValidationRunResult,
    ) -> None:
        """Track a completed validation run."""

    def list_recent(self) -> list[dict[str, str]]:
        """Return recent report metadata."""

    def load_report(self, report_id: str) -> dict[str, Any] | None:
        """Load a stored report."""


def create_router(
    *,
    report_repository: ReportRepository,
) -> APIRouter:
    """Create the API router."""
    router = APIRouter(prefix="/api")
    repository = report_repository

    @router.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        """Return a simple health response."""
        return HealthResponse(status="ok")

    @router.post("/validate", response_model=ValidationResponse)
    async def validate(
        file: UploadFile = File(...),
        key_columns: str = Form(""),
        value_column: str = Form(""),
        time_column: str = Form(""),
    ) -> ValidationResponse:
        """Validate an uploaded CSV and persist the generated report."""
        filename = Path(file.filename or "input.csv").name

        try:
            with TemporaryDirectory() as temp_dir:
                input_path = Path(temp_dir) / filename
                input_path.write_bytes(await file.read())

                report_id = str(uuid4())
                report_path = repository.build_report_path(report_id)
                result = run_validation(
                    input_path=input_path,
                    output_path=report_path,
                    key_columns=_split_columns(key_columns),
                    value_column=value_column.strip() or None,
                    time_column=time_column.strip() or None,
                )
                repository.record_run(
                    report_id=report_id,
                    input_name=filename,
                    result=result,
                )
        finally:
            await file.close()

        return ValidationResponse(
            report_id=report_id,
            report=result.report,
        )

    @router.get("/reports/recent", response_model=RecentReportsResponse)
    async def recent_reports() -> RecentReportsResponse:
        """Return the stored recent report entries."""
        entries = [
            RecentReportEntryResponse(
                report_id=entry["report_id"],
                timestamp=entry["timestamp"],
                input_name=entry["input_name"],
                run_status=entry["run_status"],
            )
            for entry in repository.list_recent()
        ]
        return RecentReportsResponse(entries=entries)

    @router.get("/reports/{report_id}", response_model=ReopenReportResponse)
    async def reopen_report(report_id: str) -> ReopenReportResponse:
        """Reload a stored report by identifier."""
        report = repository.load_report(report_id)
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found.",
            )

        return ReopenReportResponse(report_id=report_id, report=report)

    return router


def _split_columns(raw_columns: str) -> list[str]:
    """Parse a comma-delimited column list from a form field."""
    return [column.strip() for column in raw_columns.split(",") if column.strip()]
