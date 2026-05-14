# Project State

Last updated: 2026-05-14

## Active Target

The active project is an *Emerging Infectious Diseases* Research article:

> Sparse annual public EU/EEA surveillance limits calibrated one-year-ahead
> forecasting of reported hantavirus incidence; public covariates do not
> reliably improve over surveillance-history baselines.

This is a retrospective public-data benchmark, not an operational predictor.

## Current Repository State

The active branch has been organized around the EID package. Legacy ZIP
archives, extracted LLM packages, old Overleaf output, and pre-EID drafts are
preserved on:

```text
codex/archive-pre-eid-cleanup-20260514
```

The local EID package currently includes:

- `docs/submission_eid/manuscript_eid.md`
- `docs/submission_eid/manuscript_eid.docx`
- `docs/submission_eid/cover_letter_eid.md`
- `docs/submission_eid/cover_letter_eid.docx`
- `docs/submission_eid/author_statements.md`
- `docs/submission_eid/author_statements.docx`
- `docs/submission_eid/figures/Figure_1.tif`
- `docs/submission_eid/figures/Figure_2.tif`
- `docs/submission_eid/supplements/Appendix_methods_eid.md`
- `docs/submission_eid/supplements/Appendix_methods_eid.docx`
- `docs/submission_eid/submission_guide_eid.md`

The package is an advanced draft. It is not final EID-ready until the missing
modeling-compliance gates in `PUBLICATION_MASTER_PLAN.md` are complete.

## Working Data Facts

- Unit: EU/EEA country-year.
- Years: 2019-2023.
- Rows: 142 country-years.
- Primary outcome: annual reported cases and reported incidence.
- Primary test year: 2023.
- Surveillance-quality caveats: Belgium 2023 and Cyprus 2023.
- Current main result: public covariate models do not beat simple surveillance
  baselines with stable calibration.

## Must-Fix Before Submission

1. Add EID model-input Table 1 with variable ranges, lags, missingness, and sources.
2. Add a model/workflow schematic.
3. Replace coarse sensitivity with separate Belgium, Cyprus, flagged-indicator,
   COVID-era, and country-influence analyses.
4. Add calibration localization for all 2023 test predictions.
5. Redesign the detectability simulation with a null false-positive gate.
6. Add strict EID readiness tooling.
7. Rebuild manuscript, appendix, figures, and DOCX from the upgraded evidence package.

## QA Commands

```powershell
python -m pip install -e ".[dev,geo]"
python -m pytest
python -m ruff check src tests tools
git diff --check
```

Full rebuild commands are in `docs/reproducibility_manifest.md`.
