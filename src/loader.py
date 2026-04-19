"""CSV loading utilities for AIVeritas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the file does not exist or is not a file.
        ValueError: If the file is empty or the parsed dataset has no rows.
    """
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {path}")

    try:
        dataframe = pd.read_csv(path, encoding="utf-8")
    except EmptyDataError as error:
        raise ValueError(f"CSV file is empty: {path}") from error

    if dataframe.empty:
        raise ValueError(f"CSV dataset is empty: {path}")

    return dataframe
