# An open benchmark for country-level reported hantavirus incidence: retrospective one-year-ahead evaluation under sparse public surveillance

## Abstract

Background: Public hantavirus surveillance is authoritative but sparse, and it
is often unclear whether public environmental covariates improve
country-level reported-incidence prediction over simple surveillance
baselines.

Methods: We assembled an ECDC-only EU/EEA benchmark of 142 country-year rows
for 2019-2023. The unit of analysis is annual country-level reported
hantavirus infection incidence. Public covariates include World Bank
demographic context, FAOSTAT land-use summaries, TerraClimate climate and
water-balance variables, and Natural Earth country boundaries. We evaluated
retrospective one-year-ahead probabilistic predictions using WIS, relative
WIS, 90 percent empirical coverage, interval width, MAE, Brier score for any
case, and MASE where valid.

Results: The data pipeline reconciled ECDC annual totals of 4088, 1693, 4947,
2185, and 1885 cases for 2019-2023. In the primary 2022 validation target,
the all-public feature set had the lowest WIS among ablation models
(mean WIS 74.46; relative WIS 0.99; 90 percent coverage 0.76). In the 2023
test target, the land-use feature set had the lowest WIS among ablation
models (mean WIS 318.55; relative WIS 4.73; 90 percent coverage 0.68), but
coverage remained below the nominal 90 percent level.

Conclusions: The benchmark shows that simple and low-dimensional public-data
models are difficult to beat consistently under sparse annual country-level
surveillance. Negative and mixed covariate results are retained because they
are central to understanding what public EU/EEA country-year data can and
cannot support.

## Background

Hantavirus infection surveillance in Europe is shaped by reservoir ecology,
landscape context, climate and water-balance conditions, and heterogeneous
reporting systems. Authoritative annual reports provide case counts, but they
do not by themselves define a reusable benchmark for testing whether public
covariates improve retrospective prediction.

This study is a public-data benchmark, not a live risk dashboard and not a
clinical or operational alerting system. The task is retrospective
one-year-ahead evaluation of reported country-year incidence.

## Related Work And Novelty

Prior work includes Zeimes et al. on European spatial risk mapping, Kallio et
al. on rodent host dynamics, Reusken and Heyman on factors driving European
hantavirus emergence, Kazasidis, Geduhn, and Jacob on high-resolution German
Puumala warning systems, Glass et al. on remote-sensing precedent for HPS
risk, Allen, McCormack, and Jonsson on rodent infection models, and epidemic
forecast benchmark work including COVID-19 Forecast Hub and weighted interval
score methods.

The novelty here is not a first hantavirus map or a claim of causal climate
effects. The contribution is a frozen, open, source-audited benchmark that
links ECDC country-year labels to public covariates and evaluates calibrated
uncertainty against strong simple baselines.

## Methods

### Data Sources

The primary labels are ECDC Annual Epidemiological Report country-year
hantavirus infection counts for 2019-2023. The benchmark excludes UK rows from
the primary balanced panel because the United Kingdom withdrew from the EU and
ECDC reports no UK data from 2020 onward.

Belgium 2023 is flagged as `not_comprehensive` with quality grade C because
the ECDC report notes a surveillance-system change and no calculated rate.
Cyprus 2023 is flagged as `unspecified` with quality grade C. Other rows are
comprehensive quality grade B in the current seed table.

Public covariates are World Bank rurality and GDP context, FAOSTAT land-use
shares, TerraClimate annual climate and water-balance summaries, and Natural
Earth country boundaries. MODIS NDVI/EVI is not included in the current main
model because quality-masked country-year aggregation has not passed the
pre-registered gate.

### Benchmark Task

For each target year, predictors use information available no later than the
prior year where lagged covariates are required. The primary split trains on
2019-2021, validates on 2022, and tests on 2023. Leave-one-year-out analyses
are reported as sensitivity checks.

### Feature Ablation

Feature sets are nested:

- `surveillance_only`: lagged country and panel surveillance summaries plus
  target-year indicators.
- `context`: surveillance plus lagged World Bank rurality and GDP.
- `land_use`: context plus lagged FAOSTAT land-use shares.
- `climate`: land-use plus lagged TerraClimate variables.
- `all_public`: climate plus public source-quality metadata.

Imputation parameters are learned on training rows only. Constant, duplicate,
high-missingness, and highly correlated predictors are removed before model
fitting. Final modeling feature counts are reported separately from the raw
97-column processed audit table.

### Metrics

Primary metrics are WIS, relative WIS, empirical 90 percent interval coverage,
mean 90 percent interval width, MAE, Brier score for any reported case, and
MASE relative to a last-observed-rate naive denominator where valid.

## Results

The rebuilt manual case table has 142 rows, and the processed analysis table
has 142 rows and 97 raw audit columns. Annual ECDC totals reconcile exactly to
4088, 1693, 4947, 2185, and 1885 cases for 2019-2023.

In feature ablation, richer public covariates improved 2022 WIS but did not
provide a stable, well-calibrated improvement for 2023. The 2023 land-use set
had the lowest ablation WIS, but coverage remained 0.68 against the nominal
0.90 interval. This is reported as a mixed result rather than model
superiority.

Sensitivity analyses exclude non-comprehensive or unspecified surveillance
rows and COVID-era training years where sample size permits. A simulation
screen indicates that covariate detectability is sensitive to effect size and
small sample structure; it is used to frame power, not to validate model skill.

An exploratory penalized Poisson GLM with a population offset was added after
feature ablation. The best 2023 count-model feature set was `land_use`
(mean WIS 159.37; relative WIS 2.37; 90 percent coverage 0.32), which did not
meet the calibration requirements for promotion over simple baselines.

## Discussion

The core finding is that sparse, country-level public surveillance makes
simple baselines difficult to beat reliably. This result is useful for public
health informatics because it discourages overfit claims and highlights the
value of transparent source metadata, calibration, and negative results.

The maps support IJHG framing by showing country-level incidence, surveillance
metadata, predicted versus observed incidence, and uncertainty under an
area-appropriate European projection. They do not imply within-country
variation.

## Limitations

The benchmark has only five annual reporting years. It uses country-level
aggregation, which masks within-country heterogeneity. Reporting systems and
case ascertainment vary. Belgium 2023 is non-comprehensive, Cyprus 2023 has an
unspecified completeness caveat, and COVID-era 2020-2021 reporting may reflect
health-system disruption. Validation is retrospective one-year-ahead, not
prospective. MODIS vegetation claims are excluded until QA-masked aggregation
passes.

## Ethics

This study uses aggregated, publicly available surveillance data at the
country-year level. No individual-level patient data were accessed. Ethical
review was not required for secondary analysis of publicly available aggregate
data under the applicable institutional policy.
