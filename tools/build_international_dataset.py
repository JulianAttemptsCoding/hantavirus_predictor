"""Build the processed international country-year modeling table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.features.country_year import build_country_year  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "manual" / "international_country_cases.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "international_country_year.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = build_country_year(Path(args.input))
    data.to_csv(output, index=False)
    print(f"Wrote {len(data)} rows and {len(data.columns)} columns to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
