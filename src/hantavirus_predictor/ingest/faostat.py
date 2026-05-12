"""FAOSTAT land-use ingestion for country-year features."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


LAND_USE_BULK_URL = (
    "https://bulks-faostat.fao.org/production/Inputs_LandUse_E_All_Data_(Normalized).zip"
)
LAND_USE_MEMBER = "Inputs_LandUse_E_All_Data_(Normalized).csv"

ITEM_TO_FEATURE = {
    "Country area": "faostat_country_area_1000ha",
    "Land area": "faostat_land_area_1000ha",
    "Agricultural land": "faostat_agricultural_land_1000ha",
    "Cropland": "faostat_cropland_1000ha",
    "Forest land": "faostat_forest_land_1000ha",
    "Permanent meadows and pastures": "faostat_perm_meadows_pastures_1000ha",
    "Other land": "faostat_other_land_1000ha",
}

COUNTRY_NAME_OVERRIDES = {
    "Czechia": "Czechia",
    "Netherlands": "Netherlands (Kingdom of the)",
}


def build_land_use_features(
    zip_path: Path,
    countries: pd.DataFrame,
    years: list[int],
) -> pd.DataFrame:
    """Return FAOSTAT land-use features for requested countries and years."""
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing FAOSTAT land-use bulk file: {zip_path}")

    target = countries[["iso3", "country"]].drop_duplicates().copy()
    target["faostat_area"] = target["country"].map(COUNTRY_NAME_OVERRIDES).fillna(target["country"])
    area_to_iso3 = dict(zip(target["faostat_area"], target["iso3"]))

    with ZipFile(zip_path) as archive:
        with archive.open(LAND_USE_MEMBER) as handle:
            raw = pd.read_csv(
                handle,
                usecols=["Area", "Item", "Year", "Unit", "Value", "Flag"],
            )

    filtered = raw[
        raw["Area"].isin(area_to_iso3)
        & raw["Item"].isin(ITEM_TO_FEATURE)
        & raw["Year"].isin(years)
        & (raw["Unit"] == "1000 ha")
    ].copy()
    filtered["iso3"] = filtered["Area"].map(area_to_iso3)
    filtered["feature"] = filtered["Item"].map(ITEM_TO_FEATURE)

    features = (
        filtered.pivot_table(
            index=["iso3", "Year"],
            columns="feature",
            values="Value",
            aggfunc="first",
        )
        .reset_index()
        .rename(columns={"Year": "year"})
    )
    features.columns.name = None

    for column in ITEM_TO_FEATURE.values():
        if column not in features:
            features[column] = pd.NA

    expected = pd.MultiIndex.from_product(
        [target["iso3"].unique(), years],
        names=["iso3", "year"],
    ).to_frame(index=False)
    return expected.merge(features, on=["iso3", "year"], how="left")
