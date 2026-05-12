# Source Archive Audit

Audit date: 2026-05-12

Input packages:

- `hanta-pinn-st-v1.0.zip`
- `HANTA-PINN-v1.0-Complete-Package.zip`
- `HANTAVIRUS_PREDICTOR_Complete_Package_v1.0.0.zip`

The archives were extracted to `source_material/llm_archives/extracted/`. Originals remain in the repository root.

## Inventory

After extraction, the source material contains 97 files:

- 53 Python files
- 18 Markdown files
- 9 YAML files
- 1 LaTeX manuscript
- 1 BibTeX file
- supporting Docker, Makefile, setup, CFF, license, and gitignore files

## Package-Level Findings

### HANTA-PINN-v1.0-Complete-Package

Useful:

- Has a compact SEIR/PINN prototype and tests.
- Includes useful reviewer concerns and validation metrics.
- Keeps architecture smaller than the ST/foundation-model packages.

Problems:

- `pytest -q` fails 2 of 6 tests.
- Failure cause: spillover decoder expects 13 input features but receives 6, so the forward pass and loss computation fail.
- Training script uses dummy loaders and is not a real data pipeline.
- Evaluation script explicitly says to implement real data loading.

Decision:

- Preserve for ideas only.
- Do not import its model code into production until the dimensions, tests, and data loaders are rewritten.

### hanta-pinn-st-v1.0

Useful:

- Has more complete thinking around spatiotemporal validation, uncertainty, and data ingestion.
- Identifies the main scientific issue: human cases are too sparse for direct high-resolution forecasting.
- Includes synthetic data validation ideas and graph/PINN integration patterns.

Problems:

- `pytest -q` cannot collect tests without `torchdiffeq`.
- Ingestion functions for MODIS, ERA5, and data alignment are placeholders.
- Framework docs include `pass` blocks and aspirational performance claims.
- Model complexity is not justified before baselines.

Decision:

- Preserve for architecture brainstorming.
- Reuse its validation categories, but require simple baselines first.

### HANTAVIRUS_PREDICTOR_Complete_Package_v1.0.0

Useful:

- Includes a manuscript template, references, data dictionary, visualization ideas, Docker/CI concepts, and a master index.
- Good starting outline for figures and publication materials.

Problems:

- The package is flat, not an importable production layout.
- QA report is self-attested; it claims publication readiness before real data acquisition, model training, or external validation.
- Scripts contain placeholders for actual model predictions and deployment.
- Claims such as "35 percent WIS improvement" and "publication-ready" are not supported by results.

Decision:

- Use its manuscript structure and checklist ideas.
- Do not treat reported QA status as evidence.

## Cross-Archive Synthesis

Reusable concepts:

- Rodent serology should be the primary supervised label where available.
- Human cases should be a secondary validation target because public data are sparse and privacy-limited.
- Weather, vegetation, land cover, and socioeconomic covariates are plausible features.
- WIS/CRPS/coverage are the right family of probabilistic forecast metrics.
- Leave-time-out and leave-domain/site-out validation are mandatory.

Rejected or deferred concepts:

- Full ST-GAT plus PINN plus foundation model as the first implementation.
- Claims that synthetic trajectories solve data scarcity.
- Public county-level human case prediction from CDC data.
- Human mobility features from SafeGraph/Meta unless an approved data license and ethics review exist.
- Andes virus human-to-human transmission in the core U.S. Sin Nombre reservoir model.

## QA Performed

Commands run from the repo:

```powershell
python -m py_compile <all extracted .py files>
pytest -q  # HANTA-PINN-v1.0-Complete-Package/hanta-pinn-package
pytest -q  # hanta-pinn-st-v1.0/hanta-pinn-st
```

Results:

- Python syntax compilation passed for all extracted `.py` files.
- HANTA-PINN tests: 4 passed, 2 failed.
- HANTA-PINN-ST tests: 3 collection errors because `torchdiffeq` is missing.

## Production Rule

Future agents may mine `source_material/` for ideas, equations, or test cases, but production code must live in `src/hantavirus_predictor/` and must pass repository tests.

