# Data Dictionary

Last updated: 2026-05-12

This dictionary describes the publication-track ECDC country-year benchmark.
Generated CSV files live under `data/` and are intentionally ignored by git.

## Manual Case Table

File:

- `data/manual/international_country_cases.csv`

Schema:

- `schemas/international_country_cases.schema.yaml`

Validator:

- `python tools/validate_international_cases.py --strict`

Columns:

| Column | Type | Meaning |
| --- | --- | --- |
| `iso3` | string | ISO3 country code. |
| `country` | string | Country name as used for reporting. |
| `year` | integer | Reporting year. |
| `reporting_system` | string | Source-specific reporting system, currently `TESSy`. |
| `syndrome` | string | Human syndrome/reporting label. |
| `pathogen_or_virus` | string | Virus if source-reported; otherwise `unspecified_hantavirus`. |
| `cases` | integer | Reported annual case count. |
| `deaths` | integer or missing | Reported deaths when available. |
| `case_definition` | string | Source case definition summary. |
| `source_url` | string | Primary source URL. |
| `source_title` | string | Source title. |
| `accessed_date` | date | Local access date. |
| `quality_grade` | string | A-D source-quality grade. |
| `region` | string | Analysis region label. |
| `eu_eea_status` | string | EU/EEA membership status used for panel consistency. |
| `surveillance_completeness` | string | Completeness flag from source metadata. |
| `source_type` | string | Source document family, such as `annual_report`. |
| `notes` | string | Human-readable source caveats. |

Allowed `eu_eea_status` values:

- `eu_member`
- `eea_non_eu`
- `withdrawn`
- `not_applicable`

Allowed `surveillance_completeness` values:

- `comprehensive`
- `not_comprehensive`
- `unspecified`
- `not_reported`

Current source caveats:

- Belgium 2023 is `not_comprehensive` because ECDC did not calculate a rate
  after a surveillance-system change.
- Cyprus 2023 is `unspecified` for the current ECDC metadata caveat.
- United Kingdom rows are excluded from the primary ECDC seed because ECDC
  reports no UK data from 2020 onward after EU withdrawal.

## Processed Analysis Table

File:

- `data/processed/international_country_year.csv`

Builder:

- `python tools/build_international_dataset.py`

Purpose:

- Join reported cases to public demographic, land-use, climate, and manifest
  features.
- Preserve source metadata for audit.
- Derive `source_system` from `reporting_system` for source-system
  stratification in models and reports.

Important rule:

- This file is the raw processed analysis table. Its column count is not the
  modeling feature count. The manuscript must report final modeling features
  separately after feature screening and ablation.

Core feature families:

| Family | Examples | Source |
| --- | --- | --- |
| Surveillance | lagged country rate, regional mean, source system, syndrome | ECDC-derived |
| Demography | population, rural population percent, GDP per capita | World Bank |
| Land use | FAOSTAT land-use classes and lagged summaries | FAOSTAT |
| Climate | annual TerraClimate summaries and lag-1 summaries | TerraClimate |
| Vegetation optional | QA-masked NDVI/EVI and valid-pixel counts | MODIS MOD13C2 V6.1 |

Forecast feature rule:

- One-year-ahead models for year `t` may use only information available on or
  before 31 December of year `t - 1`.

## Baseline Outputs

Files:

- `data/processed/international_baseline_predictions.csv`
- `data/processed/international_baseline_metrics.csv`

Builder:

- `python tools/run_international_baselines.py`

Required metric columns:

- `target_year`
- `model`
- `n`
- `mean_observed`
- `mean_wis`
- `relative_wis_observed_mean`
- `coverage_90`
- `mean_interval_width_90`
- `mae`
- `poisson_deviance`
- `brier_any_case`

Interpretation:

- WIS measures probabilistic forecast error.
- Relative WIS contextualizes WIS against average observed cases.
- Coverage must be interpreted with interval width; a model can cover well by
  being too wide.

## Reports

Generated reports:

- `reports/00_paper_readiness_and_results.md`
- `reports/01_international_data_audit.md`
- `reports/02_international_baselines.md`
- `reports/04_markov_simulation_stress_test.md`
- `reports/05_publication_readiness_gate.md`

Reports are ignored by git and should be regenerated for each audit.
