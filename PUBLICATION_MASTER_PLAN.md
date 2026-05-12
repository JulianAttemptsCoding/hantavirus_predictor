# Publication Master Plan From Current Repo State To Journal Submission

Last updated: 2026-05-12

This is the root-level audited plan for taking this repository from its current
ECDC-only public-data benchmark state to a publication-ready manuscript and
reproducible code release.

The plan is intentionally conservative. It is written so a reviewer, future
agent, or human collaborator can see exactly what is implemented, what remains,
what claims are allowed, and what must fail QA before the paper is submitted.

## 1. Executive Decision

### 1.1 Paper Identity

Recommended project identity:

> Open Hantavirus Risk Benchmark: an open, provenance-first,
> uncertainty-calibrated benchmark for country-year reported hantavirus
> incidence using free public surveillance, demographic, land-use, and climate
> data.

Recommended manuscript title:

> An open benchmark for country-level reported hantavirus incidence forecasting
> under sparse public surveillance

The paper should be a forecast benchmark and reproducible data/methods paper.
It should not be a public alert dashboard, a clinical tool, a county-level human
risk predictor, or a generic human-to-human spread simulator.

### 1.2 Current Verdict

The repo currently passes the ECDC-only public-data benchmark gate:

- `reports/05_publication_readiness_gate.md`: PASS for the ECDC-only
  public-data benchmark manuscript path.
- `data/processed/international_country_year.csv`: 142 ECDC country-year rows,
  95 columns.
- ECDC totals reconcile exactly for 2019-2023.
- World Bank context joins all rows.
- FAOSTAT land-use joins all rows.
- TerraClimate current-year features join all rows.
- TerraClimate lag-1 forecast features are complete for all non-2019 rows.
- Baseline forecasts, metrics, figures, audit reports, and Markov-style
  stress-test outputs rebuild from scripts.

The repo is not yet ready for final journal submission because the manuscript
text, feature-ablation tables, final figure set, and target-journal package are
not done. MODIS vegetation claims and global generalization claims are not
allowed unless the corresponding data work is completed and passes QA.

### 1.3 Main Publication Path

Primary path:

1. Submit an ECDC/EU-EEA public-data benchmark paper to International Journal
   of Health Geographics.
2. Keep the manuscript narrow: EU/EEA country-year reported incidence,
   uncertainty-calibrated forecasting, climate/land-use covariate evaluation,
   and surveillance limitations.
3. Treat simulation as a stress-test appendix, not validation evidence.
4. Add PAHO and China CDC rows only if there is time to extract them with
   complete provenance and explicit source-system strata.
5. Add MODIS only if quality-masked NDVI/EVI aggregation is implemented and
   auditable; otherwise remove vegetation claims.

Fallback path:

1. If model skill is weak but data reproducibility is strong, submit as a
   Scientific Data style Data Descriptor or benchmark descriptor.
2. If PAHO/China extension becomes strong, consider PLOS Neglected Tropical
   Diseases or Emerging Infectious Diseases.

## 2. Evidence Base And Source Anchors

These are the external sources that anchor the plan. They should be cited in
the manuscript or used to justify scope decisions.

### 2.1 Surveillance And Disease Context

- ECDC Hantavirus infection Annual Epidemiological Report for 2023:
  https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
  - Planning role: primary harmonized EU/EEA seed source.
  - Current repo extracts and reconciles ECDC Table 1 for 2019-2023.
  - ECDC reports 1,885 EU/EEA cases for 2023.

- CDC reported hantavirus disease cases:
  https://www.cdc.gov/hantavirus/data-research/cases/index.html
  - Planning role: confirms public U.S. county-level human prediction is
    blocked by privacy constraints.
  - CDC states county-level data cannot be provided to protect identities.

- CDC hantavirus surveillance and case definitions:
  https://www.cdc.gov/hantavirus/php/surveillance/index.html
  - Planning role: supports case-definition and NNDSS context if U.S. state
    data are discussed.

- WHO hantavirus fact sheet:
  https://www.who.int/news-room/fact-sheets/detail/hantavirus
  - Planning role: supports disease/transmission framing and the Andes virus
    exception.

- CDC Andes virus page:
  https://www.cdc.gov/hantavirus/about/andesvirus.html
  - Planning role: confirms Andes virus is the only hantavirus type known to
    spread person-to-person.

- WHO Disease Outbreak News, 2026 DON600:
  https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600
  - Planning role: shows current public relevance, but event signals must not
    be mixed with annual surveillance labels unless separately coded.

- PAHO/WHO Hantavirus Pulmonary Syndrome alert, 2025:
  https://www.paho.org/en/documents/epidemiological-alert-hantavirus-pulmonary-syndrome-americas-region-19-december-2025
  - Planning role: optional Americas expansion source and public-health
    relevance anchor.

- China CDC Weekly HFRS article, 2014-2023:
  https://weekly.chinacdc.cn/en/article/doi/10.46234/ccdcw2025.141
  - Planning role: optional external-validation or source-system extension for
    HFRS; never pool blindly with ECDC.

### 2.2 Covariate And Geospatial Sources

- World Bank Indicators API:
  https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
  - Planning role: free country-year population, rurality, GDP, and additional
    contextual indicators.

- FAOSTAT Land Use:
  https://www.fao.org/faostat/en/#data/RL
  - Planning role: free country-year land-use covariates.

- TerraClimate Scientific Data paper:
  https://www.nature.com/articles/sdata2017191
  - Planning role: free high-resolution monthly global climate and water
    balance covariates.

- TerraClimate Earth Engine catalog:
  https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_TERRACLIMATE
  - Planning role: source documentation for variables and public availability.

- Natural Earth downloads:
  https://www.naturalearthdata.com/downloads/
  - Planning role: public country-boundary source for zonal aggregation.

- MOD13C2 product documentation, NASA LAADS:
  https://ladsweb.modaps.eosdis.nasa.gov/api/v1/productPage/product=MOD13C2
  - Planning role: optional vegetation covariates; requires QA-aware
    aggregation.

- MODIS Collection 6.1 vegetation index user guide:
  https://lpdaac.usgs.gov/documents/621/MOD13_User_Guide_V61.pdf
  - Planning role: required reference for QA flags if MODIS is implemented.

