"""Generate synthetic CSV datasets for local testing."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    """Generate sample CSV datasets under data/synthetic."""
    output_directory = Path(__file__).resolve().parent.parent / "data" / "synthetic"
    output_directory.mkdir(parents=True, exist_ok=True)

    clean = pd.DataFrame(
        {
            "ID": list(range(1, 11)),
            "DATE": pd.date_range("2026-01-01", periods=10, freq="D"),
            "VALUE": [10.0, 10.5, 11.0, 10.8, 11.2, 10.7, 10.9, 11.1, 10.6, 10.8],
            "CATEGORY": ["A", "B", "A", "B", "C", "A", "B", "C", "A", "B"],
        }
    )

    missing = clean.copy()
    missing.loc[1, "VALUE"] = None
    missing.loc[3, "CATEGORY"] = None

    duplicates = clean.copy()
    duplicates.loc[9, "ID"] = 2

    outliers = pd.DataFrame(
        {
            "ID": list(range(1, 12)),
            "DATE": pd.date_range("2026-02-01", periods=11, freq="D"),
            "VALUE": [10.0] * 10 + [100.0],
            "CATEGORY": ["A", "B", "A", "B", "C", "A", "B", "C", "A", "B", "A"],
        }
    )

    timeseries_gap = clean.drop(index=4).reset_index(drop=True)

    datasets = {
        "sample_clean.csv": clean,
        "sample_missing.csv": missing,
        "sample_duplicates.csv": duplicates,
        "sample_outliers.csv": outliers,
        "sample_timeseries_gap.csv": timeseries_gap,
    }

    for filename, dataframe in datasets.items():
        dataframe.to_csv(output_directory / filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
