# EID Submission Readiness QA Report

Date: 2026-05-14

Repository: `hantavirus_predictor`

Active branch: `main`

Audit scope: full repository organization, EID acceptance-plan implementation,
submission-package QA, reproducibility rebuild, and final local readiness for
*Emerging Infectious Diseases* submission preparation. This report excludes only
human-only submission items such as final mailing address/phone, portal
checklist responses, final Word visual inspection, and final Zenodo DOI/archive
matching.

## Executive Verdict

Local EID readiness is PASS.

The repository now implements the full EID-oriented plan: model-input Table 1,
model schematic, surveillance-quality sensitivity, country influence,
calibration localization, detectability screen, strict EID readiness checker,
submission snapshot, DOCX build, and CI parity. A full rebuild was run from
ignored/generated data after cleanup. It exposed a real reproducibility bug in
the World Bank context join, which was fixed and re-QA'd.

Remaining human-only items:

- Confirm corresponding author's mailing address and phone number.
- Verify that the final Zenodo DOI resolves to an archive matching the final
  clean commit.
- Complete EID Author Checklist, COI, funding, and AI-use portal fields.
- Open DOCX files in Word and visually inspect line numbering, editable tables,
  figure legends, and special characters.

## External EID Research Checked

Current EID guidance and related evidence were rechecked during this audit.

- EID Research article limits and required materials:
  https://wwwnc.cdc.gov/eid/article-types
- EID author instructions, cover letter, chatbot/AI disclosure, and image
  guidance:
  https://wwwnc.cdc.gov/eid/page/authors-resource-instructions
- EID style guide, including title, abstract, public-health meaning, figures,
  tables, and modeling guidance:
  https://wwwnc.cdc.gov/eid/pdfs/styleguide.pdf
- ECDC 2023 hantavirus surveillance anchor:
  https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023
- German Puumala forecasting comparison papers:
  https://www.nature.com/articles/s41598-023-30596-x
  https://www.nature.com/articles/s41598-024-60144-0
- European spatial-risk precedent:
  https://www.frontiersin.org/articles/10.3389/fpubh.2015.00054/full
- Weighted interval score methods:
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618
- EID infectious disease forecast-evaluation precedent:
  https://wwwnc.cdc.gov/eid/article/30/9/24-0026_article

## Work Done in This QA Iteration

### Repository and Documentation

- Rewrote `PUBLICATION_MASTER_PLAN.md` from a historical/forward plan into a
  final implemented EID traceability plan.
- Replaced stale "future work" language in `docs/AGENT_HANDOFF.md`.
- Replaced stale root reproducibility guidance in
  `docs/reproducibility_manifest.md`.
- Updated `README.md` quick-start commands to include the full EID-specific
  artifact and readiness sequence.
- Updated `docs/submission_eid/reproducibility_manifest.md` to use the current
  access date and include the full rebuild command sequence.
- Added this root-level `report.md` as the comprehensive audit record.

### EID Submission Package

- Added an EID Author Checklist reminder to
  `docs/submission_eid/author_statements.md`.
- Rebuilt `docs/submission_eid/author_statements.docx`.
- Rebuilt all EID DOCX outputs after edits:
  - `docs/submission_eid/manuscript_eid.docx`
  - `docs/submission_eid/cover_letter_eid.docx`
  - `docs/submission_eid/author_statements.docx`
  - `docs/submission_eid/supplements/Appendix_methods_eid.docx`

### Code and Rebuild Robustness

- Fixed World Bank API chunking in
  `src/hantavirus_predictor/ingest/world_bank.py`.
  The previous loop used overlapping slices; it now uses explicit non-overlap
  chunks.
- Fixed rebuild robustness in
  `src/hantavirus_predictor/features/country_year.py`.
  If World Bank context covariates cannot be fetched, the builder now returns
  explicit context columns with missing values rather than crashing when adding
  missingness indicators.
- Removed obsolete pre-EID report generator:
  `tools/write_paper_readiness_report.py`.
- Strengthened `tools/check_eid_submission_readiness.py` to require an EID
  Author Checklist reminder.
- Added `tests/test_eid_submission_readiness.py` so the strict EID readiness
  checker is covered by pytest.

### CI

- Updated `.github/workflows/ci.yml` to install `.[dev,geo]`.
- CI now runs:
  - `python -m pytest`
  - `python -m ruff check src tests tools`
  - `python tools/check_eid_submission_readiness.py --strict`

## Full Rebuild QA