- NASA Common Metadata Repository:
  https://www.earthdata.nasa.gov/about/esdis/eosdis/cmr
  - Planning role: discovery API for MODIS granules.

### 2.3 Journal Scope Sources

- International Journal of Health Geographics:
  https://ij-healthgeographics.biomedcentral.com/about
  - Best first target because it explicitly covers geospatial health, remote
    sensing, spatial epidemiology, spatiotemporal statistics, and surveillance
    services.

- PLOS Neglected Tropical Diseases:
  https://journals.plos.org/plosntds/s/journal-information
  - Stronger if PAHO/China rows, One Health framing, and neglected-population
    relevance are added.

- Emerging Infectious Diseases:
  https://wwwnc.cdc.gov/eid/pages/about.htm
  - Stronger if the paper emphasizes surveillance interpretation, emergence,
    public-health utility, and limitations.

- Scientific Data aims and scope:
  https://www.nature.com/sdata/aims-and-scope
  - Backup route if the data/schema/reproducibility contribution is stronger
    than model skill.

### 2.4 Competitive Context

- HantavirusMap:
  https://hantavirusmap.com/
  - Current positioning: live global hantavirus outbreak tracker and signal
    aggregator.
  - This project must not compete as a live alert map.
  - Differentiator: validated forecast benchmark, provenance, uncertainty,
    and reproducible data pipeline.

## 3. Scientific Claim Boundaries

### 3.1 Claims Allowed Now

Allowed after the current repo state and generated outputs:

- The repo provides an auditable ECDC/EU-EEA country-year benchmark for
  reported hantavirus incidence from 2019 to 2023.
- The source totals reconcile exactly to ECDC annual totals.
- Free public covariates from World Bank, FAOSTAT, and TerraClimate can be
  joined reproducibly at country-year level.
- Simple rate baselines and a gradient-boosting tabular baseline can produce
  one-year-ahead quantile forecasts.
- The current results show that simple baselines are strong and complex models
  should not be promoted unless they beat those baselines under WIS and
  calibration.
- Markov-style incidence-state simulation is useful for stress testing sparse
  surveillance dynamics.

### 3.2 Claims Not Allowed Yet

Not allowed unless new evidence is added and QA passes:

- "Global" hantavirus prediction.
- U.S. county-level human case prediction from public data.
- Individual or clinical risk prediction.
- Operational public-health warning or live outbreak detection.
- Generic human-to-human spread simulation.
- Vegetation/NDVI/EVI effects unless MODIS QA-masked aggregation is complete.
- Source-system pooled inference across ECDC, PAHO, China CDC, WHO DON, and
  news sources without explicit source-system modeling.
- Causal climate claims.
- Prospective outbreak prediction.

### 3.3 Required Language

Use:

- "reported incidence"
- "public surveillance"
- "one-year-ahead benchmark"
- "forecast distributions"
- "uncertainty-calibrated"
- "source-system stratified"
- "ECDC/EU-EEA benchmark"
- "sparse surveillance"
- "scenario stress test"

Avoid:

- "true infection risk"
- "outbreak oracle"
- "county-level predictor"
- "medical advice"
- "clinical triage"
- "live alert system"
- "global model" unless non-ECDC sources are added
- "human spread" except Andes-virus-specific discussion

## 4. Current Repo State

### 4.1 Current Branch And Commit

As of this plan:

- Branch: `main`
- Remote: `origin/main`
- Latest pushed implementation commit before this plan:
  `d51bec9 Add TerraClimate aggregation and publication QA gate`
- Current working tree may show unstaged deletions of old root note files:
  `instructions.txt`, `potential blockers.txt`,
  `potential blockers (2).txt`, and `potential blockers (3).txt`.
  These are user-side workspace changes and must not be staged unless the user
  explicitly confirms.

### 4.2 Implemented Components

Data:

- ECDC country-year case table builder:
  `src/hantavirus_predictor/datasets/ecdc_hantavirus.py`
  `tools/create_ecdc_case_table.py`
- International case validator:
  `src/hantavirus_predictor/validation/international_cases.py`
  `tools/validate_international_cases.py`
- World Bank context ingestion:
  `src/hantavirus_predictor/ingest/world_bank.py`
- FAOSTAT land-use ingestion:
  `src/hantavirus_predictor/ingest/faostat.py`
  `tools/download_faostat_land_use.py`
- TerraClimate manifest and aggregation:
  `src/hantavirus_predictor/ingest/terraclimate.py`
  `src/hantavirus_predictor/ingest/terraclimate_aggregate.py`
  `tools/create_terraclimate_manifest.py`
  `tools/download_natural_earth_countries.py`
  `tools/aggregate_terraclimate_country_year.py`
- MODIS manifest:
  `src/hantavirus_predictor/ingest/modis.py`
  `tools/create_mod13c2_manifest.py`
- Processed modeling table:
  `src/hantavirus_predictor/features/country_year.py`
  `tools/build_international_dataset.py`

Models and simulation:

- Forecast metrics:
  `src/hantavirus_predictor/metrics.py`
- Baselines:
  `src/hantavirus_predictor/models/international_baselines.py`
  `tools/run_international_baselines.py`
- Figures:
  `tools/plot_international_baselines.py`
- Markov incidence-state simulation:
  `src/hantavirus_predictor/simulations/markov_incidence.py`
  `tools/run_markov_simulation.py`

Reports and QA:

- Data audit:
  `tools/write_international_data_audit.py`
- Paper readiness:
  `tools/write_paper_readiness_report.py`
- Publication gate:
  `tools/check_publication_readiness.py`
- Earthdata credential parser:
  `src/hantavirus_predictor/ingest/earthdata.py`
  `tools/check_earthdata_credentials.py`

Tests:

- `tests/test_metrics.py`
- `tests/test_international_validator.py`
- `tests/test_data_sources.py`
- `tests/test_international_baselines.py`
- `tests/test_faostat_ingest.py`
- `tests/test_earthdata_credentials.py`
- `tests/test_source_manifests.py`
- `tests/test_markov_simulation.py`
- `tests/test_terraclimate_aggregation.py`

### 4.3 Current Generated Outputs

These are ignored by git and must be regenerated locally:

- `data/manual/international_country_cases.csv`
- `data/processed/terraclimate_country_year.csv`
- `data/processed/international_country_year.csv`
- `data/processed/international_baseline_predictions.csv`
- `data/processed/international_baseline_metrics.csv`
- `data/processed/markov_simulation_summary.csv`
- `reports/00_paper_readiness_and_results.md`
- `reports/01_international_data_audit.md`
- `reports/02_international_baselines.md`
- `reports/04_markov_simulation_stress_test.md`
- `reports/05_publication_readiness_gate.md`
- `figures/international_baseline_mean_wis.png`
- `figures/international_baseline_observed_vs_predicted.png`

### 4.4 Current Numerical Results To Preserve

From the latest QA pass:

- Rows: 142
- Years: 2019-2023
- TerraClimate joined: 142 of 142 rows
- TerraClimate lag-1 features complete: 114 of 114 non-2019 rows
- Baseline metric rows: 12
- Quantile forecast rows: 1026
- Simulation rows: 29
- Tests: 23 passed

ECDC annual reconciliation:

| Year | Cases |
|---|---:|
| 2019 | 4,088 |
| 2020 | 1,693 |
| 2021 | 4,947 |
| 2022 | 2,185 |
| 2023 | 1,885 |

Best baselines:

| Target year | Best model | Mean WIS | Coverage 90 | MAE | Brier any case |
|---|---|---:|---:|---:|---:|
| 2022 | empirical_negative_binomial_rate | 47.17 | 1.00 | 72.10 | 0.1584 |
| 2023 | last_observed_country_rate | 42.86 | 0.5714 | 47.11 | 0.06055 |

## 5. Publication Strategy

### 5.1 Journal Tiering

Target 1: International Journal of Health Geographics

- Best fit for current ECDC + geospatial + climate + benchmark scope.
- Manuscript angle:
  - open benchmark
  - geospatial public health surveillance
  - remote-sensing covariate evaluation
  - uncertainty-calibrated country-year forecasting
  - limitations of sparse surveillance
- Minimum before submission:
  - feature ablations
  - final figures and tables
  - manuscript text
  - reproducibility package
  - clear "ECDC/EU-EEA only" scope unless PAHO/China are added

Target 2: PLOS Neglected Tropical Diseases

- Use only if the paper has stronger One Health and cross-region relevance.
- Recommended upgrades before targeting:
  - PAHO Americas HPS/HCPS rows
  - China CDC HFRS rows or external-validation sensitivity
  - clearer neglected-population relevance
  - stronger reservoir/spillover framing

Target 3: Emerging Infectious Diseases

- Use if manuscript emphasizes:
  - surveillance limits
  - public-health interpretation
  - emerging/reemerging zoonotic disease relevance
  - practical benchmark for public surveillance
- Less ideal for a methods-heavy model benchmark unless the public-health
  message is very sharp.

Fallback: Scientific Data

- Use if model skill is not strong enough for a modeling paper.
- Manuscript becomes a Data Descriptor:
  - dataset design
  - provenance
  - processing pipeline
  - validation checks
  - benchmark reference outputs
  - limitations and reuse notes

### 5.2 Marketing And Positioning

Core pitch:

> Live signal trackers can tell people what is being reported now. This paper
> asks a different question: what can be validated from free public data, with
> known uncertainty, under sparse hantavirus surveillance?

Differentiators:

- Not a live map.
- Not a subscription signal product.
- Not a medical alert service.
- Reproducible source-to-feature pipeline.
- Public-data-only benchmark.
- Explicit negative results.
- Forecast distributions, not point-only risk scores.
- QA gate prevents unsupported claims from entering the paper.

Target audiences:

- health geographics researchers
- infectious disease modelers
- public-health surveillance analysts
- climate-health researchers
- One Health researchers
- data descriptor and benchmark users

## 6. End-To-End Implementation Plan

The remaining work is divided into phases. Each phase has implementation
specs, exact files, outputs, acceptance criteria, and blockers.

### Phase 0: Freeze The Publication Scope

Goal:

Choose one manuscript scope before adding advanced models.

Decision options:

1. ECDC-only benchmark, recommended.
2. ECDC + PAHO + China multi-source benchmark, stronger but slower.
3. Data Descriptor fallback, if model skill remains weak.

Recommended decision now:

- Proceed with ECDC-only IJHG-style benchmark.
- Keep PAHO/China as optional extension only.
- Remove MODIS vegetation claims unless MODIS aggregation is finished.

Implementation:

- Create `manuscript/scope.md`.
- Add final scope statement:
  - countries: EU/EEA ECDC reporting countries
  - years: 2019-2023
  - label: annual reported hantavirus infection cases
  - covariates: World Bank, FAOSTAT, TerraClimate
  - optional covariates: MODIS only if implemented
  - validation: one-year-ahead temporal validation
  - simulation: appendix stress test only

Acceptance criteria:

- `manuscript/scope.md` exists.
- `tools/check_publication_readiness.py` still passes.
- No docs or manuscript text claim global prediction.

Blockers:

- Reviewer may see ECDC-only as too narrow.
- Response: frame as benchmark/methods paper and state extensibility to PAHO
  and China CDC.

### Phase 1: Rebuild And Freeze The Reproducible Data Snapshot

Goal:

Create a deterministic local data snapshot and metadata bundle for the exact
manuscript results.

Existing commands:

```powershell
python -m pip install -e ".[dev,geo]"
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
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
python tools/validate_manual_data.py
pytest
python -m ruff check src tests tools
```

New implementation specs:

1. Add `tools/write_reproducibility_manifest.py`.
   - Inputs:
     - tracked source files under `src/`, `tools/`, `tests/`, `schemas/`,
       `configs/`, `metadata/`
     - generated ignored outputs under `data/processed/`, `reports/`,
       `figures/`
   - Outputs:
     - `metadata/reproducibility_manifest.csv`
     - columns:
       - `path`
       - `exists`
       - `size_bytes`
       - `sha256`
       - `generated_by`
       - `tracked_in_git`
       - `role`
   - Exclude:
     - secrets
     - raw Earthdata credential file
     - `.git/`
     - caches

