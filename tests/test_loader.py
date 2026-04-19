"""Tests for CSV loading utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.loader import load_csv


def test_load_csv_returns_dataframe_for_valid_file(tmp_path: Path) -> None:
    """The loader should return a DataFrame for a valid CSV file."""
    csv_path = tmp_path / "valid.csv"
    csv_path.write_text("id,value\n1,10\n2,20\n", encoding="utf-8")

    dataframe = load_csv(csv_path)

    assert dataframe.shape == (2, 2)
    assert dataframe.columns.tolist() == ["id", "value"]


def test_load_csv_raises_for_empty_dataset(tmp_path: Path) -> None:
    """The loader should reject CSV files that contain headers but no data rows."""
    csv_path = tmp_path / "empty_dataset.csv"
    csv_path.write_text("id,value\n", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV dataset is empty"):
        load_csv(csv_path)
