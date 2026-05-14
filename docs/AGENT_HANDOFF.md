# Agent Handoff

Start here after opening the repository.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev,geo]"
python -m pytest
python -m ruff check src tests tools
python tools/check_eid_submission_readiness.py --strict
```

## Read Order

1. `PUBLICATION_MASTER_PLAN.md`
2. `docs/PROJECT_STATE.md`
3. `docs/submission_eid/final_qa_report_eid.md`
4. `docs/submission_eid/submission_guide_eid.md`
5. `docs/submission_eid/reproducibility_manifest.md`
6. `docs/data_dictionary.md`
7. `docs/reviewer_response_playbook.md`
8. `configs/validation_splits.yaml`
9. `configs/data_catalog.yaml`
10. `configs/modeling_plan.yaml`

## Active State

The repository is organized around an EID Research submission package for a
retrospective EU/EEA country-year reported-incidence benchmark, 2019-2023.

The EID-specific local work is implemented:

1. Model-input Table 1 generator and checker.
2. Model/workflow schematic.
3. Surveillance-quality sensitivity for Belgium 2023, Cyprus 2023,
   flagged-row indicator, and COVID-era exclusions.
4. Leave-one-country-out influence analysis, including Finland and Germany.
5. Calibration localization for 2023 predictions.
6. Null-calibrated detectability screen.
7. Strict EID submission readiness checker.
8. Rebuilt manuscript, appendix, figures, cover letter, author statements, and
   DOCX files.

Remaining work is human-only: final contact fields, journal checklist/COI
answers, final Word visual review, and final Zenodo DOI/archive verification.

## Rules

- Do not call the current analysis prospective forecasting.
- Do not claim operational, clinical, individual, county-level, or within-country
  risk prediction.
- Do not make causal climate or land-use claims.
- Do not promote a model on WIS alone.
- Do not revive old non-EID, Overleaf, or LLM archive artifacts on the active
  branch.
- Keep raw/generated data out of git unless a submission snapshot explicitly
  requires it.
- Keep `nasa earthdata acc info.txt` ignored; never print or commit credentials.

## Archive Branch

The pre-cleanup local state is preserved on:

```text
codex/archive-pre-eid-cleanup-20260514
```
