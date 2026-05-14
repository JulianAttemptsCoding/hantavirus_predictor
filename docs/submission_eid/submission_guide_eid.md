# EID Submission Guide

This guide is for the *Emerging Infectious Diseases* upload. The current local
package passes the strict EID readiness checker; remaining work is limited to
human portal details and final DOI/archive verification.

## Submission Target

- Journal: *Emerging Infectious Diseases*
- Article type: Research
- Working title: Sparse Public Surveillance Limits Forecasting of Reported
  Hantavirus Incidence, European Union and European Economic Area, 2019-2023
- Running head: Hantavirus Forecasting Limits
- Current repository/archive DOI in draft files: https://doi.org/10.5281/zenodo.20150542

Before submission, confirm the DOI points to the final clean commit or publish a
new Zenodo version.

Suitability inquiry decision: EID does not list a Research-article
pre-submission inquiry as a required step. Use one only if the author wants an
extra editorial-risk check before portal upload; it is not a local readiness
blocker.

## Draft Files

- Main manuscript: `docs/submission_eid/manuscript_eid.docx`
- Cover letter: `docs/submission_eid/cover_letter_eid.docx`
- Main Figure 1: `docs/submission_eid/figures/Figure_1.tif`
- Main Figure 2: `docs/submission_eid/figures/Figure_2.tif`
- Main Figure 3: `docs/submission_eid/figures/Figure_3.tif`
- Appendix model schematic: `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- Supplementary appendix: `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- Author statements: `docs/submission_eid/author_statements.docx`
- Final QA record: `docs/submission_eid/final_qa_report_eid.md`
- Reproducibility manifest: `docs/submission_eid/reproducibility_manifest.md`

Do not upload archive-branch materials, old ZIP packages, old Overleaf files, or
any pre-EID journal-target files.

## Portal Fields

1. Go to https://wwwnc.cdc.gov/eid/page/submit-manuscript.
2. Start a new manuscript submission.
3. Select article type: Research.
4. Paste the final title, running head, abstract, one-sentence summary, and
   keywords from the manuscript title page.
5. Enter author details:
   - Name: Julian Juan
   - Affiliation: Independent researcher
   - ORCID: 0009-0003-7234-2245
   - Email: bubgaming3@gmail.com
6. Enter the full mailing address and phone number in the portal and title page
   if required. These personal fields cannot be inferred safely from the repo.
7. Upload the Word manuscript, cover letter, and separate TIFF figure files.
8. In the checklist/author questionnaire, disclose AI assistance as stated in
   `author_statements.docx`.

## Final Human Checks

- Strict EID readiness checker passes.
- Open `manuscript_eid.docx` in Word and confirm line numbers are visible.
- Confirm the title page is not anonymous.
- Confirm the abstract is unstructured and <=150 words.
- Confirm main text is <=3,500 words.
- Confirm references are <=50.
- Confirm tables are editable Word tables, not images.
- Confirm figures are separate TIFF files, at least 300 dpi and 5 inches wide.
- Confirm no figure is AI-generated.
- Confirm the Zenodo DOI resolves to the final archive.
- Confirm no credential files or old ZIP archives are uploaded.
