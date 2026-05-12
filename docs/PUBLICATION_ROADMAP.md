# Publication Roadmap

Authoritative update: `PUBLICATION_MASTER_PLAN.md` at repo root supersedes this
older roadmap for journal targeting, feature-ablation specifications, MODIS
decision gates, and final QA.

Goal: build a credible hantavirus surveillance, reservoir, and spillover-risk predictor that can survive peer review.

## 2026-05-12 Strategy Update

The strongest publication path is no longer U.S.-only. The primary manuscript should be an international country-year reported-incidence benchmark, with syndrome, region, and surveillance system modeled explicitly. The U.S./NEON reservoir track remains valuable as mechanistic support and as a fallback manuscript.

See `docs/INTERNATIONAL_PUBLICATION_AND_MARKETING_PLAN.md` for the detailed international plan, source matrix, QA gates, and marketing strategy.

Recommended target journals, in order:

1. PLOS Neglected Tropical Diseases - good fit if the public-health, neglected zoonotic, and One Health framing dominates.
2. Emerging Infectious Diseases - good fit if surveillance utility and reemerging infectious disease framing dominate.
3. International Journal of Health Geographics - good fit if the remote-sensing and geospatial benchmark is the main contribution.
4. PLOS Computational Biology or PLOS Digital Health - best only if the methods contribution is strong beyond hantavirus.
5. The Lancet Planetary Health or Nature Communications - only if the final work has strong climate-health evidence and partner validation.

## Publication Claim

Primary claim:

> We provide an open, uncertainty-calibrated country-year forecasting benchmark for reported hantavirus incidence, stratified by syndrome, region, and surveillance system, and benchmarked against strong statistical baselines under temporal and leave-country-out validation.

Secondary claim:

> U.S./NEON rodent serology supports the biological plausibility of climate and vegetation covariates, but it is not used to claim local human case prediction.

Blocked claims until new data exist:

- County-level human case prediction.
- Real-time operational warning system.
- Validated prospective outbreak forecast.
- Clinical diagnosis or individual risk prediction.
- Pooled global "hantavirus" prediction without syndrome and surveillance-system strata.

## Phase 0: Governance and Scope

Deliverables:

- Scope statement: international country-year reported-incidence benchmark first; U.S./NEON reservoir-risk model second.
- Ethics memo: whether IRB review is required for any human case data or risk maps.
- Data-use register: public data, restricted data, licenses, citation requirements.
- Pre-analysis plan: primary outcomes, splits, metrics, and go/no-go gates.

Implementation specs:

- Store scope in `docs/study_protocol.md`.
- Store data licenses in `metadata/data_license_register.csv`.
- Do not ingest restricted human data before permission and publication rights are documented.

QA gates:

- Every target outcome has a data source.
- Every human-data source has permission and privacy notes.
- Claims match available data resolution.

## Phase 1A: International Country-Level Data Acquisition

Primary tables:

- `data/manual/international_country_cases.csv`
- `metadata/international_case_source_matrix.csv`
- World Bank country-year population and context indicators
- TerraClimate country-year climate features
- MODIS MOD13C2 country-year NDVI/EVI features
- FAOSTAT country-year land-use features

Implementation specs:

- Use `schemas/international_country_cases.schema.yaml`.
- Run `python tools/validate_international_cases.py --strict`.
- Start with ECDC EU/EEA as the primary harmonized anchor.
- Add PAHO Americas HPS/HCPS as a separate syndrome/region stratum only after provenance is complete.
- Add China HFRS as external validation or sensitivity analysis, not as a blindly pooled source.
- Build `data/processed/international_country_year.parquet`.
- Include columns:
  - `iso3`
  - `country`
  - `region`
  - `syndrome`
  - `source_system`
  - `year`
  - `cases`
  - `deaths`
  - `population`
  - `incidence_per_100k`
  - `quality_grade`
  - climate lag features
  - vegetation lag features
  - land-use covariates
  - reporting-context covariates

QA gates:

- Source totals reconcile to official reports.
- Duplicate country-year-syndrome-source keys rejected.
- Population denominators present for every primary target row.
- HFRS and HPS/HCPS never pooled without explicit strata.
- Quality-grade D rows excluded from primary model.
- Generated `reports/01_international_data_audit.md`.

## Phase 1B: U.S./NEON Data Acquisition and Audit

Primary tables:

- NEON `DP1.10064.001` `rpt_bloodtesting`
- NEON `DP1.10072.001` `mam_pertrapnight`
- NEON `DP1.10072.001` `mam_perplotnight`
- Daymet weather by site/date
- MODIS/VIIRS vegetation and LST summaries by site buffer/date
- NLCD land-cover summaries by site/county/year
- CDC/NNDSS state-level cases

Implementation specs:

- Create `src/hantavirus_predictor/ingest/neon.py`.
- Download raw files to `data/raw/neon/...`.
- Write checksums and source URLs to `metadata/raw_file_manifest.csv`.
- Build `data/interim/site_month_reservoir.parquet`.
- Include columns:
  - `site_id`
  - `year_month`
  - `domain_id`
  - `latitude`
  - `longitude`
  - `taxon_id`
  - `trap_nights`
  - `unique_individuals`
  - `blood_tested`
  - `blood_positive`
  - `blood_negative`
  - `blood_indeterminate`
  - `seroprevalence`
  - `sampling_impractical_flag`

QA gates:

- Duplicate keys report.
- Join loss report from serology to trapping tables.
- Missingness report by site-month and species.
- Sampling effort denominator validated.
- Generated `reports/01_data_audit.md`.

