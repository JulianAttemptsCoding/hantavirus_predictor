# Hantavirus Predictor Publication Audit Report

Last updated locally: 2026-05-13

Repository:

- `C:\Users\bubga.JULIAN-LAPTOPE2\OneDrive\Desktop\coding\hantavirus_predictor`
- Branch: `main`
- Latest pushed commit at time of this report: `5715f44 Add exploratory count model benchmark`
- Prior publication-package commit: `dfb2d26 Add publication ablation maps and manuscript package`
- Handoff commit before this work package: `c0e7a68 Add next agent completion prompt`

## 1. Executive Verdict

The ECDC-only paper-preparation stage is ready for manuscript writing.

This means:

- The ECDC/EU-EEA country-year data pipeline rebuilds locally.
- The data validation and publication readiness gate pass.
- Feature ablation exists and regenerates.
- IJHG-ready country-level maps exist and regenerate.
- Sensitivity and detectability analyses exist and regenerate.
- An exploratory penalized Poisson count model exists and regenerates.
- A tracked manuscript package exists under `docs/manuscript/`.
- Tests, ruff, whitespace checks, and secret-scan review were completed.
- The relevant tracked changes were committed and pushed to `origin/main`.

This does not mean final journal submission is ready. Final submission still
requires human-only publication decisions: journal/APC confirmation, author
list, affiliations, ORCID IDs, funding, competing interests, acknowledgements,
CRediT roles, preprint decision, institutional ethics wording, and DOI archive
destination/owner/license.

## 2. Scientific Scope

The current version is an ECDC-only EU/EEA public-data benchmark.

Primary scope:

- Geography: EU/EEA countries in ECDC Annual Epidemiological Report tables.
- Years: 2019-2023.
- Unit: country-year.
- Outcome: reported annual hantavirus infection case count and incidence per
  100,000 population.
- Evaluation task: retrospective one-year-ahead evaluation.
- Primary journal target: International Journal of Health Geographics.
- Fallback journals: Scientific Data or BMC Public Health.

Required framing:

- Use "reported incidence", not true infection burden.
- Use "retrospective one-year-ahead evaluation", not prospective forecasting.
- Treat this as a public surveillance benchmark, not a live outbreak tracker.
- Keep negative results.
- If simple baselines beat complex models, that is publishable when the
  limitations are documented honestly.

Prohibited claims:

- No global generalization from ECDC-only labels.
- No county-level U.S. human prediction.
- No individual, clinical, address-level, or operational alerting claim.
- No causal climate, land-use, or vegetation effect claim.
- No MODIS NDVI/EVI or vegetation claim unless QA-masked aggregation passes.
- No pooling of ECDC, PAHO, and China CDC labels without explicit source-system
  and syndrome strata.

## 3. Human Inputs Still Required Later

No human input is needed to continue manuscript drafting for the ECDC-only
publication path.

Human input is required only at later publication/deposition points:

- Journal submission:
  - Pick final target journal: IJHG first, Scientific Data fallback, or BMC
    Public Health fallback.
  - Confirm APC/payment route.
  - Provide author list, affiliations, ORCID IDs if available, corresponding
    author, funding statement, competing interests, acknowledgements, and
    CRediT contribution roles.
  - Confirm whether to post a preprint.
  - Confirm institutional ethics wording for aggregate public data.
- DOI deposition:
  - Provide Zenodo/OSF/Figshare destination or confirm GitHub-Zenodo integration.
  - Confirm what account/name owns the DOI.
  - Confirm license for the release package.
- Restricted U.S. subnational paper:
  - Not needed for this version.
  - Would require legally shareable restricted partner data from CDC, a state
    health department, or an IRB-approved collaborator.
- NASA Earthdata:
  - Not blocking this ECDC-only manuscript path because MODIS is excluded from
    claims.
  - Needed only if MODIS becomes required.

## 4. Data Sources And Data Lineage

### 4.1 Primary Label Source

Primary label source:

- ECDC Hantavirus infection Annual Epidemiological Report for 2023.
- Rows are manually/reproducibly built by `tools/create_ecdc_case_table.py`.
- The source table is ECDC Table 1, spanning 2019-2023 country-year reported
  cases.

Current source system:

- `ECDC` only.
- `PAHO` and `China CDC` rows are intentionally not included.

### 4.2 Public Covariates

Covariates currently included:

- World Bank:
  - Population denominator.
  - Rural population percent.
  - GDP per capita.
- FAOSTAT:
  - Land area.
  - Country area.
  - Agricultural land.
  - Cropland.
  - Forest land.
  - Permanent meadows/pastures.
  - Other land.
- TerraClimate:
  - Annual deficit sum.
  - Annual precipitation sum.
  - Annual soil moisture mean.
  - Annual maximum temperature mean.
  - Annual minimum temperature mean.
  - Annual vapor pressure deficit mean.
  - Lag-1 versions are complete for non-2019 forecast rows.
- Natural Earth:
  - 1:50m Admin 0 country boundaries for maps.

Covariates not included in manuscript claims:

- MODIS MOD13C2 NDVI/EVI.
- MODIS manifest exists, but quality-masked country-year aggregation has not
  passed the pre-registered gate.

## 5. Data Dimensions And Reconciliation

Processed analysis file:

- `data/processed/international_country_year.csv`
- Rows: `142`
- Columns: `97`

Important interpretation:

