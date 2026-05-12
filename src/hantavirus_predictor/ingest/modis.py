"""MODIS MOD13C2 discovery through NASA CMR."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

import pandas as pd


CMR_GRANULES_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
MOD13C2_DOI = "10.5067/MODIS/MOD13C2.061"


def search_mod13c2_granules(years: list[int]) -> pd.DataFrame:
    """Return monthly MOD13C2 granule download URLs for selected years."""
    rows: list[dict[str, object]] = []
    for year in years:
        params = urllib.parse.urlencode(
            {
                "short_name": "MOD13C2",
                "version": "061",
                "page_size": 2000,
                "temporal": f"{year}-01-01T00:00:00Z,{year}-12-31T23:59:59Z",
                "sort_key": "start_date",
            }
        )
        request = urllib.request.Request(
            f"{CMR_GRANULES_URL}?{params}",
            headers={"Client-Id": "hantavirus-predictor"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        for entry in payload["feed"].get("entry", []):
            https_links = [
                link["href"]
                for link in entry.get("links", [])
                if link.get("href", "").startswith("https://")
                and link.get("href", "").endswith((".hdf", ".hdf.xml"))
            ]
            data_links = [link for link in https_links if link.endswith(".hdf")]
            rows.append(
                {
                    "year": year,
                    "granule_id": entry.get("id"),
                    "title": entry.get("title"),
                    "time_start": entry.get("time_start"),
                    "time_end": entry.get("time_end"),
                    "data_url": data_links[0] if data_links else "",
                    "metadata_url": next(
                        (link for link in https_links if link.endswith(".xml")), ""
                    ),
                    "doi": MOD13C2_DOI,
                }
            )
    return pd.DataFrame.from_records(rows)
