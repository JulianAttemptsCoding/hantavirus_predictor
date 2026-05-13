# Publication Master Plan

Last updated: 2026-05-12

Working title:

> An open benchmark for country-level reported hantavirus incidence: retrospective one-year-ahead evaluation under sparse public surveillance

This is the root-level handoff plan for turning this repository into a paper
package targeted at a credible journal, preferably Q1 or impact factor above
approximately 2.5. It incorporates the three external audits supplied on
2026-05-12 plus a fresh source check on 2026-05-12.

The plan is intentionally conservative. The project can be publishable only if
it is honest about the data: five ECDC annual reporting years, sparse
country-level observations, source-system quirks, and public covariates that
may or may not improve over simple baselines.

## 1. Final Scientific Position

### 1.1 Paper Identity

The paper is a public-data benchmark and reproducibility paper, not a live
outbreak tracker and not a medical advice tool.

Core identity:

> Open Hantavirus Risk Benchmark: an open, provenance-first,
> uncertainty-calibrated benchmark for country-year reported hantavirus
> incidence using free public surveillance, demographic, land-use, and climate
> data.

Allowed paper type:

- Retrospective one-year-ahead evaluation.
- Data/methods benchmark with reproducible source joins.
- Quantile forecast evaluation under sparse public surveillance.
- Geospatial health surveillance paper for EU/EEA reported incidence.
- Negative-result paper if climate or machine learning does not improve over
  simple surveillance baselines.

Not allowed:

- Do not call the current work true prospective forecasting.
- Do not claim operational alerting, medical diagnosis, or individual risk.
- Do not claim county-level U.S. prediction. CDC states hantavirus data are
  reported by state only and county-level data cannot be provided to protect
  identities.
- Do not claim causal climate effects.
- Do not claim generic human-to-human spread. Andes virus is a special case
  and is not the EU/EEA ECDC target.
- Do not pool ECDC, PAHO, and China CDC labels in one model without explicit
  syndrome and source-system strata.

### 1.2 Primary Scope

Primary manuscript scope:

- Geography: EU/EEA countries in the ECDC Annual Epidemiological Report.
- Labels: annual country-year reported hantavirus infection counts,
  2019-2023.
- Primary source system: ECDC only.
- Unit of analysis: country-year.
- Target: reported annual cases and incidence per 100,000 population.
- Evaluation: retrospective one-year-ahead evaluation, especially 2022 and
  2023, plus leave-one-year-out sensitivity analysis.
- Public covariates: World Bank population/rurality/GDP, FAOSTAT land use,
  TerraClimate climate/water-balance features, Natural Earth country
  boundaries.
- Optional covariate: MODIS MOD13C2 Collection 6.1 NDVI/EVI only if the hard
  QA gate in Section 7.4 passes.

The current ECDC seed table reconciles ECDC annual totals:

| Year | ECDC total |
| --- | ---: |
| 2019 | 4088 |
| 2020 | 1693 |
| 2021 | 4947 |
| 2022 | 2185 |
| 2023 | 1885 |

The current processed table is a raw analysis table, not the modeling feature
matrix. The audits correctly flagged that 95 raw columns for 142 rows can look
like feature inflation. The manuscript must report:

- raw processed table dimensions separately;
- final modeling matrix dimensions separately;
- the number of candidate features before and after screening;
- the exact feature sets used in ablation.

Hard rule: the final modeling matrix should normally contain 15-25 predictors
before one-hot encoding. If the model matrix has more candidate predictors than
rows, the analysis must switch to penalized or shrinkage-only models and report
that complex models are exploratory.

### 1.3 Journal Targeting

Primary target: International Journal of Health Geographics.

Why it fits:

- The journal explicitly covers GIS-enabled surveillance, remote sensing,
  spatial epidemiology, and spatio-temporal statistics in health.
- The 2024 journal impact factor shown on the journal page is 3.2.
- The paper can be framed around public geospatial health surveillance,
  uncertainty, and reproducible open covariate joins.

What IJHG will expect:

- Maps, not only tables.
- Explicit geospatial methods.
- Area-appropriate projections and clear boundaries.
- A real public health/geographic insight, even if the result is that simple
  baselines and surveillance quality dominate the signal.

Required IJHG figures:

- EU/EEA incidence choropleth by year or 2023 snapshot.
- Data-gap and surveillance-quality map.
- Predicted versus observed incidence map for the best model.
- Uncertainty map or hatching layer showing high interval width.

Strong fallback: Scientific Data.

Why it fits:

- Scientific Data publishes Data Descriptors and emphasizes data sharing and
  reusable processing methods.
- Its 2024 journal impact factor is listed as 6.9 on the journal metrics page.
- This is the best fallback if model skill is weak but the dataset, pipeline,
  provenance, and benchmark format are strong.

Strong fallback: BMC Public Health.

