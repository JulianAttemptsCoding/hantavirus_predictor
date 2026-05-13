# Archive Deposition Instructions

Do not deposit or claim a DOI until the human-only account and license choices
are confirmed.

## Before Deposition

1. Confirm destination: Zenodo, OSF, Figshare, or GitHub-Zenodo integration.
2. Confirm the owning account/name.
3. Confirm the release license for code and processed data.
4. Regenerate all data, reports, and figures from tracked scripts.
5. Run final QA: `python -m pytest`, `python -m ruff check src tests tools`,
   `git diff --check`, and the secret scan.
6. Generate SHA-256 checksums for final processed outputs and reports.

## Suggested Release Contents

- Source code and scripts.
- Data dictionary.
- Reproducibility manifest.
- Final processed ECDC benchmark tables if redistribution is license-compatible.
- Figure files and captions.
- Manuscript statements.
- Checksums.

## DOI Wording Placeholder

The final DOI and archive citation will be inserted after deposition is
completed by the confirmed owner account.
