# Figure Captions

## Figure 1. Study design

Workflow for constructing the ECDC-only EU/EEA country-year benchmark,
joining public covariates, applying train-only feature screening, and
evaluating retrospective one-year-ahead probabilistic predictions.

## Figure 2. Reported incidence choropleth

Country-level ECDC reported hantavirus infection incidence per 100,000
population in 2023. Boundaries are Natural Earth 1:50m Admin 0 countries,
projected to ETRS89 / LAEA Europe (`EPSG:3035`). The map shows country-year
reported incidence and does not imply within-country precision.

## Figure 3. Surveillance completeness metadata

ECDC surveillance completeness flags for 2023. Belgium is flagged
`not_comprehensive`; Cyprus is flagged `unspecified`; other current ECDC rows
are flagged `comprehensive`.

## Figure 4. Predicted versus observed incidence

Observed 2023 reported incidence and predicted median incidence for the best
2023 feature-ablation model by WIS. Both panels use country-level incidence
per 100,000 population.

## Figure 5. Uncertainty map

Width of the model's 90 percent prediction interval for 2023, expressed per
100,000 population. Wider intervals indicate lower sharpness and should be
interpreted together with empirical coverage.

## Figure 6. Feature ablation skill

Mean WIS and relative WIS for nested feature sets under the primary 2022
validation and 2023 test targets. Lower values indicate better probabilistic
accuracy.

## Figure 7. Calibration and interval width

Empirical interval coverage and 90 percent interval width for nested feature
sets. These panels show whether WIS improvements are accompanied by acceptable
calibration and sharpness.
