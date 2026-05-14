# EID Publication Master Plan

Last updated: 2026-05-14

Research rechecked: 2026-05-14 against EID article types, EID style guide,
ECDC 2023 hantavirus report, German PUUV forecasting papers, Zeimes et al. 2015,
Bracher et al. 2021, and an EID forecasting-evaluation precedent.

Local audit basis:

- Repository: `hantavirus_predictor`
- Cleanup audit began with `main` ahead of `origin/main` by 2 commits and a dirty worktree.
- Current HEAD at initial audit: `20fa6acb853124d35a6b2751ff39354b5be1e288`
- Current EID archive DOI in submission files: https://doi.org/10.5281/zenodo.20150542
- Current DOI resolution check: resolves to `https://zenodo.org/records/20150542`
- Local QA rerun on 2026-05-14: editable install passed, `python -m pytest` passed,
  `python -m ruff check src tests tools` passed, `python tools/check_publication_readiness.py`
  passed, `python tools/check_eid_submission_readiness.py --strict` passed, and EID
  figures verified at 600 dpi.
- Repository organization pass: legacy ZIPs, extracted LLM packages, old Overleaf
  output, pre-EID manuscript drafts, and conflicting planning docs were moved
  off the active branch and preserved on `codex/archive-pre-eid-cleanup-20260514`.
- EID evidence package implementation: model-input Table 1, model schematic,
  surveillance-quality sensitivity, country influence, calibration localization,
  detectability screen, final QA report, and reproducibility manifest are present in
  `docs/submission_eid/`.

## 1. Verdict

The EID direction remains worth pursuing, and the current repository now has the
local evidence package needed for human portal preparation. Remaining work is
limited to final author/portal details and DOI/archive verification.

The paper should be framed as an EID Research article with this claim:

> In public EU/EEA country-year surveillance data, 2019-2023, richer public
> demographic, land-use, climate, and source-quality covariates did not provide
> stable, calibrated one-year-ahead improvement over surveillance-history baselines;
> the practical finding is a public surveillance bottleneck, not a deployable
> hantavirus predictor.

This framing is EID-compatible because it reports surveillance and modeling results
through a public-health lens. It is also conservative enough for the actual dataset:
142 country-year observations, 5 annual years, heterogeneous surveillance systems,
and reported cases rather than true infection burden.

The EID-specific modeling evidence package has been implemented:

1. EID-style model inputs table with variables, values/ranges, lags, missingness, and sources.
2. Simplified model/workflow schematic.
3. Surveillance-quality sensitivity that separates Belgium 2023, Cyprus 2023, flagged-row indicator, and COVID-era exclusions.
4. Leave-one-country-out influence analysis, especially Finland and Germany.
5. Calibration localization with exact numerator/denominator coverage.
6. Null-calibrated detectability simulation with zero-effect false-positive reporting.
7. A strict EID readiness checker with exact EID article, modeling, and submission gates.
8. A tracked, reproducible submission snapshot with figures, tables, appendix, reports, and manifest.

## 2. Research Checks That Drive This Plan

### 2.1 EID article requirements

Primary target:

- Journal: Emerging Infectious Diseases.
- Article type: Research.
- Word limit: 3,500 words.
- Abstract limit: 150 words, unstructured.
- Reference limit: 50 on the current EID article-types page.
- Practical reference target: <=40 if possible, because the older EID style guide
  used 40 for major article types. Hard stop remains the current 50-reference page limit.
- Figures and tables: as needed.
- Required with article types unless otherwise noted: EID Author Checklist, abstract,
  cover letter, running head, one-sentence summary, keywords, first author biography,
  corresponding author email and mailing address, and ORCID.
- A pre-submission suitability inquiry is not listed as a Research-article requirement on
  the current article-types page. Treat it as an optional risk-reduction step if the final
  negative/mixed framing still feels vulnerable to desk rejection.
- Figures should be at least 300 dpi and at least 5 inches wide.
- Tables should be created with the MS Word table tool.

Primary source:

- https://wwwnc.cdc.gov/eid/article-types

Relevant EID style-guide requirements:

- Research articles must explain the value of findings in public-health terms.
- Titles should be brief and should not use subtitles or complete-sentence titles.
- The running title must be no more than 50 characters including spaces.
- Abstracts should include background/question, methods, results, and conclusions, and
  should state public-health implications rather than saying implications are discussed.
- Manuscripts must provide enough methods detail for independent replication.
- Modeling papers should include sensitivity analyses; one-at-a-time sensitivity alone is
  generally inadequate.
- Modeling papers should contain a Table 1 listing model inputs, values/ranges, and data sources.
- Purely conceptual modeling papers are unlikely to be practical enough for EID readers.

Primary source:

- https://wwwnc.cdc.gov/eid/pdfs/styleguide.pdf

AI disclosure requirements and precedent:

- EID Author Instructions say chatbots cannot be authors, authors must be transparent
  about chatbot use, authors remain responsible for accuracy/plagiarism/source attribution,
  EID prefers not to publish AI-created figures/graphs/images, disclosure belongs in
  Acknowledgments, and the Author Checklist must indicate chatbot use.
- A 2026 EID article provides a concise style precedent: ChatGPT was disclosed for
  language editing, with intellectual responsibility retained by the authors.
- Sources:
  - https://wwwnc.cdc.gov/eid/page/authors-resource-instructions
  - https://wwwnc.cdc.gov/eid/article/32/2/25-1043_article

### 2.2 ECDC surveillance anchor

The ECDC Annual Epidemiological Report for 2023 is the primary surveillance anchor.

Facts to preserve exactly:

