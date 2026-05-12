# International Publication and Marketing Plan

## Direct Answer

The repository was U.S.-first, not truly international. The stronger publication path is now:

1. Make international country-year reported human hantavirus incidence the primary study.
2. Keep U.S./NEON rodent serology as mechanistic support and a fallback manuscript.
3. Keep U.S. county-level human prediction blocked until restricted partner data exist.

This is a better publication strategy because country-level international surveillance avoids the U.S. county privacy blocker, increases the number of observed cases, and aligns better with global-health and climate-health framing. It only works if the model does not pretend all hantaviruses are one clean disease process. HFRS in Europe/Asia and HPS/HCPS in the Americas must be explicit syndrome strata, with region and surveillance system tracked in every row.

## Evidence From Current Research

Authoritative sources found in the 2026-05-12 research pass:

- ECDC's 2023 annual epidemiological report is a harmonized EU/EEA anchor. It says 28 EU/EEA countries reported 1,885 hantavirus infection cases for 2023, with data retrieved from TESSy on 2024-11-06: https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
- PAHO/WHO's 2025 epidemiological alert provides recent Americas HPS context. It reports eight countries in the Americas with confirmed HPS cases as of epidemiological week 47 of 2025: https://www.paho.org/sites/default/files/2025-12/2025-12-19-epidemiological-alert-hantavirus-engfinal.pdf
- China CDC Weekly provides a large HFRS external-validation signal, including reported HFRS cases in China from 2014 to 2023 and national rodent surveillance context: https://weekly.chinacdc.cn/en/article/doi/10.46234/ccdcw2025.141
- TerraClimate provides monthly global climate and water-balance covariates at high spatial resolution from 1950 to present: https://www.climatologylab.org/terraclimate.html
- MODIS MOD13C2 provides monthly global NDVI/EVI from 2000-02-01 to present: https://lpdaac.usgs.gov/products/mod13c2v061/
- World Bank Indicators API provides programmatic country-year indicators, including population denominators: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation

## Recommended Manuscript

Working title:

> Climate, vegetation, and surveillance determinants of country-level hantavirus incidence: an open international forecasting benchmark

Primary claim:

> We provide an open, uncertainty-calibrated country-year forecasting benchmark for reported hantavirus incidence, stratified by syndrome, region, and surveillance system, and tested against strong statistical baselines under temporal and leave-country-out validation.

Secondary claim:

> U.S./NEON rodent serology supports the biological plausibility of climate and vegetation covariates, but it is not used to claim local human case prediction.

Claims to avoid:

- "Global outbreak predictor."
- "County-level human risk map" unless partner data are obtained.
- "Real-time early warning system" before prospective logging.
- "Hantavirus incidence" without saying "reported incidence."
- "Single global hantavirus model" unless syndrome/source-system interactions are included.

## Exact Study Scope

### Primary Dataset

Country-year human reported cases.

Required row grain:

- one country
- one year
- one syndrome
- one pathogen or virus label where available
- one reporting system
- one source

Required file:

- `data/manual/international_country_cases.csv`

Required schema:

- `schemas/international_country_cases.schema.yaml`

Required validation command:

```powershell
python tools/validate_international_cases.py --strict
```

Required columns:

- `iso3`
- `country`
- `region`
- `syndrome`
- `pathogen_or_virus`
- `case_definition`
- `reporting_system`
- `year`
- `cases`
- `deaths`
- `population`
- `source_url`
- `source_title`
- `accessed_date`
- `source_type`
- `quality_grade`
- `notes`

Allowed syndromes:

- `HFRS`
- `HPS`
- `HCPS`
- `hantavirus_infection`
- `mixed_or_unspecified`

Quality grades:

- `A`: machine-readable official surveillance with stable definitions.
- `B`: official report or alert manually extracted with clear provenance.
- `C`: peer-reviewed or ministry summary with partial definition gaps.
- `D`: context only; exclude from the primary model.

### Data Tiers

Tier 1, primary anchor:

- ECDC EU/EEA country-year hantavirus infection/HFRS records.
- Best for the main paper because the surveillance source is harmonized and citable.
- Use as the first reproducible model because it offers the cleanest starting definition.

