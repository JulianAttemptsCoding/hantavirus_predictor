# Data Dictionary

Last updated: 2026-05-14

This dictionary describes the active EID EU/EEA country-year reported-incidence
benchmark. Generated CSV files live under `data/` and are intentionally ignored
by git.

## Manual Case Table

File:

- `data/manual/international_country_cases.csv`

Builder:

- `python tools/create_ecdc_case_table.py --accessed-date 2026-05-14`

Validator:

- `python tools/validate_international_cases.py --strict`

Schema:

- `schemas/international_country_cases.schema.yaml`

Core columns:

| Column | Meaning |
| --- | --- |
| `iso3` | ISO3 country code. |
| `country` | Country name as used for reporting. |
| `year` | Reporting year. |
| `reporting_system` | Source reporting system, currently TESSy/ECDC-derived. |
| `syndrome` | Human syndrome/reporting label. |
| `pathogen_or_virus` | Virus if source-reported; otherwise unspecified hantavirus. |
| `cases` | Reported annual case count. |
| `deaths` | Reported deaths when available. |
| `population` | Population denominator when included in the manual table. |
| `case_definition` | Source case definition summary. |
| `source_url` | Primary source URL. |
| `source_title` | Source title. |
| `accessed_date` | Local access date. |
| `quality_grade` | Source-quality grade. |
| `region` | Analysis region label. |
| `eu_eea_status` | EU/EEA membership status used for panel consistency. |
| `surveillance_completeness` | Completeness flag from source metadata. |
| `source_type` | Source document family. |
| `notes` | Human-readable source caveats. |

Current caveats:

- Belgium 2023 is `not_comprehensive` because ECDC did not calculate a rate
  after a surveillance-system change.
- Cyprus 2023 is `unspecified` for the ECDC metadata caveat.
- United Kingdom rows are excluded from the primary panel because ECDC reports
  no UK data from 2020 onward after EU withdrawal.

## Processed Analysis Table

File:

- `data/processed/international_country_year.csv`

Builder:

- `python tools/build_international_dataset.py`

Purpose:

- Join ECDC reported cases to public demographic, land-use, climate, boundary,
  and source-quality metadata.
- Preserve provenance and quality flags.
- Keep the raw processed table separate from the final screened modeling matrix.

Core feature families:

| Family | Examples | Source |
| --- | --- | --- |
| Outcome | reported annual cases, reported incidence | ECDC |
| Surveillance history | lagged country rate, historical mean rate, panel summaries | ECDC-derived |
| Demography | population, rural population percentage, GDP context | World Bank |
| Land use | forest, cropland, meadows/pastures shares | FAOSTAT |
| Climate | annual and lag-1 TerraClimate summaries | TerraClimate |
| Source quality | surveillance completeness, quality grade | ECDC-derived |
| Boundaries | country polygons for aggregation and maps | Natural Earth |

Forecast rule:

- One-year-ahead models for year `t` may use only information available on or
  before 31 December of year `t - 1`.

## Model Outputs

Baseline files:

- `data/processed/international_baseline_predictions.csv`
- `data/processed/international_baseline_metrics.csv`

Covariate-block files:

- `data/processed/feature_ablation_predictions.csv`
- `data/processed/feature_ablation_metrics.csv`
- `data/processed/feature_ablation_calibration.csv`
- `data/processed/feature_ablation_feature_screening.csv`

Count-model files:

- `data/processed/count_model_predictions.csv`
- `data/processed/count_model_metrics.csv`
- `data/processed/count_model_tuning.csv`

Sensitivity files:

- `data/processed/sensitivity_metrics.csv`
- `data/processed/power_detectability.csv`

Required metrics:

- `mean_wis`
- `coverage_90`
- `mean_interval_width_90`
- `mae`
- `brier_any_case`
- `poisson_deviance`
- `relative_wis_observed_mean`

Interpretation:

- WIS must be interpreted with coverage and interval width.
- A sharp model that undercovers cannot be promoted.
- A model with wide intervals and high coverage can be uninformative.

## Submission Artifacts

Tracked EID artifacts live in:

- `docs/submission_eid/`

The final package must add EID-specific model input, sensitivity, influence,
calibration-localization, and detectability outputs before submission.
