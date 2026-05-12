"""Download Natural Earth country boundaries for zonal covariates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.ingest.terraclimate_aggregate import NATURAL_EARTH_50M_URL  # noqa: E402


DEFAULT_OUTPUT = ROOT / "data" / "raw" / "natural_earth" / "ne_50m_admin_0_countries.zip"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--url", default=NATURAL_EARTH_50M_URL)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        print(f"Natural Earth boundaries already exist at {output}")
        return 0
    urlretrieve(args.url, output)
    print(f"Downloaded Natural Earth country boundaries to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