Tier 2, international extension:

- PAHO/WHO and national-ministry HPS/HCPS records in the Americas.
- Use as a separate syndrome/region stratum.
- Do not force direct comparability with EU/EEA HFRS.

Tier 3, external validation and sensitivity:

- China CDC Weekly and other official Asia HFRS summaries.
- Use as large-signal external validation, not as a pooled equal-weight source.
- Model `source_system` as a stratification or random-effect term.

Tier 4, context only:

- WHO Disease Outbreak News and isolated outbreak reports.
- Use for discussion, recent-event QA, and prospecting new sources.
- Do not use as a complete denominator-based time series.

## Covariate Specification

### Climate

Primary source:

- TerraClimate monthly climate and water-balance variables.

Country-year features:

- annual mean temperature
- annual minimum and maximum temperature summaries
- annual precipitation
- precipitation anomaly relative to 1991-2020 or source-supported climatology
- vapor pressure deficit
- soil moisture
- climate water deficit
- lagged features at 0, 1, 2, and 3 years
- seasonal windows where supported by ecology: winter, spring, summer, fall

QA:

- use only covariates available before or during the target year according to the pre-analysis plan
- document whether target-year covariates are explanatory nowcasts or true forecasts
- keep all lag choices pre-registered

### Vegetation

Primary source:

- MODIS/Terra MOD13C2 monthly NDVI/EVI.

Country-year features:

- annual NDVI mean
- annual EVI mean
- seasonal NDVI/EVI peaks
- anomaly from country-specific baseline
- lagged vegetation anomaly at 0, 1, 2, and 3 years

QA:

- store product DOI and access date
- apply quality flags where gridded extracts are used
- document aggregation method and country boundary version

### Demography and Reporting Context

Primary source:

- World Bank Indicators API.

Required:

- total population
- rural population percentage
- GDP per capita or similar reporting-capacity proxy

Optional:

- health expenditure
- physicians per capita
- urbanization
- agricultural employment

QA:

- population denominator must match country-year target rows
- do not treat reporting-capacity proxies as causal unless the design supports it

### Land Use

Primary source:

- FAOSTAT land-use and land-cover statistics.

Features:

- cropland area or share
- forest area or share
- agricultural land area or share
- pasture/grassland where available

QA:

- cite domain and item codes
- align by country-year and ISO3
- use missingness flags for incomplete countries

## Model Specification

### Outcome

Primary outcome:

- reported cases by country-year-syndrome-source-system.

Primary rate:

- cases per 100,000 population, modeled with a population offset when using count models.

Optional secondary outcomes:

- reported deaths
- case fatality rate
- outbreak-year indicator, pre-registered as cases above a country-specific percentile

### Baselines Required Before Any Complex Model

1. Historical country mean rate by syndrome.
2. Last-observed country rate.
3. Region-syndrome historical mean rate.
4. Negative-binomial GLM with population offset.
5. Hierarchical negative-binomial model with country, region, syndrome, and source-system effects.
6. Gradient boosting with lagged climate, vegetation, land-use, and reporting-context features.

### Main Model

Recommended main model:

- hierarchical negative-binomial panel model
- population offset
- country random effects
- region random effects
- syndrome fixed effects
- source-system fixed or random effects
- climate/vegetation lags as pre-registered covariates
- optional interaction terms: syndrome x climate, region x vegetation, source_system x year

Why this first:

- reviewers will trust it more than deep learning on sparse disease counts
- it handles overdispersed counts
- it makes surveillance heterogeneity visible
- it produces interpretable estimates and uncertainty

### Machine Learning Benchmark

Use gradient boosting only as a benchmark unless it clearly improves calibration and held-out performance.

Requirements:

- no target leakage
- nested feature selection inside training folds
- quantile or distributional outputs, not point predictions only
- SHAP or permutation importance only as descriptive interpretation, not causal proof

### Advanced Models

Advanced models are optional and must be demoted if they do not beat baselines:

- spatiotemporal graph model only if graph edges are transparent and defensible
- TimesFM/Chronos only as a benchmark or prior
- PINN only for a separate mechanistic appendix after the statistical benchmark works

