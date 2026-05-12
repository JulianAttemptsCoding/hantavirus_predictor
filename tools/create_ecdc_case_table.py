"""Create the manual ECDC country-year hantavirus case seed table."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hantavirus_predictor.datasets.ecdc_hantavirus import (  # noqa: E402
    KNOWN_2023_DEATHS,
    REPORTING_SYSTEM,
    SOURCE_TITLE,
    SOURCE_URL,
    iter_reported_rows,
)
from hantavirus_predictor.ingest.world_bank import fetch_indicator  # noqa: E402
from hantavirus_predictor.validation.international_cases import REQUIRED_COLUMNS  # noqa: E402


OUTPUT = ROOT / "data" / "manual" / "international_country_cases.csv"


def _fetch_populations(iso3_codes: list[str]) -> dict[tuple[str, int], int]:
    values = fetch_indicator(iso3_codes, "SP.POP.TOTL", 2019, 2023)
    populations: dict[tuple[str, int], int] = {}
    for value in values:
        if value.value is None:
            continue
        populations[(value.iso3, value.year)] = int(value.value)
    return populations


def build_rows(accessed_date: str) -> list[dict[str, str]]:
    reported_rows = iter_reported_rows()
    iso3_codes = [country.iso3 for country, _, _, _ in reported_rows]
    populations = _fetch_populations(iso3_codes)
    rows = []
    for country, year, cases, source_rate in reported_rows:
        population = populations.get((country.iso3, year))
        if population is None:
            raise RuntimeError(f"Missing World Bank population for {country.iso3} {year}")

        if year == 2023:
            deaths = str(KNOWN_2023_DEATHS.get(country.iso3, 0))
            death_note = "2023 deaths recorded from ECDC narrative; non-listed countries coded 0."
        else:
            deaths = ""
            death_note = "Deaths not available in extracted ECDC 2019-2022 country-year table."

        rate_note = (
            "Belgium 2023 rate not calculated by ECDC after surveillance-system change."
            if source_rate is None
            else f"ECDC table rate: {source_rate} per 100,000."
        )
        rows.append(
            {
                "iso3": country.iso3,
                "country": country.country,
                "region": "Europe",
                "syndrome": "hantavirus_infection",
                "pathogen_or_virus": "unspecified_hantavirus",
                "case_definition": (
                    "ECDC TESSy hantavirus infection annual surveillance; EU viral "
                    "haemorrhagic fever case definition, alternative national "
                    "definition, or unspecified definition depending on country."
                ),
                "reporting_system": REPORTING_SYSTEM,
                "year": str(year),
                "cases": str(cases),
                "deaths": deaths,
                "population": str(population),
                "source_url": SOURCE_URL,
                "source_title": SOURCE_TITLE,
                "accessed_date": accessed_date,
                "source_type": "annual_report",
                "quality_grade": "B",
                "notes": (
                    "Manually transcribed from ECDC Table 1; population denominator "
                    f"joined from World Bank SP.POP.TOTL. {rate_note} {death_note}"
                ),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT))
    parser.add_argument("--accessed-date", default=date.today().isoformat())
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = build_rows(args.accessed_date)
    columns = [
        "iso3",
        "country",
        "region",
        "syndrome",
        "pathogen_or_virus",
        "case_definition",
        "reporting_system",
        "year",
        "cases",
        "deaths",
        "population",
        "source_url",
        "source_title",
        "accessed_date",
        "source_type",
        "quality_grade",
        "notes",
    ]
    if set(columns) != REQUIRED_COLUMNS:
        raise RuntimeError("Case-table columns no longer match validator requirements")
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