2. Add `metadata/source_versions.yaml`.
   - Include:
     - ECDC report URL and accessed date
     - World Bank API date
     - FAOSTAT ZIP download date
     - TerraClimate THREDDS URLs and years
     - Natural Earth boundary URL and date
     - MODIS CMR query date
     - software versions

3. Add `tools/write_data_dictionary.py`.
   - Output:
     - `docs/DATA_DICTIONARY.md`
   - Include every column in:
     - `international_country_cases.csv`
     - `terraclimate_country_year.csv`
     - `international_country_year.csv`
     - `international_baseline_predictions.csv`
     - `international_baseline_metrics.csv`
     - `markov_simulation_summary.csv`

Acceptance criteria:

- Rebuild commands run clean.
- `metadata/reproducibility_manifest.csv` exists.
- `docs/DATA_DICTIONARY.md` exists.
- No secrets appear in tracked files:
  - `rg -n "password|token|secret|urs|earthdata" .`
  - Manual review confirms `nasa earthdata acc info.txt` remains ignored.
- `reports/05_publication_readiness_gate.md` says PASS.

Blockers:

- FAOSTAT or World Bank APIs may change values.
- Response: pin generated manuscript snapshot by date and checksum; mention
  source access dates.

### Phase 2: Add Feature Ablation Benchmark

Goal:

Show what public data actually add beyond simple surveillance history.

Current status:

- Existing baselines run but do not produce a full feature-ablation table.
- Gradient boosting uses lagged covariates when available.

Implementation specs:

1. Add feature-set definitions in
   `src/hantavirus_predictor/models/feature_sets.py`.

Feature sets:

```text
surveillance_only:
  year, iso3, region, syndrome, source_system, population/log_population

context:
  surveillance_only
  rural_population_pct_lag1
  gdp_per_capita_current_usd_lag1

land_use:
  context
  faostat_cropland_1000ha_lag1
  faostat_forest_land_1000ha_lag1
  faostat_perm_meadows_pastures_1000ha_lag1
  faostat_agricultural_land_1000ha_lag1

climate:
  context
  terraclimate_ppt_annual_sum_mm_lag1
  terraclimate_tmin_annual_mean_c_lag1
  terraclimate_tmax_annual_mean_c_lag1
  terraclimate_vpd_annual_mean_kpa_lag1
  terraclimate_soil_annual_mean_mm_lag1
  terraclimate_def_annual_sum_mm_lag1

all_public:
  context + land_use + climate

vegetation:
  only if MODIS is implemented
```

2. Modify `src/hantavirus_predictor/models/international_baselines.py`.
   - Add `feature_set` argument to the gradient boosting model.
   - Keep simple rate baselines unchanged.
   - Emit model names:
     - `gradient_boosting_surveillance_only`
     - `gradient_boosting_context`
     - `gradient_boosting_land_use`
     - `gradient_boosting_climate`
     - `gradient_boosting_all_public`
   - If MODIS is implemented:
     - `gradient_boosting_vegetation`
     - `gradient_boosting_all_public_plus_vegetation`

3. Add `tools/run_feature_ablation_benchmarks.py`.
   - Inputs:
     - `data/processed/international_country_year.csv`
   - Outputs:
     - `data/processed/feature_ablation_predictions.csv`
     - `data/processed/feature_ablation_metrics.csv`
     - `reports/03_feature_ablation_benchmark.md`
   - Metrics:
     - WIS
     - 90 percent interval coverage
     - MAE
     - Poisson deviance
     - Brier score for any case
   - Grouping:
     - target year
     - model
     - feature set

4. Add tests:
   - `tests/test_feature_sets.py`
   - `tests/test_feature_ablation_baselines.py`

Test assertions:

- Feature sets do not include current-year non-lagged covariates for forecasts.
- Feature matrix contains no target leakage columns:
  - `cases`
  - `deaths`
  - `incidence_per_100k`
  - current-year TerraClimate values
  - current-year FAOSTAT values
- All feature-set model names appear in output.
- Quantile forecasts have 0.05, 0.50, and 0.95 rows.
- Missing covariate values are imputed using training data only.

Acceptance criteria:

- `reports/03_feature_ablation_benchmark.md` exists.
- Climate feature set is included and evaluated.
- Report clearly states whether climate improves WIS or calibration.
- No advanced model is promoted if it fails coverage.

Blockers:

- Small sample may make covariate improvements unstable.
- Response: report uncertainty, use negative result honestly, and emphasize
  benchmark value.

### Phase 3: Upgrade Count Models

Goal:

Add a stronger statistical count model suitable for a methods paper.

Why:

Current empirical negative-binomial baselines are useful but not enough as a
final statistical model. A journal reviewer will expect a proper count model
with exposure, overdispersion, and interpretable covariates.

Recommended implementation:

1. Add dependency:
   - `statsmodels>=0.14`

2. Add module:
   - `src/hantavirus_predictor/models/count_models.py`

3. Implement models:

Model A: Poisson GLM

- Target: `cases`
- Offset: `log(population)`
- Predictors:
  - year trend
  - region
  - country fixed effect or shrinkage proxy
  - source system
  - lagged context covariates
  - lagged land-use covariates
  - lagged TerraClimate covariates
- Output:
  - predictive mean
  - quantiles via parametric predictive distribution

Model B: Negative-binomial GLM

- Same target and predictors.
- Estimate or tune overdispersion.
- Output predictive count quantiles.
- This is the likely main statistical model.

Model C: Regularized negative-binomial or fallback ridge Poisson

- Use if fixed effects are unstable.
- Keep as sensitivity, not main if not robust.

4. Optional later:
   - Bayesian hierarchical negative-binomial model.
   - Use only if implemented with reproducible diagnostics.
   - Candidate dependency: PyMC or Stan, but do not add unless needed.

Files:

- `src/hantavirus_predictor/models/count_models.py`
- `tools/run_count_model_benchmarks.py`
- `reports/06_count_model_benchmarks.md`
- `tests/test_count_models.py`

Acceptance criteria:

- Models produce quantile forecasts for 2022 and 2023.
- Negative-binomial model is compared against all simple baselines.
- WIS and coverage are reported.
- Model is not promoted unless:
  - WIS improves by at least 10 percent over best simple baseline, or
  - it provides substantially better calibration/interpretable covariate
    analysis without overclaiming predictive superiority.
- Coefficient interpretation is cautious and non-causal.

