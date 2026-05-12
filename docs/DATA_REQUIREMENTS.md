# Data Requirements

This project can start without asking the user for anything else, but it cannot finish a county-level human case predictor from public data alone. The recommended publication path is now international country-level reported incidence first, with U.S./NEON as mechanistic support.

## What Is Already Set Up

The repo contains:

- Data directories with placeholders.
- `configs/data_catalog.yaml` with source definitions and QA rules.
- `tools/summarize_neon_products.py` to refresh NEON product metadata.
- `tools/validate_manual_data.py` to validate manual restricted CSVs.
- `tools/validate_international_cases.py` to validate international country-level case rows.
- `schemas/international_country_cases.schema.yaml` for the new publication-track case table.
- `metadata/neon_products_summary.json` can be generated locally.

## Data That Future Agents Can Download

### International Country-Level Human Hantavirus Cases

Primary manual table: `data/manual/international_country_cases.csv`

Validator:

```powershell
python tools/validate_international_cases.py --strict
```

Required role: primary human reported-incidence label for the international publication track.

Required source tiers:

- ECDC EU/EEA annual hantavirus infection surveillance:
  - Source: https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
  - Role: primary harmonized Europe anchor.
  - Caveat: extract country-year totals with report year, access date, and TESSy retrieval date where reported.
- PAHO/WHO Americas HPS alerts and cited national sources:
  - Source: https://www.paho.org/sites/default/files/2025-12/2025-12-19-epidemiological-alert-hantavirus-engfinal.pdf
  - Role: Americas HPS/HCPS extension and outbreak context.
  - Caveat: alerts are not complete long-term time series by themselves.
- China CDC Weekly HFRS publications:
  - Source: https://weekly.chinacdc.cn/en/article/doi/10.46234/ccdcw2025.141
  - Role: large HFRS external validation/sensitivity source.
  - Caveat: model as separate source system; do not assume comparability with EU/EEA.

Required columns are defined in `schemas/international_country_cases.schema.yaml`. Minimum required fields include `iso3`, `country`, `region`, `syndrome`, `year`, `cases`, `deaths`, `population`, `source_url`, `source_title`, `reporting_system`, and `quality_grade`.

Hard QA rules:

- Do not pool HFRS with HPS/HCPS unless syndrome is an explicit model stratum.
- Do not use rows without source URLs or clear extraction notes.
- Do not include quality-grade D rows in the primary model.
- Do not call counts "incidence" unless population denominators are joined.

### International Covariates

Country-year population and context:

- World Bank Indicators API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- Minimum indicators: total population, rural population percentage, GDP per capita or similar reporting-context proxy.

Climate:

- TerraClimate: https://www.climatologylab.org/terraclimate.html
- Minimum variables: precipitation, temperature, vapor pressure deficit, soil moisture, and water deficit.
- Required lags: 0, 1, 2, and 3 years, pre-registered before model tuning.

Vegetation:

- MODIS MOD13C2: https://lpdaac.usgs.gov/products/mod13c2v061/
- Minimum variables: NDVI and EVI.
- Caveat: NASA Earthdata credentials may be needed; do not commit them.

Land use:

- FAOSTAT land-use data: https://www.fao.org/faostat/en/#data/RL
- Minimum variables: cropland, forest, agricultural land, and pasture/grassland where available.

### NEON Hantavirus Serology

- Source: `DP1.10064.001`
- API: https://data.neonscience.org/api/v0/products/DP1.10064.001
- Put raw downloads under: `data/raw/neon/hantavirus/`
- Key table: `rpt_bloodtesting`
- Primary role: rodent infection/seroprevalence label
- Caveat: ends in 2019; do not use post-2019 small mammal data as infection status.

### NEON Small Mammal Box Trapping

- Source: `DP1.10072.001`
- API: https://data.neonscience.org/api/v0/products/DP1.10072.001
- Put raw downloads under: `data/raw/neon/small_mammals/`
- Key tables: `mam_pertrapnight`, `mam_perplotnight`
- Primary role: trap effort, species, abundance/trap-success proxy
- Caveat: must account for sampling effort, missing bouts, and site-specific sampling calendars.

