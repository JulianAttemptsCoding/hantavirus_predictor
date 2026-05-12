"""Build the international country-year modeling table."""

from __future__ import annotations

from pathlib import Path
import warnings

import pandas as pd

from hantavirus_predictor.ingest.faostat import ITEM_TO_FEATURE, build_land_use_features
from hantavirus_predictor.ingest.world_bank import INDICATORS, fetch_indicators


WORLD_BANK_CONTEXT_INDICATORS = ["SP.RUR.TOTL.ZS", "NY.GDP.PCAP.CD"]
DEFAULT_FAOSTAT_ZIP = Path("data/raw/faostat_land_use_normalized.zip")


def _normalise_source_system(reporting_system: str) -> str:
    if "ECDC" in reporting_system:
        return "ECDC"
    if "PAHO" in reporting_system:
        return "PAHO"
    if "China" in reporting_system:
        return "China CDC"
    return reporting_system


def _world_bank_context(cases: pd.DataFrame) -> pd.DataFrame:
    iso3_codes = sorted(cases["iso3"].unique())
    start_year = int(cases["year"].min())
    end_year = int(cases["year"].max())
    try:
        values = fetch_indicators(iso3_codes, WORLD_BANK_CONTEXT_INDICATORS, start_year, end_year)
    except Exception as exc:
        warnings.warn(
            f"World Bank context covariates could not be fetched: {exc}",
            RuntimeWarning,
            stacklevel=2,
        )
        return pd.DataFrame(columns=["iso3", "year"])
    records = [
        {
            "iso3": value.iso3,
            "year": value.year,
            INDICATORS[value.indicator]: value.value,
        }
        for value in values
    ]
    if not records:
        return pd.DataFrame(columns=["iso3", "year"])
    long = pd.DataFrame.from_records(records)
    context = long.groupby(["iso3", "year"], as_index=False).first()
    return context


def _join_faostat_land_use(cases: pd.DataFrame, faostat_zip: Path) -> pd.DataFrame:
    if not faostat_zip.exists():
        for column in ITEM_TO_FEATURE.values():
            cases[column] = pd.NA
        cases["faostat_land_use_joined"] = False
        return cases

    years = sorted(int(year) for year in cases["year"].unique())
    land_use = build_land_use_features(faostat_zip, cases[["iso3", "country"]], years)
    joined = cases.merge(land_use, on=["iso3", "year"], how="left", validate="many_to_one")
    joined["faostat_land_use_joined"] = ~joined[list(ITEM_TO_FEATURE.values())].isna().all(axis=1)
    for column in ITEM_TO_FEATURE.values():
        joined[f"{column}_missing"] = joined[column].isna()
    return joined


def build_country_year(
    case_table: Path,
    faostat_zip: Path = DEFAULT_FAOSTAT_ZIP,
) -> pd.DataFrame:
    """Return an analysis table from the validated case table and public context data."""
    cases = pd.read_csv(case_table)
    cases["source_system"] = cases["reporting_system"].map(_normalise_source_system)
    cases["population"] = cases["population"].astype(int)
    cases["cases"] = cases["cases"].astype(int)
    cases["deaths"] = pd.to_numeric(cases["deaths"], errors="coerce").astype("Int64")
    cases["incidence_per_100k"] = cases["cases"] / cases["population"] * 100_000
    cases["death_missing"] = cases["deaths"].isna()

    context = _world_bank_context(cases)
    joined = cases.merge(context, on=["iso3", "year"], how="left", validate="many_to_one")

    for column in ("rural_population_pct", "gdp_per_capita_current_usd"):
        joined[f"{column}_missing"] = joined[column].isna()

    joined = _join_faostat_land_use(joined, faostat_zip)

    # Explicit placeholders make the data audit honest before gridded inputs are available.
    for family in ("terraclimate", "mod13c2"):
        joined[f"{family}_joined"] = False

    sort_columns = ["source_system", "region", "country", "syndrome", "year"]
    return joined.sort_values(sort_columns).reset_index(drop=True)
