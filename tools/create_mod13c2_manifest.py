"""Create a CMR-discovered MOD13C2 granule manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.ingest.modis import search_mod13c2_granules  # noqa: E402


DEFAULT_OUTPUT = ROOT / "metadata" / "mod13c2_granule_manifest.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, default=[2019, 2020, 2021, 2022, 2023])
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    manifest = search_mod13c2_granules(args.years)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(output, index=False)
    print(f"Wrote {len(manifest)} MOD13C2 granules to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
