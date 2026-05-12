"""Small World Bank Indicators API client used by reproducible data builders."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass


WORLD_BANK_API = "https://api.worldbank.org/v2"

INDICATORS = {
    "SP.POP.TOTL": "population",
    "SP.RUR.TOTL.ZS": "rural_population_pct",
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
}


@dataclass(frozen=True)
class IndicatorValue:
    iso3: str
    year: int
    indicator: str
    value: float | None


def fetch_indicator(
    iso3_codes: list[str],
    indicator: str,
    start_year: int,
    end_year: int,
) -> list[IndicatorValue]:
    """Fetch one indicator for many ISO3 countries from the World Bank API."""
    if indicator not in INDICATORS:
        raise ValueError(f"Unsupported World Bank indicator: {indicator}")
    if start_year > end_year:
        raise ValueError("start_year must be <= end_year")

    rows: list[IndicatorValue] = []
    codes = sorted(set(iso3_codes))
    for start in range(0, len(codes), 4):
        rows.extend(
            _fetch_indicator_chunk(codes[start : start + 8], indicator, start_year, end_year)
        )
    return rows


def _fetch_indicator_chunk(
    iso3_codes: list[str],
    indicator: str,
    start_year: int,
    end_year: int,
) -> list[IndicatorValue]:
    countries = ";".join(iso3_codes)
    path = f"/country/{urllib.parse.quote(countries)}/indicator/{indicator}"
    query = urllib.parse.urlencode(
        {
            "format": "json",
            "per_page": 20000,
            "date": f"{start_year}:{end_year}",
        }
    )
    url = f"{WORLD_BANK_API}{path}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "hantavirus-predictor/0.1"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1 + attempt)
    else:
        raise RuntimeError(
            f"World Bank request failed for {indicator} {iso3_codes}"
        ) from last_error

    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError(f"Unexpected World Bank response for {indicator}")

    rows = []
    for item in payload[1]:
        country = item.get("countryiso3code")
        date = item.get("date")
        if not country or not date:
            continue
        rows.append(
            IndicatorValue(
                iso3=country,
                year=int(date),
                indicator=indicator,
                value=item.get("value"),
            )
        )
    return rows


def fetch_indicators(
    iso3_codes: list[str],
    indicators: list[str],
    start_year: int,
    end_year: int,
) -> list[IndicatorValue]:
    """Fetch multiple World Bank indicators."""
    values: list[IndicatorValue] = []
    for indicator in indicators:
        values.extend(fetch_indicator(iso3_codes, indicator, start_year, end_year))
    return values
