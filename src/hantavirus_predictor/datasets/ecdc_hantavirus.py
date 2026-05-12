"""ECDC hantavirus infection annual report table extraction for 2019-2023."""

from __future__ import annotations

from dataclasses import dataclass


SOURCE_URL = "https://www.ecdc.europa.eu/sites/default/files/documents/HANTA_AER_2023.pdf"
SOURCE_TITLE = "Hantavirus infection - Annual Epidemiological Report for 2023"
REPORTING_SYSTEM = "ECDC TESSy annual report"


@dataclass(frozen=True)
class EcdcCountry:
    iso3: str
    country: str
    counts: dict[int, int | None]
    rates: dict[int, float | None]


COUNTRIES: tuple[EcdcCountry, ...] = (
    EcdcCountry(
        "AUT",
        "Austria",
        {2019: 276, 2020: 30, 2021: 233, 2022: 24, 2023: 97},
        {2019: 3.1, 2020: 0.3, 2021: 2.6, 2022: 0.3, 2023: 1.1},
    ),
    EcdcCountry(
        "BEL",
        "Belgium",
        {2019: 94, 2020: 45, 2021: 81, 2022: 80, 2023: 99},
        {2019: 0.8, 2020: 0.4, 2021: 0.7, 2022: 0.7, 2023: None},
    ),
    EcdcCountry(
        "BGR",
        "Bulgaria",
        {2019: 6, 2020: 1, 2021: 11, 2022: 1, 2023: 6},
        {2019: 0.1, 2020: 0.0, 2021: 0.2, 2022: 0.0, 2023: 0.1},
    ),
    EcdcCountry(
        "HRV",
        "Croatia",
        {2019: 191, 2020: 17, 2021: 7, 2022: 6, 2023: 2},
        {2019: 4.8, 2020: 0.4, 2021: 0.2, 2022: 0.2, 2023: 0.1},
    ),
    EcdcCountry(
        "CYP",
        "Cyprus",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "CZE",
        "Czechia",
        {2019: 15, 2020: 5, 2021: 8, 2022: 7, 2023: 11},
        {2019: 0.1, 2020: 0.0, 2021: 0.1, 2022: 0.1, 2023: 0.1},
    ),
    EcdcCountry(
        "DNK",
        "Denmark",
        {2019: None, 2020: None, 2021: None, 2022: None, 2023: None},
        {2019: None, 2020: None, 2021: None, 2022: None, 2023: None},
    ),
    EcdcCountry(
        "EST",
        "Estonia",
        {2019: 26, 2020: 17, 2021: 12, 2022: 13, 2023: 19},
        {2019: 2.0, 2020: 1.3, 2021: 0.9, 2022: 1.0, 2023: 1.4},
    ),
    EcdcCountry(
        "FIN",
        "Finland",
        {2019: 1256, 2020: 1164, 2021: 1427, 2022: 1299, 2023: 806},
        {2019: 22.8, 2020: 21.1, 2021: 25.8, 2022: 23.4, 2023: 14.5},
    ),
    EcdcCountry(
        "FRA",
        "France",
        {2019: 131, 2020: 26, 2021: 324, 2022: 23, 2023: 50},
        {2019: 0.2, 2020: 0.0, 2021: 0.5, 2022: 0.0, 2023: 0.1},
    ),
    EcdcCountry(
        "DEU",
        "Germany",
        {2019: 1535, 2020: 237, 2021: 1740, 2022: 143, 2023: 335},
        {2019: 1.8, 2020: 0.3, 2021: 2.1, 2022: 0.2, 2023: 0.4},
    ),
    EcdcCountry(
        "GRC",
        "Greece",
        {2019: 1, 2020: 1, 2021: 4, 2022: 0, 2023: 1},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "HUN",
        "Hungary",
        {2019: 13, 2020: 4, 2021: 3, 2022: 1, 2023: 11},
        {2019: 0.1, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.1},
    ),
    EcdcCountry(
        "ISL",
        "Iceland",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: None},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: None},
    ),
    EcdcCountry(
        "IRL",
        "Ireland",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "ITA",
        "Italy",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "LVA",
        "Latvia",
        {2019: 5, 2020: 3, 2021: 3, 2022: 3, 2023: 4},
        {2019: 0.3, 2020: 0.2, 2021: 0.2, 2022: 0.2, 2023: 0.2},
    ),
    EcdcCountry(
        "LIE",
        "Liechtenstein",
        {2019: None, 2020: None, 2021: 0, 2022: 0, 2023: 0},
        {2019: None, 2020: None, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "LTU",
        "Lithuania",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "LUX",
        "Luxembourg",
        {2019: 8, 2020: 0, 2021: 33, 2022: 2, 2023: 5},
        {2019: 1.3, 2020: 0.0, 2021: 5.2, 2022: 0.3, 2023: 0.8},
    ),
    EcdcCountry(
        "MLT",
        "Malta",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "NLD",
        "Netherlands",
        {2019: 6, 2020: 3, 2021: 6, 2022: 1, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "NOR",
        "Norway",
        {2019: 11, 2020: 12, 2021: 38, 2022: 20, 2023: 15},
        {2019: 0.2, 2020: 0.2, 2021: 0.7, 2022: 0.4, 2023: 0.3},
    ),
    EcdcCountry(
        "POL",
        "Poland",
        {2019: 9, 2020: 3, 2021: 42, 2022: 5, 2023: 43},
        {2019: 0.0, 2020: 0.0, 2021: 0.1, 2022: 0.0, 2023: 0.1},
    ),
    EcdcCountry(
        "PRT",
        "Portugal",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "ROU",
        "Romania",
        {2019: 4, 2020: 1, 2021: 12, 2022: 7, 2023: 6},
        {2019: 0.0, 2020: 0.0, 2021: 0.1, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "SVK",
        "Slovakia",
        {2019: 94, 2020: 49, 2021: 117, 2022: 84, 2023: 154},
        {2019: 1.7, 2020: 0.9, 2021: 2.1, 2022: 1.5, 2023: 2.8},
    ),
    EcdcCountry(
        "SVN",
        "Slovenia",
        {2019: 252, 2020: 14, 2021: 569, 2022: 7, 2023: 64},
        {2019: 12.1, 2020: 0.7, 2021: 27.0, 2022: 0.3, 2023: 3.0},
    ),
    EcdcCountry(
        "ESP",
        "Spain",
        {2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0},
        {2019: 0.0, 2020: 0.0, 2021: 0.0, 2022: 0.0, 2023: 0.0},
    ),
    EcdcCountry(
        "SWE",
        "Sweden",
        {2019: 155, 2020: 61, 2021: 277, 2022: 459, 2023: 157},
        {2019: 1.5, 2020: 0.6, 2021: 2.7, 2022: 4.4, 2023: 1.5},
    ),
)

KNOWN_2023_DEATHS = {"EST": 1, "HUN": 1, "SVK": 1}


def iter_reported_rows() -> list[tuple[EcdcCountry, int, int, float | None]]:
    """Return rows with reported counts, excluding NDR/NA cells."""
    rows = []
    for country in COUNTRIES:
        for year, cases in country.counts.items():
            if cases is None:
                continue
            rows.append((country, year, cases, country.rates[year]))
    return rows
