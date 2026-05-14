# Archive and DOI Instructions for EID Submission

Use these steps only after the strict EID readiness gate passes.

## 1. Create A Clean Submission Tag

From a clean active branch:

```powershell
git status --short
git tag -a v0.1.0-eid-submission -m "EID submission archive - EU/EEA hantavirus benchmark 2019-2023"
git push origin v0.1.0-eid-submission
```

## 2. Build A Clean Archive

Preferred:

```powershell
git archive --format=zip HEAD -o hantavirus_benchmark_eid_submission.zip
```

Do not archive the working directory directly. The working directory can contain
ignored generated data, caches, or credentials.

Never include:

- `.env`
- credential files
- `nasa earthdata acc info.txt`
- old ZIP packages
- archive branch materials
- old Overleaf files
- pre-EID journal-target files

## 3. Deposit On Zenodo

1. Go to https://zenodo.org and log in.
2. Create a new upload or a new version of the existing record.
3. Upload the clean `git archive` ZIP.
4. Fill metadata:
   - Title: "Sparse Public Surveillance Limits Forecasting of Reported Hantavirus Incidence,
     European Union and European Economic Area, 2019-2023"
   - Creator: Julian Juan
   - Resource type: Software or Dataset, depending on deposited contents.
   - License: MIT for code; preserve source-data attribution in metadata.
   - Description: "Code, public-data processing scripts, manuscript support files,
     and reproducibility materials for an EID submission."
5. Reserve or publish the DOI.

Current draft DOI in local files:

```text
https://doi.org/10.5281/zenodo.20150542
```

Before submission, verify that this DOI points to the final archive version. If
a new version is published, replace the DOI in:

- `docs/submission_eid/manuscript_eid.md`
- `docs/submission_eid/cover_letter_eid.md`
- `docs/submission_eid/author_statements.md`

## 4. Verify DOI

```powershell
python -c "import urllib.request; print(urllib.request.urlopen('https://doi.org/10.5281/zenodo.20150542').geturl())"
```

## 5. Final Manuscript Packaging

Use `tools/build_eid_docx.py` to rebuild DOCX files after the final Markdown
changes. Then open the DOCX in Word and confirm:

- 12-point Times New Roman or EID-acceptable formatting.
- Double spacing.
- Continuous line numbers.
- Editable Word tables.
- Tables at the end of the manuscript.
- Figure legends at the end of the manuscript.
- Figures uploaded as separate TIFF files.

## 6. Human-Only Fields

Confirm:

- ORCID is correct.
- Corresponding author email is correct.
- Full mailing address and phone number are entered in the portal and title page
  if required.
