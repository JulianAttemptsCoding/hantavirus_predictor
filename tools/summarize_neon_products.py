"""Fetch compact NEON product metadata used by the project.

This avoids committing huge API responses while preserving enough provenance
for future agents to confirm current site and month availability.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen


PRODUCTS = {
    "DP1.10064.001": "Rodent pathogen status, hantavirus",
    "DP1.10072.001": "Small mammal box trapping",
}


def fetch_json(url: str) -> dict:
    with urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def summarize_product(product_id: str) -> dict:
    url = f"https://data.neonscience.org/api/v0/products/{product_id}"
    data = fetch_json(url)["data"]
    months = sorted(
        {m for site in data.get("siteCodes", []) for m in site.get("availableMonths", [])}
    )
    sites = sorted(site["siteCode"] for site in data.get("siteCodes", []))
    return {
        "product_id": product_id,
        "name": data.get("productName"),
        "status": data.get("productStatus"),
        "description": data.get("productDescription"),
        "api_url": url,
        "site_count": len(sites),
        "sites": sites,
        "first_month": months[0] if months else None,
        "last_month": months[-1] if months else None,
        "available_month_count": len(months),
        "releases": [release.get("release") for release in data.get("releases", [])],
        "notes": data.get("productRemarks"),
    }


def main() -> None:
    output_dir = Path("metadata")
    output_dir.mkdir(exist_ok=True)
    summary = {
        "generated_by": "tools/summarize_neon_products.py",
        "products": [summarize_product(product_id) for product_id in PRODUCTS],
    }
    output_path = output_dir / "neon_products_summary.json"
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