Why it fits:

- The journal scope includes infectious disease epidemiology, environmental
  health, public health informatics, and surveillance.
- The journal page lists a 2024 impact factor of 3.6.
- This is a better fallback than PLOS NTD for an ECDC-only paper if the
  geospatial contribution is less central.

Conditional reach: PLOS Computational Biology.

Use only if the modeling contribution becomes methodologically stronger, for
example a reusable benchmark framework with strong uncertainty evaluation and
substantial biological insight. The current ECDC-only seed is probably too
small for this as a primary target.

Do not target PLOS Neglected Tropical Diseases for the ECDC-only paper.

Reason:

- PLOS NTD defines its core scope around poverty-promoting diseases that
  primarily occur in rural or poor urban areas in low-income and middle-income
  countries, and explicitly says high-income-country work is out of scope
  unless it has consequences in LMIC.
- The ECDC-only panel is dominated by high-income European surveillance.
- PLOS NTD becomes plausible only after a PAHO/LMIC One Health expansion with
  clear relevance to neglected populations. That is post-submission work, not
  version 1.

Do not prioritize Epidemics under the user's journal constraint.

Reason:

- Epidemics is scientifically relevant for infectious disease dynamics, but
  the current page lists a 2.4 impact factor, below the requested approximate
  threshold of 2.5.
- It can remain a backup only if the user relaxes the journal metric
  constraint or if the paper becomes a stronger transmission-dynamics paper.

## 2. Source Anchors And Evidence

These sources must appear in the manuscript references, data availability
statement, or cover-letter justification.

### 2.1 ECDC Surveillance

Primary ECDC source:

- https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
- ECDC citation: European Centre for Disease Prevention and Control.
  Hantavirus infection. In: ECDC. Annual Epidemiological Report for 2023.
  Stockholm: ECDC; 2025.

Required ECDC metadata handling:

- The report is based on 2023 TESSy data retrieved on 2024-11-06.
- In 2023, 28 EU/EEA countries reported 1885 cases.
- Finland and Germany accounted for 60.5 percent of 2023 cases.
- The United Kingdom had no data from 2020 onward because it withdrew from the
  EU on 2020-01-31. The current ECDC seed table excludes UK rows entirely so
  the panel is consistent. If a future table adds UK 2019, it must be flagged
  as `eu_eea_status = withdrawn` and excluded from the primary balanced-panel
  analysis.
- Belgium 2023 must be flagged because ECDC says its surveillance system
  changed and was no longer comprehensive, so the rate was not calculated.
  Current repo action: `surveillance_completeness = not_comprehensive` and
  `quality_grade = C`.
- Cyprus 2023 is flagged by ECDC metadata as unspecified/not available for
  some rate context. Current repo action: `surveillance_completeness =
  unspecified` and `quality_grade = C`.
- The paper must include a sensitivity analysis excluding Belgium 2023 and any
  other non-comprehensive rows.

### 2.2 CDC Privacy Boundary

CDC source:

- https://www.cdc.gov/hantavirus/data-research/cases/index.html

Use in manuscript:

- CDC reports U.S. hantavirus data by state only and states that county-level
  data cannot be provided to protect identities.
- This justifies why the paper does not attempt U.S. county-level human
  prediction using free public data.

### 2.3 Competitor And Market Position

HantavirusMap exists:

- https://hantavirusmap.com/

Positioning:

- HantavirusMap is a live signal tracker and public-facing map.
- This paper must not compete as another live alert map.
- The novelty is the auditable benchmark: frozen labels, public covariates,
  source provenance, uncertainty-calibrated evaluation, calibration plots,
  feature ablations, and negative-result transparency.

One-line marketing statement for cover letter:

> Existing public trackers aggregate signals; this study provides a frozen,
> reproducible benchmark that tests whether public climate and land-use
> covariates actually improve country-year hantavirus reported-incidence
> evaluation over strong surveillance baselines.

### 2.4 Public Covariates And Licenses

World Bank:

- Source: https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets
- Default license: CC BY 4.0 unless specifically labeled otherwise.
- Required attribution in data availability statement.

FAOSTAT:

- Source: https://www.fao.org/statistics/data-dissemination/agrifood-systems/en
- FAO provides free and unrestricted access to statistical databases and has an
  open data licensing policy.
- Required attribution: acknowledge FAO/FAOSTAT in the data availability and
  figure/table notes where land-use data are used.

TerraClimate:

- Source paper: Abatzoglou JT, Dobrowski SZ, Parks SA, Hegewisch KC.
  TerraClimate, a high-resolution global dataset of monthly climate and
  climatic water balance from 1958-2015. Scientific Data. 2018;5:170191.
  https://doi.org/10.1038/sdata.2017.191
- Use as lagged climate/water-balance covariates.
- Required caveat: country-level aggregation can mask within-country exposure
  heterogeneity.
