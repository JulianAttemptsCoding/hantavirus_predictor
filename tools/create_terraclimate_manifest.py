"""Create a TerraClimate NetCDF source manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.ingest.terraclimate import build_terraclimate_manifest  # noqa: E402


DEFAULT_OUTPUT = ROOT / "metadata" / "terraclimate_source_manifest.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, default=[2019, 2020, 2021, 2022, 2023])
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    manifest = build_terraclimate_manifest(args.years)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(output, index=False)
    print(f"Wrote {len(manifest)} TerraClimate source rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
