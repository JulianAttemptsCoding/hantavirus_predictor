# EID Draft QA Report

Date: 2026-05-14

## Verdict

The current EID package is an advanced draft, not final submission-ready.
Formatting artifacts exist, tests pass, and the core negative result is coherent,
but EID modeling-compliance work remains before portal submission.

## Passing Checks

| Gate | Result |
| --- | --- |
| Article type target | Research |
| Abstract length in current draft | <=150 words |
| Main text length in current draft | <=3,500 words |
| References in current draft | <=50 |
| Current figures | TIFF, 600 dpi |
| ECDC annual total reconciliation | PASS in generated reports |
| Rows | 142 country-years |
| Quality flags | Belgium 2023 and Cyprus 2023 flagged |
| MODIS/vegetation claims | Excluded from primary claims |
| Local tests | `python -m pytest` passes |
| Local lint | `python -m ruff check src tests tools` passes |

## Blocking EID Gaps

These must be completed before submission:

1. EID model-input Table 1 with variables, ranges, lags, missingness, and sources.
2. Model/workflow schematic.
3. Separate surveillance-quality sensitivity for Belgium 2023, Cyprus 2023,
   combined exclusion, flagged-row indicator, and COVID-era exclusions.
4. Leave-one-country-out influence analysis, especially Finland and Germany.
5. Calibration localization for every 2023 country-year prediction.
6. Null-calibrated detectability simulation with false-positive reporting.
7. Strict EID readiness checker.
8. Rebuilt manuscript, appendix, DOCX, figures, and final archive after the above.

## Submission Files In Draft Package

- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/submission_guide_eid.md`

## Human-Only Items

- Confirm corresponding author's full mailing address and phone number in the
  portal and title page if required.
- Confirm the final Zenodo DOI points to the final clean submission commit.
- Open the final DOCX in Word and visually inspect line numbering, tables,
  figure legends, special characters, and layout.
