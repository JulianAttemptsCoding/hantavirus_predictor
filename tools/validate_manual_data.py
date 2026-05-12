"""Validate manually supplied restricted/public-health CSVs.

By default this reports missing optional files without failing. Use --strict in
publication QA once required partner data have been obtained.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCHEMAS = {
    "data/manual/cdc_county_month_cases.csv": {
        "county_fips",
        "report_year",
        "report_month",
        "cases",
        "condition",
        "source_url_or_dua_id",
        "release_date",
        "suppression_flag",
    },
    "data/manual/state_health_dept_cases.csv": {
        "jurisdiction",
        "spatial_unit",
        "fips",
        "period_start",
        "period_end",
        "cases",
        "source_url_or_dua_id",
        "access_notes",
    },
}


def read_header(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        return set(next(reader, []))


def validate_file(path: Path, required_columns: set[str]) -> list[str]:
    if not path.exists():
        return [f"MISSING optional manual file: {path}"]
    actual = read_header(path)
    missing = sorted(required_columns - actual)
    if missing:
        return [f"{path}: missing columns: {', '.join(missing)}"]
    return [f"OK: {path}"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Fail if files are missing.")
    args = parser.parse_args()

    messages: list[str] = []
    has_problem = False
    for file_name, columns in SCHEMAS.items():
        path = Path(file_name)
        result = validate_file(path, columns)
        messages.extend(result)
        if result[0].startswith("MISSING"):
            has_problem = has_problem or args.strict
        elif "missing columns" in result[0]:
            has_problem = True

    for message in messages:
        print(message)
    return 1 if has_problem else 0


if __name__ == "__main__":
    raise SystemExit(main())

