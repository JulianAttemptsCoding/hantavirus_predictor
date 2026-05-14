"""Canonical public data-source registry for the EID benchmark path.

The active project is an EU/EEA country-year reported-incidence benchmark. Keep
the registry narrow so agents do not revive archived site-scale or restricted
subnational modeling paths.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataSource:
    source_id: str
    name: str
    url: str
    access: str
    spatial_unit: str
    temporal_unit: str
    coverage: str
    manual_required: bool
    notes: str


DATA_SOURCES: tuple[DataSource, ...] = (
    DataSource(
        source_id="ecdc_hantavirus_surveillance",
        name="ECDC hantavirus infection surveillance",
        url="https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023",
        access="public annual reports and surveillance exports",
        spatial_unit="EU/EEA country",
        temporal_unit="annual",
        coverage="report-dependent; 2023 report based on TESSy data retrieved 2024-11-06",
        manual_required=True,
        notes="Best harmonized anchor for a country-year HFRS/hantavirus infection paper.",
    ),
    DataSource(
        source_id="world_bank_indicators",
        name="World Bank Indicators API",
        url="https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        access="public API",
        spatial_unit="country",
        temporal_unit="annual",
        coverage="indicator-dependent; many series date back over 50 years",
        manual_required=False,
        notes="Population, rural population, GDP, health-system and reporting covariates.",
    ),
    DataSource(
        source_id="faostat_land_use",
        name="FAOSTAT land use and land cover statistics",
        url="https://www.fao.org/faostat/en/#data/RL",
        access="public download/API",
        spatial_unit="country",
        temporal_unit="annual",
        coverage="domain-dependent",
        manual_required=False,
        notes="Country-level cropland, forest, agriculture, and rural land-use covariates.",
    ),
    DataSource(
        source_id="terraclimate_global",
        name="TerraClimate monthly climate and water balance",
        url="https://www.climatologylab.org/terraclimate.html",
        access="public netCDF/THREDDS/Google Earth Engine",
        spatial_unit="global terrestrial grid",
        temporal_unit="monthly",
        coverage="1950-present, updated annually",
        manual_required=False,
        notes="Preferred global country-level climate covariates for publication phase 1.",
    ),
    DataSource(
        source_id="mod13c2_global_vegetation",
        name="MODIS/Terra MOD13C2 monthly global vegetation indices",
        url="https://lpdaac.usgs.gov/products/mod13c2v061/",
        access="NASA Earthdata",
        spatial_unit="global 0.05 degree grid",
        temporal_unit="monthly",
        coverage="2000-02-01 to present",
        manual_required=True,
        notes=(
            "Optional vegetation covariate source. Exclude from primary claims unless "
            "quality-masked country-year aggregation passes the source-quality gate."
        ),
    ),
    DataSource(
        source_id="natural_earth_countries",
        name="Natural Earth country boundaries",
        url="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/",
        access="public download",
        spatial_unit="country boundary",
        temporal_unit="static release",
        coverage="global",
        manual_required=False,
        notes="Boundary data for country-level display only; not evidence of within-country risk.",
    ),
)


def list_sources() -> tuple[DataSource, ...]:
    return DATA_SOURCES


def get_source(source_id: str) -> DataSource:
    for source in DATA_SOURCES:
        if source.source_id == source_id:
            return source
    raise KeyError(f"Unknown source_id: {source_id}")