- ECDC citation: European Centre for Disease Prevention and Control. Hantavirus infection.
  In: ECDC. Annual Epidemiological Report for 2023. Stockholm: ECDC; 2025.
- Report publication date: 2025-03-07.
- TESSy retrieval date: 2024-11-06.
- In 2023, 28 EU/EEA countries reported 1,885 cases.
- 2023 notification rate: 0.4 cases per 100,000 population.
- 2023 and 2020 were the lowest notification-rate years in 2019-2023.
- Finland and Germany accounted for 60.5% of 2023 reported cases.
- Surveillance was comprehensive in all countries except Belgium, with "other system",
  and Cyprus, with unspecified surveillance context.
- Belgium 2023 rate was not calculated because the surveillance system changed and was
  no longer comprehensive.
- Denmark and Iceland did not report 2023 data.
- United Kingdom had no data from 2020 onward because of EU withdrawal on 2020-01-31.

Sources:

- https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
- https://www.ecdc.europa.eu/sites/default/files/documents/HANTA_AER_2023.pdf

### 2.3 Literature positioning

Use these as the minimum comparison set:

1. Kazasidis and Jacob 2023.
   - Correct title: "Machine learning identifies straightforward early warning rules
     for human Puumala hantavirus outbreaks."
   - Correct authors: Orestis Kazasidis and Jens Jacob.
   - Model used German district-level PUUV data from 2006-2021 and selected 66 districts.
   - The reported classifier used 3 weather parameters and achieved 84.8% sensitivity
     and 71.4% precision in the article text.
   - Source: https://www.nature.com/articles/s41598-023-30596-x

2. Kazasidis, Geduhn, and Jacob 2024.
   - Correct title: "High-resolution early warning system for human Puumala hantavirus
     infection risk in Germany."
   - Correct authors: Orestis Kazasidis, Anke Geduhn, and Jens Jacob.
   - This is a high-resolution German setting, not a public pan-European country-year
     benchmark.
   - Important nuance: the 2023 validation overestimated risk, especially in the flowering
     intensity model. The manuscript should use this as a calibration caution, not only as
     evidence that "early warning works."
   - Source: https://www.nature.com/articles/s41598-024-60144-0

3. Zeimes et al. 2015.
   - Correct title: "Landscape and Regional Environmental Analysis of the Spatial
     Distribution of Hantavirus Human Cases in Europe."
   - This supports environmental/spatial plausibility but is not an annual country-year
     forecast benchmark.
   - Source: https://www.frontiersin.org/articles/10.3389/fpubh.2015.00054/full

4. Bracher et al. 2021.
   - Weighted interval score is appropriate for interval-format epidemic forecasts.
   - WIS should be explained as jointly reflecting sharpness and calibration, not as a
     point-accuracy metric.
   - Source: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618

5. Fox et al. 2024 EID Research Letter.
   - EID has published practical infectious disease forecasting evaluation using baseline-
     standardized performance and WIS.
   - Use this to support the value of baseline comparisons and public-health forecasting
     design, not to imply this hantavirus paper is an operational forecast hub.
   - Source: https://wwwnc.cdc.gov/eid/article/30/9/24-0026_article

### 2.4 Current May 2026 hantavirus news

The current manuscript and cover letter mention a May 2026 Andes-virus cruise ship
cluster. That topic is evolving and is not the study target. Use it only as a brief
risk-communication hook, or remove it entirely.

Hard rule:

- Do not let the cruise-ship paragraph become the rationale for an EU/EEA annual HFRS
  surveillance benchmark.
- If retained, cite exact source and access date, distinguish Andes virus/HPS from
  European hantavirus/HFRS, and re-check the latest WHO/ECDC/CDC pages immediately before
  submission.

## 3. What Changes From The Supplied Plan

Keep:

- EID Research as the target.
- Negative/mixed result as the public-health finding.
- Retrospective EU/EEA country-year scope, 2019-2023.
- Public covariates only.
- No operational predictor, no live dashboard, no causal climate claim, no within-country
  risk map.
- Calibration gate before promoting any model.
- MODIS exclusion unless quality-masked aggregation is actually implemented and audited.

Revise:

- The current repo already has an EID submission package, so Phase 0 is now a cleanup,
  consistency, and readiness correction.
- The old `PUBLICATION_MASTER_PLAN.md` was the worst active contradiction; this file now
  supersedes it.
- Keep fallbacks only in archival strategy notes. The active package should target EID only.
- Do not demand that every archived historical file erase old target language. Instead,
  define active files and archived files explicitly, and fail only if active files present
  a non-EID live target.
- DOI and ORCID are no longer future placeholders; they are present locally. The plan now
  requires verifying that the DOI archive matches the current submission commit and generated
  files.
- The existing `docs/submission_eid/final_qa_report_eid.md` should be downgraded from
  "ready" to "draft QA passed; EID modeling package incomplete."
- The current detectability screen must not be used as evidence because the zero-effect
  false-positive rate is too high.
- Add country influence and calibration localization before the manuscript rewrite.

Delete or avoid:

- "First" and other primacy language.
- "Operationally" as a positive claim. It can appear only in a negated guardrail.
- Any incorrect attribution of the 2023/2024 German PUUV papers.
- "Variance decomposition" unless a formal variance-component model is added.
- Broad "predictor" branding in title, abstract, or repository summary.
- Unstable 2026 outbreak framing as the central motivation.

## 4. Active File Policy

Active EID-facing files are:

- `README.md`
- `pyproject.toml`
- `PUBLICATION_MASTER_PLAN.md`
- `docs/PROJECT_STATE.md`
- `docs/AGENT_HANDOFF.md`
- `docs/submission_eid/**`
- `docs/manuscript/**` only if referenced by README or submission guide
- `tools/create_eid_figures.py`
- `tools/build_eid_docx.py`
- all new EID readiness, table, and sensitivity tools

Archived or superseded files may retain historical target language only if clearly labeled as
superseded and kept off the active branch:

- old cover-letter drafts
- old map-generation scripts
- old Overleaf bundle files
- older planning docs under `docs/` that are not linked as current guidance

Acceptance gate:

```powershell
rg -n "current first target|first journal target|Scientific Data|BMC Public Health" README.md pyproject.toml docs/submission_eid docs/PROJECT_STATE.md docs/AGENT_HANDOFF.md
```

Allowed results:

- None in active EID-facing files.

Not allowed:

- Any statement that a non-EID journal is the current first target.

## 5. Current Repo Audit

### 5.1 Strengths already present

- EID submission directory exists: `docs/submission_eid/`.
- Main manuscript and DOCX exist.
- Cover letter and author statements exist.
- EID figures exist as TIFF files at 600 dpi.
- DOI resolves.
- ORCID is filled.
- Tests and ruff currently pass locally.
- ECDC totals are reconciled in reports.
- MODIS is excluded from manuscript claims.
- The current manuscript mostly avoids operational and causal overclaiming.
- The current manuscript reports coverage as numerators and denominators for several main
  results.
- Active legacy ZIPs, extracted LLM packages, old Overleaf output, old manuscript drafts,
  and conflicting planning files have been removed from `main` and preserved on
  `codex/archive-pre-eid-cleanup-20260514`.
- The active data-source registry is now scoped to ECDC, World Bank, FAOSTAT,
  TerraClimate, MODIS-as-excluded/optional, and Natural Earth.

### 5.2 Blocking gaps

1. Current manuscript title is safe but not optimal:

   - Current: "Public Surveillance Benchmark for Reported Hantavirus Incidence, EU/EEA, 2019-2023"
   - Better EID title: "Sparse Public Surveillance and Forecasting of Reported Hantavirus Incidence, European Union and European Economic Area, 2019-2023"
   - Stronger but slightly more assertive: "Sparse Public Surveillance Limits Forecasting of Reported Hantavirus Incidence, European Union and European Economic Area, 2019-2023"

   Preferred final title: the stronger version, if the added sensitivity analyses support it.
   Use the less assertive version if influence/sensitivity results are mixed.

2. Current Table 1 is a source and quality audit. It is not the EID-requested model-input
   table with values/ranges and data sources.

3. Current sensitivity analysis is too coarse. It does not separately test Belgium 2023,
   Cyprus 2023, flagged-row indicator, or leave-one-country-out influence.

4. Current detectability simulation has a high apparent improvement rate at zero injected
   effect. That makes it unsuitable for supporting "limited power" claims until redesigned.

5. Current figures omit an EID-ready sensitivity/influence/calibration figure. Figure 1 also
   needs a clear visual mark for grade-C rows if those rows remain discussed.

6. Current strict EID readiness tooling does not exist. `tools/check_publication_readiness.py`
   is a useful broad publication gate after cleanup, but it is not a full EID submission
   checker.

7. Generated reports are ignored by git. The final submission snapshot must include
   tracked or archived reports/tables from a clean manifest.

8. The Markdown files displayed mojibake in PowerShell for punctuation such as en dashes.
    This may be terminal encoding rather than file corruption, but final DOCX/PDF rendering
    must be visually checked. Prefer ASCII in active Markdown where possible.

## 6. Final Scientific Position

### 6.1 What the paper is

This paper is a retrospective public-surveillance benchmark.

It asks:

> Do public demographic, land-use, climate, and source-quality covariates improve calibrated
> one-year-ahead forecasts of reported EU/EEA country-year hantavirus incidence beyond simple
> surveillance-history baselines, and are performance failures associated with sparse annual
> reporting and surveillance-completeness caveats?

### 6.2 What the paper is not

The paper is not:

- a prospective forecast;
- a validated early warning system;
- an operational public-health tool;
- a clinical tool;
- an individual risk model;
- a within-country risk map;
- a causal climate analysis;
- a true infection-burden estimate;
- a general hantavirus transmission model;
- a model of Andes-virus person-to-person transmission;
- a global hantavirus surveillance benchmark.

### 6.3 Promotion rule

A covariate model can be described as better only if all criteria pass on the 2023 test year
and are directionally stable in sensitivity analyses:

1. WIS improves by at least 5% relative to the best simple surveillance-history baseline, or
   WIS is comparable and coverage is materially closer to 90%.
2. 90% coverage is not lower than the best simple baseline by more than 5 percentage points.
3. Mean interval width is interpretable, not merely inflated.
4. No target-year outcome is used in features, imputation, screening, or tuning.
5. Result survives flagged-row sensitivity.
6. Result is not driven solely by Finland or Germany.
7. Model interpretation avoids causal coefficient claims.

Expected result based on current outputs:

- No public covariate model will pass.

That is acceptable if the manuscript makes the public-health meaning clear.

## 7. Implementation Plan

### Phase 0: Freeze the EID target and align readiness language

Goal:

- Align active repo language with EID and remove stale non-EID or incomplete-package claims.

Files:

- `README.md`
- `pyproject.toml`
- `docs/PROJECT_STATE.md`
- `docs/AGENT_HANDOFF.md`
- `docs/submission_eid/final_qa_report_eid.md`
- `docs/submission_eid/submission_guide_eid.md`
- `PUBLICATION_MASTER_PLAN.md`