Blockers:

- Small panel may cause unstable coefficients.
- Response:
  - simplify formula
  - regularize
  - group covariates into ablation sets
  - keep empirical negative-binomial as main benchmark if GLM fails.

### Phase 4: Decide MODIS Vegetation Branch

Goal:

Either implement quality-masked MODIS NDVI/EVI aggregation or remove vegetation
claims from the paper.

Decision gate:

Implement MODIS only if it can be completed without weakening reproducibility.
Otherwise, explicitly state:

> Vegetation products are discovered in a manifest but not included in the
> manuscript analyses because quality-masked aggregation was outside the final
> benchmark scope.

Implementation specs if proceeding:

1. Confirm Earthdata credentials.
   - Existing file:
     - `nasa earthdata acc info.txt`
   - Existing parser:
     - `tools/check_earthdata_credentials.py`
   - Must not print secrets.

2. Extend MODIS ingest:
   - `src/hantavirus_predictor/ingest/modis.py`
   - Add download or streaming support for MOD13C2 granules.
   - Use NASA CMR metadata for discovery.

3. Add aggregation module:
   - `src/hantavirus_predictor/ingest/modis_aggregate.py`

4. Required inputs:
   - `metadata/mod13c2_granule_manifest.csv`
   - Natural Earth boundaries
   - Earthdata credentials if protected download is required

5. Required variables:
   - NDVI
   - EVI
   - VI Quality
   - pixel reliability or equivalent QA layers available in product

6. Required feature outputs:
   - `data/processed/mod13c2_country_year.csv`
   - columns:
     - `iso3`
     - `country`
     - `year`
     - `mod13c2_ndvi_annual_mean_lag1`
     - `mod13c2_evi_annual_mean_lag1`
     - `mod13c2_ndvi_growing_season_mean_lag1`
     - `mod13c2_evi_growing_season_mean_lag1`
     - `mod13c2_valid_pixel_share_lag1`
     - `mod13c2_joined`
     - missingness flags

7. QA rules:
   - Apply valid range scaling.
   - Mask poor-quality pixels.
   - Report valid-pixel share.
   - Exclude country-years with inadequate valid-pixel share or flag them.
   - Never use current target-year vegetation values for a one-year-ahead
     forecast.

8. Add tests:
   - `tests/test_modis_aggregation.py`
   - Synthetic HDF/array test if real HDF testing is too heavy.

Acceptance criteria:

- At least 95 percent of non-2019 ECDC forecast rows have valid lag-1
  vegetation features or documented QA missingness.
- Valid-pixel share is reported.
- Feature ablation includes vegetation.
- Manuscript makes no vegetation claim unless vegetation ablation is reported.

Blockers:

- Earthdata auth may fail.
- Human input needed if credentials stop working:
  1. Log into https://urs.earthdata.nasa.gov/
  2. Confirm the account is active.
  3. Put the username and password in `nasa earthdata acc info.txt` at repo
     root using the existing format.
  4. Run `python tools/check_earthdata_credentials.py`.
  5. Do not commit the credential file.

- MODIS HDF handling may be heavy.
- Response:
  - use manifest-only and remove vegetation claims
  - keep TerraClimate as the remote-sensing/environmental covariate family
  - state MODIS as future work.

### Phase 5: Optional PAHO And China CDC Source Expansion

Goal:

Improve generalizability and make PLOS NTD/EID more plausible.

Decision:

Do this only after ECDC + covariate + feature-ablation results are stable.

PAHO implementation specs:

1. Create `data/manual/paho_hantavirus_cases.csv`.
2. Create schema:
   - `schemas/paho_hantavirus_cases.schema.yaml`
3. Create builder:
   - `tools/create_paho_case_table.py`
4. Create validator:
   - `tools/validate_paho_cases.py`
5. Required columns:
   - `iso3`
   - `country`
   - `year`
   - `cases`
   - `deaths`
   - `syndrome`
   - `pathogen_or_virus`
   - `reporting_system`
   - `source_url`
   - `source_title`
   - `source_publication_date`
   - `source_accessed_date`
   - `quality_grade`
   - `extraction_note`
6. Required QA:
   - every row has primary source URL
   - source totals reconcile to PAHO/national source
   - syndrome is HPS or HCPS where appropriate
   - Americas source system is never treated as identical to ECDC

China CDC implementation specs:

1. Create `data/manual/china_hfrs_cases.csv`.
2. Create schema:
   - `schemas/china_hfrs_cases.schema.yaml`
3. Create builder:
   - `tools/create_china_hfrs_case_table.py`
4. Create validator:
   - `tools/validate_china_hfrs_cases.py`
5. Required columns:
   - same as PAHO, plus province fields if available
6. Required QA:
   - separate source system: `China CDC`
   - syndrome: `HFRS`
   - do not pool with ECDC without source effects
   - use as external validation or sensitivity before main pooled inference

Integration specs:

1. Modify `tools/build_international_dataset.py` to accept multiple case-table
   inputs.
2. Add `source_system` and `quality_grade` effects to all baselines.
3. Add validation splits:
   - leave-source-system-out
   - train ECDC, test PAHO/China, only as sensitivity
   - train all but source system, test held-out source
4. Update `tools/check_publication_readiness.py` to have two modes:
   - `--scope ecdc`
   - `--scope international`

Acceptance criteria:

- Source totals reconcile for every added source.
- Source-system-specific missingness is reported.
- No source-system pooling claim is made without sensitivity results.

Blockers:

- PAHO alert data may be event-based rather than full annual country series.
- China CDC article may not provide country-year rows in a directly reusable
  table.
- Response:
  - keep as context or external validation
  - do not force incomplete signals into annual labels.

### Phase 6: Simulation Upgrade

Goal:

Make the simulation useful without pretending simulated data are evidence.

Current state:

- Markov-style zero/low/high incidence-state simulation exists.
- It is suitable as an appendix stress test.

Recommended upgraded simulation:

1. Keep existing state model.
2. Add climate anomaly scenario stress test using TerraClimate.
3. Do not simulate human-to-human spread except for an Andes-specific future
   project with its own evidence base.

Implementation specs:

1. Add module:
   - `src/hantavirus_predictor/simulations/climate_scenarios.py`

