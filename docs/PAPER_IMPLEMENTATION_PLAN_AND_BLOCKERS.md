# Paper Implementation Plan And Blocker Register

Last revised: 2026-05-12

## Final Goal

The goal is a publishable research paper and reproducible code release, not a public alert dashboard.

Recommended paper identity:

> **Open Hantavirus Risk Benchmark:** a reproducible, uncertainty-calibrated benchmark for country-year reported hantavirus incidence under sparse international surveillance.

The benchmark should answer:

> What can free public surveillance, climate, vegetation, land-use, and reporting-context data forecast about reported hantavirus incidence, and where do simple baselines beat complex models?

The paper should not claim:

- live outbreak detection
- clinical guidance
- individual risk
- county-level human prediction
- human-to-human spread prediction for generic hantavirus
- operational public-health warning

## Research Basis Checked

Use these sources as the current evidence base for the plan:

| Topic | Source | Planning implication |
|---|---|---|
| ECDC EU/EEA hantavirus surveillance | https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023 | ECDC is the cleanest public harmonized country-year seed source. |
| U.S. public case limits | https://www.cdc.gov/hantavirus/data-research/cases/index.html | U.S. public data are state-level; county-level human claims remain blocked. |
| Hantavirus transmission and Andes exception | https://www.who.int/news-room/fact-sheets/detail/hantavirus and https://www.cdc.gov/hantavirus/about/andesvirus.html | Model reservoir/environment/spillover dynamics, not generic human spread. Andes-specific human-to-human simulation is a separate, source-specific project. |
| 2026 WHO DON cruise cluster | https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600 | Shows public relevance, but event signals should not be mixed into annual benchmark labels unless separately coded. |
| World Bank Indicators API | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392 | Free country-year denominator and reporting-context indicators. |
| TerraClimate | https://www.nature.com/articles/sdata2017191 and https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_TERRACLIMATE | Free global monthly climate/water-balance covariates, suitable for country-year lag features. |
| MOD13C2 | https://lpdaac.usgs.gov/products/mod13c2v061/ and https://ladsweb.modaps.eosdis.nasa.gov/api/v1/productPage/product=MOD13C2 | Free monthly global NDVI/EVI with quality fields; requires careful aggregation and QA flags. |
| FAOSTAT land use | https://www.fao.org/faostat/en/#data/RL | Free country-year land-use covariates already suitable for joins. |
| IJHG scope | https://ij-healthgeographics.biomedcentral.com/about | Best first journal fit for geospatial/remote-sensing benchmark and validation. |
| PLOS NTD scope | https://journals.plos.org/plosntds/s/journal-information | Fit improves if PAHO/China CDC rows and One Health framing are added. |
| EID journal info | https://wwwnc.cdc.gov/eid/pages/about.htm | Fit if framed around surveillance limits and emerging zoonotic disease relevance. |
| Scientific Data submission guidance | https://www.nature.com/sdata/publish/submission-guidelines | Backup route if model skill is weak but data/schema/reproducibility are strong. |

## Benchmark Or Risk Predictor Or Simulation?

### Decision

The main paper should be a **forecast benchmark**, not a one-time static risk assessment and not a standalone simulation paper.

Why:

- A one-time risk score is less publishable because HantavirusMap and similar trackers already serve map/signal audiences.
- A simulation-only paper is risky because public human labels are sparse and synthetic data can look like overclaiming.
- A forecast benchmark is publishable because it has validation, uncertainty, reusable data infrastructure, and honest negative results.

### Primary benchmark output

One forecast task:

> For each country-year-source-system-syndrome row, predict the next complete calendar year's reported cases and incidence rate using only data available at or before forecast time.

Required prediction table:

- `forecast_date`
- `target_year`
- `target`
- `horizon`
- `iso3`
- `country`
- `syndrome`
- `source_system`
- `model`
- `quantile`
- `value`

Current implementation:

- `tools/run_international_baselines.py`
- `data/processed/international_baseline_predictions.csv`

### Secondary risk assessment output

Use risk assessment only as a derived display from forecast distributions:

- probability of any reported cases
- probability of exceeding a country-specific historical percentile
- probability of year-over-year increase

Do not make a separate unvalidated risk-score product.

### Simulation output

Simulation should be secondary and clearly labeled:

> reservoir-spillover or reported-incidence scenario stress test.

Current implementation:

- `tools/run_markov_simulation.py`
- `reports/04_markov_simulation_stress_test.md`

Future simulation should not be "human spread" unless it is Andes-virus-specific and supported by source-specific evidence.

## Exact Paper Plan

### Paper Type A: Main Preferred Paper

