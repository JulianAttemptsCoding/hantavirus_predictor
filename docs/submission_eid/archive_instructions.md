# Archive and DOI Instructions — EID Submission

Follow these steps to get the Zenodo DOI needed before final submission.

## Step 1: Make GitHub repo public

Go to https://github.com/JulianAttemptsCoding/hantavirus_predictor/settings
→ Danger Zone → Change repository visibility → Make public.

(OR prepare a private-for-review archive ZIP if you prefer not to make it public.)

## Step 2: Create the EID submission git tag (run once)

```powershell
git tag -a v0.1.0-eid-submission -m "EID submission archive — EU/EEA hantavirus benchmark 2019-2023"
git push origin v0.1.0-eid-submission
```

## Step 3: Deposit on Zenodo

1. Go to https://zenodo.org → log in (free account, can use GitHub OAuth).
2. Click "New upload".
3. If repo is public on GitHub: connect GitHub → select hantavirus_predictor → select tag v0.1.0-eid-submission.
4. If private: zip the repo (`git archive --format=zip HEAD -o hantavirus_benchmark_eid.zip`) and upload the ZIP.
5. Fill metadata:
   - Title: "Public Surveillance Benchmark for Reported Hantavirus Incidence, EU/EEA, 2019-2023 — Analysis Code"
   - Authors: Julian Juan
   - Description: "Code, processed public data tables, and reproducibility scripts for the EID submission."
   - License: MIT
   - Resource type: Software
   - Access: Open Access
6. Click "Reserve DOI" (this gives you the DOI before publishing).
7. Copy the DOI (format: 10.5281/zenodo.XXXXXXX).
8. Publish.

## Step 4: Insert DOI into manuscript and cover letter

Replace `[AUTHOR: INSERT DOI...]` in:
- `docs/submission_eid/manuscript_eid.md` (Methods — Ethics and reproducibility section)
- `docs/submission_eid/cover_letter_eid.md`
- `docs/submission_eid/author_statements.md`

## Step 5: Insert ORCID

If you don't have an ORCID:
1. Go to https://orcid.org → Register (free).
2. Copy your 16-digit ORCID (format: 0000-0000-0000-0000).

Replace `[AUTHOR: INSERT ORCID...]` in:
- `docs/submission_eid/manuscript_eid.md` (Title Page)
- `docs/submission_eid/cover_letter_eid.md`
- `docs/submission_eid/author_statements.md`

## Step 6: Convert manuscript to Word

```powershell
# Install pandoc if not installed: https://pandoc.org/installing.html
# Then from docs/submission_eid/:
pandoc manuscript_eid.md -o manuscript_eid.docx --reference-doc=reference.docx
```

Or paste content into Word manually and apply:
- Font: 12-pt Times New Roman
- Line spacing: Double
- Alignment: Left justified
- Line numbers: Layout → Page Setup → Line Numbers → Continuous
- Tables: Reproduce using Word table tool (Insert → Table)
- Place tables at end of document (after references)
- Place figure legends at end (after tables)
- Figures: attach as separate files in the submission system

## EID Submission Portal

Submit at: https://wwwnc.cdc.gov/eid/page/submit-manuscript

Article type: Research
Section: cover letter dropdown → select appropriate section

## Checklist Before Submitting

- [ ] Abstract ≤ 150 words (currently 135 ✓)
- [ ] Main text ≤ 3,500 words (currently ~3,350 ✓)
- [ ] References ≤ 50 (currently 15 ✓)
- [ ] DOI placeholder replaced with real Zenodo DOI
- [ ] ORCID placeholder replaced with real ORCID
- [ ] Word manuscript: 12-pt Times New Roman, double-spaced, line-numbered
- [ ] Title page complete (not anonymous)
- [ ] One-sentence summary included
- [ ] Keywords included
- [ ] Author biography included
- [ ] Figure legends at end of document
- [ ] Tables at end of document (Word table tool, not images)
- [ ] Figure files separate (Figure_1.tif and Figure_2.tif, both 600 dpi ✓)
- [ ] Cover letter complete with DOI and ORCID
- [ ] AI disclosure included in acknowledgments ✓
- [ ] No "Available from:" in references (all have "Available at:" ✓)
- [ ] Ethics statement complete ✓
- [ ] Funding statement complete ✓
- [ ] Competing interests complete ✓
