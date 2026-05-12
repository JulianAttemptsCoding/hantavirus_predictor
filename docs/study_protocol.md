# Study Protocol Draft

Status: draft for future agent refinement.

## Study Question

Can public ecological, climate, and land-cover data forecast rodent hantavirus seroprevalence and spillover-risk proxies better than simple baselines, with calibrated uncertainty?

## Primary Outcome

NEON site-month rodent hantavirus seroprevalence from `DP1.10064.001`, aggregated by site, month, and reservoir species where sample size supports species-specific modeling.

## Secondary Outcomes

- Rodent abundance/trap-success proxy from NEON `DP1.10072.001`.
- State-level reported human hantavirus cases from CDC/NNDSS for external plausibility.
- County-level human cases only if restricted data are supplied and approved.

## Exclusions

- Individual clinical risk prediction.
- Public county-level human case prediction without partner data.
- Andes virus human-to-human outbreak modeling in the core U.S. reservoir model.

## Primary Validation

Rolling temporal validation over the serology years, plus spatial leave-site/domain-out validation.

## Primary Metrics

- Weighted interval score.
- Empirical coverage for 50, 80, and 90 percent intervals.
- MAE/RMSE for point summaries.
- Calibration diagnostics.

## Model Promotion Criteria

A complex model can enter the main manuscript only if it improves mean WIS by at least 10 percent over the best simple baseline and keeps 90 percent empirical coverage between 85 and 95 percent overall.

## Ethics and Communication

Risk maps must be reported with uncertainty and broad classes. Do not publish county rankings or operational warnings without public-health partner review.