- Verify current endpoint before final data freeze because mirrors and THREDDS
  endpoints can change.

Natural Earth:

- Source: https://www.naturalearthdata.com/about/terms-of-use/
- Public domain.
- Recommended attribution line even though not required: "Made with Natural
  Earth. Free vector and raster map data at naturalearthdata.com."

MODIS MOD13C2:

- Source: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod13c2-061
- Product: MODIS/Terra Vegetation Indices Monthly L3 Global 0.05Deg CMG
  Version 6.1.
- Includes NDVI, EVI, VI QA, and spatial statistics.
- Requires NASA Earthdata access but is free with registration.
- Use only if the Section 7.4 decision gate passes.

### 2.5 Optional Non-ECDC Sources

PAHO:

- Source: https://www.paho.org/en/documents/epidemiological-alert-hantavirus-pulmonary-syndrome-americas-region-19-december-2025
- The PAHO alert is event/epidemiological-alert information about Hantavirus
  Pulmonary Syndrome in the Americas, not a harmonized annual country-year
  surveillance table.
- Do not use PAHO alerts as primary labels for the ECDC v1 paper. At most,
  use them as post-submission external-stress-test material.

China CDC Weekly:

- Source: https://weekly.chinacdc.cn/en/article/doi/10.46234/ccdcw2025.141
- Covers HFRS in China from 2014-2023 and includes county/PLAD information and
  HTNV/SEOV diversity.
- Do not pool with ECDC v1. China data are a different spatial scale and a
  different source system.

## 3. Related Work And Novelty Defense

The paper must not pretend there are no hantavirus risk models. The novelty is
not "first hantavirus map" and not "first climate model." It is the first
audited, open, public-data, country-year reported-incidence benchmark that
links ECDC labels to public covariates and evaluates uncertainty-calibrated
one-year-ahead retrospective predictions against strong baselines.

Required related work:

- Zeimes et al. 2015, Landscape and Regional Environmental Analysis of the
  Spatial Distribution of Hantavirus Human Cases in Europe. Frontiers in
  Public Health. This is the closest European spatial risk-map competitor. It
  used environmental/spatial modeling, boosted regression trees, and
  multilevel logistic regression. Differentiate by saying it is spatial
  distribution/risk mapping, while this project is a temporal country-year
  benchmark with probabilistic evaluation and reproducible public-data
  covariate joins.
- Kallio et al. 2009, Cyclic hantavirus epidemics in humans predicted by
  rodent host dynamics. Differentiate by saying that mechanistic reservoir
  dynamics require richer rodent/host time series; this project asks what can
  be done with free public human surveillance and broad covariates.
- Reusken and Heyman 2013, Factors driving hantavirus emergence in Europe.
  Use as background for multi-factorial reservoir, land-use, climate, and
  anthropogenic drivers. Do not turn this into causal claims.
- Kazasidis, Geduhn, and Jacob 2024, High-resolution early warning system for
  human Puumala hantavirus infection risk in Germany. This is a key
  district-level German PUUV early warning and map platform comparator.
  Differentiate by geographic scope, public-data benchmark format, and
  evaluation of cross-country surveillance limitations.
- Glass et al. 2000, remotely sensed data for HPS risk. Use as remote-sensing
  precedent in hantavirus ecology, not as evidence for ECDC country-year
  prediction.
- Allen, McCormack, and Jonsson 2006, mathematical models for hantavirus
  infection in rodents. Use to justify why mechanistic spread simulation is
  biologically interesting but not the main validation evidence here.
- Forecast-benchmark literature such as COVID-19 Forecast Hub and Bracher,
  Ray, Gneiting, and Reich on weighted interval score. Use to justify WIS,
  coverage, sharpness, and probabilistic forecast formats.

Novelty paragraph to use in the introduction:

> Authoritative surveillance reports provide annual case totals, and prior
> hantavirus studies have mapped ecological suitability or local outbreak risk.
> However, there is no frozen, open-source benchmark that reconciles EU/EEA
> country-year reported hantavirus labels, links them to public climate,
> land-use, and demographic covariates, and tests whether those covariates
> improve probabilistic retrospective one-year-ahead evaluation over simple
> surveillance baselines. This benchmark fills that gap and makes negative
> results visible rather than burying them.

## 4. Claims Policy

### 4.1 Allowed Claims After QA

- The dataset reconciles ECDC annual totals for 2019-2023.
- The pipeline links ECDC country-year labels to public World Bank, FAOSTAT,
  TerraClimate, and Natural Earth sources.
- The benchmark evaluates simple baselines and selected covariate models using
  WIS, relative WIS, interval coverage, interval width, MAE, Brier score, and
  calibration plots.
- If true after ablation: covariates do or do not improve over surveillance
  baselines.
