"""CLI wrapper for validating international country-level case rows."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.validation.international_cases import (  # noqa: E402
    DEFAULT_CASE_TABLE,
    validate_file,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=str(DEFAULT_CASE_TABLE), help="CSV to validate.")
    parser.add_argument("--strict", action="store_true", help="Fail if the table is missing.")
    args = parser.parse_args()

    path = Path(args.path)
    result = validate_file(path)
    ok = result.ok and (path.exists() or not args.strict)
    for message in result.messages:
        print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