Promotion gate:

- at least 10 percent mean WIS improvement over the best baseline
- empirical 90 percent interval coverage between 85 and 95 percent overall
- no major region or syndrome stratum below 80 percent coverage without explicit caveat
- improvement must persist in temporal and leave-country-out validation

## Validation Specification

Primary split:

- train on earlier years
- validate on middle years
- test on the most recent complete years

Minimum fold design:

- rolling-origin temporal validation
- leave-country-out validation
- leave-region-out sensitivity
- source-system holdout if enough sources exist

Metrics:

- weighted interval score
- log score or negative-binomial deviance
- empirical coverage
- interval width
- MAE/RMSE for point estimates
- Brier score only for pre-registered outbreak thresholds

Stratification:

- syndrome
- region
- source system
- population size band
- high versus low reporting-capacity proxy

Leakage checks:

- all covariates timestamped
- no target-year future information in true forecasting experiments
- feature selection performed inside folds
- country-year duplicate keys rejected by validator

## Implementation Work Packages

### Package 1: Data Registry

Status:

- started in `configs/data_catalog.yaml`
- started in `src/hantavirus_predictor/data_sources.py`
- started in `metadata/international_case_source_matrix.csv`

Specs:

- add every source before extracting data
- record access mode, spatial unit, temporal unit, and QA notes
- update `metadata/data_license_register.csv` before committing source-derived outputs

Done when:

- each row in the case table can be traced to a source URL or partner data agreement

### Package 2: Manual Case Table

Status:

- schema created in `schemas/international_country_cases.schema.yaml`
- validator created in `tools/validate_international_cases.py`

Specs:

- create `data/manual/international_country_cases.csv`
- begin with ECDC EU/EEA rows
- add PAHO rows only with `syndrome=HPS` or `HCPS`
- add China rows as `HFRS` with separate reporting system
- exclude quality-grade D rows from primary model

Done when:

- `python tools/validate_international_cases.py --strict` passes
- source totals reconcile with source documents
- missingness table is written to `reports/01_international_data_audit.md`

### Package 3: Country-Year Covariates

Planned files:

- `src/hantavirus_predictor/ingest/world_bank.py`
- `src/hantavirus_predictor/ingest/terraclimate.py`
- `src/hantavirus_predictor/ingest/modis_global.py`
- `src/hantavirus_predictor/ingest/faostat.py`
- `src/hantavirus_predictor/features/country_year.py`

Processed output:

- `data/processed/international_country_year.parquet`

Required keys:

- `iso3`
- `year`
- `syndrome`
- `source_system`

Done when:

- every primary target row has a population denominator
- climate and vegetation lag fields are non-leaky
- missing covariates have explicit missingness flags

### Package 4: Baselines

Planned file:

- `src/hantavirus_predictor/models/international_baselines.py`

Required prediction table:

- `forecast_date`
- `target`
- `horizon`
- `location`
- `iso3`
- `syndrome`
- `source_system`
- `model`
- `quantile`
- `value`

Done when:

- all baselines run on every validation fold
- WIS and coverage are computed by the shared metrics module
- `reports/02_international_baselines.md` exists

### Package 5: Main Model

Planned file:

- `src/hantavirus_predictor/models/international_hierarchical.py`

Minimum parameters to report:

- country effect variance
- region effect variance
- syndrome effects
- source-system effects
- climate lag coefficients
- vegetation lag coefficients
- overdispersion

Done when:

- posterior or bootstrap intervals are available
- calibration is reported by syndrome and region
- effect plots use uncertainty intervals

### Package 6: Manuscript Figures

Required figures:

1. Data availability map and timeline.
2. Source-system and syndrome schematic.
3. International validation design.
4. Baseline versus final model skill.
5. Calibration and empirical coverage.
6. Country-level risk/rate trajectories with uncertainty.
7. Climate and vegetation effect summaries.
8. NEON mechanistic support panel or appendix figure.

Done when:

- every figure can be rebuilt from scripts
- captions name data limitations
- maps avoid unsupported fine-scale claims

