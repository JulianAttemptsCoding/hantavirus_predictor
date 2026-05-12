# Blocker Response Plan

This plan responds to the blocker notes in:

- `potential blockers.txt`
- `potential blockers (2).txt`
- `potential blockers (3).txt`

## Main Strategic Change

The blockers correctly identify the biggest danger: a flashy model could end up predicting rodent proxies, not validated human hantavirus cases. The repo therefore pivots to a staged, evidence-gated framework:

1. Reservoir seroprevalence and trap-success modeling first.
2. Human spillover risk second, only at data-supported resolution.
3. Complex neural models only after simple baselines are beaten.

## Data Blockers

| Blocker | Response |
|---|---|
| NEON serology ends 2019 | Verified. Make serology the primary 2014-2019 label. Use post-2019 trapping only as abundance proxy, not infection truth. |
| NEON geographic/site bias | Use leave-site and leave-domain validation; report failure modes by region and species. |
| Sparse seroprevalence positives | Use binomial/beta-binomial models with effort denominators and partial pooling; avoid deep learning until sample counts justify it. |
| CDC county-level data unavailable | Verified public blocker. County human model is blocked until restricted partner data are supplied. |
| CDC underreporting | Treat NNDSS as reported-case surveillance; do not call it true incidence. |
| MODIS cloud contamination | Use AppEEARS quality flags; prefer site summaries and gap-fill only with documented uncertainty. |
| ERA5 coarseness/rate limits | Defer ERA5. Use Daymet 1 km daily North America weather first. |
| No real-time rodent surveillance | Frame operational forecasts as batch risk updates, not live infection surveillance. |

## Technical Blockers

| Blocker | Response |
|---|---|
| PINN instability | PINN is optional phase 3, never phase 1. Must pass unit tests and beat baselines. |
| ODE solver divergence | Start with hierarchical statistical models and discrete-time state-space models before neural ODEs. |
| PyTorch Geometric/CUDA issues | Avoid graph neural network dependency until graph edges and performance gains are justified. |
| Mixed precision NaNs | Do not use FP16 for physics loss until FP32 baseline is stable. |
| Dask/raster deadlocks | First extract site/county summaries through AppEEARS/Daymet APIs; avoid bulk raster processing until needed. |
| TimesFM unavailable | Outdated as of 2026-05-12; TimesFM 2.5 is public. Still optional and must be benchmarked. |

## Scientific Blockers

| Blocker | Response |
|---|---|
| Synthetic distribution shift | Synthetic data may regularize or test code, but cannot validate real-world skill. |
| R0 identifiability | Any mechanistic parameter estimates must include identifiability analysis and posterior/sensitivity intervals. |
| Sex-structured SEIR overfit | Start without sex structure; add only if it improves held-out serology and is identifiable. |
| 2-year climate lag speculative | Pre-register lag search windows and use nested validation. Do not present lags as causal without causal design. |
| Spatial CV failure | If it fails, the publishable result is restricted-scope forecasting plus explicit non-generalization. |
| Human-to-human Andes module | Keep outside core model; add appendix only for cruise-ship/Andes scenario modeling. |

## Reviewer Blockers

| Reviewer concern | Response |
|---|---|
| "Not enough data for deep learning" | Agree by design. Baselines and hierarchical models come first; deep learning is gated. |
| "Why not SARIMA/SARIMAX?" | SARIMAX is mandatory baseline. |
| "No prospective validation" | Run retrospective validation first, then set up a prospective forecast log before submission if time allows. |
| "No human case validation" | Human claims are limited unless restricted or state-level validation supports them. |
| "Black box risk maps could stigmatize communities" | Use broad risk classes, uncertainty intervals, and ethics review; avoid public county rankings without partner review. |

## Operational Blockers

| Blocker | Response |
|---|---|
| Live feeds required | First product is reproducible batch pipeline, not real-time operations. |
| Public-health trust | Include interpretable baselines, calibration plots, and uncertainty-first outputs. |
| IRB/regulatory concerns | Start IRB/ethics consultation before restricted human data or local risk maps. |
| Compute cost | Make CPU/simple baseline path the required first milestone; GPU models are optional. |

## Go/No-Go Gates

Proceed to manuscript only if:

- Data joins are reproducible and audited.
- Best model beats simple baselines by at least 10 percent mean WIS or has a clear secondary scientific value.
- 90 percent intervals achieve 85-95 percent empirical coverage overall.
- Results survive temporal and spatial holdouts.
- Claims are scoped to the data resolution actually validated.

Stop or re-scope if:

- Serology labels are too sparse after QC.
- Spatial validation collapses without a clear ecological explanation.
- Human case validation is impossible beyond descriptive state-level comparison.
- Complex models do not beat simple baselines.