2. Add tool:
   - `tools/run_climate_scenario_stress_test.py`

3. Inputs:
   - `data/processed/international_country_year.csv`
   - fitted benchmark model predictions
   - TerraClimate lagged covariates

4. Scenarios:
   - precipitation +1 standard deviation
   - vapor pressure deficit +1 standard deviation
   - soil moisture +1 standard deviation
   - climate water deficit +1 standard deviation
   - combined wet scenario
   - combined dry scenario

5. Outputs:
   - `data/processed/climate_scenario_summary.csv`
   - `reports/07_climate_scenario_stress_test.md`

6. Required columns:
   - `scenario`
   - `iso3`
   - `country`
   - `baseline_median_cases`
   - `scenario_median_cases`
   - `absolute_difference`
   - `relative_difference`
   - `q05_cases`
   - `q95_cases`
   - `interpretation_note`

7. Interpretation:
   - If model coefficients are unstable, scenario output is illustrative only.
   - Do not claim causal effect.
   - Do not include in main results if it distracts from the benchmark.

Acceptance criteria:

- Scenario report labels outputs as stress tests.
- The paper does not use simulated rows to train or validate models.
- The simulation section improves usefulness by showing uncertainty sensitivity.

Blockers:

- Current panel may be too small for reliable climate-response estimates.
- Response:
  - keep Markov state model as appendix
  - omit climate scenarios from main manuscript
  - include as future work.

### Phase 7: Final Figure And Table Set

Goal:

Generate a complete, publication-quality visual and tabular package.

Required tables:

Table 1: Data sources and roles

- ECDC surveillance labels
- World Bank context
- FAOSTAT land use
- TerraClimate climate/water balance
- Natural Earth boundaries
- MODIS manifest or vegetation features, depending on branch
- Optional PAHO/China sources

Table 2: Data audit and missingness

- rows by year
- cases by year
- countries by year
- missingness by feature family
- source reconciliation

Table 3: Baseline benchmark metrics

- target year
- model
- WIS
- coverage
- MAE
- Brier any-case
- deviance

Table 4: Feature ablation metrics

- feature set
- target year
- WIS
- coverage
- delta from surveillance-only
- delta from best simple baseline

Table 5: Sensitivity and simulation summary

- Markov state transitions
- scenario stress-test summary if included

Required figures:

Figure 1: Study design diagram

- source data -> validated country-year table -> covariates -> forecasts ->
  evaluation -> stress test

Figure 2: ECDC reported cases by year and country

- country rows, year columns, cases/incidence
- avoid implying sub-country precision

Figure 3: Covariate coverage and missingness

- feature family coverage
- TerraClimate lag completeness

Figure 4: Forecast skill comparison

- WIS by target year and model
- include simple baselines and gradient boosting

Figure 5: Observed vs predicted

- best model for 2023
- show uncertainty or quantile interval if possible

Figure 6: Calibration/coverage

- interval coverage by model
- any-case Brier score

Figure 7: Simulation appendix figure

- Markov transition matrix or scenario uncertainty bands

Implementation specs:

1. Extend `tools/plot_international_baselines.py`.
2. Add:
   - `tools/plot_data_audit.py`
   - `tools/plot_feature_ablation.py`
   - `tools/plot_simulation_outputs.py`
3. Outputs:
   - `figures/figure_01_study_design.png`
   - `figures/figure_02_ecdc_cases_heatmap.png`
   - `figures/figure_03_covariate_coverage.png`
   - `figures/figure_04_forecast_skill.png`
   - `figures/figure_05_observed_vs_predicted.png`
   - `figures/figure_06_calibration.png`
   - `figures/figure_07_simulation_stress_test.png`
4. Add high-resolution output:
   - 300 dpi PNG
   - optional PDF/SVG for journal submission

Acceptance criteria:

- Every figure has a caption in `manuscript/figure_captions.md`.
- Every figure can be regenerated by a script.
- No map suggests within-country precision.
- Figure colors are interpretable in grayscale where possible.

### Phase 8: Manuscript Draft

Goal:

Create a complete manuscript package.

Recommended files:

- `manuscript/README.md`
- `manuscript/title_page.md`
- `manuscript/abstract.md`
- `manuscript/introduction.md`
- `manuscript/methods.md`
- `manuscript/results.md`
- `manuscript/discussion.md`
- `manuscript/limitations.md`
- `manuscript/data_availability.md`
- `manuscript/code_availability.md`
- `manuscript/ethics_statement.md`
- `manuscript/author_contributions.md`
- `manuscript/conflicts_of_interest.md`
- `manuscript/funding.md`
- `manuscript/references.bib`
- `manuscript/figure_captions.md`
- `manuscript/tables/`
- `manuscript/submission_checklist.md`
- `manuscript/cover_letter_ijhg.md`

Abstract spec:

- Background:
  - Hantavirus surveillance is sparse and heterogeneous.
  - Live trackers provide signals but not validated forecast benchmarks.
- Methods:
  - ECDC country-year table, 2019-2023.
  - Public covariates from World Bank, FAOSTAT, TerraClimate.
  - One-year-ahead forecast benchmark.
  - Quantile forecasts and WIS/coverage/Brier metrics.
- Results:
  - 142 rows, annual totals, covariate coverage, best baselines.
  - State whether climate/land-use improved skill after feature ablation.
- Conclusions:
  - Open benchmark prevents false precision.
  - Simple baselines are hard to beat.
  - Public-data limitations define appropriate scope.

Methods spec:

1. Data sources.
2. Case table construction.
3. Covariate joins.
4. TerraClimate zonal aggregation.
5. Forecast task.
6. Baseline models.
7. Feature ablation.
8. Evaluation metrics.
9. Simulation stress test.
10. Reproducibility and code.
11. Ethics and limitations.

Results spec:

1. Source reconciliation.
2. Covariate coverage.
3. Baseline performance.
4. Feature ablation.
5. Statistical count model performance.
6. Simulation stress test.
7. Sensitivity analysis.

Discussion spec:

1. What public data can support.
2. Why simple baselines matter.
3. How this differs from live signal maps.
4. Limits of ECDC-only data.
5. Why county-level U.S. prediction is blocked.
6. How to extend responsibly to PAHO and China CDC.
7. What not to overclaim.