- If true after QA: simple empirical baselines are hard to beat in sparse
  country-year public surveillance.
- The open benchmark is useful because it reveals what current public data can
  and cannot support.

### 4.2 Prohibited Claims

- No causal effect of climate, land use, or vegetation.
- No real-time outbreak detection.
- No authoritative risk map.
- No clinical decision support.
- No individual, county, or address-level risk.
- No global generalization from ECDC-only labels.
- No superiority of machine learning unless it improves WIS, relative WIS,
  coverage, and interval width against the best simple baseline.
- No vegetation/NDVI/EVI claim until MODIS QA-masked aggregation passes.
- No simulation-as-validation claim.

### 4.3 Required Language

Use:

- "reported incidence"
- "public surveillance"
- "retrospective one-year-ahead evaluation"
- "probabilistic benchmark"
- "calibration and sharpness"
- "country-year"
- "source-system stratified"
- "uncertainty-calibrated"
- "negative results retained"

Avoid unless a true prospective component is added:

- "prospective forecast"
- "predicts outbreaks"
- "live risk"
- "spread prediction"
- "causal driver"
- "early warning system" except when discussing related work.

## 5. Current Repo State

Branch: `main`.

Known current tracked state before this revision:

- Latest pushed commit before this audit pass: `26e5757 Add publication master
  plan`.
- TerraClimate and publication QA gate implementation exists in prior commit
  `d51bec9`.
- The repo has generated data and reports ignored by git; agents must rebuild
  them locally.
- NASA Earthdata credentials may exist in `nasa earthdata acc info.txt`; this
  file must remain ignored and must never be printed or committed.

Current implemented components:

- ECDC case-table creation and validation.
- International country-year processed table builder.
- World Bank, FAOSTAT, TerraClimate, Natural Earth, and MODIS manifest code.
- Simple baseline forecast models.
- Nested feature ablation with train-only imputation, feature screening, WIS,
  relative WIS, coverage, interval width, MAE, Brier score, MASE, and
  calibration outputs.
- Exploratory penalized Poisson GLM with population offset and
  validation-selected ridge penalty.
- IJHG map generator using Natural Earth and ETRS89 / LAEA Europe
  (`EPSG:3035`) for incidence, surveillance metadata, predicted versus
  observed incidence, and uncertainty maps.
- Sensitivity and simulation-based detectability analysis for flagged
  surveillance rows and COVID-era training-year checks.
- First-pass Markov incidence-state simulation.
- Data audit, baseline, paper-readiness, and publication-gate reports.
- Tracked manuscript skeleton under `docs/manuscript/`.
- Tests for validation, features, metrics, sources, and simulation.

Current audit-pass code additions:

- `eu_eea_status` in the case schema.
- `surveillance_completeness` in the case schema.
- Belgium 2023 and Cyprus 2023 source-quality flags.
- Relative WIS and mean 90 percent interval width metrics.
- Publication readiness gate warning for calibration concerns.
- TerraClimate lag-1 per-variable missingness report.

Generated outputs are not committed. Rebuild them with the commands in Section
12.

## 6. Dataset Specification

### 6.1 Manual Case Table

Tracked schema:

- `schemas/international_country_cases.schema.yaml`
- Validator: `src/hantavirus_predictor/validation/international_cases.py`

Required columns:

- `iso3`
- `country`
- `year`
- `reporting_system`
- `syndrome`
- `pathogen_or_virus`
- `cases`
- `deaths`
- `population`
- `case_definition`
- `source_url`
- `source_title`
- `accessed_date`
- `source_type`
- `quality_grade`
- `region`
- `eu_eea_status`
- `surveillance_completeness`
- `notes`

Required source metadata:

- `source_url` must be nonempty.
- `accessed_date` must be nonempty.
- `source_system` is derived in the processed table from `reporting_system`
  and is used for model stratification.
- `case_definition` must distinguish reportable disease definitions when
  known.
- `pathogen_or_virus` must use a known virus only when source-reported;
  otherwise use `unspecified_hantavirus`.

Required quality metadata:

- `quality_grade = A`: official, comprehensive, harmonized, primary-source
  series.
- `quality_grade = B`: official table but extracted manually or with some
  denominator/source caveat.
- `quality_grade = C`: official but non-comprehensive, rate not calculated,
  or completeness caveat.
- `quality_grade = D`: event-based alert or media-derived signal. Do not use
  as a primary label for the ECDC v1 paper.

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

### 6.2 Processed Analysis Table

File:

- `data/processed/international_country_year.csv`

Purpose:

- Audit and analysis table. It may contain many raw/source/intermediate
  columns.

Hard manuscript rule:

- Do not describe all raw columns as model features.
- Report modeling matrix dimensions separately.
- Report missingness per variable and per feature family.

Required no-leakage rules:

- Forecast features for target year `t` must use only information available on
  or before 31 December of `t - 1`.
