"""Response models for the local FastAPI backend."""

from __future__ import annotations

from pydantic import BaseModel

from src.schemas import Report


class HealthResponse(BaseModel):
    """Health check response."""

    status: str


class RecentReportEntryResponse(BaseModel):
    """Recent report metadata exposed by the API."""

    report_id: str
    timestamp: str
    input_name: str
    run_status: str


class RecentReportsResponse(BaseModel):
    """Recent report list response."""

    entries: list[RecentReportEntryResponse]


class ValidationResponse(BaseModel):
    """Validation response using the shared report payload."""

    report_id: str
    report_location: str
    report: Report


class ReopenReportResponse(BaseModel):
    """Reopened report response using the shared report payload."""

    report_id: str
    report_location: str
    report: Report
