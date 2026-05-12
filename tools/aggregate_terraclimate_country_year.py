"""Aggregate TerraClimate gridded covariates to country-year features."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.ingest.terraclimate_aggregate import (  # noqa: E402
    EUROPE_CLIP_BOUNDS,
    aggregate_terraclimate_country_year,
    read_country_boundaries,
)


DEFAULT_CASES = ROOT / "data" / "manual" / "international_country_cases.csv"
DEFAULT_MANIFEST = ROOT / "metadata" / "terraclimate_source_manifest.csv"
DEFAULT_BOUNDARIES = ROOT / "data" / "raw" / "natural_earth" / "ne_50m_admin_0_countries.zip"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "terraclimate_country_year.csv"


def _parse_bounds(value: str) -> tuple[float, float, float, float]:
    parts = [float(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bounds must be min_lon,min_lat,max_lon,max_lat")
    return tuple(parts)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--boundaries", default=str(DEFAULT_BOUNDARIES))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--variables",
        nargs="+",
        default=["ppt", "tmin", "tmax", "vpd", "soil", "def"],
    )
    parser.add_argument("--years", nargs="+", type=int, default=None)
    parser.add_argument("--lags", nargs="+", type=int, default=[1])
    parser.add_argument("--clip-bounds", type=_parse_bounds, default=EUROPE_CLIP_BOUNDS)
    parser.add_argument("--no-opendap", action="store_true")
    args = parser.parse_args()

    cases = pd.read_csv(args.cases)
    manifest = pd.read_csv(args.manifest)
    boundaries = read_country_boundaries(
        Path(args.boundaries),
        cases[["iso3", "country"]].drop_duplicates(),
        clip_bounds=args.clip_bounds,
    )
    features = aggregate_terraclimate_country_year(
        cases,
        manifest,
        boundaries,
        variables=args.variables,
        years=args.years,
        lags=args.lags,
        bounds=args.clip_bounds,
        use_opendap=not args.no_opendap,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output, index=False)
    joined = int(features["terraclimate_joined"].sum())
    print(f"Wrote {len(features)} TerraClimate country-year rows to {output}")
    print(f"Rows with at least one TerraClimate feature: {joined} of {len(features)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