- No current-year climate, land-use, or reporting completeness values in
  one-year-ahead models unless explicitly labeled as a retrospective
  explanatory sensitivity analysis.
- Imputation parameters must be learned on training data only and applied to
  validation/test data.

## 7. Implementation Plan From Here To Submission

### 7.1 Phase 0: Freeze The V1 Scope

Decision:

- V1 is ECDC-only, EU/EEA, 2019-2023.
- PAHO and China are deferred.
- MODIS is decision-gated early.
- Simulation is appendix only.

Deliverables:

- Update `PUBLICATION_MASTER_PLAN.md`.
- Update `docs/AGENT_HANDOFF.md`.
- Run schema validation and publication gate.

QA:

- Root plan is ASCII.
- Root plan contains no claim that ECDC-only work is a global risk predictor.
- PLOS NTD is not listed as an ECDC-only target.

### 7.2 Phase 1: Rebuild And Freeze Reproducible Snapshot

Deliverables:

- `data/manual/international_country_cases.csv`
- `data/processed/international_country_year.csv`
- `reports/01_international_data_audit.md`
- `reports/05_publication_readiness_gate.md`
- `docs/data_dictionary.md`
- `docs/reproducibility_manifest.md`

Implementation specs:

- Rebuild ECDC seed table from `tools/create_ecdc_case_table.py`.
- Validate strict schema.
- Rebuild covariate joins.
- Reconcile annual totals.
- Report surveillance metadata flags.
- Report per-variable TerraClimate missingness.
- Report raw analysis columns and final modeling features separately.
- Add checksums for frozen processed CSVs.
- Prepare Zenodo or OSF deposition plan before manuscript submission.

Do not commit:

- Raw large downloads.
- NASA credentials.
- Any user-provided secret file.

Secret scan:

```powershell
rg -n "password\s*=|token\s*=|secret\s*=|api_key|BEGIN [A-Z ]*PRIVATE KEY" .
```

Manual review required:

- `nasa earthdata acc info.txt` must remain ignored and uncommitted.

### 7.3 Phase 2: Feature Ablation Benchmark

Purpose:

- Answer whether public covariates add measurable value beyond surveillance
  history.

Feature-set definitions:

- `surveillance_only`: country historical mean rate, last observed country
  rate, regional mean, source system, syndrome, target year, pandemic-period
  indicator.
- `context`: `surveillance_only` plus lagged World Bank rurality and GDP.
- `land_use`: `context` plus lagged FAOSTAT land-use shares.
- `climate`: `context` plus lagged TerraClimate annual summaries.
- `all_public`: `context` plus lagged FAOSTAT plus lagged TerraClimate.
- `modis_optional`: `all_public` plus MODIS NDVI/EVI only if Section 7.4
  passes.

Feature sets are nested. Every set is compared on the same rows and splits.

Imputation:

- Continuous variables: training-set median.
- Binary flags: training-set mode.
- Categorical variables: explicit `missing` level if needed.
- Save imputation parameters for each split.
- Never impute using validation/test distributions.

Feature reduction:

- Drop exact duplicates and constant features.
- Drop features with more than 40 percent missingness before imputation unless
  biologically essential and pre-registered.
- For highly correlated continuous features, use VIF screening or pairwise
  correlation thresholding.
- Target final modeling matrix: normally 15-25 predictors before one-hot
  encoding.
- If more predictors are retained, require LASSO/ridge/elastic-net shrinkage
  and label results exploratory.

Evaluation:

- Primary split: train 2019-2021, validation 2022, test 2023.
- Primary sensitivity: leave-one-year-out CV.
- Secondary sensitivity: leave-one-country-out CV for robustness only.
- Bootstrap paired country-level WIS differences where sample size permits.
- Diebold-Mariano tests only if the paired error series is large enough to be
  meaningful; otherwise report paired differences and bootstrap intervals.

Metrics:

- WIS.
- Relative WIS = WIS / mean observed cases for that target-year/model.
- 90 percent empirical coverage.
- Mean 90 percent prediction interval width.
- MAE.
- Brier score for any-case threshold.
- MASE using a last-observed-country-rate naive denominator where valid.
- Calibration plot: empirical coverage versus nominal coverage.
- Sharpness plot: interval width by model/year.

Promotion rule:

- A covariate model can be emphasized only if it improves WIS or relative WIS
  and does not degrade coverage or interval width in a way that makes the
  improvement meaningless.
- If covariates fail, report the negative result as a core contribution.

### 7.4 Phase 3: MODIS Decision Gate

Deadline:

- Decide by Week 2 of the manuscript sprint.

Implementation required before inclusion:

- Use MOD13C2 Version 6.1.
- Parse NDVI, EVI, VI QA, and valid-pixel fields.
- Apply QA masking before aggregation.
- Aggregate monthly country-level values, then annual and lag-1 summaries.
- Record the number of valid pixels and total pixels per country-month.
- Save exact product version, access date, granule list, and checksums.

Inclusion thresholds:

- At least 95 percent valid-pixel coverage for at least 90 percent of
  country-years after QA masking.
- MODIS feature family improves WIS or relative WIS by at least 5 percent
  against `all_public` on the fixed evaluation split.
- MODIS does not materially worsen 90 percent coverage.
- The download and aggregation pipeline can be rerun from documented inputs.

If any threshold fails:

- Remove NDVI/EVI/vegetation claims from the main manuscript.
- Keep MODIS as future work only.
- Use TerraClimate water-balance variables as a cautious proxy for ecological
  moisture/productivity context, not as vegetation.

### 7.5 Phase 4: Count Models

Purpose:

- Evaluate count-distribution models without overfitting 142 rows.

Do not use unregularized country fixed effects with many covariates.

Required model ladder:

- Empirical Poisson rate baseline.
- Empirical negative-binomial rate baseline.
- Hierarchical shrinkage rate baseline.
- Penalized Poisson or negative-binomial GLM with population offset.
- Optional hierarchical/mixed count model if implementation is stable.

Preferred implementation:

- Python penalized GLM where feasible.
- R `glmnet`, `glmmTMB`, `brms`, or `rstanarm` only if the environment and
  reproducibility package can support it.

Required specifications:

- Offset: log population.
- Candidate predictors come only from the selected feature set.
- Regularization path: pre-specified lambda grid.
- Hyperparameter selection: validation 2022 or leave-one-year-out CV, never
  2023 test.
- Coefficients are not interpreted causally.
- If overdispersion or convergence fails, report instability and fall back to
  empirical negative-binomial baseline.

### 7.6 Phase 5: COVID-19 And Surveillance Sensitivity

Rationale:

- ECDC reported low totals in 2020 and 2023.
- 2020-2021 public health systems may reflect pandemic-period reporting
  disruption.
- Belgium 2023 changed surveillance.

Required sensitivity analyses:

- Add `pandemic_period` indicator for 2020-2021.
- Run primary metrics with and without 2020-2021 in model training where the
  sample size permits.
- Run analysis excluding Belgium 2023 and any non-comprehensive rows.
- Report whether conclusions change.

### 7.7 Phase 6: Power And Detectability Analysis

Purpose:

- Prevent reviewers from over-reading null covariate results.

Implementation:

- Simulate country-year count panels with the observed country/year structure.
- Use observed population offsets and baseline rates.
- Inject covariate effects of increasing magnitude.
- Run the planned feature-ablation pipeline.
- Estimate the minimum effect size detectable with acceptable false-positive
  and false-negative behavior.

Interpretation:

- If the panel has low power, say so.
- Use this to frame negative results as "not detectable at this scale" rather
  than "climate does not matter."

### 7.8 Phase 7: Simulation

Current simulation:

- Markov-style incidence-state simulation exists as a sparse surveillance
  stress test.

V1 rule:

- Keep simulation in appendix only.
- Do not use simulation as validation evidence.
- Do not add human-to-human spread simulation for ECDC v1.

Optional upgraded simulation:

- State space: zero, low, medium, high reported-incidence state per country.
- Transition probabilities estimated from observed historical states with
  smoothing.
- Climate-anomaly scenario only if clearly defined as a stress test.
- Anomaly baseline: historical TerraClimate distribution over available years,
  with one-standard-deviation shifts documented.
- Validation: compare simulated state frequencies with observed frequencies.

If the simulation is too thin:

- Remove it from the main text.
- Mention as appendix or future work only.

### 7.9 Phase 8: Figures And Tables

Tables:

- Table 1: Data sources, licenses, time coverage, access dates, variables.
- Table 2: ECDC country-year summary, including UK/Brexit, Belgium 2023,
  Cyprus 2023, and source-quality flags.
- Table 3: Feature families, feature counts, missingness, imputation rules.
- Table 4: Baseline and model metrics by target year.
- Table 5: Feature ablation results with WIS, relative WIS, coverage, interval
  width, MAE, Brier, and MASE.
- Table 6: Sensitivity analyses: Belgium exclusion, pandemic-period handling,
  leave-one-year-out CV.
- Supplementary table: Full data dictionary and checksums.

Figures:

- Figure 1: Study design diagram.
- Figure 2: EU/EEA incidence choropleth, 2023 or multi-panel by year.
- Figure 3: Surveillance completeness/data-gap map.
- Figure 4: Covariate coverage and missingness.
- Figure 5: Forecast skill comparison with WIS and relative WIS.
- Figure 6: Calibration and interval width.
- Figure 7: Observed versus predicted incidence map with uncertainty layer.
- Supplementary figure: Markov stress-test output, if retained.

