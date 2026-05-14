# EID Reproducibility Manifest

Generated on: 2026-05-14

Repository: `JulianAttemptsCoding/hantavirus_predictor`

Branch: `main`

Purpose: frozen local submission snapshot for an *Emerging Infectious Diseases*
Research article package. The final archive DOI and repository commit should be
verified immediately before journal upload.

## Software Environment

- Python package manager: `pip`
- Package install target: `python -m pip install -e ".[dev,geo]"`
- Operating system used for this manifest: Windows
- Required geospatial stack: `geopandas`, `shapely`, `pyproj`, `rasterio`
- Figure rendering: `matplotlib`, `Pillow`

## Rebuild Commands

The current submission package is produced by this state-gated command sequence:

```powershell
python tools/create_ecdc_case_table.py --accessed-date 2026-05-13
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
python -m pytest
python -m ruff check src tests tools
```

## Required Snapshot Artifacts

- Manuscript: `docs/submission_eid/manuscript_eid.md`
- Manuscript DOCX: `docs/submission_eid/manuscript_eid.docx`
- Appendix: `docs/submission_eid/supplements/Appendix_methods_eid.md`
- Appendix DOCX: `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- Cover letter: `docs/submission_eid/cover_letter_eid.md`
- Cover letter DOCX: `docs/submission_eid/cover_letter_eid.docx`
- Author statements: `docs/submission_eid/author_statements.md`
- Author statements DOCX: `docs/submission_eid/author_statements.docx`
- Main figures: `docs/submission_eid/figures/Figure_1.tif`,
  `docs/submission_eid/figures/Figure_2.tif`,
  `docs/submission_eid/figures/Figure_3.tif`
- Model schematic: `docs/submission_eid/figures/Appendix_Figure_model_schematic.tif`
- EID model-input table: `docs/submission_eid/tables/table1_model_inputs.csv`
- Sensitivity tables: `docs/submission_eid/tables/appendix_surveillance_quality_sensitivity.csv`,
  `docs/submission_eid/tables/appendix_country_influence.csv`,
  `docs/submission_eid/tables/appendix_calibration_localization.csv`,
  `docs/submission_eid/tables/appendix_detectability_screen.csv`

## Submission Checks

The strict readiness checker verifies:

- Abstract word count is at most 150 words.
- Main text word count is at most 3,500 words.
- Reference count is at most 50.
- Title contains no colon.
- Running head is at most 50 characters.
- EID suitability elements are present: ethics, AI disclosure, data/code
  availability, source audit, model schematic, model-input table, sensitivity
  analyses, exact coverage numerators and denominators, and high-resolution
  figures.
- Submission-facing text contains no active IJHG framing, incorrect literature
  attribution, primacy claim, causal overclaim, or operational prediction claim.

## Human Verification Before Upload

- Verify the final DOI resolves to the clean archive matching the final commit.
- Confirm mailing address and phone number in the EID portal.
- Confirm all author metadata and ORCID information.
- Confirm author approval and journal conflict-of-interest checklist responses.