## Phase 2: Feature Engineering

Feature families:

- Weather lags: precipitation, temperature, vapor pressure, snow, shortwave radiation.
- Vegetation lags: NDVI/EVI level, anomaly, seasonal percentile, quality-weighted gap indicators.
- Habitat: NLCD class proportions around NEON sites and counties.
- Reservoir ecology: species, trap effort, prior trap success, prior seroprevalence.
- Climate regime: ONI/RONI/ENSO phase as sensitivity covariate.
- Human exposure for descriptive spillover only: population, rurality, SVI/ACS features.

Implementation specs:

- Create lag windows: 0, 1, 2, 3, 6, 9, 12 months.
- Pre-register lag search. Do not tune lags on the test set.
- Store feature build config in `configs/features.yaml`.
- Build `data/processed/model_matrix_reservoir.parquet`.

QA gates:

- No feature timestamp later than target timestamp.
- Lag features reproduce from raw sources.
- Unit tests for date alignment and leakage checks.

## Phase 3: Baselines

Required baselines:

1. Historical climatology by site/species/month.
2. SARIMAX or dynamic regression with exogenous weather/vegetation.
3. Binomial or beta-binomial GLMM/GAM with effort denominators.
4. Gradient boosting on lagged tabular features.
5. Null human spillover model using state historical rates only.

Implementation specs:

- Create `src/hantavirus_predictor/models/baselines.py`.
- Every model must output quantiles, not just point predictions.
- Store predictions in a Forecast Hub-like table:
  - `forecast_date`
  - `target`
  - `horizon`
  - `location`
  - `model`
  - `quantile`
  - `value`

QA gates:

- Baseline predictions generated for all validation folds.
- WIS and coverage calculated using tested shared metrics.
- Results saved to `reports/02_baselines.md`.

## Phase 4: Mechanistic and Advanced Models

Order:

1. Hierarchical reservoir state-space model.
2. Mechanistic climate-to-carrying-capacity model.
3. PINN only if the mechanistic model is stable and baselines leave room.
4. TimesFM/Chronos only as time-series priors or benchmarks.
5. Graph neural network only if edges are defensible without private mobility data.

Implementation specs:

- Keep each advanced model behind a config flag.
- Require ablation against the same model without the advanced component.
- Track parameter count, compute time, seed sensitivity, and calibration.

QA gates:

- Complex model must improve mean WIS by at least 10 percent over best baseline, or be excluded from main results.
- Empirical 90 percent coverage must remain between 85 and 95 percent overall.
- No biome/domain subgroup below 80 percent coverage without explicit caveat.
- Five random seeds for any neural result used in the manuscript.

## Phase 5: Validation

Primary split:

- Temporal rolling origin over NEON serology years.

Secondary split:

- Leave-site-out and leave-NEON-domain-out.

Human external validation:

- State/year CDC/NNDSS cases only unless restricted county data are provided.
- Evaluate rank correlation, calibration by broad risk tier, and descriptive alignment.
- Do not score county-month human forecasts without county-month labels.

Metrics:

- WIS for quantile forecasts.
- MAE/RMSE for point forecasts.
- Empirical coverage and interval width.
- PR-AUC/Brier only for pre-registered outbreak/risk thresholds.
- Calibration plots and PIT-style diagnostics where applicable.

QA gates:

- Validation report generated at `reports/03_validation.md`.
- All metrics stratified by horizon, region/domain, and species where sample size allows.
- Negative results included.

## Phase 6: Manuscript and Reproducibility

Main figures:

1. Data map and availability timeline.
2. NEON serology/trapping audit.
3. Model and validation design diagram.
4. Baseline versus final model forecast skill by horizon.
5. Calibration and interval coverage.
6. Spatial/domain generalization results.
7. Feature effects or interpretable ecological associations.
8. Human spillover context, clearly labeled as state-level/descriptive unless partner data exist.

Manuscript sections:

- Introduction: public-health need and data scarcity.
- Methods: data, feature construction, baselines, final model, validation, uncertainty.
- Results: data audit, forecast skill, calibration, ablations, limitations.
- Discussion: what can and cannot be predicted from public data.
- Ethics and data availability: privacy, risk-map limitations, code/data release.

Reproducibility specs:

- Commit code and configs.
- Publish data manifests and derived non-sensitive features when licenses allow.
- Archive model predictions and metrics.
- Mint Zenodo DOI after acceptance or preprint.

## Phase 7: Submission Path

Before preprint:

- Run full tests.
- Rebuild all tables from raw data.
- Freeze dependency lock file.
- Run independent agent/code review.
- Confirm all source citations and data licenses.

Before journal submission:

- Add structured limitations table.
- Add ethics statement.
- Add data/code availability statement.
- Include reviewer-response playbook:
  - Data scarcity.
  - Public county data unavailable.
  - Deep learning not used unless justified.
  - Synthetic data limited to priors/tests.
  - Human predictions scoped to validation resolution.

## Practical Timeline

Minimum credible timeline:

- Weeks 1-2: data audit and feature matrix.
- Weeks 3-4: baselines and validation framework.
- Weeks 5-6: mechanistic model and uncertainty calibration.
- Weeks 7-8: optional advanced models and ablations.
- Weeks 9-10: manuscript figures and reproducibility package.
- Weeks 11-12: internal review, preprint, journal submission.

This is aggressive. If restricted human data or IRB review are needed, add 1-3 months.
