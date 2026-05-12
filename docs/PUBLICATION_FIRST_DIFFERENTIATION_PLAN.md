# Publication-First Differentiation Plan

Last checked: 2026-05-12

## Executive Decision

Do not compete with HantavirusMap as a live outbreak map.

HantavirusMap already occupies the public-facing signal-tracker lane: live map, active alerts, curated news, official/public-health source aggregation, country reports, and subscriptions. A publication-quality project should instead become the open, peer-reviewable benchmark that answers a different question:

> Given sparse and heterogeneous public surveillance, what can be forecast or stress-tested about reported hantavirus incidence, with calibrated uncertainty, explicit source provenance, and honest negative results?

The paper should be framed as an open research benchmark and validation study, not as a live public-health dashboard.

## Marketable Core Package

### One-sentence pitch

> The Open Hantavirus Risk Benchmark is a reproducible, uncertainty-calibrated benchmark for country-level reported hantavirus incidence that tests what public surveillance, climate, vegetation, and land-use data can and cannot forecast.

### One-paragraph public summary

Hantavirus surveillance is sparse, delayed, and inconsistent across countries. Public signal maps are useful for awareness, but they do not answer a peer-review question: how much predictive skill is actually possible from public data, and where do simple baselines outperform more complex models? This project builds an audited country-year benchmark with source provenance, syndrome/source-system strata, environmental covariates, calibrated forecast distributions, and scenario simulations that make uncertainty visible instead of hiding it behind a risk score.

### What makes it relevant

- Hantaviruses are climate- and ecology-sensitive zoonoses, but public human case data are sparse.
- Health agencies and researchers need realistic benchmarks before operational alert systems can be trusted.
- The project turns a negative result into a contribution: if public data cannot support fine-scale forecasts, the benchmark shows that rigorously.
- The benchmark is reusable: new agencies, countries, covariates, or partner datasets can plug into the same schema and validation framework.

### What makes it marketable

- It has a clear name: **Open Hantavirus Risk Benchmark**.
- It has a clear enemy: false precision in sparse zoonotic forecasting.
- It has a clear promise: transparent uncertainty and source provenance.
- It has a clean contrast with HantavirusMap: HantavirusMap tracks signals; this project validates forecasts.
- It has useful artifacts beyond the paper: schema, validators, source manifests, baseline leaderboard, figures, and simulation stress tests.

### Taglines

- "Forecasting limits made visible."
- "A benchmark before a warning system."
- "Reported incidence, calibrated uncertainty, no false precision."
- "A reproducible test bed for hantavirus risk modeling."

### Audiences

Primary scientific audience:

- infectious-disease modelers
- zoonotic disease ecologists
- One Health researchers
- climate-health and health-geography researchers
- surveillance-methods reviewers

Practical audience:

- public-health surveillance teams
- regional or national health agencies
- labs holding non-public subnational data
- funders interested in climate-sensitive disease early warning

Public audience:

- keep limited and careful; this is not a public alert product.

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

## Journal Positioning

### Best first target: International Journal of Health Geographics

Why it fits:

- The journal explicitly covers GIS/geospatial health applications, remote sensing, spatial epidemiology, spatiotemporal statistics, and surveillance services.
- The benchmark can be framed around country-level spatial health data infrastructure, remote-sensing covariates, and forecast validation.
- It is a better first target than a live-alert framing because the paper is methodological and geospatial.

How to pitch:

> We provide a reproducible country-year benchmark and validation framework for reported hantavirus incidence, integrating surveillance provenance, country-level covariates, remote-sensing source manifests, uncertainty-calibrated baselines, and scenario stress tests.

### Second target: PLOS Neglected Tropical Diseases

Why it can fit:

- Strong if the manuscript emphasizes One Health, zoonotic spillover, neglected populations, public-health relevance, and LMIC applicability.
- Needs a careful argument because the current ECDC-only seed is high-income-region heavy.

How to pitch:

> This benchmark helps quantify what public surveillance can and cannot support for a neglected zoonotic disease, with an upgrade path for Latin American and Asian HPS/HFRS data.

