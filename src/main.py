"""CLI entry point for AIVeritas."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# pylint: disable=wrong-import-position
from src.services.validation_service import run_validation


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Validate a CSV dataset and generate a structured JSON report.",
    )
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON report.")
    parser.add_argument(
        "--key-columns",
        nargs="+",
        default=[],
        help="One or more key columns used for duplicate detection.",
    )
    parser.add_argument(
        "--value-column",
        default=None,
        help="Numeric column used for z-score outlier detection.",
    )
    parser.add_argument(
        "--time-column",
        default=None,
        help="Date or period column used for time series gap detection.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the AIVeritas CLI flow.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        Process exit code.
    """
    args = parse_args(argv)
    result = run_validation(
        input_path=args.input,
        output_path=args.output,
        key_columns=args.key_columns,
        value_column=args.value_column,
        time_column=args.time_column,
    )

    if not result.success:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1

    print(f"Validation report saved to {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