- The 97 columns are raw processed/audit columns.
- They are not the modeling feature count.
- Final modeling feature counts are reported separately in the feature
  screening output.

Rows by year:

| Year | Rows |
| --- | ---: |
| 2019 | 28 |
| 2020 | 28 |
| 2021 | 29 |
| 2022 | 29 |
| 2023 | 28 |

ECDC annual case reconciliation:

| Year | Rebuilt cases | Expected ECDC total | Difference |
| --- | ---: | ---: | ---: |
| 2019 | 4088 | 4088 | 0 |
| 2020 | 1693 | 1693 | 0 |
| 2021 | 4947 | 4947 | 0 |
| 2022 | 2185 | 2185 | 0 |
| 2023 | 1885 | 1885 | 0 |

Quality grades:

| Quality grade | Rows |
| --- | ---: |
| B | 140 |
| C | 2 |

Surveillance completeness flags:

| Completeness flag | Rows |
| --- | ---: |
| comprehensive | 140 |
| not_comprehensive | 1 |
| unspecified | 1 |

Special source-quality rows:

- Belgium 2023:
  - Cases: `99`
  - `surveillance_completeness = not_comprehensive`
  - `quality_grade = C`
  - Reason: ECDC did not calculate a rate after a surveillance-system change.
- Cyprus 2023:
  - Cases: `0`
  - `surveillance_completeness = unspecified`
  - `quality_grade = C`
  - Reason: ECDC metadata caveat/unspecified completeness context.

United Kingdom handling:

- UK rows are excluded from the primary ECDC seed because the 2023 ECDC table
  marks 2020 onward as not applicable after EU withdrawal.

## 6. Missingness And Data Quality

Missingness from the generated data audit:

| Field | Missing rows | Missing percent |
| --- | ---: | ---: |
| population | 0 | 0 |
| rural_population_pct | 0 | 0 |
| gdp_per_capita_current_usd | 0 | 0 |
| deaths | 114 | 80.28 |
| faostat_country_area_1000ha | 0 | 0 |
| faostat_land_area_1000ha | 0 | 0 |
| faostat_agricultural_land_1000ha | 0 | 0 |
| faostat_cropland_1000ha | 0 | 0 |
| faostat_forest_land_1000ha | 0 | 0 |
| faostat_perm_meadows_pastures_1000ha | 5 | 3.521 |
| faostat_other_land_1000ha | 0 | 0 |

Covariate join status:

| Covariate family | Joined | Missing rows |
| --- | --- | ---: |
| World Bank population | True | 0 |
| World Bank rurality/GDP | True | 0 |
| TerraClimate | True | 0 |
| MODIS MOD13C2 | False | 142 |
| FAOSTAT land use | True | 0 |

TerraClimate lag-1 missingness:

| Field | Missing rows | Missing percent |
| --- | ---: | ---: |
| terraclimate_def_annual_sum_mm_lag1 | 0 | 0 |
| terraclimate_ppt_annual_sum_mm_lag1 | 0 | 0 |
| terraclimate_soil_annual_mean_mm_lag1 | 0 | 0 |
| terraclimate_tmax_annual_mean_c_lag1 | 0 | 0 |
| terraclimate_tmin_annual_mean_c_lag1 | 0 | 0 |
| terraclimate_vpd_annual_mean_kpa_lag1 | 0 | 0 |

Duplicate primary keys:

- None found.

Death data caveat:

- Deaths are only populated for 2023 because the extracted ECDC country-year
  table does not provide 2019-2022 country death counts.
- Deaths are not a primary modeling target.

## 7. Rebuild Commands

The current pipeline is rebuilt from tracked scripts.

Environment:

```powershell
python -m pip install -e ".[dev,geo]"
```

Core data and baseline rebuild:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/create_mod13c2_manifest.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/plot_international_baselines.py
```

Publication-analysis rebuild:

```powershell
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/create_ijhg_maps.py
python tools/run_sensitivity_power.py
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
```

Repo QA:

```powershell
python -m pytest
python -m ruff check src tests tools
git diff --check
rg -n "password\s*=|token\s*=|secret\s*=|api_key|BEGIN [A-Z ]*PRIVATE KEY" .
```

## 8. Exact Math And Metric Definitions

### 8.1 Incidence Rate

For country-year row `i`:

```text
incidence_per_100k_i = cases_i / population_i * 100000
```

### 8.2 Count Mean From Rate

For a predicted rate per 100,000:

```text
mean_count_i = predicted_rate_i / 100000 * population_i
```

### 8.3 Central Interval Score

For observation `y`, lower interval bound `l`, upper interval bound `u`, and
miscoverage level `alpha`:

```text
IS_alpha(y, l, u) =
  (u - l)
  + (2 / alpha) * (l - y) * 1(y < l)
  + (2 / alpha) * (y - u) * 1(y > u)
```

For 90 percent intervals, `alpha = 0.1`.

### 8.4 Weighted Interval Score

The implementation uses the epidemic-forecast convention from Bracher et al.
with median absolute error weight `0.5` and interval weight `alpha / 2`.

With one central interval:

```text
WIS_i =
  [0.5 * |y_i - median_i| + (alpha / 2) * IS_alpha_i]
  / (1 + 0.5)
```

Mean WIS is the arithmetic mean over target rows.

### 8.5 Relative WIS

```text
relative_wis_observed_mean =
  mean_wis / mean(observed_cases_in_target_set)