Acceptance criteria:

- Manuscript text matches generated outputs.
- Every numeric claim appears in a generated report/table.
- Every data-source claim has a citation.
- No prohibited claim appears.
- The abstract can stand alone without overclaiming.

### Phase 9: Reproducibility Package

Goal:

Make the project usable by reviewers and future researchers.

Implementation specs:

1. Add `Makefile` or `justfile`.
   - Targets:
     - `make data`
     - `make benchmarks`
     - `make figures`
     - `make reports`
     - `make qa`
     - `make manuscript`

2. Add `environment.yml` or lock file if needed.
   - Include geospatial dependencies.
   - Keep `requirements.txt` and `pyproject.toml` synchronized.

3. Add `docs/REPRODUCIBILITY.md`.
   - Step-by-step build from fresh clone.
   - Expected runtimes.
   - Network requirements.
   - Data sources.
   - Known optional credentials.
   - Expected output checksums.

4. Add GitHub Actions.
   - Lightweight CI:
     - `pytest`
     - `ruff`
     - schema validation
   - Do not run remote-heavy TerraClimate or MODIS downloads in CI unless
     cached or explicitly scheduled.

5. Add release checklist:
   - GitHub release
   - Zenodo DOI if desired
   - citation metadata updated
   - data availability statement
   - exact commit hash in manuscript

Acceptance criteria:

- Fresh clone can run unit tests without private credentials.
- Fresh clone can rebuild all public-data outputs with network access.
- Remote-heavy steps are documented.
- Generated outputs are ignored by git but reproducible.

### Phase 10: Pre-Submission Audit

Goal:

Catch contradictions before submission.

Required audit commands:

```powershell
git status --short --branch
python tools/validate_international_cases.py --strict
python tools/validate_manual_data.py
python tools/build_international_dataset.py
python tools/run_international_baselines.py
python tools/run_feature_ablation_benchmarks.py
python tools/run_count_model_benchmarks.py
python tools/run_markov_simulation.py
python tools/write_international_data_audit.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
pytest
python -m ruff check src tests tools
rg -n "global prediction|county-level predictor|medical advice|clinical|outbreak oracle|human spread|vegetation" README.md docs manuscript src tools
```

Manual audit:

1. Verify every manuscript number appears in generated outputs.
2. Verify every source URL still resolves.
3. Verify all generated figures match captions.
4. Verify no raw restricted data are tracked.
5. Verify no credentials are tracked.
6. Verify limitations are explicit.
7. Verify journal scope and formatting.
8. Verify author details, conflicts, funding, and acknowledgments.
9. Verify license compatibility for Natural Earth, ECDC, FAOSTAT, World Bank,
   TerraClimate, and any NASA data.
10. Verify data availability statement does not redistribute data in a way that
    violates source terms.

Acceptance criteria:

- All automated checks pass.
- All manual checks signed off in `manuscript/submission_checklist.md`.
- Git working tree is clean except intentionally ignored generated outputs.

## 7. Exact Software Backlog

Priority order:

1. `tools/write_reproducibility_manifest.py`
2. `tools/write_data_dictionary.py`
3. Feature-ablation benchmark modules and report.
4. Negative-binomial GLM benchmark.
5. Final plotting scripts.
6. Manuscript folder and first full draft.
7. Reproducibility docs and Makefile.
8. Optional MODIS branch.
9. Optional PAHO/China branch.
10. Optional climate scenario stress test.

Do not start:

- PINN
- graph neural network
- time-series foundation model
- deep learning ensemble
- live dashboard
- alerting service

until all simple baselines, feature ablations, count models, and manuscript
figures are complete.

## 8. Exact Data Schema Requirements

### 8.1 Case Table Schema

Required core columns:

- `iso3`
- `country`
- `year`
- `cases`
- `deaths`
- `population`
- `incidence_rate_per_100k_source`
- `syndrome`
- `pathogen_or_virus`
- `reporting_system`
- `source_url`
- `source_title`
- `source_accessed_date`
- `quality_grade`
- `extraction_note`

Rules:

- `iso3`, `year`, `syndrome`, `pathogen_or_virus`, and `reporting_system`
  must define a unique primary key.
- `cases` must be integer and non-negative.
- `population` must be positive.
- `source_url` must be present.
- `quality_grade` must be documented.
- Deaths may be missing when the source does not report country-year deaths.

### 8.2 Processed Model Table Schema

Required join keys:

- `iso3`
- `country`
- `year`
- `syndrome`
- `source_system`

Required target columns:

- `cases`
- `population`
- `incidence_per_100k`

Required context columns:

- `rural_population_pct`
- `gdp_per_capita_current_usd`
- `rural_population_pct_lag1`
- `gdp_per_capita_current_usd_lag1`

Required land-use columns:

- `faostat_cropland_1000ha`
- `faostat_forest_land_1000ha`
- `faostat_perm_meadows_pastures_1000ha`
- `faostat_agricultural_land_1000ha`
- lag-1 versions and missingness flags

Required TerraClimate columns:

- `terraclimate_ppt_annual_sum_mm`
- `terraclimate_tmin_annual_mean_c`
- `terraclimate_tmax_annual_mean_c`
- `terraclimate_vpd_annual_mean_kpa`
- `terraclimate_soil_annual_mean_mm`
- `terraclimate_def_annual_sum_mm`
- lag-1 versions and missingness flags

Required provenance flags:

- `faostat_land_use_joined`
- `terraclimate_joined`
- `mod13c2_joined`
- missingness flags for every feature family

Rules:

- Forecast models must use lagged covariates only.
- Current-year covariates may be reported descriptively but must not enter
  one-year-ahead forecasts.
- Target columns must never appear in feature matrices.

## 9. Exact Modeling Rules

### 9.1 Forecast Task

Task:

> For each country-year-source-system-syndrome row, predict next complete
> calendar-year reported hantavirus cases using only data available at or before
> the forecast date.

Forecast date:

- `target_year - 1-12-31`

Horizon:

- one year

Required prediction format:

- `forecast_date`
- `target_year`
- `target`
- `horizon`
- `location`
- `iso3`
- `country`
- `syndrome`
- `source_system`
- `model`
- `feature_set`
- `quantile`
- `value`

Required quantiles:

