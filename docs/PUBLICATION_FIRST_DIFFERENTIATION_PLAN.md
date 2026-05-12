# Publication-First Differentiation Plan

Last checked: 2026-05-12

## Executive Decision

Do not compete with HantavirusMap as a live outbreak map.

HantavirusMap already occupies the public-facing signal-tracker lane: live map, active alerts, curated news, official/public-health source aggregation, country reports, and subscriptions. A publication-quality project should instead become the open, peer-reviewable benchmark that answers a different question:

> Given sparse and heterogeneous public surveillance, what can be forecast or stress-tested about reported hantavirus incidence, with calibrated uncertainty, explicit source provenance, and honest negative results?

The paper should be framed as an open research benchmark and validation study, not as a live public-health dashboard.

## What HantavirusMap Already Does

Observed from `https://hantavirusmap.com/` and its About/Outbreak pages on 2026-05-12:

- Aggregates WHO, ProMED, GDELT/news, CDC, ECDC, PAHO, and regional health-agency signals.
- Presents active alerts, endemic zones, and historical cases.
- Uses editorial curation and risk summaries.
- Labels signals as early indications, not confirmed case counts.
- Explicitly says it is informational, not authoritative, not medical advice, and not affiliated with official agencies.
- Provides live/update-oriented products such as alerts, country reports, RSS/JSON feeds, and a paid digest.

Important implication:

- A new project will look redundant if it mainly offers a current global map, country pins, active alerts, or source aggregation.

## What This Project Can Still Publish

The defensible contribution is not "another hantavirus map." It is:

1. A reproducible country-year reported-incidence benchmark.
2. A source-provenance schema that separates HFRS, HPS, HCPS, source system, region, and reporting definitions.
3. Strict temporal and leave-country validation.
4. Uncertainty-calibrated baselines that expose when complex models do not improve.
5. Climate, vegetation, land-use, and reporting-context covariate evaluation with pre-registered lags.
6. Scenario stress tests, such as Markov incidence-state simulations, clearly labeled as synthetic sensitivity analysis.
7. A reusable benchmark package that other researchers can rerun, extend, and cite.

## Recommended Manuscript Title

Primary:

> An open benchmark for country-level reported hantavirus incidence forecasting under sparse international surveillance

Alternative:

> Forecasting reported hantavirus incidence from public surveillance: an audited international benchmark with uncertainty-calibrated baselines

Avoid:

- Live global hantavirus map
- Outbreak tracker
- Real-time warning system
- Global risk dashboard
- HantavirusMap-style signal intelligence

## Paper Thesis

The paper should make this claim:

> Public hantavirus surveillance can support a transparent country-year reported-incidence benchmark, but not reliable fine-scale outbreak prediction from public data alone. Simple baselines are strong, calibration is difficult, and source-system/syndrome heterogeneity must be modeled rather than hidden.

This is useful because it gives researchers and public-health modelers a realistic benchmark, not another alert feed.

## Required Differentiators

### 1. Reproducibility Instead Of Live Curation

HantavirusMap is current and editorial. This project must be reproducible and archival.

Deliverables:

- Frozen source manifests.
- Source-total reconciliation.
- Data schema with provenance.
- Rebuild scripts.
- Versioned model outputs.
- A clear distinction between raw/source data, processed data, and redistributable artifacts.

Current status:

- ECDC 2019-2023 country-year table builder exists.
- Source totals reconcile exactly.
- World Bank and FAOSTAT covariates join.
- TerraClimate and MOD13C2 manifests exist.

Gap:

- TerraClimate and MODIS country-year aggregation is not done.

### 2. Forecast Evaluation Instead Of Signal Alerts

HantavirusMap alerts readers to current signals. This project must score forecasts against held-out data.

Required validation:

- Temporal split: train 2019-2021, validate 2022, test 2023 for the current ECDC seed.
- Rolling-origin validation as more years/sources are added.
- Leave-country-out validation after enough data exist.
- Source-system holdout after PAHO/China CDC rows are added.

Metrics:

- Weighted interval score.
- 90 percent empirical coverage.
- MAE/RMSE for medians.
- Poisson or negative-binomial deviance.
- Brier score for pre-registered any-case or high-incidence thresholds.

Current result:

- 2022 best WIS: empirical negative-binomial rate.
- 2023 best WIS: last-observed country rate.
- Gradient boosting is currently weak and undercovers. This is important and should not be hidden.

### 3. Scientific Uncertainty Instead Of Risk Scores

HantavirusMap uses signal strength/risk summaries. This project should use calibrated predictive distributions.

Paper angle:

- Show that intuitive "risk score" products can obscure uncertainty.
- Use quantile forecasts and empirical coverage.
- Make undercoverage a result, not an embarrassment.

Needed:

- Calibration plots.
- Interval-width/coverage tradeoff.
- Stratified performance by region, syndrome, source system, and country-size band.

### 4. Climate/Vegetation Hypothesis Testing

HantavirusMap is source aggregation. A paper needs scientific explanatory value.