```

This contextualizes WIS against the target-year average case count.

### 8.6 90 Percent Empirical Coverage

```text
coverage_90 = mean( q05_i <= observed_i <= q95_i )
```

Coverage must be interpreted together with interval width. A model can achieve
high coverage by being too wide.

### 8.7 Mean 90 Percent Interval Width

```text
mean_interval_width_90 = mean(q95_i - q05_i)
```

### 8.8 MAE

```text
MAE = mean(|observed_i - q50_i|)
```

### 8.9 Brier Score For Any Case

Binary target:

```text
z_i = 1(observed_i > 0)
```

Brier score:

```text
Brier = mean((probability_positive_i - z_i)^2)
```

### 8.10 MASE

The feature ablation reports MASE where the denominator is valid. The naive
reference is the last-observed-country-rate forecast.

```text
MASE = MAE_model / mean(|observed_i - naive_last_observed_rate_count_i|)
```

If the denominator is zero or invalid, MASE is not promoted.

### 8.11 Poisson Deviance

For observed count `y` and predicted mean `mu`:

```text
D_i = 2 * [ y_i * log(y_i / mu_i) - (y_i - mu_i) ]
```

For `y_i = 0`, the log term is defined as zero.

### 8.12 Poisson Predictive Distribution

For Poisson baselines and count GLM outputs:

```text
Y_i ~ Poisson(mu_i)
q05_i = PoissonPPF(0.05, mu_i)
q50_i = PoissonPPF(0.50, mu_i)
q95_i = PoissonPPF(0.95, mu_i)
probability_positive_i = 1 - P(Y_i = 0)
```

### 8.13 Negative Binomial Predictive Distribution

For empirical negative-binomial baselines:

```text
alpha_nb = max((variance(counts) - mean(counts)) / mean(counts)^2, 1e-6)
size = 1 / alpha_nb
probability = size / (size + mean_count)
Y_i ~ NegBin(size, probability)
```

Quantiles and probability-positive values are taken from that distribution.

### 8.14 Penalized Poisson GLM

The count model uses:

```text
log(mu_i) = log(population_i / 100000) + beta_0 + X_i beta
```

where:

- `log(population_i / 100000)` is the population offset.
- `X_i` is the screened feature vector.
- Non-intercept coefficients are penalized by ridge/L2 penalty.
- Validation year 2022 selects the penalty alpha.
- Test year 2023 is not used for tuning.

Optimization objective:

```text
sum_i [mu_i - y_i * eta_i] + 0.5 * alpha * sum_j beta_j^2
```

where:

```text
eta_i = offset_i + beta_0 + X_i beta
mu_i = exp(eta_i)
```

Coefficients are not interpreted causally.

## 9. Baseline Models

Implemented baseline models:

- `country_historical_mean_rate`
- `last_observed_country_rate`
- `region_syndrome_mean_rate`
- `empirical_negative_binomial_rate`
- `hierarchical_negative_binomial_rate`
- `gradient_boosting_rate`

Baseline split:

- Target years: 2022 and 2023.
- For each target year, training history is all years before that target year.
- Validation target: 2022.
- Test target: 2023.

All baseline metrics:

| Target year | Model | n | Mean observed | Mean WIS | Relative WIS | Coverage 90 | Mean interval width 90 | MAE | Poisson deviance | Brier any-case |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022 | country_historical_mean_rate | 29 | 75.344828 | 65.575862 | 0.870343 | 0.620690 | 21.068970 | 69.793103 | 98.503558 | 0.025459 |
| 2022 | empirical_negative_binomial_rate | 29 | 75.344828 | 47.174713 | 0.626117 | 1.000000 | 694.206897 | 72.103448 | 98.503558 | 0.158368 |
| 2022 | gradient_boosting_rate | 29 | 75.344828 | 92.306025 | 1.225114 | 0.000000 | 0.000000 | 92.306025 | 168.256844 | 0.278729 |
| 2022 | hierarchical_negative_binomial_rate | 29 | 75.344828 | 47.381609 | 0.628863 | 1.000000 | 693.517200 | 72.793103 | 147.887495 | 0.197742 |
| 2022 | last_observed_country_rate | 29 | 75.344828 | 101.462069 | 1.346636 | 0.551724 | 24.551720 | 108.068966 | 158.913969 | 0.033341 |
| 2022 | region_syndrome_mean_rate | 29 | 75.344828 | 154.857471 | 2.055317 | 0.137931 | 29.517240 | 163.344828 | 425.726166 | 0.308743 |
| 2023 | country_historical_mean_rate | 28 | 67.321429 | 52.472619 | 0.779434 | 0.535714 | 20.607140 | 58.142857 | 41.301722 | 0.036442 |
| 2023 | empirical_negative_binomial_rate | 28 | 67.321429 | 43.751190 | 0.649885 | 1.000000 | 660.035700 | 65.250000 | 41.301722 | 0.189876 |
| 2023 | gradient_boosting_rate | 28 | 67.321429 | 49.648446 | 0.737484 | 0.000000 | 0.000000 | 49.648446 | 65.831091 | 0.179646 |
| 2023 | hierarchical_negative_binomial_rate | 28 | 67.321429 | 43.895238 | 0.652025 | 1.000000 | 659.357100 | 65.750000 | 61.869565 | 0.214552 |
| 2023 | last_observed_country_rate | 28 | 67.321429 | 42.855952 | 0.636587 | 0.571429 | 14.607140 | 47.107143 | 44.704104 | 0.060549 |
| 2023 | region_syndrome_mean_rate | 28 | 67.321429 | 115.985714 | 1.722865 | 0.107143 | 28.857140 | 124.357143 | 268.506748 | 0.286644 |

Best baseline by target year:

| Target year | Best model | Mean WIS | Relative WIS | Coverage 90 | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| 2022 | empirical_negative_binomial_rate | 47.174713 | 0.626117 | 1.000000 | Accurate by WIS but over-wide intervals |
| 2023 | last_observed_country_rate | 42.855952 | 0.636587 | 0.571429 | Best WIS but under-covered |

Baseline conclusion:

- Simple empirical baselines are strong.
- Negative-binomial baselines can have excellent coverage by using very wide
  intervals.
- Last-observed rate is sharp and WIS-competitive in 2023 but under-covered.
- Any covariate model must beat these simple baselines without unacceptable
  calibration loss before being promoted.

## 10. Feature Ablation

Tracked implementation:

- `src/hantavirus_predictor/models/feature_ablation.py`
- `tools/run_feature_ablation.py`
- Tests: `tests/test_feature_ablation.py`

Generated outputs:

- `data/processed/feature_ablation_predictions.csv`
- `data/processed/feature_ablation_metrics.csv`
- `data/processed/feature_ablation_calibration.csv`
- `data/processed/feature_ablation_feature_screening.csv`
- `reports/03_feature_ablation.md`
- Figures:
  - `figures/03_feature_ablation_wis.png`
  - `figures/03_feature_ablation_relative_wis.png`
  - `figures/03_feature_ablation_coverage.png`
  - `figures/03_feature_ablation_interval_width.png`
  - `figures/03_feature_ablation_calibration.png`

Feature sets:

- `surveillance_only`:
  - target year
  - pandemic-period indicator
  - country historical rate
  - country last rate
  - country prior years
  - country zero share
  - region historical rate
  - overall historical rate
- `context`:
  - `surveillance_only`
  - lagged rural population percent
  - lagged GDP per capita
  - missingness indicators for those fields
- `land_use`:
  - `context`
  - lagged FAOSTAT land-use shares
  - FAOSTAT join flag
- `climate`:
  - `land_use`
  - lagged TerraClimate annual summaries
  - TerraClimate lag-1 missingness flags
- `all_public`:
  - `climate`
  - EU/EEA status
  - surveillance completeness
  - quality grade

Feature-screening rules:

- Train-only imputation.
- Continuous variables: train-set median.
- Binary flags: train-set mode.
- Categorical variables: explicit missing level.
- Drop features with more than 40 percent missingness unless essential.
- Drop constant features.
- Drop duplicate features.
- Drop highly correlated numeric features using pairwise correlation threshold
  `0.95`.
- Keep final feature count normally at or below 25 before one-hot encoding.

Feature ablation outputs:

- Prediction rows: `995`
- Metric rows: `35`
- Calibration rows: `70`
- Screening rows: `35`

Primary split:

- Train: 2019-2021.
- Validate: 2022.
- Test: 2023.

Leave-one-year-out sensitivity:

- Implemented for 2019, 2020, 2021, 2022, and 2023.

Primary feature-ablation metrics:

| Split | Target year | Feature set | n | Mean observed | Mean WIS | Relative WIS | Coverage 90 | Mean interval width 90 | MAE | MASE last observed rate | Poisson deviance | Brier any-case | Raw candidate features | Final model features before one-hot |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| primary_validation_2022 | 2022 | surveillance_only | 29 | 75.344828 | 94.422025 | 1.253199 | 0.689655 | 298.005835 | 131.775839 | 1.218772 | 236.763073 | 0.368305 | 8 | 7 |
| primary_validation_2022 | 2022 | context | 29 | 75.344828 | 94.110273 | 1.249061 | 0.724138 | 303.113618 | 133.915163 | 1.238558 | 224.287453 | 0.348918 | 12 | 9 |
| primary_validation_2022 | 2022 | land_use | 29 | 75.344828 | 93.808736 | 1.245059 | 0.758621 | 305.732089 | 134.052929 | 1.239832 | 215.683888 | 0.343749 | 18 | 14 |
| primary_validation_2022 | 2022 | climate | 29 | 75.344828 | 75.624457 | 1.003711 | 0.758621 | 271.640726 | 112.473549 | 1.040248 | 179.405916 | 0.368551 | 30 | 19 |
| primary_validation_2022 | 2022 | all_public | 29 | 75.344828 | 74.457079 | 0.988218 | 0.758621 | 264.921524 | 109.886938 | 1.016325 | 174.000216 | 0.385960 | 33 | 20 |
| primary_test_2023 | 2023 | surveillance_only | 28 | 67.321429 | 326.984894 | 4.857070 | 0.642857 | 314.497961 | 370.060963 | 7.853086 | 607.461808 | 0.285180 | 8 | 7 |
| primary_test_2023 | 2023 | context | 28 | 67.321429 | 333.071796 | 4.947486 | 0.678571 | 322.465975 | 381.249934 | 8.090527 | 620.058129 | 0.291142 | 12 | 9 |
| primary_test_2023 | 2023 | land_use | 28 | 67.321429 | 318.545603 | 4.731712 | 0.678571 | 325.866084 | 367.443960 | 7.797550 | 591.638148 | 0.293556 | 18 | 14 |
| primary_test_2023 | 2023 | climate | 28 | 67.321429 | 348.182044 | 5.171935 | 0.678571 | 293.203492 | 395.438370 | 8.391621 | 649.208144 | 0.312964 | 30 | 19 |
| primary_test_2023 | 2023 | all_public | 28 | 67.321429 | 331.345544 | 4.921844 | 0.642857 | 282.797337 | 374.726321 | 7.952090 | 608.931033 | 0.304642 | 33 | 20 |

Best feature-ablation model by target:

| Target year | Best ablation set | Mean WIS | Relative WIS | Coverage 90 | Interval width | MAE |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2022 | all_public | 74.457079 | 0.988218 | 0.758621 | 264.921524 | 109.886938 |
| 2023 | land_use | 318.545603 | 4.731712 | 0.678571 | 325.866084 | 367.443960 |

Feature ablation conclusion:

- Public covariates helped the ablation model in 2022 relative to its own
  surveillance-only ablation baseline.
- The richer models did not beat the best simple empirical baselines.
- 2023 remained difficult and under-covered.
- These are mixed/negative results and should be reported as such.

## 11. MODIS Decision

MODIS status:

- `tools/create_mod13c2_manifest.py` creates a manifest.
- `metadata/mod13c2_granule_manifest.csv` has 60 granule rows.
- No QA-masked country-year HDF aggregation has passed.
- `mod13c2_joined = False` for all 142 processed rows.

Pre-registered inclusion gate:

- MOD13C2 Version 6.1 QA-masked aggregation implemented.
- Valid-pixel coverage at least 95 percent for at least 90 percent of
  country-years.
- MODIS improves WIS or relative WIS by at least 5 percent against
  `all_public`.
- MODIS does not materially worsen 90 percent coverage.
- Pipeline reproducible from documented inputs.

Gate result:

- Fails/not complete for manuscript inclusion.

Consequence:

- No NDVI/EVI claim.
- No vegetation claim.
- MODIS remains future work.
- TerraClimate water-balance variables can be described only as climate and
  water-balance context, not vegetation.

## 12. IJHG Maps

Tracked implementation:

- `tools/create_ijhg_maps.py`

Generated report:

- `reports/06_ijhg_maps.md`

Generated map figures:

| Figure file | Size in bytes |
| --- | ---: |
| `figures/ijhg_incidence_choropleth_2023.png` | 160203 |
| `figures/ijhg_surveillance_completeness_2023.png` | 177653 |
| `figures/ijhg_predicted_observed_incidence_2023.png` | 240678 |
| `figures/ijhg_uncertainty_interval_width_2023.png` | 163225 |

Map methods:

- Boundaries: Natural Earth 1:50m Admin 0 countries.
- Projection: ETRS89 / LAEA Europe, `EPSG:3035`.
- Unit: country-level fills only.
- Palettes:
  - `viridis`
  - `cividis`
  - Okabe-Ito categorical colors
- Best 2023 ablation model used for prediction map: `land_use`.

Map guardrail:

- Captions must say these are country-level maps.
- Do not imply within-country precision.
- Do not imply individual risk.
- Do not imply causal spatial effects.

## 13. Penalized Count Model

Tracked implementation:

- `src/hantavirus_predictor/models/count_models.py`
- `tools/run_count_models.py`
- Tests: `tests/test_count_models.py`

Generated outputs:

- `data/processed/count_model_predictions.csv`
- `data/processed/count_model_metrics.csv`
- `data/processed/count_model_tuning.csv`
- `reports/08_count_models.md`

Model:

- Penalized Poisson GLM.
- Offset: `log(population / 100000)`.
- Ridge penalty on non-intercept coefficients.
- Hyperparameter selected using 2022 validation WIS.
- Test target: 2023.
- No causal coefficient interpretation.

2023 count-model metrics:

| Feature set | Alpha | Mean WIS | Relative WIS | Coverage 90 | Mean interval width 90 | MAE | Brier any-case | Final features |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| surveillance_only | 0.01 | 250.665476 | 3.723413 | 0.321429 | 35.321429 | 260.678571 | 0.123201 | 7 |
| context | 0.01 | 275.796429 | 4.096711 | 0.321429 | 37.107143 | 286.535714 | 0.122751 | 10 |
| land_use | 0.01 | 159.365476 | 2.367233 | 0.321429 | 28.821429 | 167.642857 | 0.098988 | 15 |
| climate | 10.00 | 274.564286 | 4.078408 | 0.250000 | 35.500000 | 285.000000 | 0.138783 | 20 |
| all_public | 10.00 | 262.778571 | 3.903342 | 0.214286 | 35.142857 | 273.035714 | 0.147307 | 21 |

Best count model:

- Feature set: `land_use`
- Alpha: `0.01`
- Mean WIS: `159.365476`
- Relative WIS: `2.367233`
- Coverage 90: `0.321429`

Count-model conclusion:

- The count model is exploratory.
- It does not beat the best simple 2023 baseline by WIS.
- It has unacceptable 90 percent coverage.
- It should not be promoted as the main result.
- The empirical baselines remain the scientific anchor.

## 14. Sensitivity And Detectability

Tracked implementation:

- `tools/run_sensitivity_power.py`

Generated outputs:

- `data/processed/sensitivity_metrics.csv`
- `data/processed/power_detectability.csv`
- `reports/07_sensitivity_power.md`

Sensitivity scenarios:

- `primary_all_rows`
- `exclude_non_comprehensive_or_unspecified`
- `exclude_2020_2021_training_years`

Sensitivity output:

- Metric rows: `87`

Power/detectability simulation:

- Rows: `5`
- Iterations per effect size: `50`
- Structure: preserves observed country-year structure and population offsets.
- Injected signal: standardized precipitation effect on simulated count rates.
- Detectability criterion: climate-augmented model improves 2023 WIS by at
  least 5 percent over a simple surveillance-rate model.

Detectability output:

| Log-rate effect per SD | Iterations | Mean relative WIS improvement | Median relative WIS improvement | Detectability rate at 5 percent WIS |
| ---: | ---: | ---: | ---: | ---: |
| 0.00 | 50 | 0.066736 | 0.116514 | 0.64 |
| 0.25 | 50 | 0.480018 | 0.748009 | 0.84 |
| 0.50 | 50 | 0.857787 | 0.887365 | 1.00 |
| 0.75 | 50 | 0.869396 | 0.873667 | 1.00 |
| 1.00 | 50 | 0.832912 | 0.831141 | 1.00 |

Interpretation caveat:

- This is a power screen, not validation evidence.
- It should be used to frame what effect sizes may be detectable at this sparse
  public country-year scale.
- It must not be used to claim a true climate effect in the observed data.

## 15. Markov Simulation

Tracked implementation:

- `src/hantavirus_predictor/simulations/markov_incidence.py`
- `tools/run_markov_simulation.py`

Generated outputs:

- `data/processed/markov_simulation_summary.csv`
- `reports/04_markov_simulation_stress_test.md`

Rows:

- `29`

Interpretation:

- Reported-incidence state stress test only.
- Appendix/supplementary material only.
- Not validation evidence.
- Not a human-to-human transmission model.
- Not an operational spread predictor.

## 16. Publication Readiness Gate

Generated report:

- `reports/05_publication_readiness_gate.md`

Verdict:

- `PASS for an ECDC-only public-data benchmark manuscript path.`

Gate criteria:

| Area | Status | Evidence |
| --- | --- | --- |
| ECDC source reconciliation | pass | Annual totals match ECDC Table 1 for 2019-2023. |
| Processed analysis table | pass | 142 rows across 5 years. |
| World Bank context | pass | Population, rurality, and GDP are non-missing for all rows. |
| FAOSTAT land use | pass | 142 joined rows. |
| TerraClimate current-year features | pass | 142 joined rows. |
| TerraClimate lag features | pass | 6 lag-1 climate features complete for 114 non-2019 rows. |
| Surveillance metadata flags | pass | Belgium 2023 and Cyprus 2023 are flagged for sensitivity analyses. |
| Forecast benchmark outputs | pass | 12 metric rows and 1026 quantile rows. |
| Calibration caution | warn | 2022 best baseline over-wide; 2023 best baseline under-covered. |
| Feature ablation outputs | pass | 35 feature-ablation metric rows. |
| Model feature dimensions | pass | 35 screening rows with raw and final feature counts. |
| Sensitivity and power analyses | pass | 87 sensitivity metric rows and 5 detectability rows. |
| Penalized count-model check | pass | 5 penalized count-model metric rows. |
| IJHG map package | pass | Natural Earth map notes exist with projection and palette details. |
| Simulation appendix | pass | 29 reported-incidence state simulation rows. |
| MODIS vegetation claims | warn | MODIS is manifest-only; vegetation claims must be removed. |
| International generalization claims | warn | PAHO and China CDC rows are not extracted. |

Warnings are not blockers for the ECDC-only manuscript. They are required
scientific caution.

## 17. Manuscript Package

Tracked manuscript directory:

- `docs/manuscript/`

Files:

| File | Purpose |
| --- | --- |
| `docs/manuscript/main_manuscript_draft.md` | Main manuscript draft with abstract, methods, results, limitations, ethics |
| `docs/manuscript/figure_captions.md` | Draft captions with country-level precision guardrails |
| `docs/manuscript/table_shells.md` | Table shells for sources, audit, feature families, metrics, sensitivity, count model |
| `docs/manuscript/cover_letter_ijhg.md` | Draft IJHG cover letter |
| `docs/manuscript/statements.md` | Data availability, code availability, ethics, funding, competing interests, acknowledgements |
| `docs/manuscript/credit_contributions.md` | CRediT contribution template |
| `docs/manuscript/reviewer_response_draft.md` | Response draft for likely reviewer criticisms |
| `docs/manuscript/archive_deposition_instructions.md` | Zenodo/OSF/Figshare release instructions without faking DOI |

Manuscript framing already included:

- Exact time span: 2019-2023.
- Exact row count: 142.
- ECDC-only primary scope.
- Novelty against live trackers and Zeimes-style spatial risk mapping.
- Negative-result framing.
- No county-level, global, causal, vegetation, or operational claims.

Manuscript still needs human metadata:

- Author list.
- Affiliations.
- ORCID IDs.
- Corresponding author.
- Funding.
- Competing interests.
- Acknowledgements.
- CRediT roles.
- APC/payment route.
- Preprint decision.
- Institutional ethics wording.

## 18. Figures

Generated figure files:

| Figure | File | Size in bytes |
| --- | --- | ---: |
| Baseline WIS | `figures/international_baseline_mean_wis.png` | 137137 |
| Baseline observed vs predicted | `figures/international_baseline_observed_vs_predicted.png` | 69210 |
| Ablation WIS | `figures/03_feature_ablation_wis.png` | 89603 |
| Ablation relative WIS | `figures/03_feature_ablation_relative_wis.png` | 79011 |
| Ablation coverage | `figures/03_feature_ablation_coverage.png` | 99398 |
| Ablation interval width | `figures/03_feature_ablation_interval_width.png` | 103877 |
| Ablation calibration | `figures/03_feature_ablation_calibration.png` | 147865 |
| IJHG incidence map | `figures/ijhg_incidence_choropleth_2023.png` | 160203 |
| IJHG surveillance map | `figures/ijhg_surveillance_completeness_2023.png` | 177653 |
| IJHG predicted-observed map | `figures/ijhg_predicted_observed_incidence_2023.png` | 240678 |
| IJHG uncertainty map | `figures/ijhg_uncertainty_interval_width_2023.png` | 163225 |

Figure policy:

- Generated figures are ignored by git.
- Scripts are tracked.
- Regenerate figures locally with the rebuild commands.

## 19. Tests And QA Results

Most recent QA results from this work session:

- `python -m pytest`: `26 passed`
- `python -m ruff check src tests tools`: `All checks passed`
- `git diff --check`: passed
- `tools/check_publication_readiness.py`: `PASS`

Secret scan command:

```powershell
rg -n "password\s*=|token\s*=|secret\s*=|api_key|BEGIN [A-Z ]*PRIVATE KEY" .
```

Secret scan output was reviewed. Hits were expected false positives:

- The regex command itself in documentation.
- Earthdata parser code that reads credentials without printing them.
- Dummy test credentials in `tests/test_earthdata_credentials.py`.
- Archived source-material examples under `source_material/llm_archives/...`.

Credential status:

- `nasa earthdata acc info.txt` remains ignored.
- No real credential file was staged or committed.

## 20. Git And Repo Status

Latest pushed commits:

```text
5715f44 Add exploratory count model benchmark
dfb2d26 Add publication ablation maps and manuscript package
c0e7a68 Add next agent completion prompt
```

Pushed state:

- `main` is pushed to `origin/main`.

Pre-existing user-side working-tree dirt remains intentionally untouched:

```text
D  HANTA-PINN-v1.0-Complete-Package.zip
D  HANTAVIRUS_PREDICTOR_Complete_Package_v1.0.0.zip
D  hanta-pinn-st-v1.0.zip
D  instructions.txt
D  potential blockers (2).txt
D  potential blockers (3).txt
D  potential blockers.txt
?? HANTAVIRUS_PREDICTOR_Complete_Package_v1.0.0 new.zip
```

Those zip/text deletions and the untracked new zip were not staged, reverted,
deleted, or committed.

This new `report.md` file is created after those commits and is not included
in the pushed commits unless separately staged and committed later.

## 21. Key Source Files Added Or Updated

New/important tracked implementation files:

- `src/hantavirus_predictor/models/feature_ablation.py`
- `src/hantavirus_predictor/models/count_models.py`
- `tools/run_feature_ablation.py`
- `tools/run_count_models.py`
- `tools/create_ijhg_maps.py`
- `tools/run_sensitivity_power.py`
- `tests/test_feature_ablation.py`
- `tests/test_count_models.py`

Updated QA/documentation files:

- `tools/check_publication_readiness.py`
- `PUBLICATION_MASTER_PLAN.md`
- `docs/AGENT_HANDOFF.md`
- `docs/PROJECT_STATE.md`
- `docs/data_dictionary.md`
- `docs/reproducibility_manifest.md`
- `docs/manuscript/*`

## 22. Problems, Risks, And Reviewer Vulnerabilities

### 22.1 Sparse Time Span

There are only five annual ECDC years, 2019-2023.

Risk:

- Weak temporal generalization.
- Limited power to detect covariate effects.
- Complex models can overfit easily.

Response:

- Keep model matrix small.
- Use strong baselines.
- Report negative results.
- Use sensitivity and detectability analysis.

### 22.2 Country-Level Aggregation

Country-year data mask within-country exposure heterogeneity.

Risk:

- Maps could be misread as local risk maps.
- Environmental covariates may be too coarse.

Response:

- Use country-level map captions.
- Avoid false within-country precision.
- Do not claim county/district/local prediction.

### 22.3 Reporting Heterogeneity

ECDC reports harmonized annual data, but surveillance systems differ.

Risk:

- Country comparisons can reflect reporting differences, not true burden.

Response:

- Include source-quality flags.
- Flag Belgium 2023 and Cyprus 2023.
- Run sensitivity excluding non-comprehensive/unspecified rows.

### 22.4 COVID-Era Reporting Disruption

2020-2021 may reflect public-health-system disruption.

Risk:

- Model training may learn pandemic-period reporting artifacts.

Response:

- Include pandemic-period indicator.
- Run sensitivity excluding 2020-2021 where sample size permits.

### 22.5 MODIS Not Ready

MODIS QA-masked country-year aggregation is not implemented.

Risk:

- Vegetation claims would be unsupported.

Response:

- Remove vegetation claims.
- Keep MODIS as future work.

### 22.6 Calibration Weakness

Coverage is imperfect:

- Best 2022 baseline coverage is 1.0 but interval width is very large.
- Best 2023 baseline coverage is 0.571429, under nominal 0.90.
- Best count model coverage is 0.321429, unacceptable for promotion.

Risk:

- Reviewers may challenge predictive usefulness.

Response:

- Present calibration and sharpness explicitly.
- Do not promote miscalibrated complex models.
- Frame as a benchmark showing limits of public country-year data.

### 22.7 Complex Models Do Not Beat Simple Baselines

Feature ablation and count models do not beat the strongest simple baselines.

Risk:

- Manuscript might look like a modeling failure.

Response:

- Make this the scientific result: simple baselines are hard to beat in sparse
  public surveillance.
- Emphasize reproducibility, negative-result transparency, and source-quality
  auditing.

## 23. Best Current Manuscript Argument

The strongest paper is not "we built a powerful outbreak predictor."

The strongest paper is:

> We created a frozen, auditable, open EU/EEA country-year benchmark for
> reported hantavirus incidence, linked it to public demographic, land-use, and
> climate covariates, and showed with probabilistic metrics that simple
> surveillance baselines remain hard to beat under sparse public annual
> reporting. This benchmark makes negative results and calibration problems
> visible instead of hiding them.

This is a credible IJHG framing because it includes:

- Public geospatial surveillance.
- Country-level maps.
- Source-quality metadata.
- Reproducible covariate joins.
- Projection and cartographic guardrails.
- Uncertainty and calibration.
- Honest limitations.

## 24. Suggested Paper Structure

Recommended manuscript structure:

1. Title:
   - "An open benchmark for country-level reported hantavirus incidence:
     retrospective one-year-ahead evaluation under sparse public surveillance"
2. Abstract:
   - State ECDC-only, EU/EEA, 2019-2023, 142 country-year rows.
   - State WIS, coverage, interval width, MAE, Brier, MASE.
   - State mixed/negative covariate results.
3. Introduction:
   - Surveillance problem.
   - Need for open benchmark.
   - Difference from live trackers and ecological suitability maps.
4. Related work:
   - Zeimes et al.
   - Kallio et al.
   - Reusken/Heyman.
   - Kazasidis/Geduhn/Jacob.
   - Glass et al.
   - Allen et al.
   - Forecast Hub/Bracher WIS literature.
5. Data:
   - ECDC labels.
   - World Bank, FAOSTAT, TerraClimate, Natural Earth.
   - Source-quality flags.
6. Methods:
   - Rebuild pipeline.
   - Feature sets.
   - Train/validation/test.
   - Metrics.
   - Sensitivity and detectability.
   - Maps.
7. Results:
   - ECDC reconciliation.
   - Baseline metrics.
   - Feature ablation.
   - Count model exploratory check.
   - Maps.
   - Sensitivity/power.
8. Discussion:
   - Simple baselines hard to beat.
   - Public data limitations.
   - Need for better surveillance or richer source-system-specific data.
9. Limitations:
   - Sparse years.
   - Country aggregation.
   - Reporting heterogeneity.
   - Belgium 2023.
   - COVID-era sensitivity.
   - Retrospective validation only.
   - No MODIS vegetation claim.
10. Data/code/ethics/CRediT statements.

## 25. Archive And DOI Status

Current archive preparation:

- `LICENSE` exists.
- `CITATION.cff` exists.
- Data dictionary exists and is updated.
- Reproducibility manifest exists and is updated.
- Archive deposition instructions exist at
  `docs/manuscript/archive_deposition_instructions.md`.

Not done:

- No DOI has been deposited.
- No DOI is claimed.
- No archive owner/account is assumed.
- No final release license choice is assumed beyond existing repo files.

Before DOI:

- Confirm destination: Zenodo, OSF, Figshare, or GitHub-Zenodo.
- Confirm owner account/name.
- Confirm release license.
- Regenerate all outputs.
- Generate checksums.
- Run final QA.

## 26. What Is Done Versus Not Done

Done for this stage:

- ECDC-only data rebuild.
- Strict validation.
- FAOSTAT download/join.
- TerraClimate manifest and aggregation.
- Natural Earth download.
- Processed dataset build.
- MODIS manifest creation.
- Data audit report.
- Baseline models and figures.
- Feature ablation.
- Calibration outputs.
- MASE where valid.
- IJHG map package.
- Penalized Poisson count-model exploratory check.
- Sensitivity analyses.
- Detectability simulation.
- Markov simulation.
- Publication readiness gate.
- Manuscript skeleton.
- Reviewer-response draft.
- Archive instructions.
- Tests and ruff.
- Clean intended commits pushed.

Not done or intentionally deferred:

- MODIS QA-masked NDVI/EVI aggregation.
- MODIS/vegetation claims.
- PAHO/China source-system expansion.
- U.S. county-level human prediction.
- Final author metadata.
- Final journal submission package.
- DOI deposition.
- Generated data/reports/figures committed to git.
- User-side zip/text working-tree dirt resolution.

## 27. Final Current Recommendation

Start writing the paper now.

The best paper should be written as an honest benchmark and negative/mixed
result study:

- Lead with the open, auditable ECDC/EU-EEA benchmark.
- Show that ECDC totals reconcile exactly.
- Emphasize probabilistic evaluation, calibration, and uncertainty.
- Report that simple baselines are hard to beat.
- Keep the penalized count model exploratory.
- Exclude MODIS/vegetation claims.
- Use IJHG maps to support the geospatial public-health framing.
- Ask for human-only submission metadata only when the manuscript is ready for
  journal submission.
