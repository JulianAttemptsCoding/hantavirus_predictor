"""Download the FAOSTAT normalized land-use bulk file."""

from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "faostat_land_use_normalized.zip"
URL = "https://bulks-faostat.fao.org/production/Inputs_LandUse_E_All_Data_(Normalized).zip"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists() and not args.force:
        print(f"Already exists: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "hantavirus-predictor/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        output.write_bytes(response.read())
    print(f"Wrote {output.stat().st_size} bytes to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
