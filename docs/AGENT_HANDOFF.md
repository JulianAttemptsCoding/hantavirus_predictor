# Agent Handoff

Start here after opening the repository.

## First Commands

```powershell
git status --short --branch
python -m pip install -e ".[dev,geo]"
python -m pytest
python -m ruff check src tests tools
```

## Read Order

1. `PUBLICATION_MASTER_PLAN.md`
2. `docs/PROJECT_STATE.md`
3. `docs/submission_eid/submission_guide_eid.md`
4. `docs/data_dictionary.md`
5. `docs/reproducibility_manifest.md`
6. `docs/reviewer_response_playbook.md`
7. `configs/validation_splits.yaml`
8. `configs/data_catalog.yaml`
9. `configs/modeling_plan.yaml`

## Active Work

The repository is organized around an EID Research submission package for a
retrospective EU/EEA country-year reported-incidence benchmark, 2019-2023.

Do next:

1. Implement the EID model-input Table 1 generator and checker.
2. Implement the model/workflow schematic.
3. Implement surveillance-quality sensitivity for Belgium 2023, Cyprus 2023,
   flagged-row indicator, and COVID-era exclusions.
4. Implement leave-one-country-out influence, especially Finland and Germany.
5. Implement calibration localization for 2023 predictions.
6. Replace the current detectability screen with a null-calibrated simulation.
7. Add `tools/check_eid_submission_readiness.py`.
8. Rewrite the EID manuscript and appendix after those outputs exist.

## Rules

- Do not call the current analysis prospective forecasting.
- Do not claim operational, clinical, individual, county-level, or within-country risk prediction.
- Do not make causal climate or land-use claims.
- Do not promote a model on WIS alone.
- Do not revive old non-EID, Overleaf, or LLM archive artifacts on the active branch.
- Keep raw/generated data out of git unless a submission snapshot explicitly requires it.
- Keep `nasa earthdata acc info.txt` ignored; never print or commit credentials.

## Archive Branch

The pre-cleanup local state is preserved on:

```text
codex/archive-pre-eid-cleanup-20260514
```
