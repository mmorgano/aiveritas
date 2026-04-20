"""Recent report history storage for local GUI use."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(slots=True)
class RecentReportEntry:
    """Metadata stored for a recent validation report."""

    report_id: str
    timestamp: str
    input_name: str
    report_path: str
    run_status: str


class RecentReportStore:
    """Persist and retrieve recent report metadata in a JSON file."""

    def __init__(self, index_path: Path, limit: int = 10) -> None:
        """Initialize the store.

        Args:
            index_path: JSON file used to persist the history index.
            limit: Maximum number of entries to retain.
        """
        self._index_path = index_path
        self._limit = limit

    def add_entry(
        self,
        *,
        report_id: str,
        report_path: Path,
        input_name: str,
        run_status: str,
    ) -> None:
        """Add a recent report entry and persist the trimmed history."""
        entries = self.list_entries()
        entries.insert(
            0,
            asdict(
                RecentReportEntry(
                    report_id=report_id,
                    timestamp=datetime.now(UTC).isoformat(),
                    input_name=input_name,
                    report_path=str(report_path),
                    run_status=run_status,
                )
            ),
        )
        self._write_entries(entries[: self._limit])

    def list_entries(self) -> list[dict[str, str]]:
        """Return the stored recent report entries."""
        if not self._index_path.exists():
            return []

        try:
            with self._index_path.open(encoding="utf-8") as file_handle:
                return list(json.load(file_handle))
        except json.JSONDecodeError:
            return []

    def _write_entries(self, entries: list[dict[str, str]]) -> None:
        """Write history entries to disk."""
        self._index_path.parent.mkdir(parents=True, exist_ok=True)
        with self._index_path.open("w", encoding="utf-8") as file_handle:
            json.dump(entries, file_handle, indent=2)
            file_handle.write("\n")
