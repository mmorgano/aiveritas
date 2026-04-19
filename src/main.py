"""CLI entry point for AIVeritas."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ai_module import explain_issue
from src.loader import load_csv
from src.report import build_validation_report, save_report
from src.schemas import build_processing_issue
from src.validator import run_validations


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
    configuration = {
        "key_columns": list(args.key_columns),
        "value_column": args.value_column,
        "time_column": args.time_column,
    }
    executed_checks = _build_executed_checks(
        key_columns=args.key_columns,
        value_column=args.value_column,
        time_column=args.time_column,
    )
    dataframe = None
    run_stage = "load"

    try:
        dataframe = load_csv(args.input)
        run_stage = "validation"
        issues = run_validations(
            dataframe,
            key_columns=args.key_columns,
            value_column=args.value_column,
            time_column=args.time_column,
        )

        enriched_issues = []
        for issue in issues:
            enriched_issue = dict(issue)
            enriched_issue["ai_explanation"] = explain_issue(issue)
            enriched_issues.append(enriched_issue)

        report = build_validation_report(
            args.input,
            dataframe,
            enriched_issues,
            run_status="succeeded",
            validation_status="failed" if enriched_issues else "passed",
            run_stage="completed",
            configuration=configuration,
            executed_checks=executed_checks,
        )
        output_path = save_report(report, args.output)
    except Exception as error:
        failure_issue = build_processing_issue(
            error,
            input_path=args.input,
            stage=run_stage,
        )
        failure_issue["ai_explanation"] = explain_issue(failure_issue)
        failure_report = build_validation_report(
            args.input,
            dataframe,
            [failure_issue],
            run_status="failed",
            validation_status="not_run" if run_stage == "load" else "failed",
            run_stage=run_stage,
            configuration=configuration,
            executed_checks=executed_checks,
        )
        save_report(failure_report, args.output)
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Validation report saved to {output_path}")
    return 0


def _build_executed_checks(
    *,
    key_columns: Sequence[str],
    value_column: str | None,
    time_column: str | None,
) -> list[str]:
    """Build the list of enabled validation checks for the current CLI run."""
    checks = ["missing_values"]

    if key_columns:
        checks.append("duplicate_rows")

    if value_column:
        checks.append("numeric_outlier")

    if time_column:
        checks.append("time_series_gap")

    return checks


if __name__ == "__main__":
    raise SystemExit(main())