Title:

> An open benchmark for country-level reported hantavirus incidence forecasting under sparse international surveillance

Target journal:

1. International Journal of Health Geographics
2. PLOS Neglected Tropical Diseases, if PAHO/China extension is strong
3. Emerging Infectious Diseases, if surveillance interpretation is strong

Core contribution:

- audited surveillance benchmark
- environmental covariate evaluation
- uncertainty-calibrated baselines
- simulation stress-test appendix

Minimum result needed:

- ECDC country-year benchmark with climate/vegetation/land-use features
- at least temporal validation
- ideally leave-country validation
- negative results included

### Paper Type B: Data/Benchmark Descriptor Backup

Target journal:

- Scientific Data
- GigaScience
- Data in Brief only as fallback

Use if:

- model skill is weak
- source expansion is valuable
- data schema and reproducibility are strong

Core contribution:

- standardized multi-source country-year hantavirus reported-incidence table
- source provenance
- rebuild pipeline
- baseline reference outputs

### Paper Type C: Reservoir-Spillover Simulation Paper

Do not pursue first.

Use later if:

- TerraClimate/MODIS features are complete
- NEON or other rodent/reservoir data are integrated
- simulation is calibrated to empirical data

Core contribution:

- latent reservoir pressure and reported-spillover state model
- climate/vegetation scenario analysis
- underreporting stress tests

## Exact Implementation Specs

### Phase 1: Freeze The ECDC Benchmark Seed

Status: mostly done.

Files:

- `src/hantavirus_predictor/datasets/ecdc_hantavirus.py`
- `tools/create_ecdc_case_table.py`
- `schemas/international_country_cases.schema.yaml`
- `tools/validate_international_cases.py`
- `reports/01_international_data_audit.md`

Acceptance criteria:

- `python tools/create_ecdc_case_table.py --accessed-date 2026-05-12`
- `python tools/validate_international_cases.py --strict`
- source totals match ECDC for all years in the report
- no duplicate primary keys
- population denominator missingness is zero

Known limitation:

- ECDC seed is only 2019-2023 and Europe-heavy.

### Phase 2: Finish Free Public Covariates

Status:

- World Bank: done.
- FAOSTAT: done.
- TerraClimate: manifest only.
- MOD13C2: manifest only.

Implement:

1. Country polygon source:
   - use Natural Earth Admin 0 or World Bank/GeoBoundaries equivalent
   - store boundary metadata and version
   - do not commit large shapefiles unless license and size are acceptable

2. TerraClimate aggregation:
   - input: `metadata/terraclimate_source_manifest.csv`
   - variables: `ppt`, `tmin`, `tmax`, `vpd`, `soil`, `def`
   - output: `data/processed/terraclimate_country_year.csv`
   - features:
     - annual mean/sum as appropriate
     - seasonal summaries
     - lag 0, 1, 2, 3 years
     - country-specific anomaly relative to available baseline
   - QA:
     - row coverage by iso3/year
     - missingness by variable
     - no use of future years in lag features

3. MOD13C2 aggregation:
   - input: `metadata/mod13c2_granule_manifest.csv`
   - variables: NDVI, EVI, QA
   - output: `data/processed/mod13c2_country_year.csv`
   - features:
     - annual mean NDVI/EVI
     - growing-season peak if regionally meaningful
     - anomaly and lag features
     - QA-weighted missingness and valid-pixel share
   - QA:
     - valid range after scale factor
     - QA mask documented
     - no hidden interpolation without flags

4. Feature matrix:
   - output: `data/processed/international_model_matrix.csv`
   - keys:
     - `iso3`
     - `year`
     - `syndrome`
     - `source_system`
   - include missingness flags for every covariate family

Acceptance criteria:

- every ECDC row has World Bank and FAOSTAT covariates
- at least 95 percent of rows have TerraClimate features
- at least 95 percent of rows have MODIS features or documented QA missingness
- audit report lists missingness for every feature family

### Phase 3: Baseline Forecast Benchmark

Status: first pass exists.

Files:

- `src/hantavirus_predictor/models/international_baselines.py`
- `tools/run_international_baselines.py`
- `tools/plot_international_baselines.py`
- `reports/02_international_baselines.md`

Required baseline models:

1. country historical mean rate
2. last-observed country rate
3. region/syndrome/source mean rate
4. empirical negative-binomial rate
5. hierarchical shrinkage negative-binomial rate
6. gradient boosting with tabular covariates

Upgrade needed:

- replace empirical negative-binomial with a proper negative-binomial GLM or Bayesian hierarchical model
- add feature ablations:
  - surveillance-only
  - +World Bank
  - +FAOSTAT
  - +TerraClimate
  - +MODIS
  - all covariates