Risk:

- An ECDC-only paper may be too Europe/high-income focused unless expanded with PAHO/China CDC or positioned as a methods benchmark with clear global extension.

### Third target: Emerging Infectious Diseases

Why it can fit:

- Good if the paper emphasizes surveillance, emergence, public-health interpretation, and the limits of current public data.

Risk:

- EID may prefer stronger public-health findings or outbreak/surveillance conclusions over a benchmark-methods paper.

### Do not target first

- Nature Communications, Lancet Planetary Health, or PLOS Computational Biology until the covariate and validation results are much stronger.
- Any venue expecting a real-time operational system.

## Title, Abstract, And Cover-Letter Strategy

### Recommended title

> An open benchmark for country-level reported hantavirus incidence forecasting under sparse international surveillance

### Subtitle option

> Calibrated baselines, environmental covariates, and simulation stress tests without false precision

### Abstract spine

Background:

- Hantavirus surveillance is sparse and heterogeneous.
- Public signal trackers exist, but forecast validation benchmarks are missing.

Methods:

- Construct a source-provenance country-year table.
- Join population, rurality, GDP, land use, and planned climate/vegetation covariates.
- Evaluate baselines under temporal validation.
- Add Markov/reservoir-spillover simulations as scenario stress tests.

Results:

- Report row counts and exact source reconciliation.
- Show baseline performance and calibration.
- Show whether environmental covariates improve forecasts.
- Report where complex models fail to beat simple baselines.

Conclusion:

- The paper provides a reusable benchmark and shows the practical limits of public surveillance for hantavirus forecasting.

### Cover-letter hook

> Unlike live signal maps, this manuscript asks what can be validated from public surveillance. The result is a reusable benchmark that helps prevent false precision in climate-sensitive zoonotic disease forecasting.

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
- TerraClimate country-year covariates join for the ECDC seed table.
- MOD13C2 manifest exists.

Gap:

- MODIS quality-masked country-year aggregation is not done.
- PAHO and China CDC rows are not extracted.

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

## Spread Simulation Decision

### Important biological correction

Do not market this as a generic human "spread simulation." Human-to-human transmission is not the normal mechanism for most hantaviruses, and reviewers will punish a paper that implies COVID-style spread dynamics. The defensible simulation target is:

> environmental suitability -> reservoir infection/activity -> reported human spillover -> surveillance observation.

Use "spillover simulation," "reservoir-spillover scenario model," or "reported-incidence state simulation." Avoid "human spread simulator" unless modeling a specific virus/context where human-to-human transmission is documented and sourced.

### Simulation should answer one of three paper-relevant questions

1. **Surveillance dynamics question**
   - How persistent are zero, low, and high reported-incidence states?
   - Current Markov state model supports this.
   - Good for an appendix now.

2. **Reservoir-spillover scenario question**
   - If climate/vegetation anomalies change reservoir suitability, how does the distribution of reported human cases shift?
   - TerraClimate is now available; vegetation claims still require MODIS aggregation.
   - Best long-term simulation contribution.

3. **Benchmark stress-test question**
   - Under underreporting, reporting delays, or source-system changes, which metrics and baselines remain stable?
   - Useful for methods reviewers.
   - Does not require pretending simulations are real data.

### Recommended simulation architecture

Layer 1: latent environmental suitability

- Country-year climate and vegetation anomalies.
- Land-use context.
- Optional ENSO/regional climate indicators.

Layer 2: reservoir pressure

- Latent reservoir activity/infection pressure.
- Autoregressive persistence.
- Climate/vegetation lag effects.
- Region/syndrome/source-system random effects.

Layer 3: human spillover/reporting

- Reported cases as overdispersed counts.
- Population offset.
- Reporting-capacity covariates such as GDP/rurality.
- Underreporting multiplier scenarios.

Layer 4: surveillance observation

- Reporting delays.
- missingness.
- source-system differences.
- thresholded alert states.

Minimum model family:

- Hidden Markov model or Markov-switching negative-binomial state model.

Better later model family:

- Hierarchical Bayesian state-space model with latent reservoir pressure and observation model.