### Package 7: Reproducibility

Required before preprint:

- tests passing
- raw data manifests
- source extraction notes
- dependency lock
- model configs frozen
- derived non-sensitive tables archived when licenses allow
- code and manuscript build instructions

Done when:

- a clean clone can rebuild processed data from documented raw/manual inputs

## Blocker Response

| Blocker | International response |
|---|---|
| U.S. county-level public human data unavailable | Pivot primary human model to country-year international surveillance; keep U.S. county models blocked until partner data. |
| NEON serology ends in 2019 | Use NEON as mechanistic/reservoir support, not as the main human publication label. |
| Sparse human cases in the U.S. | International country-level data increases event counts and makes public data more feasible. |
| Different hantavirus syndromes | Make syndrome a required field and model stratum. |
| Different surveillance systems | Make `reporting_system` and `source_system` required fields; include source effects. |
| Underreporting | Model reported incidence, include reporting-capacity covariates, and state underreporting as a limitation. |
| Deep learning overkill | Put hierarchical count models and reviewer baselines first. |
| Synthetic-data overclaim | Use synthetic data only for code tests or priors, never as validation evidence. |
| Risk-map stigma | Publish country-level uncertainty and avoid local rankings without partner review. |
| Publication novelty concern | Sell the open benchmark, reproducible data audit, cross-region comparison, and uncertainty calibration. |

## Journal Strategy

Best first targets:

1. PLOS Neglected Tropical Diseases: good if the paper emphasizes zoonotic spillover, neglected populations, One Health, and policy relevance. The journal explicitly considers viral hemorrhagic fevers and One Health approaches, but asks authors to justify NTD relevance.
2. Emerging Infectious Diseases: good if the paper emphasizes surveillance, public-health utility, and emergence. EID says it focuses on new and reemerging infectious diseases around the world and asks manuscripts to explain public-health meaning.
3. International Journal of Health Geographics: good if the geospatial, remote-sensing, and spatiotemporal modeling contribution is the center.
4. PLOS Computational Biology or PLOS Digital Health: only if the modeling contribution is genuinely novel and reproducible beyond hantavirus.
5. Nature Communications or The Lancet Planetary Health: only after strong validation and a clear climate-health result.

Cover-letter angle:

- "This is the first open, syndrome-stratified international benchmark for country-level reported hantavirus incidence forecasting using harmonized surveillance provenance, global climate data, and uncertainty-calibrated validation."

Reviewer-resistance angle:

- "We intentionally start with count models and strong baselines rather than claiming deep-learning superiority on sparse surveillance data."

## Marketing Strategy

### Positioning

Use this short positioning statement:

> Hantavirus Predictor is an open research benchmark for country-level hantavirus risk, designed to make sparse zoonotic surveillance data usable, auditable, and uncertainty-aware.

Do not market it as:

- an outbreak oracle
- a clinical tool
- a public county risk dashboard
- a finished public-health warning system

### Names

Repository name can stay `hantavirus_predictor` for GitHub search. Public-facing project title options:

- HantaRisk Atlas
- HantaCast
- Open Hantavirus Risk Benchmark

Recommended title for publication and credibility:

- Open Hantavirus Risk Benchmark

Reason:

- "benchmark" signals rigor and avoids overclaiming operational prediction.
- "open" helps with citations, collaborators, and funders.
- "risk" is broader and safer than "outbreak forecast."

### Audiences

Primary scientific audience:

- infectious-disease modelers
- zoonotic disease ecologists
- One Health researchers
- climate-health researchers

Primary practical audience:

- public-health surveillance teams
- regional health agencies
- environmental health groups
- academic labs seeking an open benchmark

Secondary audience:

- funders interested in climate-sensitive disease surveillance
- data-science collaborators
- journalists covering emerging infectious diseases, only after peer review or preprint

### Core Messages

For journals:

- "A rigorous international benchmark for sparse zoonotic surveillance."
- "Uncertainty first, not black-box maps."
- "Syndrome and surveillance heterogeneity are modeled, not ignored."

For public-health agencies:

- "A reproducible way to compare climate and vegetation signals with reported case data."
- "Designed for country-level planning and research, not individual prediction."
- "Can accept partner data later without changing the governance structure."