Metrics:

- WIS
- 90 percent empirical coverage
- MAE/RMSE
- Poisson or negative-binomial deviance
- Brier score for pre-registered thresholds

Acceptance criteria:

- predictions generated for all validation rows
- all models output quantiles
- reports include negative results
- no model is promoted unless it improves WIS and maintains coverage

### Phase 4: Validation Design

Status: initial config exists.

Files:

- `configs/validation_splits.yaml`

Required splits:

1. temporal holdout
2. rolling-origin validation
3. leave-country-out
4. leave-source-system-out after PAHO/China rows exist

Acceptance criteria:

- split file is frozen before tuning
- no feature timestamp after target year
- feature selection happens inside training folds

### Phase 5: Simulation/Scenario Stress Test

Status: Markov incidence-state simulation exists.

Files:

- `src/hantavirus_predictor/simulations/markov_incidence.py`
- `tools/run_markov_simulation.py`
- `reports/04_markov_simulation_stress_test.md`

Current acceptable use:

- supplement or methods appendix
- state persistence
- underreporting stress tests

Next upgrade:

- move from zero/low/high Markov states to a reservoir-spillover scenario model:
  - latent environmental suitability
  - latent reservoir pressure
  - overdispersed reported spillover counts
  - observation/reporting layer

Acceptance criteria:

- simulation parameters estimated from observed data or justified from literature
- simulated data are never added to training labels
- all figures label outputs as simulated

### Phase 6: Source Expansion

Add only after ECDC + covariate benchmark works.

PAHO Americas:

- syndrome: HPS or HCPS
- source type: epidemiological alert or national ministry source
- caveat: alert data are not complete long-term series unless backfilled

China CDC:

- syndrome: HFRS
- source type: peer-reviewed/article surveillance summary
- caveat: separate source system; do not pool blindly with ECDC

WHO DON:

- use for event context and recent relevance, not annual benchmark labels unless systematically coded

Acceptance criteria:

- each row has source URL, title, accessed date, source type, quality grade, and extraction note
- source-total reconciliation report exists
- source-system effects are modeled

### Phase 7: Manuscript Package

Files to create:

- `manuscript/outline.md`
- `manuscript/methods.md`
- `manuscript/results.md`
- `manuscript/limitations.md`
- `manuscript/cover_letter_ijhg.md`

Required figures:

1. benchmark workflow schematic
2. data availability and source reconciliation
3. baseline skill and calibration
4. environmental covariate ablation
5. simulation stress-test transition/scenario panel
6. limitations/governance panel

Acceptance criteria:

- every figure can be rebuilt
- every claim links to a report or source
- limitations are in main text, not buried

## Potential Blockers And Revisions

| Blocker | Why it matters | Revision to get past it | Go/no-go rule |
|---|---|---|---|
| HantavirusMap already exists | A live map/tracker would look derivative. | Do not build a live tracker. Publish a forecast-validation benchmark with uncertainty and reproducibility. | Any "map-first" plan is no-go. |
| Public U.S. county human data unavailable | Blocks fine-scale human prediction claims. | Use international country-year labels; keep county work partner-only. | No county-level human claims without DUA/partner data. |
| ECDC seed has only 5 years | Weak for complex models. | Start with simple baselines, rolling-origin validation, and possibly ECDC-only methods/data paper. Add PAHO/China later. | No deep learning main result on seed-only data. |
| Syndromes differ by region | HFRS and HPS/HCPS are not interchangeable. | Require syndrome/source-system strata in every row and model. | No pooled global "hantavirus" model without strata. |
| Source systems differ | ECDC, PAHO, China CDC, WHO DON are not comparable raw streams. | Model source system and quality grade; use holdout sensitivity. | No pooled source claim without source effects. |
| Underreporting varies | Reported incidence is not true incidence. | Use "reported incidence"; include GDP/rurality/reporting context and underreporting simulations. | Never call output true infection incidence. |
| HantavirusMap and other trackers use live signals | Active alerts are not annual labels. | Keep signals as context or a separate event dataset; do not mix with annual case labels. | No mixed signal/count target. |
| Human-to-human spread framing is risky | Most hantaviruses are reservoir-to-human; Andes is special. | Use reservoir-spillover or incidence-state simulation; Andes-specific spread only as a separate sourced module. | No generic human spread simulation. |
| TerraClimate aggregation is heavy | Gridded data can be slow and error-prone. | Start with country-year zonal means for ECDC countries only, cache outputs, report missingness. | No climate claim until aggregation QA passes. |
| MODIS QA complexity | NDVI/EVI without QA can be misleading. | Apply QA/valid-range masks and report valid-pixel share. | No vegetation claim without QA flags. |
| FAOSTAT country names/ISO joins | Name mismatches can silently drop rows. | Use explicit country mapping and missingness tests. | Join missingness must be reported. |
| Model skill may be weak | Weak skill can feel unpublishable. | Frame negative result as benchmark value: simple baselines define realistic limits. | If skill is weak, submit data/methods benchmark or Scientific Data-style paper. |
| Gradient boosting currently undercovers | ML result may look bad. | Keep it as negative result unless calibration improves; do not promote. | No ML main claim without WIS and coverage win. |
| Simulation may look like fake data | Reviewers dislike synthetic validation. | Use simulation only for stress testing and uncertainty explanation. | No simulated labels in model validation. |
| Death data incomplete | Mortality analysis is not supported. | Keep deaths as secondary/context only until complete source table exists. | No mortality model until deaths are complete. |
| Licensing/redistribution | Some raw data may not be redistributable. | Commit scripts/manifests; keep raw data ignored; document licenses. | No raw redistribution without permission. |
| Current 2026 Andes/cruise outbreak changes public interest | It can tempt overclaiming. | Mention as relevance/context only; do not reshape annual benchmark around one active event. | Event modeling is separate from annual benchmark. |
| Journal mismatch | Wrong journal can reject despite good work. | Target IJHG first; PLOS NTD only after stronger One Health/global extension. | Choose journal after final scope is known. |