- 0.05
- 0.50
- 0.95

Optional:

- 0.10
- 0.25
- 0.75
- 0.90

### 9.2 Required Baselines

Simple baselines:

1. Country historical mean rate.
2. Last observed country rate.
3. Region/syndrome/source mean rate.
4. Empirical negative-binomial rate.
5. Hierarchical negative-binomial shrinkage rate.

Tabular baseline:

6. Gradient boosting with feature ablations.

Statistical model:

7. Negative-binomial GLM with population offset.

Promotion rule:

- A model can be emphasized only if it improves WIS and does not destroy
  calibration.
- If complex models do not beat simple baselines, the paper should say that.

### 9.3 Required Metrics

Primary:

- Weighted interval score for central 90 percent interval.

Secondary:

- 90 percent empirical coverage.
- MAE.
- RMSE if added.
- Poisson or negative-binomial deviance.
- Brier score for any reported case.

Calibration:

- coverage by year
- coverage by model
- optional reliability curve for any-case probability

### 9.4 Validation Splits

Current ECDC seed:

- Train: 2019-2021
- Validation: 2022
- Test: 2023

Rolling origin:

- train through 2020, test 2021
- train through 2021, test 2022
- train through 2022, test 2023

Do not overclaim:

- The ECDC-only panel has only five years.
- Rolling-origin checks are useful but limited.
- Leave-country-out is optional sensitivity, not a strong final claim unless
  source expansion or more years are added.

## 10. Human Inputs Needed Before Actual Submission

No human input is needed to continue implementation and manuscript drafting
right now, assuming the current public data sources remain reachable and the
local Earthdata credential file remains valid.

Human input will be required before journal submission:

1. Author list and order.
2. Affiliations.
3. Corresponding author details.
4. ORCID IDs.
5. Funding statement.
6. Conflict-of-interest statement.
7. Ethics/IRB determination wording.
8. Acknowledgments.
9. Target journal confirmation.
10. APC/payment plan if the selected journal charges publication fees.
11. Journal account access for submission.
12. Approval of preprint posting, if desired.

Human input may be required earlier only if:

- Earthdata credentials fail and MODIS is still required.
- A source blocks access or changes licensing.
- A journal-specific submission requirement needs author-only information.
- A collaborator provides restricted data.

If restricted data are introduced:

- Stop implementation.
- Create a data-use and IRB checklist.
- Do not commit restricted data.
- Do not train or publish from restricted data until rights are documented.

## 11. Blocker Register And Responses

| Blocker | Risk | Response | Publication effect |
|---|---|---|---|
| HantavirusMap already exists | Live tracker novelty is gone | Do not build a tracker; publish validated benchmark | Strengthens differentiation |
| CDC county data unavailable | U.S. county predictor blocked | Use ECDC country-year; keep U.S. county work restricted-data only | Avoids privacy overclaim |
| ECDC has only 5 years | Weak for complex models | Simple baselines, WIS, coverage, cautious claims | Methods/data benchmark rather than deep learning paper |
| TerraClimate aggregation heavy | Reproducibility risk | Implemented via OPeNDAP + Natural Earth; checksum/report | Climate covariates allowed |
| MODIS QA complexity | Bad NDVI/EVI claims possible | Implement QA-masked aggregation or remove vegetation | Vegetation claim is optional |
| PAHO event alerts incomplete | Inconsistent labels | Add only full country-year/provenance rows | Optional extension |
| China source differs | Non-comparable source system | Treat as separate source/external validation | Optional extension |
| Model skill weak | Rejection risk for prediction paper | Emphasize benchmark, negative results, Scientific Data fallback | Still publishable if framed honestly |
| Simulation overclaim | Synthetic data mistaken for evidence | Label as stress test only | Appendix/supporting result |
| Journal mismatch | Desk rejection | Target IJHG first for ECDC-only; PLOS NTD/EID only if expanded | Scope controls journal |
| API changes | Reproducibility drift | Source versions, manifests, checksums, dates | Auditable snapshot |
| Secrets in repo | Security risk | Keep credentials ignored; audit with `rg` | Mandatory before release |

## 12. Final Submission Package Checklist

Before submission, the repo must contain:

- `PUBLICATION_MASTER_PLAN.md`
- `docs/REPRODUCIBILITY.md`
- `docs/DATA_DICTIONARY.md`
- `metadata/reproducibility_manifest.csv`
- `metadata/source_versions.yaml`
- `reports/01_international_data_audit.md`
- `reports/02_international_baselines.md`
- `reports/03_feature_ablation_benchmark.md`
- `reports/05_publication_readiness_gate.md`
- `reports/06_count_model_benchmarks.md`
- `manuscript/` full draft
- final figures
- final tables
- cover letter
- submission checklist

Before submission, these must pass:

- `pytest`
- `python -m ruff check src tests tools`
- `python tools/validate_international_cases.py --strict`
- `python tools/check_publication_readiness.py`
- all manuscript number checks
- all source URL checks
- secret scan
- clean git status except intentional ignored generated files

## 13. Exact Next 10 Tasks

Do these in order:

1. Add reproducibility manifest writer.
2. Add data dictionary writer.
3. Add feature-ablation benchmark and report.
4. Add negative-binomial GLM benchmark.
5. Add final plotting scripts and manuscript tables.
6. Create `manuscript/` and draft the ECDC-only IJHG manuscript.
7. Add `docs/REPRODUCIBILITY.md` and a `Makefile`.
8. Run full QA and update `reports/05_publication_readiness_gate.md`.
9. Decide MODIS branch: implement QA-masked NDVI/EVI or remove vegetation from
   all claims.
10. Decide PAHO/China branch: implement with provenance or keep manuscript
    ECDC-only.

## 14. Bottom Line

The publishable idea is not another hantavirus map.

The publishable idea is an auditable benchmark that shows what free public data
can and cannot support for hantavirus reported-incidence forecasting. The paper
will be strongest if it is honest about sparse surveillance, strict about
source provenance, and willing to report that simple baselines can beat complex
models.

The current repo is past the toy stage and passes the ECDC-only public-data
benchmark gate. The remaining work is manuscript-grade rigor: feature
ablations, a stronger count model, final figures/tables, reproducibility
packaging, and journal-specific writing.
