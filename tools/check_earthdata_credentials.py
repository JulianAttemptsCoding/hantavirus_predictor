"""Parse Earthdata credentials without printing secrets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.ingest.earthdata import load_earthdata_credentials  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=str(ROOT / "nasa earthdata acc info.txt"))
    args = parser.parse_args()

    credentials = load_earthdata_credentials(Path(args.path))
    print(
        "Earthdata credentials parsed: "
        f"username_chars={len(credentials.username)} password_chars={len(credentials.password)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