## Revised Plan To Get Past Blockers

### If the data remain ECDC-only

Publish as:

> A reproducible EU/EEA reported-incidence benchmark and validation study.

Target:

- International Journal of Health Geographics
- Scientific Data if data/reuse contribution dominates

Claims:

- ECDC/EU-EEA only
- reported incidence only
- benchmark methods and limitations

Do not claim:

- global generalization
- HPS/HCPS conclusions
- operational forecast

### If PAHO and China rows are added

Publish as:

> A syndrome-stratified international benchmark.

Target:

- International Journal of Health Geographics
- PLOS Neglected Tropical Diseases
- Emerging Infectious Diseases

Claims:

- international source-stratified benchmark
- differences between HFRS and HPS/HCPS source systems
- environmental covariate contribution by region/source

### If covariates improve little

Publish as:

> Public surveillance limits paper.

Claim:

- Simple baselines are hard to beat.
- Public data are insufficient for precise early warning.
- The benchmark prevents false precision.

This is still publishable if framed honestly.

### If covariates improve skill

Publish as:

> Environmental-covariate forecast benchmark.

Claim:

- Specific lagged climate/vegetation features improve WIS or calibration in specified strata.
- Improvement is bounded and source-dependent.

### If simulation becomes strong

Use as:

- main-text conceptual model plus supplementary scenario results

Claim:

- Simulation stress tests show how underreporting or environmental anomalies affect forecast uncertainty.

Do not claim:

- simulation validates real outbreaks
- simulated data increase sample size

## Exact Next Agent Handoff

Next agent should do this in order:

1. Read this file and `docs/PUBLICATION_FIRST_DIFFERENTIATION_PLAN.md`.
2. Run the full QA command block in `docs/PROJECT_STATE.md`.
3. Implement TerraClimate country-year aggregation for ECDC countries only.
4. Add tests for:
   - expected output columns
   - no future leakage in lag features
   - missingness reporting
5. Rebuild `data/processed/international_country_year.csv`.
6. Update `reports/01_international_data_audit.md`.
7. Re-run baselines with feature ablations.
8. Update `reports/02_international_baselines.md`.
9. Decide whether MODIS aggregation is feasible locally.
10. Only after climate/vegetation QA, consider PAHO/China extraction.

## Final QA Checklist

Before calling the paper plan ready:

- `python tools/validate_international_cases.py --strict`
- `python tools/validate_manual_data.py`
- `python tools/build_international_dataset.py`
- `python tools/run_international_baselines.py`
- `python tools/run_markov_simulation.py`
- `python tools/write_paper_readiness_report.py`
- `pytest`
- `python -m ruff check src tests tools`
- confirm generated reports match the scope claimed in docs
- confirm no secrets or raw restricted data are tracked
- confirm root file deletions are intentional before staging them

## Bottom Line

The best publishable idea is a benchmark paper, not a live map and not a standalone spread simulator.

Simulation is useful if it is explicitly a scenario stress test for reservoir-spillover and surveillance uncertainty. It should support the benchmark, not replace empirical validation.
