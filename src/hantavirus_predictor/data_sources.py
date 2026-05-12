"""Canonical data-source registry for the project.

The registry intentionally separates public, downloadable data from manual or
restricted data so agents do not silently build models on unavailable labels.
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
        source_id="neon_hantavirus_serology",
        name="NEON Rodent pathogen status, hantavirus",
        url="https://data.neonscience.org/api/v0/products/DP1.10064.001",
        access="public API",
        spatial_unit="NEON site and plot",
        temporal_unit="sampling bout/month",
        coverage="2014-04 to 2019-11 in current API summary",
        manual_required=False,
        notes="Primary serology ground truth; testing switched away from hantavirus after 2019.",
    ),
    DataSource(
        source_id="neon_small_mammal_box_trapping",
        name="NEON Small mammal box trapping",
        url="https://data.neonscience.org/api/v0/products/DP1.10072.001",
        access="public API",
        spatial_unit="NEON site, plot, trap",
        temporal_unit="sampling bout/month",
        coverage="2013-06 to 2026-03 in current API summary",
        manual_required=False,
        notes="Reservoir abundance and trap-success proxy; not infection status after 2019.",
    ),
    DataSource(
        source_id="cdc_hantavirus_cases_public",
        name="CDC reported hantavirus disease cases",
        url="https://www.cdc.gov/hantavirus/data-research/cases/index.html",
        access="public web tables and NNDSS annual tables",
        spatial_unit="state",
        temporal_unit="annual public aggregate",
        coverage="1993-2023 on CDC page updated Apr. 23, 2026",
        manual_required=False,
        notes="CDC says county-level data cannot be provided publicly to protect identities.",
    ),
    DataSource(
        source_id="cdc_or_state_county_cases_restricted",
        name="Restricted CDC or state/local county-level case data",
        url="state or CDC data-use agreement",
        access="restricted partner data",
        spatial_unit="county or finer",
        temporal_unit="case date/report month",
        coverage="depends on agreement",
        manual_required=True,
        notes="Required for county-level human spillover validation or claims.",
    ),
    DataSource(
        source_id="daymet",
        name="Daymet daily surface weather",
        url="https://daymet.ornl.gov/",
        access="public API/direct download",
        spatial_unit="1 km grid",
        temporal_unit="daily",
        coverage="North America from 1980 through most recent complete calendar year",
        manual_required=False,
        notes="Preferred weather source for NEON/site-scale models before ERA5.",
    ),
    DataSource(
        source_id="modis_viirs_appeears",
        name="NASA AppEEARS MODIS/VIIRS vegetation products",
        url="https://www.earthdata.nasa.gov/data/tools/appeears",
        access="Earthdata login; AppEEARS API",
        spatial_unit="point or polygon sample",
        temporal_unit="8-day or 16-day depending on product",
        coverage="depends on product",
        manual_required=True,
        notes="Use quality flags and request only site/county summaries to avoid bulk raster sprawl.",
    ),
    DataSource(
        source_id="nlcd",
        name="USGS Annual NLCD",
        url="https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access",
        access="public download, web services, or AWS S3",
        spatial_unit="30 m raster",
        temporal_unit="annual",
        coverage="CONUS 1985-2024",
        manual_required=False,
        notes="Land-cover and developed/open-space features for exposure and habitat.",
    ),
    DataSource(
        source_id="svi",
        name="CDC/ATSDR Social Vulnerability Index",
        url="https://www.atsdr.cdc.gov/place-health/php/svi/index.html",
        access="public download",
        spatial_unit="county or tract",
        temporal_unit="release year",
        coverage="release-dependent",
        manual_required=False,
        notes="Use for sensitivity analyses, not causal claims.",
    ),
    DataSource(
        source_id="census_acs",
        name="U.S. Census ACS API",
        url="https://www.census.gov/programs-surveys/acs/data/data-via-api.html",
        access="public API",
        spatial_unit="county, tract, and other Census geographies",
        temporal_unit="annual release",
        coverage="ACS 1-year and 5-year releases",
        manual_required=False,
        notes="Human population denominators and exposure covariates.",
    ),
    DataSource(
        source_id="noaa_oni",
        name="NOAA Oceanic Nino Index",
        url="https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php",
        access="public table",
        spatial_unit="global climate index",
        temporal_unit="3-month season",
        coverage="1950-present",
        manual_required=False,
        notes="Climate-regime covariate; NOAA notes RONI is now official for ENSO monitoring.",
    ),
)


def list_sources() -> tuple[DataSource, ...]:
    return DATA_SOURCES


def get_source(source_id: str) -> DataSource:
    for source in DATA_SOURCES:
        if source.source_id == source_id:
            return source
    raise KeyError(f"Unknown source_id: {source_id}")