Required edits:

1. State that the active target is EID Research.
2. State that fallback journals are outside the active submission package.
3. Replace stale incomplete-package language with "ready for human portal preparation except final contact, checklist, and DOI/archive verification."
4. Make the title, abstract, and one-sentence summary consistent.
5. Keep old non-EID files only on the archive branch or as explicitly superseded history.

Gate:

```powershell
rg -n "current first target|first journal target|Scientific Data|BMC Public Health" README.md pyproject.toml docs/submission_eid docs/PROJECT_STATE.md docs/AGENT_HANDOFF.md
python -m pytest
python -m ruff check src tests tools
```

Pass condition:

- No active file presents a non-EID first target.
- Tests and lint pass.

### Phase 1: Reproducibility rebuild and snapshot discipline

Goal:

- Make reviewer confidence independent of ignored local outputs.

Commands:

```powershell
python -m pip install -e ".[dev,geo]"
python tools/create_ecdc_case_table.py --accessed-date 2026-05-14
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/run_sensitivity_power.py
python tools/create_eid_figures.py
python tools/build_eid_docx.py
python -m pytest
python -m ruff check src tests tools
```

Create:

- `docs/submission_eid/reproducibility_manifest.md`
- `docs/submission_eid/reports/`
- `docs/submission_eid/tables/`
- `docs/submission_eid/figures/`
- `docs/submission_eid/supplements/`

Manifest must include:

- commit hash;
- dirty-worktree status;
- Python version;
- OS;
- exact command list;
- exact row counts;
- annual ECDC totals;
- report paths;
- figure paths and DPI;
- DOI/version status;
- statement that no credential files are included.

Gate:

```powershell
git status --short
git ls-files docs/submission_eid
python -c "from PIL import Image; from pathlib import Path; [print(p.name, Image.open(p).size, Image.open(p).info.get('dpi')) for p in Path('docs/submission_eid/figures').glob('*.tif')]"
```

Pass condition:

- Submission-critical files are tracked or explicitly included in a clean generated archive.
- Figures are at least 300 dpi and 5 inches wide.
- DOI archive either matches the final commit or is clearly marked as needing a new version.

### Phase 2: EID model-input Table 1

Goal:

- Replace the current source-audit Table 1 with an EID-compliant model-input table.

Add scripts:

- `tools/write_eid_model_inputs_table.py`
- `tools/check_eid_model_inputs_table.py`

Outputs:

- `docs/submission_eid/tables/table1_model_inputs.csv`
- `docs/submission_eid/tables/table1_model_inputs.md`

Columns:

- `category`
- `variable_name`
- `plain_language_definition`
- `unit`
- `source`
- `source_url_or_citation`
- `years_available`
- `lag_used`
- `training_range_min`
- `training_range_max`
- `missing_count_training`
- `missing_count_validation`
- `missing_count_test`
- `missingness_rule`
- `included_in_feature_sets`
- `reason_for_inclusion`
- `known_limitation`
- `leakage_check`

Rows must cover:

- outcome count;
- population denominator;
- reported incidence;
- lagged country rate;
- country historical mean rate;
- panel/regional surveillance summaries;
- World Bank population/rurality/GDP;
- FAOSTAT land-use shares;
- TerraClimate lagged climate and water-balance summaries;
- surveillance-completeness and quality flags;
- country boundary data;
- MODIS NDVI/EVI exclusion row.

Tests:

- `tests/test_eid_model_inputs_table.py`

Gate:

```powershell
python tools/write_eid_model_inputs_table.py
python tools/check_eid_model_inputs_table.py
python -m pytest tests/test_eid_model_inputs_table.py
```

Pass condition:

- Every final model variable appears exactly once.
- Every model variable has source, range, lag, missingness, and leakage-check fields.
- Table is small enough to fit in the main manuscript as an EID table or has a compact main
  version plus a complete appendix version.

### Phase 3: Model schematic

Goal:

- Give non-CS epidemiology reviewers a one-panel workflow they can understand.

Add:

- `tools/write_eid_model_schematic.py` or implement in `tools/create_eid_figures.py`

Outputs:

- `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- `docs/submission_eid/supplements/model_schematic_notes.md`

Schematic blocks:

1. Public ECDC country-year labels.
2. Public covariate joins by ISO3 and year.
3. Training-only imputation and feature screening.
4. Surveillance baselines.
5. Covariate-block models.
6. Penalized count model.
7. Validation on 2022.
8. Locked test on 2023.
9. Metrics: WIS, coverage, interval width, MAE, Brier.
10. Sensitivity analyses.

Gate:

```powershell
python tools/write_eid_model_schematic.py
```

Pass condition:

- Figure has no false spatial precision.
- Text is readable at EID print size.
- All acronyms are defined in the caption or appendix.

### Phase 4: Surveillance-quality sensitivity

Goal:

- Show whether conclusions depend on flagged surveillance rows or COVID-era years.

Add:

- `tools/run_surveillance_quality_sensitivity.py`

Outputs:

- `data/processed/surveillance_quality_sensitivity_metrics.csv`
- `data/processed/surveillance_quality_sensitivity_predictions.csv`
- `docs/submission_eid/tables/appendix_surveillance_quality_sensitivity.csv`
- `docs/submission_eid/reports/surveillance_quality_sensitivity.md`

Required scenarios:

1. Primary all rows.
2. Exclude Belgium 2023 only.
3. Exclude Cyprus 2023 only.
4. Exclude Belgium 2023 and Cyprus 2023.
5. Retain flagged rows with a flagged-row indicator.
6. Exclude 2020 training rows where feasible.
7. Exclude 2021 training rows where feasible.
8. Exclude 2020-2021 training rows where feasible.

Metrics:

- WIS;
- relative WIS versus best simple baseline;
- 90% coverage as numerator/denominator and fraction;
- mean interval width;
- MAE;
- Brier any-case;
- number of rows retained;
- number of countries retained;
- best-ranked feature set;
- whether promotion rule passed.

Tests:

- `tests/test_surveillance_quality_sensitivity.py`

Gate:

```powershell
python tools/run_surveillance_quality_sensitivity.py
python -m pytest tests/test_surveillance_quality_sensitivity.py
```

Pass condition:

- Main negative result remains unchanged or any exception is reported plainly.
- Coverage is always reported as numerator/denominator and percentage.
- No scenario is described as causal.

### Phase 5: Country influence analysis

Goal:

- Answer the predictable reviewer question: "Is this driven by Finland, Germany, or one
  high-incidence country?"

Add:

- `tools/run_country_influence.py`

Outputs:

- `data/processed/country_influence_metrics.csv`
- `docs/submission_eid/tables/appendix_country_influence.csv`
- `docs/submission_eid/figures/Appendix_Figure_country_influence.tif`
- `docs/submission_eid/reports/country_influence.md`

Design:

- For each country, remove all rows for that country.
- Rebuild feature-ablation metrics and simple baselines.
- Record delta WIS, delta coverage, delta interval width, and change in best model.
- Mark Finland and Germany as pre-specified high-influence checks because ECDC reports they
  account for 60.5% of 2023 cases.

Tests:

- `tests/test_country_influence.py`

Gate:

```powershell
python tools/run_country_influence.py
python -m pytest tests/test_country_influence.py
```

Pass condition:

- Main conclusion holds when Finland is removed.
- Main conclusion holds when Germany is removed.
- If the conclusion changes, the manuscript must explicitly say the result is high-country
  dependent and EID submission should be reconsidered or narrowed.

### Phase 6: Calibration localization

Goal:

- Show where interval coverage fails without implying within-country precision.

Add:

- `tools/write_calibration_localization.py`
- optionally `tools/plot_eid_calibration_localization.py`

Outputs:

- `data/processed/calibration_localization.csv`
- `docs/submission_eid/tables/appendix_calibration_localization.csv`
- `docs/submission_eid/figures/Appendix_Figure_calibration_localization.tif`
- possibly main `Figure_3.tif`

Fields:

- country;
- ISO3;
- year;
- model;
- feature set;
- observed count;
- predicted median;
- lower 90% interval;
- upper 90% interval;
- covered yes/no;
- absolute error;
- interval width;
- quality flag;
- reported incidence;
- notes for Finland/Germany/flagged rows.

Main text requirement:

- State exact numerator/denominator:
  "The nominal 90% intervals covered X/Y country-year observations in 2023."

Gate:

```powershell
python tools/write_calibration_localization.py
```

Pass condition:

- All 2023 test predictions are traceable.
- Coverage failures can be summarized by country and model.
- Figure remains country-level only.

### Phase 7: Null-calibrated detectability simulation

Goal:

- Replace the current underpowered and false-positive-prone screen with a reviewer-safe
  simulation.

Current problem:

- `reports/07_sensitivity_power.md` reports 64% "detectability" at zero injected effect.
  This cannot support an EID claim about limited power or modest covariate effects.

Add or rewrite:

- `tools/run_detectability_screen.py`

Outputs:

- `data/processed/detectability_screen.csv`
- `docs/submission_eid/tables/appendix_detectability_screen.csv`
- `docs/submission_eid/figures/Appendix_Figure_detectability.tif`
- `docs/submission_eid/reports/detectability_screen.md`

Simulation design:

- Use actual country-year panel structure.
- Use actual country populations.
- Match observed baseline incidence distribution.
- Use negative-binomial or Poisson-gamma simulation with overdispersion levels:
  `low`, `observed_like`, `high`.
- Use effect sizes:
  `0`, `small`, `moderate`, `large`.
- Use missingness/flag patterns:
  `none`, `observed_like`.
- Fit baseline and covariate models using the same train/validate/test design as the real analysis.
- Compute probability that the covariate model beats the surveillance baseline.
- Compute false-positive selection probability when effect size is zero.
- Compute coverage under observed-like overdispersion.

Mandatory false-positive gate:

- At effect size zero, the probability of selecting the covariate model must be <= 0.10
  under the declared selection rule, or the selection rule must be tightened.

Interpretation gate:

- Allowed wording:
  "Simulation results do not validate model skill; they indicate that this sample structure
  has limited ability to detect modest covariate effects under the tested assumptions."

- Not allowed:
  "The simulation proves covariates have no effect."
  "The simulation validates the model."

Tests:

- `tests/test_detectability_screen.py`

Gate:

```powershell
python tools/run_detectability_screen.py --iterations 500
python -m pytest tests/test_detectability_screen.py
```

Pass condition:

- Null false-positive selection rate is reported.
- Any high false-positive result is interpreted as a limitation, not as evidence.

### Phase 8: EID figure and table pack

Goal:

- Build a compact EID-readable evidence package.

Main-text tables:

1. Table 1: Public data sources and model inputs for reported hantavirus incidence
   forecasting, European Union and European Economic Area, 2019-2023.
2. Table 2: Primary model performance, validation year 2022 and test year 2023.
3. Optional Table 3: Sensitivity summary if Figure 3 cannot carry it clearly.

Main-text figures:

1. Figure 1: Country-level 2023 reported incidence map with grade-C row marking.
2. Figure 2: Model performance and calibration-sharpness tradeoff.
3. Figure 3: Sensitivity/influence/calibration summary.

Appendix figures:

- model schematic;
- complete calibration localization;
- country influence full leave-one-country-out plot;
- detectability simulation curves;
- feature-screening flow;
- MODIS exclusion gate, if helpful.

Figure rules:

- Use Python/matplotlib/geopandas outputs only.
- No AI-generated figures.
- No within-country risk gradients.
- Caption must state that maps show country-level reported incidence and do not indicate
  within-country risk.
- Use exact values in text or tables, not only in graphics.
- Keep colors accessible and restrained.

Add:

- `tools/plot_eid_model_performance.py`
- `tools/plot_eid_sensitivity.py`
- `tools/plot_eid_calibration_localization.py`

Gate:

```powershell
python tools/create_eid_figures.py
python tools/plot_eid_sensitivity.py
python tools/plot_eid_calibration_localization.py
python -c "from PIL import Image; from pathlib import Path; [print(p.name, Image.open(p).size, Image.open(p).info.get('dpi')) for p in Path('docs/submission_eid/figures').glob('*.tif')]"
```

Pass condition:

- Every main claim in the Results has a corresponding table/figure or exact text value.
- Figures meet EID resolution requirements.
- Main figures are interpretable without the appendix.

### Phase 9: Manuscript rewrite

Goal:

- Convert the current polished draft into an EID-ready Research article that reflects the
  upgraded evidence package.

Primary file:

- `docs/submission_eid/manuscript_eid.md`

Generated file:

- `docs/submission_eid/manuscript_eid.docx`

Target title:

- If sensitivity/influence supports the claim:
  "Sparse Public Surveillance Limits Forecasting of Reported Hantavirus Incidence,
  European Union and European Economic Area, 2019-2023"

- If sensitivity/influence is mixed:
  "Sparse Public Surveillance and Forecasting of Reported Hantavirus Incidence,
  European Union and European Economic Area, 2019-2023"

Running title:

- "Hantavirus Forecasting Limits"

One-sentence summary:

- "Sparse annual public surveillance data did not support stable, calibrated covariate-driven
  forecasts of reported EU/EEA hantavirus incidence."

Abstract requirements:

- <=150 words.
- One paragraph.
- No references.
- No "first."
- Include:
  - public surveillance problem;
  - EU/EEA country-year benchmark, 2019-2023;
  - one-year-ahead probabilistic evaluation;
  - WIS and coverage;
  - negative/mixed result;
  - public-health implication.

Candidate abstract:

```text
Public hantavirus surveillance reports are essential for public health monitoring, but their
ability to support country-level forecasting across heterogeneous systems is unclear. We
assembled a European Union/European Economic Area country-year benchmark of reported
hantavirus incidence for 2019-2023 and linked labels to public demographic, land-use,
climate, and source-quality covariates. We compared surveillance baselines and low-dimensional
public-covariate models using one-year-ahead probabilistic evaluation, weighted interval
score, 90% empirical coverage, interval width, mean absolute error, Brier score, and
sensitivity analyses for flagged surveillance rows, COVID-era years, and country influence.
Public covariates did not provide stable, calibrated improvement on the 2023 test year; sharp
models undercovered observations, whereas overdispersed baselines used wide intervals.
These findings suggest that standardized completeness metadata, longer comparable panels,
and explicit uncertainty reporting may improve pan-European hantavirus forecasting more than
adding coarse public covariates alone.
```

Section plan:

1. Introduction, 400-500 words.
   - Disease and surveillance context.
   - ECDC 2023 facts.
   - Why forecasting is plausible but hard.
   - Contrast with German district-level PUUV work.
   - European mapping precedent.
   - Research question.
   - Optional one-sentence 2026 outbreak/risk-communication hook only if still current.

2. Materials and Methods, 850-1,000 words.
   - Retrospective observational forecasting benchmark.
   - STROBE/reporting-guideline statement.
   - Data sources.
   - Unit of analysis.
   - Model families.
   - Validation split.
   - Metrics.
   - Missing data and leakage prevention.
   - Sensitivity and detectability design.
   - Ethics and reproducibility.

3. Results, 950-1,100 words.
   - Data reconstruction and ECDC total reconciliation.
   - Primary baseline and covariate-block results.
   - Count-model calibration failure.
   - Surveillance-quality sensitivity.
   - Finland/Germany/country influence.
   - Calibration localization.
   - Detectability screen, if null-calibrated.

4. Discussion, 850-1,000 words.
   - Direct answer first.
   - Public-health meaning.
   - Contrast with Germany.
   - Surveillance implications.
   - Limitations.
   - Conclusion.

Required exact language:

- "reported cases" or "reported incidence," not unqualified "infections," when discussing
  model targets.
- "retrospective one-year-ahead evaluation," not "prospective."
- "associated with" or "consistent with," not "caused by."
- "source-quality metadata," not causal surveillance effects.
- "public country-year data," not "local risk."

Search gate:

```powershell
rg -n "first|operational predictor|live dashboard|caused by|significant|prospective|early warning system" docs/submission_eid/manuscript_eid.md docs/submission_eid/cover_letter_eid.md
```

Pass condition:

- Every hit is manually justified or removed.
- "significant" appears only for statistical significance.
- "early warning system" appears only when citing German literature or explicitly negated.

### Phase 10: Appendix rewrite

Goal:

- Move technical detail out of the main text while keeping enough Methods detail for replication.

Primary file:

- `docs/submission_eid/supplements/Appendix_methods_eid.md`

Generated file:

- `docs/submission_eid/supplements/Appendix_methods_eid.docx`

Required sections:

1. Source audit and data construction.
2. Complete feature dictionary and model inputs.
3. Model schematic.
4. Forecasting workflow.
5. Weighted interval score details.
6. Missing-data handling.
7. Feature-screening rules.
8. Baseline model formulas.
9. Covariate-block model details.
10. Penalized Poisson model details.
11. Penalized Poisson coefficient/performance table or explicit note that coefficients
    are penalized, exploratory, and not inferential.
12. Surveillance-quality sensitivity.
13. Leave-one-country-out influence.
14. Calibration localization.
15. Detectability simulation.
16. MODIS exclusion gate.
17. Reproducibility commands.

Gate:

```powershell
rg -n "Appendix" docs/submission_eid/manuscript_eid.md
```

Pass condition:

- Every appendix section is cited at least once in the main manuscript.
- The appendix does not make stronger claims than the main paper.

### Phase 11: Cover letter and author statements

Goal:

- Align cover letter with the final evidence package and EID expectations.

Files:

- `docs/submission_eid/cover_letter_eid.md`
- `docs/submission_eid/author_statements.md`

Cover letter must include:

- Article type: Research.
- Public-health problem.
- What was done.
- Main result.
- Why EID readers should care.
- Originality/not under review statement.
- Author approval statement.
- No competing interests.
- Data/code availability.
- AI disclosure.
- If done before portal submission, note that EID was contacted with a pre-submission
  inquiry and summarize any editorial response.

Revise:

- Do not say "can and cannot support operationally" unless carefully negated.
- Reduce the 2026 cruise-ship hook to one sentence or remove it.
- Add a sentence that the manuscript follows EID modeling guidance with a model-input table,
  schematic, sensitivity analyses, and reproducibility archive.

AI disclosure preferred wording:

```text
Artificial intelligence tools were used to assist with manuscript planning,
language editing, and pre-submission quality checks. No confidential or nonpublic
data were entered into AI tools. The author verified all analyses, references,
and claims and accepts responsibility for the final manuscript. No AI-generated
figures were used.
```

Gate:

```powershell
rg -n "AI|artificial intelligence|confidential|nonpublic|not submitted|approved" docs/submission_eid/cover_letter_eid.md docs/submission_eid/author_statements.md
```

Pass condition:

- All required statements are present.

### Phase 11.5: Optional EID suitability inquiry

Goal:

- Reduce desk-rejection risk before portal upload without treating this as an EID
  Research-article requirement.

Trigger:

- Use only after the title, 150-word abstract, one-sentence summary, core results,
  and EID-specific sensitivity package are stable.

Inquiry contents:

- Proposed article type: Research.
- Final title.
- Full author list.
- 150-word abstract.
- Two to three sentences explaining why the negative/mixed surveillance-modeling
  result has practical public-health value for EID readers.
- Explicit statement that the manuscript includes model-input Table 1, schematic,
  sensitivity analyses, public data/code archive, and no operational prediction claim.

Documentation:

```text
If sent, record date sent, editor response, and any requested reframing in
docs/submission_eid/submission_guide_eid.md. If skipped, document that it was a strategic
choice, not an omitted formal requirement.
```

### Phase 12: Strict EID readiness checker

Goal:

- Replace broad publication readiness with exact EID readiness.

Add:

- `tools/check_eid_submission_readiness.py`

It should fail on:

- title contains colon;
- title contains `EU/EEA` instead of spelling out the place;
- abstract >150 words;
- main text >3,500 words;
- references >50;
- missing running title or running title >50 characters;
- no one-sentence summary;
- missing corresponding author email or mailing-address placeholder;
- missing ORCID;
- missing author biography;
- active EID files contain a non-EID live target;
- incorrect German PUUV paper attribution appears;
- primacy language appears;
- operational/live-dashboard claims appear;
- unsupported causal language appears;
- "significant" appears outside statistical context;
- no EID model-input Table 1;
- Table 1 lacks source/range/missingness/lag columns;
- no model schematic;
- no STROBE/reporting statement;
- no ethics statement;
- no AI disclosure;
- no data/code availability statement;
- no Author Checklist reminder;
- no exact numerator/denominator coverage text;
- no surveillance-quality sensitivity report;
- no country influence report;
- no calibration localization report;
- no detectability false-positive report;
- figures missing or below required resolution;
- tables missing;
- appendix missing;
- reproducibility manifest missing;
- final DOI does not resolve.

It should warn, not fail, on:

- references >40 but <=50;
- no optional suitability-inquiry note or explicit decision to skip it.

Tests:

- `tests/test_eid_submission_readiness.py`

Gate:

```powershell
python tools/check_eid_submission_readiness.py --strict
python -m pytest tests/test_eid_submission_readiness.py
```

Pass condition:

```text
EID readiness: PASS
```

### Phase 13: Final QA and archive

Goal:

- Produce a submission artifact that matches the manuscript and repo state.

Commands:

```powershell
python -m pytest
python -m ruff check src tests tools
python tools/check_eid_submission_readiness.py --strict
git diff --check
```

Archive gate:

- Use `git archive` from a clean commit/tag, or build a controlled ZIP from a manifest.
- Do not include:
  - `.env`;
  - `nasa earthdata acc info.txt`;
  - credential files;
  - old LLM archive ZIPs;
  - old Overleaf bundle;
  - obsolete non-EID cover letter as an upload candidate.

Final deliverables:

- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/figures/Figure_3.tif`, if retained
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/reproducibility_manifest.md`
- updated Zenodo DOI/version

Human-only final checks:

- Corresponding author's full mailing address and phone number in portal/title page if required.
- Confirm title page is not anonymous.
- Open the DOCX in Word and verify line numbers, tables, and special characters.
- Confirm figures are uploaded as separate files.
- Confirm tables are editable Word tables.
- Confirm DOI resolves and points to the final archive version.

## 8. Manuscript Acceptance Logic

### Reviewer question: Why is a negative result publishable?

Answer:

- Because it identifies a practical public-health surveillance bottleneck.
- The result is not "the model failed"; it is "coarse public annual reporting cannot support
  the level of calibrated prediction implied by richer covariate models."

Evidence needed:

- WIS/coverage tradeoff.
- Flagged-row sensitivity.
- Finland/Germany country influence.
- Calibration localization.
- Null-calibrated detectability screen.

### Reviewer question: Is this only too small a dataset?

Answer:

- Yes, partly, and that is the point. The study quantifies what this public data structure
  can and cannot support.

Evidence needed:

- `n = 142` country-years.
- Five annual years.
- Final feature count before one-hot encoding.
- Simulation screen with honest false-positive rate.

### Reviewer question: Why not use German district-level methods?

Answer:

- German PUUV studies use richer within-country district data and more biologically specific
  predictors. This study asks a different public-data question: pan-European annual
  country-year reported incidence under heterogeneous surveillance.

Evidence needed:

- Kazasidis and Jacob 2023 citation.
- Kazasidis, Geduhn, and Jacob 2024 citation.
- Direct statement that the findings do not contradict those studies.

### Reviewer question: Why country-year?

Answer:

- Because public EU/EEA surveillance reports provide a harmonizable country-year panel across
  countries. Monthly and district-level work would answer a different, country-specific
  question and often require nonpublic systems.

Evidence needed:

- ECDC source table.
- ECDC monthly limitations if discussed.

### Reviewer question: Are these infections or reported cases?

Answer:

- Reported cases only.

Evidence needed:

- Title, abstract, Methods, tables, and figures consistently say "reported."

### Reviewer question: Why include COVID-era years?

Answer:

- They are part of the available public surveillance period, but sensitivity analyses test
  their influence.

Evidence needed:

- Exclude 2020, exclude 2021, exclude 2020-2021 scenarios.

### Reviewer question: Could Belgium/Cyprus flags drive the result?

Answer:

- Test directly with separate and combined flagged-row exclusions plus flagged-row indicator.

Evidence needed:

- Surveillance-quality sensitivity table.

### Reviewer question: Why no MODIS NDVI/EVI?

Answer:

- The source manifest exists, but quality-masked country-year aggregation did not pass the
  prespecified inclusion gate. Excluding it is a strength because the paper avoids vegetation
  claims it cannot support.

Evidence needed:

- MODIS exclusion row in Table 1 and appendix.

### Reviewer question: Why WIS?

Answer:

- WIS is a proper score for interval-format epidemic forecasts and summarizes sharpness and
  calibration. EID has published infectious disease forecast-evaluation work using WIS.

Evidence needed:

- Bracher et al. 2021.
- Fox et al. 2024 EID.

### Reviewer question: Why not promote the Poisson model?

Answer:

- It has poor calibration. Current 2023 land-use penalized Poisson model coverage is 9/28,
  about 32%, far below nominal 90%.

Evidence needed:

- Count model table.

## 9. Final Readiness Checklist

Do not submit until every item is complete:

- [ ] Active target is EID Research everywhere in active files.
- [ ] Current final QA no longer overstates readiness.
- [ ] Tests pass.
- [ ] Ruff passes.
- [ ] Full pipeline rebuilds from a clean environment.
- [ ] ECDC totals reconcile: 4,088, 1,693, 4,947, 2,185, 1,885.
- [ ] Belgium 2023 and Cyprus 2023 are flagged and tested.
- [ ] Finland/Germany influence analysis exists.
- [ ] EID Table 1 lists inputs, values/ranges, lags, missingness, and sources.
- [ ] Model schematic exists.
- [ ] Calibration localization exists.
- [ ] Detectability screen reports a null false-positive rate and passes its gate.
- [ ] MODIS exclusion is documented.
- [ ] Main map has no within-country risk implication.
- [ ] Title has no colon and spells out European Union and European Economic Area.
- [ ] Abstract <=150 words.
- [ ] Main text <=3,500 words.
- [ ] References <=50.
- [ ] References targeted to <=40 unless an EID-critical citation requires more.
- [ ] Running title <=50 characters.
- [ ] One-sentence summary included.
- [ ] Author biography included.
- [ ] ORCID included and correct.
- [ ] Corresponding author email included.
- [ ] Mailing address/phone handled in portal or title page.
- [ ] Ethics statement accurate for aggregate public data.
- [ ] AI disclosure includes no confidential/nonpublic data entered.
- [ ] Data/code availability DOI resolves and points to final archive version.
- [ ] Figures are separate TIFF files, at least 300 dpi and 5 inches wide.
- [ ] Tables are editable Word tables.
- [ ] Appendix is self-contained and cited from main text.
- [ ] Optional EID suitability inquiry sent, skipped, or deferred with rationale.
- [ ] Strict EID readiness checker passes.
- [ ] Final archive excludes secrets and obsolete upload candidates.
- [ ] Senior methodological review obtained if available.

Bottom line:

The EID submission can be credible if the next iteration proves restraint and
traceability. The winning version is not "we built a predictor." It is "we tested
the public-data forecasting ceiling honestly and found that surveillance
standardization and uncertainty reporting are the binding constraints."