Figure QA:

- Use a projection appropriate for Europe; document projection.
- Use Natural Earth boundaries.
- No misleading within-country precision.
- Colorblind-safe palette.
- Greyscale legibility.
- 300 dpi minimum.
- Width target: 180-190 mm for full-width figures unless journal instructions
  specify otherwise.

### 7.10 Phase 9: Manuscript

Target length:

- Abstract: 250 words.
- Introduction: 800 words.
- Methods: 2000 words.
- Results: 1500 words.
- Discussion: 1200 words.
- Limitations: 500 words.
- Data/code/ethics statements: 300 words.
- Total target: 6000-6500 words.

Required abstract details:

- Exact time span: 2019-2023.
- Exact unit: EU/EEA country-year.
- Exact row count after final freeze.
- Primary source: ECDC Annual Epidemiological Report.
- Main metric: WIS and coverage.
- Honest conclusion: whether public covariates improved or not.

Required manuscript sections:

- Background.
- Related work and novelty.
- Data sources and licenses.
- Surveillance metadata and source-quality flags.
- Covariate construction.
- Benchmark task.
- Model specifications.
- Evaluation metrics.
- Results.
- Sensitivity analyses.
- Limitations.
- Data and code availability.
- Ethics statement.

Ethics statement:

> This study uses aggregated, publicly available surveillance data at the
> country-year level. No individual-level patient data were accessed. Ethical
> review was not required for secondary analysis of publicly available
> aggregate data under the applicable institutional policy.

Author contributions:

- Use CRediT taxonomy.

Preprint policy:

- Decide before journal submission whether to post on medRxiv, bioRxiv, or
  arXiv.
- Confirm the selected journal allows the chosen preprint server.

### 7.11 Phase 10: Reproducibility Package

Required tracked files:

- Source code in `src/`.
- CLI scripts in `tools/`.
- Tests in `tests/`.
- Schemas in `schemas/`.
- Configs in `configs/`.
- `README.md`.
- `LICENSE` for code, preferably MIT or Apache 2.0.
- `CITATION.cff`.
- `docs/data_dictionary.md`.
- `docs/reproducibility_manifest.md`.
- `docs/reviewer_response_playbook.md`.

Data deposition:

- Small processed tables can be included in a Zenodo/OSF release if licenses
  permit.
- Large raw downloads are documented with source URLs, access dates, and
  checksums.
- Final release gets a DOI.
- GitHub release tag matches manuscript version.

Repository rule:

- Generated `data/`, `reports/`, `figures/`, and credential files remain
  ignored unless a deliberate publication snapshot is being created.

## 8. Blocker Register And Responses

| Blocker | Risk | Response |
| --- | --- | --- |
| Only five years of ECDC data | High risk for weak models | Frame as sparse public surveillance benchmark; use simple baselines, uncertainty, and power analysis |
| 142 rows and many candidate features | Overfitting | Cap modeling features, VIF/correlation screening, penalized models |
| Belgium 2023 not comprehensive | Bias | Flag as `quality_grade = C`; sensitivity excluding Belgium 2023 |
| UK withdrawal after 2020 | Structural break | Exclude UK from primary panel or flag withdrawn if added |
| Cyprus/other metadata caveats | Bias | Flag and sensitivity analysis |
| COVID-19 period | Reporting disruption | Pandemic-period indicator and exclusion sensitivity |
| Climate/land-use effects not detectable | Reviewer skepticism | Power analysis and negative-result framing |
| TerraClimate endpoint migration | Reproducibility | Verify endpoint before data freeze; record checksums; fallback mirror documented |
| FAO attribution | Licensing | Add FAOSTAT attribution |
| MODIS QA complexity | Bad vegetation claims | Hard decision gate; remove vegetation claims if not passed |
| Earthdata credentials fail | MODIS blocked | Stop and tell user exactly how to create/refresh Earthdata credentials; proceed without MODIS if not essential |
| PAHO alerts are event-based | Label incompatibility | Defer to post-submission; use only as external stress test |
| China data uses PLAD/county/HFRS | Scale and syndrome incompatibility | Defer; never pool with ECDC coefficients |
| HantavirusMap already exists | Novelty challenge | Differentiate live signal tracker versus reproducible benchmark |
| Zeimes et al. already mapped Europe | Novelty challenge | Differentiate spatial risk mapping versus temporal probabilistic benchmark |
| Reviewer asks for county-level data | Granularity challenge | Cite CDC privacy restriction; explain public-data country-year scope |
| Model coverage poor | Rejection risk | Report calibration honestly; do not promote miscalibrated models |
| Impact factor target | Journal fit | Primary IJHG; fallbacks Scientific Data and BMC Public Health |

## 9. Reviewer Response Playbook

Likely question: What does this add beyond ECDC annual reports?

Response:

- ECDC reports authoritative totals; this paper provides a reproducible
  benchmark linking those totals to public covariates and evaluating
  probabilistic one-year-ahead predictions against transparent baselines.

Likely question: How is this different from Zeimes et al. 2015?

Response:

- Zeimes et al. modeled spatial distribution/risk in Europe. This paper
  provides a temporal country-year reported-incidence benchmark with frozen
  public labels, uncertainty metrics, feature ablation, and reproducible
  source joins.

Likely question: Why country-year and not district/county?

Response:

- Publicly available cross-national human surveillance data are sparse and
  privacy-limited. CDC explicitly withholds county-level U.S. data; ECDC
  harmonized annual reports are country-level for this use case. The paper
  benchmarks exactly what public data can support.

Likely question: Why are complex models weak?

Response:

- Sparse surveillance, short time span, reporting heterogeneity, and
  country-level aggregation make simple baselines difficult to beat. That is
  a useful result because it redirects attention toward surveillance quality
  and transparent uncertainty rather than opaque models.

Likely question: Why not include PAHO or China?

Response:

- PAHO alerts and China CDC HFRS analyses differ in syndrome, source system,
  geography, and reporting scale. Pooling them would create a false sense of
  comparability. They are reserved for source-system-specific follow-up.

Likely question: Is this forecast or retrospective validation?

Response:

- This is retrospective one-year-ahead evaluation. The word "prospective" is
  avoided unless future predictions are issued before labels are released.

## 10. Exact Next Tasks

1. Rebuild ECDC case table with the new source-quality metadata columns.
2. Run strict validation.
3. Rebuild the processed country-year table.
4. Rerun baselines so metrics include relative WIS and interval width.
5. Regenerate reports and publication readiness gate.
6. Add `docs/data_dictionary.md` and `docs/reproducibility_manifest.md` if not
   already present.
7. Implement feature ablation with nested feature sets and train-only
   imputation.
8. Add MASE and calibration plotting if not already implemented.
9. Decide MODIS by the Week 2 gate.
10. Implement choropleth/data-gap/prediction maps for IJHG.
11. Add power analysis.
12. Draft manuscript and reviewer response playbook.
13. Create Zenodo/OSF archive and DOI.
14. Run final pre-submission QA.

## 11. QA Gates

Required local commands:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-12
python tools/validate_international_cases.py --strict
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/plot_international_baselines.py
python tools/run_markov_simulation.py
python tools/write_paper_readiness_report.py
python tools/check_publication_readiness.py
python -m pytest
python -m ruff check src tests tools
git diff --check
```

Manual QA checklist:

- ECDC totals equal 4088, 1693, 4947, 2185, 1885.
- Belgium 2023 is flagged not comprehensive.
- UK/Brexit handling is explicit.
- TerraClimate lag-1 missingness is reported per variable.
- Baseline metrics include WIS, relative WIS, coverage, interval width, MAE,
  Brier score, and later MASE.
- Any under-coverage is discussed.
- MODIS is either implemented with QA or removed from claims.
- PLOS NTD is not presented as an ECDC-only target.
- HantavirusMap is acknowledged as a tracker competitor and differentiated.
- Zeimes/Kallio/Reusken/Kazasidis/Glass/Allen/Forecast Hub literature is
  cited.
- Source licenses and attribution are documented.
- Ethics statement is present.
- No credentials or API keys are committed.

## 12. Submission Package Checklist

Before submission:

- Manuscript PDF/DOCX.
- Cover letter tailored to IJHG.
- Title page.
- Abstract with exact row count and time span.
- Figures at journal resolution.
- Supplementary tables.
- Reproducibility archive DOI.
- GitHub release tag.
- Data availability statement.
- Code availability statement.
- Ethics statement.
- Funding statement.
- Competing interests statement.
- CRediT author contribution statement.
- Reviewer response playbook.
- Preprint decision documented.

## 13. Bottom Line

This project is publishable if it stops trying to be larger than the public
data support. The strongest paper is not a dramatic outbreak predictor. It is
an audited benchmark showing, with maps and calibrated uncertainty, what free
public surveillance plus public environmental covariates can and cannot do for
EU/EEA hantavirus reported incidence.

The novelty is defensible:

- not another live map;
- not another static ecological suitability map;
- not an overfit deep-learning demo;
- an open, source-audited, uncertainty-calibrated benchmark with strong
  baselines and negative results retained.

The acceptance strategy is:

1. Target International Journal of Health Geographics first.
2. Prepare Scientific Data as the strongest fallback if model skill is weak
   but the reproducible dataset and benchmark are clean.
3. Use BMC Public Health as a practical fallback if the surveillance and
   public-health-informatics framing is stronger than the geospatial methods.
4. Defer PLOS NTD, PAHO, China, and global claims until a separate
   source-system-stratified expansion exists.
