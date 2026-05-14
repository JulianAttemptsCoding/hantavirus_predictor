# EID Final QA Report

Date: 2026-05-14

## Verdict

The local EID submission package is ready for human portal preparation. The
remaining work is not additional modeling or repo organization; it is final
human verification of contact information, journal checklist answers, and DOI
archive matching.

## Passing Checks

| Gate | Result |
| --- | --- |
| Active journal target | Emerging Infectious Diseases Research article |
| Abstract length | 129 words, below 150 |
| Main text length | 1,706 words, below 3,500 |
| References | 15, below 50 |
| Title style | No colon |
| Running head | 30 characters |
| EID model-input Table 1 | Present and checker passes |
| Model schematic | Present as appendix figure |
| Surveillance-quality sensitivity | Belgium, Cyprus, combined, flagged indicator, and COVID-era scenarios present |
| Country influence | Leave-one-country-out analysis present; Finland and Germany prespecified |
| Calibration localization | 2023 country-year interval coverage table present |
| Detectability screen | Null false-positive reporting present |
| Main figures | Three TIFF files, 600 dpi |
| AI disclosure | Present in manuscript, cover letter, and author statements |
| Ethics statement | Present for aggregate public data |
| Data/code availability | Present with DOI verification reminder |
| Strict EID checker | `python tools/check_eid_submission_readiness.py --strict` passes |

## EID-Relevant Interpretation

The manuscript does not claim individual infection prediction, within-country
risk mapping, causal climate attribution, or deployable public-health
forecasting. It presents a conservative public-health modeling result: in a
short, heterogeneous EU/EEA country-year surveillance panel, richer public
covariates did not provide stable, calibrated one-year-ahead improvement over
surveillance-history baselines.

## Submission Files

- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/figures/Figure_3.tif`
- `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- `docs/submission_eid/tables/table1_model_inputs.csv`
- `docs/submission_eid/tables/appendix_surveillance_quality_sensitivity.csv`
- `docs/submission_eid/tables/appendix_country_influence.csv`
- `docs/submission_eid/tables/appendix_calibration_localization.csv`
- `docs/submission_eid/tables/appendix_detectability_screen.csv`
- `docs/submission_eid/reproducibility_manifest.md`

## Human-Only Items

- Confirm corresponding author's full mailing address and phone number in the
  EID portal.
- Verify the final Zenodo DOI points to an archive made from the final clean
  commit.
- Complete the EID author checklist, including AI-use disclosure.
- Open the final DOCX files in Word and visually inspect tables, figure
  legends, special characters, and layout.
