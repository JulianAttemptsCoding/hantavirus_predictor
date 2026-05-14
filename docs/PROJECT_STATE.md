# Project State

Last updated: 2026-05-14

## Active Target

The active project is an *Emerging Infectious Diseases* Research article:

> Sparse annual public EU/EEA surveillance limits calibrated one-year-ahead
> forecasting of reported hantavirus incidence; public covariates do not
> reliably improve over surveillance-history baselines.

This is a retrospective public-data benchmark, not a deployable forecasting
tool.

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

The package now passes the strict local EID readiness checker. Remaining work is
limited to human-only portal/archive verification, including final mailing
address, phone number, final DOI/archive match, and author checklist responses.

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

No local analysis or repo-organization blockers remain. Human-only items before
portal submission:

1. Confirm corresponding author's mailing address and phone number.
2. Verify that the final DOI resolves to the archive matching the final commit.
3. Complete the EID author checklist and conflict-of-interest responses.
4. Open the DOCX files in Word for final visual inspection.

## QA Commands

```powershell
python -m pip install -e ".[dev,geo]"
python -m pytest
python -m ruff check src tests tools
git diff --check
```

Full rebuild commands are in `docs/submission_eid/reproducibility_manifest.md`.