Do not start with:

- agent-based human-to-human transmission
- county-level maps without labels
- neural simulator
- synthetic data used to enlarge training data

### What the simulation adds to the paper

Useful additions:

- An interpretable state-transition view of incidence persistence.
- Scenario stress tests for underreporting and environmental anomalies.
- A reviewer-friendly explanation of why forecast intervals need to be wide.
- A way to test whether a model is robust to sparse surveillance artifacts.

Not useful:

- Generating fake cases to make sample size look bigger.
- Showing dramatic outbreak animations.
- Claiming operational forecasts without prospective validation.

### Simulation figure plan

Figure S1:

- Markov zero/low/high transition matrix.

Figure S2:

- Simulated next-year reported-case distributions under baseline, 2x underreporting correction, and high environmental-suitability scenarios.

Figure S3:

- Metric stress test: WIS and coverage under different reporting multipliers.

Main-text figure only if mature:

- A simple schematic of the reservoir-spillover observation process.

### Simulation go/no-go

Use in main paper only if:

- It is calibrated to observed country-year data.
- It improves interpretation of uncertainty or validation limits.
- It is clearly separated from empirical validation.

Keep in supplement if:

- It is only the current zero/low/high Markov state model.

Remove if:

- Reviewers could interpret it as unsupported synthetic validation.

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

Recommended figures:

1. **Benchmark schematic:** source systems -> schema -> covariates -> baselines -> validation.
2. **Data audit:** countries/years/source systems and reconciliation.
3. **Forecast skill:** WIS, coverage, and MAE by baseline and year.
4. **Calibration:** observed versus predicted and interval coverage.
5. **Environmental covariate ablation:** baseline versus climate/vegetation/land-use feature sets.
6. **Simulation stress test:** transition matrix and scenario distributions.
7. **Limitations panel:** what public data can and cannot support.

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

## Marketing And Release Plan

### Pre-submission

- README headline should say "research benchmark," not "map" or "tracker."
- Add a static image of the benchmark workflow, not a live risk map.
- Publish a model-card style limitations table.
- Include a small leaderboard table for baselines.
- Add clear "not for public-health warning" language.

### Preprint launch

- Title the post around the benchmark problem: "How much can public hantavirus surveillance actually forecast?"
- Lead with the negative/realistic finding if simple baselines are hard to beat.
- Share the data audit and reproducibility scripts.
- Avoid alarmist maps or country rankings.

### GitHub release

- Tag a release only when scripts rebuild all non-sensitive outputs.
- Include generated reports, source manifests, and frozen configs.
- Put raw restricted or credentialed data outside the release.

### Outreach targets

- infectious disease modeling groups
- One Health surveillance researchers
- climate-health modelers
- ECDC/PAHO-adjacent surveillance analysts
- labs with restricted subnational hantavirus data

### Messaging guardrails

Say:

- "reported incidence"
- "country-year benchmark"
- "uncertainty-calibrated"
- "source-provenance first"
- "scenario stress test"

Do not say:

- "real-time risk map"
- "outbreak oracle"
- "human spread predictor"
- "validated warning system"
- "case counts are complete"

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

1. Add calibration panels and feature-ablation report.
2. Decide whether the first paper is ECDC-only.
3. Implement MOD13C2 quality-masked country-year NDVI/EVI aggregation only if vegetation improves the manuscript; otherwise remove vegetation claims.
4. If not ECDC-only, extract PAHO and China CDC rows with complete provenance.
5. Upgrade the count model to a proper negative-binomial GLM or Bayesian hierarchical model.
6. Expand the simulation from current incidence-state Markov model to reservoir-spillover scenario stress test using TerraClimate anomalies.
7. Write a manuscript skeleton with figure captions before adding advanced models.

## Go/No-Go Recommendation Today

No-go for final journal submission today because manuscript text, feature ablations, and final target-journal formatting are not done.

Go for continued development toward a publication-quality benchmark. The current repo is past "toy project" stage, but the paper's novelty depends on benchmark rigor, validation, and covariate evaluation, not on being a live map.