### Public CDC/NNDSS Hantavirus Data

- CDC page: https://www.cdc.gov/hantavirus/data-research/cases/index.html
- NNDSS data locations: https://www.cdc.gov/nndss/infectious-disease/weekly-and-annual-disease-data-tables.html
- Put exports under: `data/raw/cdc/nndss/`
- Primary role: state-level context and weak external validation
- Caveat: public CDC page says county-level data cannot be provided publicly.

### Weather and Remote Sensing

- Daymet: https://daymet.ornl.gov/
  - Put under: `data/raw/daymet/`
  - Preferred for NEON site-scale weather because it is 1 km daily North America coverage.
- NASA AppEEARS: https://www.earthdata.nasa.gov/data/tools/appeears
  - Put request JSON and generated README under: `data/raw/appeears/`
  - Use for MODIS/VIIRS NDVI, EVI, LST, and quality flags.
  - Requires NASA Earthdata account. Do not commit credentials.
- USGS Annual NLCD: https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access
  - Put under: `data/raw/nlcd/`
  - Use for annual land cover and developed/open/forest/grassland features.

### Demographic and Vulnerability Covariates

- CDC/ATSDR SVI: https://www.atsdr.cdc.gov/place-health/php/svi/index.html
  - Put under: `data/raw/svi/`
- Census ACS API: https://www.census.gov/programs-surveys/acs/data/data-via-api.html
  - Put API exports under: `data/raw/census/`
- NOAA ONI/RONI context: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php
  - Put under: `data/raw/noaa/`

## Data The User Must Provide If County-Level Human Prediction Is Desired

Public CDC data are not enough for county-level human case modeling. Put one or both of these files in `data/manual/` only after obtaining the right permissions:

### `data/manual/cdc_county_month_cases.csv`

Required columns:

- `county_fips`
- `report_year`
- `report_month`
- `cases`
- `condition`
- `source_url_or_dua_id`
- `release_date`
- `suppression_flag`

Minimum acceptable provenance:

- Data-use agreement ID, CDC/state contact, or public source URL.
- Suppression and privacy rules.
- Confirmation that modeling and publication are allowed.

### `data/manual/state_health_dept_cases.csv`

Required columns:

- `jurisdiction`
- `spatial_unit`
- `fips`
- `period_start`
- `period_end`
- `cases`
- `source_url_or_dua_id`
- `access_notes`

Use this when state health departments provide custom county, region, or outbreak-line-list summaries.

Validate manual data:

```powershell
python tools/validate_manual_data.py --strict
```

## Credentials

Do not put secrets in git. Use environment variables or an untracked `.env`:

- `EARTHDATA_USERNAME`
- `EARTHDATA_PASSWORD`
- `CDSAPI_URL`
- `CDSAPI_KEY`

ERA5/CDS is optional in the first publication plan because Daymet is simpler, higher resolution for North America, and enough to build a strong first study.

## Minimal Publishable Dataset

A first defensible international paper can be built with:

1. ECDC country-year reported hantavirus infection/HFRS data.
2. World Bank population denominators and rurality/context indicators.
3. TerraClimate country-year climate lags.
4. MODIS MOD13C2 NDVI/EVI country-year summaries.
5. FAOSTAT land-use covariates.
6. Strict baselines and leave-country/temporal validation.

A fallback U.S./NEON reservoir paper can be built with:

1. NEON hantavirus serology through 2019.
2. NEON small mammal trapping through at least 2019, plus post-2019 proxy analysis as a limitation.
3. Daymet weather covariates for NEON sites.
4. MODIS/VIIRS vegetation covariates with quality flags.
5. NLCD land cover for habitat/exposure features.
6. CDC state-level cases as external context only.

The project should only add county-level human outcomes after a partner data agreement is documented.
