# Final EID QA Report

Date: 2026-05-13

## Verdict

The active EID package is ready for final human portal entry, with one required
author-only item remaining: enter the corresponding author's full mailing address
and phone number in the submission portal and title page if requested.

## EID Format Checks

| Item | Result |
|---|---|
| Article type | Research |
| Manuscript format | Word docx generated |
| Line numbering | Embedded in manuscript docx |
| Abstract length | 138 words |
| Main text length | 3,284 words |
| References | 16 |
| Tables | 2 editable Word tables |
| Figures | 2 separate TIFF files |
| Figure DPI | 600 dpi each |
| Supplement | Statistical methods appendix docx |
| AI disclosure | Included |
| Ethics/funding/conflicts | Included |
| Archive DOI | Resolves: https://doi.org/10.5281/zenodo.20150542 |
| Clean current local archive | `hantavirus_benchmark_eid_submission_2026-05-13.zip` |

## Scientific QA

| Gate | Result |
|---|---|
| ECDC annual total reconciliation | PASS: 2019-2023 totals exactly match ECDC report table |
| Rows | PASS: 142 country-years |
| Quality flags | PASS: 140 grade B, Belgium 2023 and Cyprus 2023 grade C |
| Primary 2023 result | PASS: last-observed country-rate WIS 42.86; coverage 16/28 |
| Negative-binomial tradeoff | PASS: 28/28 coverage with wide intervals |
| Covariate promotion rule | PASS: no covariate-rich model promoted |
| MODIS/vegetation claims | PASS: excluded and explicitly guarded |
| Operational/local/global claims | PASS: active manuscript uses guarded language |

## Command QA

| Command | Result |
|---|---|
| `python -m pip install -e ".[dev,geo]"` | PASS |
| `python tools/create_ecdc_case_table.py --accessed-date 2026-05-13` | PASS, 142 rows |
| `python tools/validate_international_cases.py --strict` | PASS |
| `python tools/build_international_dataset.py` | PASS, 142 rows x 97 columns |
| `python tools/write_international_data_audit.py` | PASS |
| `python tools/run_international_baselines.py` | PASS |
| `python tools/run_feature_ablation.py` | PASS |
| `python tools/run_count_models.py` | PASS |
| `python tools/run_sensitivity_power.py` | PASS |
| `python tools/check_publication_readiness.py` | PASS |
| `python tools/create_eid_figures.py` | PASS |
| `python tools/build_eid_docx.py` | PASS |
| `python -m pytest` | PASS, 26 tests |
| `python -m ruff check src tests tools` | PASS |
| `git diff --check` | PASS |
| Clean archive content check | PASS: Word files, TIFF figures, supplement, processed data, reports included; no secret-name hits |

## Submission Files

- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/submission_guide_eid.md`

## Notes for Submission

Use `submission_guide_eid.md` for the upload sequence. Do not upload the old
Overleaf bundle or legacy ZIP archives. If you create a new repository archive,
prefer `git archive` from a clean commit/tag so ignored local credential files
cannot be included.