For GitHub and technical users:

- "Source registry, schema, validators, reproducible feature builds, and baseline models."
- "Designed so unsupported claims fail QA before they reach the manuscript."

For funders/collaborators:

- "Low-cost open infrastructure for neglected zoonotic risk modeling."
- "Clear upgrade path from public country-year data to partner-approved subnational data."

### Assets To Build

Before preprint:

- polished `README.md` with a one-paragraph project statement
- data provenance diagram
- one static global map of data availability
- methods schematic
- model-card style limitations table
- reproducible benchmark leaderboard

At preprint:

- preprint thread or short technical blog post
- two-page policy brief PDF
- GitHub release with tagged code
- Zenodo archive if derived data can be redistributed

After peer review:

- interactive dashboard only for aggregated country-level results
- recorded 5-minute project walkthrough
- outreach email to surveillance and One Health groups

### Marketing Guardrails

Every public page should include:

- "reported incidence"
- "country-level"
- "research benchmark"
- "uncertainty intervals"
- "not for clinical diagnosis or individual risk prediction"

Avoid:

- red-alert maps with no uncertainty
- country rankings without confidence intervals
- claims about causality without causal design
- local public-health advice unless copied from official sources

### Success Metrics

Scientific:

- preprint downloads
- GitHub stars/forks from epidemiology or modeling users
- citations
- journal review outcome
- independent reproduction attempt

Practical:

- number of countries/sources with complete provenance
- number of partner conversations
- number of external issues or data contributions
- successful addition of one non-U.S. validation source

## Timeline From Here To Submission

Week 1:

- finish ECDC extraction protocol
- create first `international_country_cases.csv`
- pass validator
- write `reports/01_international_data_audit.md`

Week 2:

- join World Bank population and rurality
- build country-year skeleton table
- implement duplicate, missingness, and source-total reconciliation QA

Week 3:

- aggregate TerraClimate to country-year lag features
- document boundaries and lag choices
- freeze feature config

Week 4:

- add MOD13C2 NDVI/EVI country-year summaries
- add FAOSTAT land-use covariates
- finalize primary model matrix

Week 5:

- implement historical and persistence baselines
- implement negative-binomial GLM
- generate first validation report

Week 6:

- implement hierarchical count model
- compare against baselines
- run syndrome and region stratified calibration

Week 7:

- add PAHO Americas rows if country backfills are sufficient
- decide whether Americas is primary extension or discussion-only

Week 8:

- add China HFRS external validation if extraction quality is sufficient
- run source-system sensitivity analysis

Week 9:

- write results narrative
- generate all figures
- build limitations and ethics tables

Week 10:

- independent QA review
- run clean rebuild
- freeze dependencies

Week 11:

- write preprint
- create GitHub release candidate
- prepare policy brief and project positioning

Week 12:

- submit preprint
- submit to first-choice journal
- start prospective country-year forecast log for later update paper

## Go/No-Go Criteria

Proceed to preprint only if:

- international case table validates
- source totals reconcile with official reports
- at least one region has enough country-year observations for meaningful validation
- baselines and main model both run in reproducible scripts
- final model beats or clearly complements baselines
- calibration is acceptable or limitations are explicit
- claims never exceed validated resolution

Re-scope to a data paper if:

- surveillance extraction is valuable but model skill is weak
- international comparability is worse than expected
- source definitions are too inconsistent for a pooled model

Re-scope to U.S./NEON reservoir paper if:

- international human surveillance cannot be made reproducible
- country-year data remain too sparse after QA
- journal positioning is stronger as reservoir ecology than human incidence forecasting

## Immediate Next Engineering Steps

1. Fill `data/manual/international_country_cases.csv` with ECDC country-year rows.
2. Run `python tools/validate_international_cases.py --strict`.
3. Add `src/hantavirus_predictor/ingest/world_bank.py`.
4. Build `data/processed/international_country_year.parquet`.
5. Implement international baselines before any advanced model.
6. Produce `reports/01_international_data_audit.md` and `reports/02_international_baselines.md`.