The full rebuild sequence was run from ignored/generated data state. Commands
successfully completed after the World Bank context bug fix:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-14
python tools/validate_international_cases.py --strict
python tools/download_faostat_land_use.py
python tools/create_terraclimate_manifest.py
python tools/download_natural_earth_countries.py
python tools/aggregate_terraclimate_country_year.py
python tools/build_international_dataset.py
python tools/create_mod13c2_manifest.py
python tools/write_international_data_audit.py
python tools/run_international_baselines.py
python tools/run_markov_simulation.py
python tools/run_feature_ablation.py
python tools/run_count_models.py
python tools/run_sensitivity_power.py
python tools/write_eid_model_inputs_table.py
python tools/check_eid_model_inputs_table.py
python tools/run_surveillance_quality_sensitivity.py
python tools/run_country_influence.py
python tools/write_calibration_localization.py
python tools/run_detectability_screen.py --iterations 100
python tools/create_eid_figures.py
python tools/build_eid_docx.py
python tools/check_publication_readiness.py
python tools/check_eid_submission_readiness.py --strict
```

Rebuild outputs:

- ECDC manual case table: 142 rows.
- TerraClimate country-year rows: 145 rows, all with at least one feature.
- International modeling table: 142 rows and 97 columns.
- Baseline forecasts: 1,026 quantile rows and 12 metric rows.
- Feature ablation: 995 prediction rows, 35 metric rows, 70 calibration rows,
  35 screening rows.
- Count models: 140 prediction rows, 5 metric rows, 20 tuning rows.
- Surveillance-quality sensitivity: 252 metric rows and 7,122 prediction rows.
- Country influence: 29 leave-one-country-out rows.
- Calibration localization: 420 rows.
- Detectability screen: 24 rows.

## Plan Implementation Matrix

| Planned Gate | Evidence | Status |
| --- | --- | --- |
| EID-only active target | README, project state, submission guide | PASS |
| Repo organized, legacy material removed from active branch | archive branch `codex/archive-pre-eid-cleanup-20260514` | PASS |
| EID Research article framing | manuscript, cover letter, master plan | PASS |
| No active IJHG/fallback target language | text search | PASS |
| No primacy claim | strict checker/manual search | PASS |
| Correct Kazasidis/Jacob attribution | manuscript refs and no incorrect attribution in submission files | PASS |
| No deployable/causal/within-country overclaim | strict checker/manual search | PASS |
| EID model-input Table 1 | `table1_model_inputs.csv`, 38 rows | PASS |
| Table 1 has source/range/lag/missingness | `check_eid_model_inputs_table.py` | PASS |
| Model schematic | `Appendix_Figure_model_schematic.tif` | PASS |
| Surveillance-quality sensitivity | 8 summary scenarios | PASS |
| Belgium/Cyprus separate and combined tests | sensitivity table | PASS |
| Flagged-row indicator test | sensitivity table | PASS |
| COVID-era training-year sensitivity | sensitivity table | PASS |
| Finland/Germany country influence | country influence table | PASS |
| Calibration localization | 420 country/model rows | PASS |
| Detectability screen with null false-positive reporting | maximum null selection probability 0.000 | PASS |
| WIS/coverage/width interpreted jointly | manuscript Results/Discussion and Figure 2 | PASS |
| Penalized Poisson not overpromoted | manuscript reports undercoverage | PASS |
| MODIS exclusion documented | Table 1 and appendix | PASS |
| AI disclosure | manuscript, cover letter, author statements | PASS |
| Ethics statement | manuscript and author statements | PASS |
| Data/code availability | manuscript and author statements | PASS |
| EID Author Checklist reminder | author statements and submission guide | PASS |
| Strict readiness checker | `EID readiness: PASS` | PASS |
| CI parity | workflow updated | PASS |

## Manuscript and Artifact Counts

- Abstract: 129 words.
- Main text: 1,706 words.
- References: 15.
- Model-input Table 1: 38 rows.
- Surveillance-quality sensitivity summary: 8 rows.
- Country influence table: 29 rows.
- Calibration-localization table: 420 rows.
- Detectability-screen table: 24 rows.

Figure QA:

| Figure | Pixel size | DPI | Width |
| --- | ---: | ---: | ---: |
| `Appendix_Figure_model_schematic.tif` | 4740 x 1619 | 600 | 7.90 in |
| `Figure_1.tif` | 4132 x 3336 | 600 | 6.89 in |
| `Figure_2.tif` | 4123 x 2931 | 600 | 6.87 in |
| `Figure_3.tif` | 5828 x 2085 | 600 | 9.71 in |

All figures exceed EID's 300 dpi and 5 inch width requirements.

## Final QA Commands and Results

```powershell
python -m pytest
```

Result: PASS, 32 tests passed.

```powershell
python -m ruff check src tests tools
```

Result: PASS.

```powershell
python tools/check_eid_model_inputs_table.py
```

Result: PASS.

```powershell
python tools/check_eid_submission_readiness.py --strict
```

Result: PASS.

Expected warnings:

- Mailing address/phone still require human portal confirmation.
- DOI must be verified or updated after final archive/version.

```powershell
python tools/check_publication_readiness.py
```

Result: PASS.

```powershell
git diff --check
```

Result: PASS.

## Submission Package Files

- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/figures/Figure_3.tif`
- `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- `docs/submission_eid/tables/table1_model_inputs.csv`
- `docs/submission_eid/tables/table1_model_inputs.md`
- `docs/submission_eid/tables/appendix_surveillance_quality_sensitivity.csv`
- `docs/submission_eid/tables/appendix_country_influence.csv`
- `docs/submission_eid/tables/appendix_calibration_localization.csv`
- `docs/submission_eid/tables/appendix_detectability_screen.csv`
- `docs/submission_eid/reports/surveillance_quality_sensitivity.md`
- `docs/submission_eid/reports/country_influence.md`
- `docs/submission_eid/reports/calibration_localization.md`
- `docs/submission_eid/reports/detectability_screen.md`
- `docs/submission_eid/final_qa_report_eid.md`
- `docs/submission_eid/reproducibility_manifest.md`
- `docs/submission_eid/submission_guide_eid.md`

## Residual Risk

Residual risk is limited to normal submission and peer-review risk, not local
unfinished local implementation.

- The DOI in the manuscript package must be verified against the final clean
  archive.
- The EID portal requires human-entered contact/checklist information.
- DOCX visual QA must be performed in Word because automated text/DOCX rebuilds
  cannot guarantee final journal-layout appearance.
- EID may still desk reject a negative/mixed modeling result; the manuscript
  mitigates that risk by emphasizing public-health surveillance meaning,
  conservative claims, source auditability, model-input transparency,
  sensitivity analyses, and uncertainty calibration.

## Final Determination

Everything in the EID acceptance plan that can be implemented locally has been
implemented and QA'd. The package is locally ready for EID human portal
preparation, excluding only final DOI/archive verification and author/portal
metadata tasks.