Primary hypothesis:

- Lagged climate, vegetation, and land-use covariates improve country-year reported-incidence forecasts only in specific regions/source systems, and may not beat persistence everywhere.

Covariates:

- TerraClimate: precipitation, temperature, vapor pressure deficit, soil moisture, water deficit.
- MOD13C2: NDVI/EVI monthly summaries and anomalies.
- FAOSTAT: cropland, forest land, agricultural land, permanent meadows/pastures.
- World Bank: population, rurality, GDP as denominator/reporting-context covariates.

Pre-register lags:

- 0, 1, 2, and 3 years.

Do not claim:

- Causality.
- Individual risk.
- Local outbreak prediction.

### 5. Simulation As Scenario Stress Test

The user's Markov-chain idea is useful if carefully framed.

Recommended simulation module:

- A Markov incidence-state model with states like zero, low, high, and surge.
- Transition probabilities estimated by country/source/syndrome where data are sufficient.
- Reporting multiplier scenarios for under-detection.
- Climate/vegetation shock scenarios after covariates are joined.
- Synthetic panels used only for stress-testing metrics and uncertainty behavior.

Allowed paper use:

- "Scenario stress test."
- "Sensitivity analysis."
- "Benchmark robustness under sparse surveillance."

Blocked paper use:

- "We generated enough data."
- "Synthetic simulations validate the model."
- "This predicts real outbreaks."

Current status:

- A first Markov zero/low/high incidence-state simulation exists.
- It should be treated as an appendix until more source systems are added.

## Recommended Paper Structure

### Abstract

Emphasize:

- Open benchmark.
- Reported incidence.
- Country-year resolution.
- Syndrome/source-system stratification.
- Calibration and negative results.

Do not emphasize:

- Live map.
- Alerts.
- Operational prediction.

### Introduction

Core argument:

- Hantavirus surveillance is sparse, heterogeneous, and delayed.
- Public-facing signal maps are useful for awareness, but scientific forecasting needs benchmark datasets and validation.
- This paper fills the benchmark/validation gap.

### Methods

Sections:

1. Data sources and provenance.
2. Case table schema and source reconciliation.
3. Covariate construction.
4. Validation design.
5. Baselines.
6. Optional hierarchical/negative-binomial model.
7. Markov simulation stress test.
8. Ethics and limitations.

### Results

Minimum result panels:

1. Data audit and source-total reconciliation.
2. Country-year availability by source/syndrome.
3. Baseline skill table.
4. Calibration and coverage.
5. Climate/vegetation feature contribution after aggregation is complete.
6. Markov stress-test transition matrix and scenario outputs.
7. Negative result panel: where ML does not beat persistence.

### Discussion

Core message:

- The useful contribution is disciplined uncertainty and benchmark infrastructure.
- Sparse public data are not enough for operational local alerts.
- This benchmark gives future researchers a stronger starting point than ad hoc maps or unsupported model demos.

## Minimum Submission Criteria

Do not submit until all of these are true:

- ECDC table validates and source totals reconcile.
- TerraClimate country-year features are aggregated and non-leaky.
- MOD13C2 NDVI/EVI country-year features are aggregated or explicitly removed from claims.
- FAOSTAT/World Bank joins are complete.
- Baselines run and produce quantile forecasts.
- Calibration plots exist.
- Markov simulation is clearly labeled as stress testing.
- At least one of these is true:
  - the manuscript is explicitly ECDC/EU-EEA only, or
  - PAHO/China CDC rows are added with complete provenance and source-system strata.
- Claims avoid live-map, alerting, or public-health authority language.

## Competitive Positioning Against HantavirusMap

| Dimension | HantavirusMap | This project |
|---|---|---|
| Primary role | Live signal tracker | Peer-reviewable benchmark |
| Update style | Continuous/editorial | Reproducible/versioned |
| Data grain | Signals, regions, countries | Country-year source-stratified table |
| Output | Alerts, map, country reports | Forecast distributions and validation |
| Strength | Current awareness | Auditable science |
| Risk | Not peer-reviewed, signals not counts | Sparse data, weaker immediacy |
| Publication angle | Not enough by itself | Benchmark/data/methods paper |

## Next Engineering Work Package

1. Implement TerraClimate country-year aggregation.
2. Implement MOD13C2 quality-masked country-year NDVI/EVI aggregation.
3. Rebuild processed model table with lagged climate/vegetation features.
4. Add calibration panels and feature-ablation report.
5. Decide whether the first paper is ECDC-only.
6. If not ECDC-only, extract PAHO and China CDC rows with complete provenance.
7. Upgrade the count model to a proper negative-binomial GLM or Bayesian hierarchical model.
8. Re-run Markov stress tests with source/syndrome strata once more data exist.

## Go/No-Go Recommendation Today

No-go for journal submission today.

Go for continued development toward a publication-quality benchmark. The current repo is past "toy project" stage, but the paper's novelty depends on benchmark rigor, validation, and covariate evaluation, not on being a live map.
