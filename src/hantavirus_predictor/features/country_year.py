"""Build the international country-year modeling table."""

from __future__ import annotations

from pathlib import Path
import warnings

import pandas as pd

from hantavirus_predictor.ingest.faostat import ITEM_TO_FEATURE, build_land_use_features
from hantavirus_predictor.ingest.terraclimate import annual_feature_column
from hantavirus_predictor.ingest.world_bank import INDICATORS, fetch_indicators


WORLD_BANK_CONTEXT_INDICATORS = ["SP.RUR.TOTL.ZS", "NY.GDP.PCAP.CD"]
DEFAULT_FAOSTAT_ZIP = Path("data/raw/faostat_land_use_normalized.zip")
DEFAULT_TERRACLIMATE = Path("data/processed/terraclimate_country_year.csv")


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


def _add_country_lags(
    data: pd.DataFrame,
    columns: list[str],
    lags: tuple[int, ...] = (1,),
) -> pd.DataFrame:
    result = data.sort_values(["iso3", "year"]).copy()
    for column in columns:
        if column not in result.columns:
            continue
        for lag in lags:
            lag_column = f"{column}_lag{lag}"
            if lag_column not in result.columns:
                result[lag_column] = result.groupby("iso3")[column].shift(lag)
            result[f"{lag_column}_missing"] = result[lag_column].isna()
    return result


def _join_terraclimate(cases: pd.DataFrame, terraclimate_csv: Path) -> pd.DataFrame:
    annual_columns = [
        annual_feature_column(variable) for variable in ("def", "ppt", "soil", "tmax", "tmin", "vpd")
    ]
    if not terraclimate_csv.exists():
        cases["terraclimate_joined"] = False
        for column in annual_columns:
            cases[column] = pd.NA
            cases[f"{column}_missing"] = True
            lag_column = f"{column}_lag1"
            cases[lag_column] = pd.NA
            cases[f"{lag_column}_missing"] = True
        return cases

    terraclimate = pd.read_csv(terraclimate_csv)
    joined = cases.merge(
        terraclimate,
        on=["iso3", "country", "year"],
        how="left",
        validate="many_to_one",
        suffixes=("", "_terraclimate"),
    )
    feature_columns = [column for column in annual_columns if column in joined.columns]
    joined["terraclimate_joined"] = joined[feature_columns].notna().any(axis=1)
    for column in feature_columns:
        joined[f"{column}_missing"] = joined[column].isna()
        lag_column = f"{column}_lag1"
        if lag_column in joined.columns:
            joined[f"{lag_column}_missing"] = joined[lag_column].isna()
    return joined


def build_country_year(
    case_table: Path,
    faostat_zip: Path = DEFAULT_FAOSTAT_ZIP,
    terraclimate_csv: Path = DEFAULT_TERRACLIMATE,
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
    joined = _add_country_lags(
        joined,
        [
            "rural_population_pct",
            "gdp_per_capita_current_usd",
            *ITEM_TO_FEATURE.values(),
        ],
    )
    joined = _join_terraclimate(joined, terraclimate_csv)

    # MODIS remains explicit until quality-masked vegetation aggregation is implemented.
    joined["mod13c2_joined"] = False

    sort_columns = ["source_system", "region", "country", "syndrome", "year"]
    return joined.sort_values(sort_columns).reset_index(drop=True)
