# Appendix: Methods and EID Evidence Package

## A. Source Audit and Data Construction

The benchmark uses public aggregate EU/EEA country-year reported hantavirus
surveillance labels for 2019-2023. Annual totals reconcile exactly to ECDC:
4,088; 1,693; 4,947; 2,185; and 1,885 reported cases. Belgium 2023 and Cyprus
2023 are flagged as source-quality grade C; all other rows are grade B.

Primary source and model-input files:

- `docs/submission_eid/tables/table1_model_inputs.csv`
- `docs/submission_eid/tables/table1_model_inputs.md`
- `docs/submission_eid/reproducibility_manifest.md`

## B. Complete Feature Dictionary and Inclusion Logic

The complete EID Table 1 contains category, variable name, definition, unit,
source, years available, lag, training range, missingness counts, missingness
rule, feature-set inclusion, rationale, limitation, and leakage check.

Feature blocks:

1. Surveillance only: target year, pandemic-period indicator, lagged country
   rate summaries, regional history, and overall panel history.
2. Context: surveillance plus World Bank rurality and GDP.
3. Land use: context plus FAOSTAT land-use shares.
4. Climate: land use plus TerraClimate lag-1 climate and water-balance summaries.
5. All public: climate plus ECDC/source-quality metadata.

MODIS NDVI/EVI is documented as an excluded candidate because quality-masked
country-year aggregation was not implemented and audited for this submission.

## C. Model Schematic

Appendix Figure model_schematic shows the workflow:

```text
ECDC labels -> public covariate joins -> training-only imputation/screening ->
baselines and covariate blocks -> 2022 validation / 2023 locked test ->
WIS, coverage, width, MAE, Brier -> sensitivity, influence, detectability
```

The schematic is stored at:

```text
docs/submission_eid/figures/Appendix_Figure_model_schematic.tif
```

## D. Forecasting Workflow

Primary split:

```text
train: 2019-2021
validate: 2022
test: 2023
```

All imputation, feature screening, and tuning steps use training rows or the
validation year only. Target-year case counts are never used as predictors.

## E. Weighted Interval Score Details

For observed count y, lower bound l, upper bound u, median m, and alpha = 0.10:

```text
IS_alpha = (u - l)
         + (2 / alpha) * (l - y) * 1(y < l)
         + (2 / alpha) * (y - u) * 1(y > u)

WIS = [0.5 * abs(y - m) + (alpha / 2) * IS_alpha] / 1.5
```

Coverage and sharpness were reported as:

```text
coverage_90 = mean(q05 <= observed <= q95)
interval_width = mean(q95 - q05)
MAE = mean(abs(observed - q50))
Brier = mean((P(Y > 0) - 1(observed > 0))^2)
```

## F. Missing-Data Handling

Continuous features were imputed with training-set medians. Binary features were
imputed with training-set modes. Missingness indicators were retained where
defined. Features with greater than 40% training missingness were excluded
unless they were required surveillance-history features.

## G. Feature-Screening Rules

Feature screening was performed inside the training workflow. The rules were:

1. Remove high-missingness features.
2. Remove constant features in the training matrix.
3. Remove duplicate columns.
4. Remove highly correlated numeric predictors with absolute training
   correlation greater than 0.95.
5. Cap the pre-one-hot feature set at 25 variables using the prespecified
   feature-family priority order.

## H. Baseline Model Formulas

Last-observed country-rate baseline:

```text
r_hat_it = incidence_i,t-1
mu_hat_it = r_hat_it / 100,000 * population_it
Y_it ~ Poisson(mu_hat_it)
```

Country historical mean-rate baseline:

```text
r_hat_it = mean(incidence_i,s for all s < t)
mu_hat_it = r_hat_it / 100,000 * population_it
Y_it ~ Poisson(mu_hat_it)
```

Empirical negative-binomial baseline:

```text
alpha_nb = max((var(y_train) - mean(y_train)) / mean(y_train)^2, 1e-6)
size = 1 / alpha_nb
prob = size / (size + mu_hat_it)
Y_it ~ NegBin(size, prob)
```

## I. Penalized Poisson Model Details

The exploratory count model used a log population offset:

```text
log(mu_it) = log(population_it / 100,000) + beta_0 + X_it beta
```

The ridge penalty was applied only to non-intercept coefficients. The penalty
parameter was selected on 2022 validation WIS from {0.01, 0.1, 1, 10}. The best
2023 model used the land-use block with alpha = 0.01 but covered only 9/28
observations. Coefficients are penalized, exploratory, and not inferential.

## J. Surveillance-Quality Sensitivity

The sensitivity report is stored at:

```text
docs/submission_eid/reports/surveillance_quality_sensitivity.md
```

Scenarios included primary all rows, Belgium 2023 exclusion, Cyprus 2023
exclusion, combined Belgium/Cyprus exclusion, retained flagged-row indicator,
and COVID-era training exclusions. No scenario supported promotion of a public
covariate model.

## K. Leave-One-Country-Out Influence

The influence report is stored at:

```text
docs/submission_eid/reports/country_influence.md
```

Finland and Germany were pre-specified influence checks because ECDC reported
that they accounted for 60.5% of 2023 reported cases. Removing either country
did not make a covariate block outperform surveillance baselines.

## L. Calibration Localization

The calibration-localization report is stored at:

```text
docs/submission_eid/reports/calibration_localization.md
```

The table lists each 2023 country prediction, observed count, lower 90% bound,
median, upper 90% bound, coverage indicator, interval width, absolute error, and
source-quality flag.

## M. Detectability Simulation

The detectability report is stored at:

```text
docs/submission_eid/reports/detectability_screen.md
```

The simulation preserves the observed country-year structure and country
populations, then tests effect sizes from none to large across low,
observed-like, and high overdispersion and with/without observed-like
missingness patterns. The maximum null covariate-selection probability was
0.000 under the conservative selection rule.

Interpretation is limited:

```text
Simulation results do not validate model skill; they indicate that this sample
structure has limited ability to detect modest covariate effects under the
tested assumptions.
```

## N. MODIS Exclusion Gate

MODIS MOD13C2 NDVI/EVI is not used in primary models. The source manifest exists,
but quality-masked country-year aggregation was not implemented and audited.
The manuscript therefore makes no vegetation claims.

## O. Reproducibility Commands

Core commands:

```powershell
python -m pip install -e ".[dev,geo]"
python tools/create_ecdc_case_table.py --accessed-date 2026-05-14
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/run_international_baselines.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/write_eid_model_inputs_table.py
python tools/run_surveillance_quality_sensitivity.py
python tools/run_country_influence.py
python tools/write_calibration_localization.py
python tools/run_detectability_screen.py --iterations 100
python tools/create_eid_figures.py
python tools/build_eid_docx.py
python tools/check_eid_submission_readiness.py --strict
python -m pytest
python -m ruff check src tests tools
git diff --check
```
