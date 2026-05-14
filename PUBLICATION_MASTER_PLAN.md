# EID Publication Master Plan

Last updated: 2026-05-14

Status: implemented and QA-passed for local EID submission preparation. The only
remaining items are human-only journal/author/archive tasks: final mailing
address and phone number, EID checklist/COI answers, final Word visual review,
and final Zenodo archive/DOI verification.

## Target

- Journal: *Emerging Infectious Diseases*.
- Article type: Research.
- Scope: retrospective EU/EEA country-year reported hantavirus incidence,
  2019-2023.
- Main claim: public demographic, land-use, climate, and source-quality
  covariates did not provide stable, calibrated one-year-ahead improvement over
  surveillance-history baselines; the public-health finding is a surveillance
  metadata and reporting bottleneck, not a deployable predictor.
- Nonclaims: no individual infection prediction, no clinical tool, no
  within-country risk map, no dashboard product claim, no causal climate claim, and no
  prospective validation claim.

## Current EID Requirements Checked

Current EID guidance was rechecked on 2026-05-14.

- Research article text limit: 3,500 words.
- Abstract limit: 150 words, unstructured.
- Reference limit: 50.
- Required submission components: EID Author Checklist, abstract, cover letter,
  running head, one-sentence summary, keywords, first-author biographical sketch,
  corresponding author contact information, and ORCID for first/corresponding
  authors.
- Figures: separate high-resolution files, at least 300 dpi and at least 5
  inches wide.
- Tables: Word table tool at final submission.
- Modeling/reporting: enough method detail for replication; model-input table
  with values/ranges and sources; schematic/workflow; sensitivity analysis
  beyond one-at-a-time checks; transparent chatbot/AI disclosure in
  acknowledgments/checklist.

Primary sources:

- https://wwwnc.cdc.gov/eid/article-types
- https://wwwnc.cdc.gov/eid/page/authors-resource-instructions
- https://wwwnc.cdc.gov/eid/pdfs/styleguide.pdf

## Implementation Trace

| Gate | Implementation | Status |
| --- | --- | --- |
| EID-only active target | `README.md`, `docs/PROJECT_STATE.md`, `docs/submission_eid/submission_guide_eid.md` | PASS |
| Title without colon and place/time stated | `docs/submission_eid/manuscript_eid.md` | PASS |
| Running head <=50 characters | `Hantavirus Forecasting Limits` | PASS |
| One-sentence summary | manuscript title page | PASS |
| Abstract <=150 words | 129 words | PASS |
| Main text <=3,500 words | 1,706 words | PASS |
| References <=50 | 15 references | PASS |
| Public-health meaning clear | Abstract, Introduction, Discussion, cover letter | PASS |
| Reported cases only | Title, abstract, methods, tables, figure legends | PASS |
| No operational/causal/within-country claims | strict checker and manual search | PASS |
| ECDC totals reconcile | 4,088; 1,693; 4,947; 2,185; 1,885 | PASS |
| EID model-input Table 1 | `docs/submission_eid/tables/table1_model_inputs.csv` and `.md` | PASS |
| Table 1 source/range/lag/missingness fields | `tools/check_eid_model_inputs_table.py` | PASS |
| Model/workflow schematic | `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif` | PASS |
| Surveillance-quality sensitivity | Belgium, Cyprus, combined, flagged indicator, COVID-era scenarios | PASS |
| Finland/Germany influence | `docs/submission_eid/tables/appendix_country_influence.csv` | PASS |
| Calibration localization | `docs/submission_eid/tables/appendix_calibration_localization.csv` | PASS |
| Detectability screen | null false-positive reporting in `appendix_detectability_screen.csv` | PASS |
| MODIS exclusion | Table 1, appendix, manuscript limitations | PASS |
| WIS/coverage/width interpreted jointly | Results, Discussion, Table 2, Figure 2 | PASS |
| AI disclosure | manuscript acknowledgments, cover letter, author statements | PASS |
| Ethics statement | manuscript Methods and author statements | PASS |
| Data/code availability | manuscript and author statements, with DOI verification reminder | PASS |
| Cover letter | `docs/submission_eid/cover_letter_eid.md` and `.docx` | PASS |
| Appendix self-contained | `docs/submission_eid/supplements/Appendix_methods_eid.md` and `.docx` | PASS |
| Figures high resolution | 600 dpi, all >5 inches wide | PASS |
| Strict EID readiness checker | `tools/check_eid_submission_readiness.py --strict` | PASS |
| Regression tests | `python -m pytest` | PASS |
| Lint | `python -m ruff check src tests tools` | PASS |
| Whitespace | `git diff --check` | PASS |

## Submission Package

- Manuscript: `docs/submission_eid/manuscript_eid.docx`
- Cover letter: `docs/submission_eid/cover_letter_eid.docx`
- Author statements: `docs/submission_eid/author_statements.docx`
- Appendix: `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- Figures: `docs/submission_eid/figures/Figure_1.tif`,
  `docs/submission_eid/figures/Figure_2.tif`,
  `docs/submission_eid/figures/Figure_3.tif`
- Appendix schematic: `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- Evidence tables and reports: `docs/submission_eid/tables/` and
  `docs/submission_eid/reports/`
- Final QA report: `docs/submission_eid/final_qa_report_eid.md`
- Reproducibility manifest: `docs/submission_eid/reproducibility_manifest.md`

## Final Local QA Commands

```powershell
python -m pytest
python -m ruff check src tests tools
python tools/check_eid_model_inputs_table.py
python tools/check_eid_submission_readiness.py --strict
git diff --check
```

## Human-Only Preupload Checklist

- Confirm corresponding author's mailing address and phone number.
- Verify the final Zenodo DOI resolves to an archive matching the final clean
  commit.
- Complete the EID Author Checklist, including AI-use disclosure.
- Complete conflict-of-interest and funding fields in the portal.
- Open the DOCX files in Word and visually inspect title page, line numbering,
  editable tables, figure legends, and special characters.
- Upload figures as separate TIFF files.

## Acceptance Logic

The paper is positioned as a disciplined negative/mixed surveillance-modeling
result. It is EID-compatible because it explains what the findings mean for
public health: coarse, heterogeneous public country-year reporting cannot
support confident pan-European annual hantavirus forecasting claims without
better completeness metadata, longer comparable panels, and calibrated
uncertainty reporting.
