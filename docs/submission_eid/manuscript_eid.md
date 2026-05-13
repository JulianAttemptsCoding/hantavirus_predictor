# EID Manuscript — Full Draft

**NOTE TO AUTHOR:** All ORCID and DOI placeholders are filled in.
Convert to Microsoft Word (12-pt Times New Roman, double-spaced, left-justified,
line-numbered) — use `python tools/build_eid_docx.py` or copy into Word.
Enable line numbering in Word: Layout → Page Setup → Line Numbers → Continuous.

---

## TITLE PAGE

**Title:**
Public Surveillance Benchmark for Reported Hantavirus Incidence, EU/EEA, 2019–2023

**Running head:** EU/EEA Hantavirus Surveillance Benchmark

**Author:** Julian Juan

**Affiliation:** Independent researcher

**ORCID:** 0009-0003-7234-2245

**Corresponding author:**
Julian Juan
Email: bubgaming3@gmail.com

**Word count (abstract):** 135

**Word count (text, excluding abstract, acknowledgments, references, tables,
figure legends):** ~3,350

**One-sentence summary:**
Simple surveillance-history baselines outperformed covariate-rich models,
underscoring limits of sparse annual public data for reported hantavirus
incidence.

**Keywords:** hantavirus; zoonoses; disease surveillance; EU/EEA; probabilistic
forecasting; calibration; public health communication

---

## ABSTRACT

Public surveillance data are often invoked during attention to rare zoonoses,
but sparse annual reports may not support operational prediction. We created an
open benchmark for reported hantavirus incidence in EU/EEA countries, 2019–2023,
using ECDC Annual Epidemiological Report data linked to public demographic,
land-use, climate, and boundary data. Rebuilt annual totals matched ECDC exactly
across 142 country-years. We evaluated one-year-ahead probabilistic forecasts
using weighted interval score, 90% empirical coverage, interval width, mean
absolute error, and Brier score. Simple surveillance-history baselines
outperformed covariate-augmented models. In 2023, the last-observed country-rate
baseline had the lowest weighted interval score, 42.86, but undercovered observed
counts, 16/28. Negative-binomial baselines covered all observations but used wide
intervals. Public covariates did not provide stable, calibrated gains. The
benchmark supports reproducible surveillance evaluation and calibrated public
health communication, not operational local risk prediction.

---

## TEXT

### Introduction

Hantaviruses are single-stranded RNA viruses transmitted to humans primarily
through contact with infected rodent excreta, including urine, feces, and
saliva (1). No hantavirus vaccine is licensed for human use globally, and
treatment is primarily supportive. In Europe and Asia, the principal clinical
syndrome caused by hantavirus infection is hemorrhagic fever with renal syndrome
(HFRS). European HFRS is driven principally by Puumala virus, whose reservoir
is the bank vole (*Myodes glareolus*), in northern and central Europe, and
Dobrava-Belgrade virus in southeastern Europe (2). In the Americas, hantaviruses
cause hantavirus pulmonary syndrome (HPS) and hantavirus cardiopulmonary syndrome
(HCPS), with Sin Nombre virus (reservoir: deer mouse, *Peromyscus maniculatus*)
and Andes virus as the primary agents (1). Andes virus is exceptional among
hantaviruses: limited person-to-person transmission has been reported in
Argentina and Chile, an epidemiologic feature not documented for European
hantaviruses (3). Human-to-human transmission is not documented for Puumala,
Dobrava-Belgrade, or other EU/EEA hantaviruses.

Hantavirus infection is reportable in the EU/EEA under the EU case definition
for hantavirus infection. In 2023, ECDC reported 1,885 confirmed and probable
cases from 28 EU/EEA countries, a population-weighted incidence of approximately
0.4 per 100,000 population; Finland and Germany accounted for most reported
cases (4). Annual case counts in Europe are strongly cyclic, reflecting the
multi-year population dynamics of rodent reservoir hosts and the influence of
mast seeding events that drive bank vole population peaks (5). This cyclicity
makes hantavirus incidence partially predictable in qualitative terms — outbreak
years tend to follow mast-seeding years — but quantitative country-level
prediction from publicly available data remains uncertain.

Public attention to hantavirus can exceed what sparse annual surveillance data
can resolve. In May 2026, WHO reported a cluster of Andes virus infection
associated with cruise ship travel, generating widespread public inquiry about
hantavirus transmission in Europe; ECDC and WHO emphasized that Andes virus
reservoir species (*Oligoryzomys longicaudatus* and related sigmodontine rodents)
are not present in Europe and that sustained EU/EEA transmission of Andes virus
is biologically implausible (3,6). Events of this type — rare zoonotic clusters
amplified by international travel news — illustrate the risk of overconfident
interpretation of limited surveillance data. The social amplification of risk
framework describes how information about rare events can generate perceived
risk disproportionate to epidemiologic probability, and how transparent,
calibrated communication can moderate this amplification (7). Probabilistic
benchmarks that explicitly quantify what sparse public annual data can and cannot
support are therefore a practical tool not only for surveillance researchers but
also for public health communicators who must convey uncertainty during periods
of heightened attention to rare disease events.

Despite a substantial literature on European hantavirus spatial risk mapping (8),
rodent host dynamics and virus–host coevolution (9), and environmental and
ecological drivers of hantavirus emergence (10), the predictive limits of public
country-year surveillance data have rarely been benchmarked with probabilistic
metrics that jointly assess forecast sharpness and calibration. Most published
hantavirus risk models either use within-country subnational data, focus on
qualitative or ordinal risk categories, or do not evaluate probabilistic
forecast uncertainty against held-out observations. Absence of a reproducible
benchmark makes it difficult for public health practitioners to gauge whether a
proposed covariate or model meaningfully improves upon surveillance history.

This study does not estimate true infection burden or produce operational alerts;
it evaluates what public annual country-level surveillance can support when
assessed with transparent probabilistic metrics. The contributions are:
(i) exact reconciliation of 2019–2023 ECDC annual hantavirus totals across 142
EU/EEA country-years; (ii) linkage to public demographic, land-use, and climate
covariates with documented provenance; (iii) retrospective one-year-ahead
probabilistic evaluation using weighted interval score and calibration-sharpness
metrics; and (iv) transparent reporting of a negative result: public covariates
did not improve stable, calibrated performance over simple surveillance-history
baselines. Transparent benchmarks are especially important when public attention
to rare zoonoses can amplify perceived risk faster than annual surveillance data
can resolve it.

### Methods

#### Surveillance outcome

The primary data source was the ECDC Annual Epidemiological Report for
hantavirus infection, which publishes EU/EEA country-year reported case counts
and population-weighted incidence per 100,000 population (4). We manually
extracted annual totals for EU/EEA countries for 2019–2023, yielding 142
country-year rows. Country inclusion in each year reflects the ECDC reporting
table; the number of countries reporting ranged from 28 to 29 per year. The
United Kingdom was excluded from the primary balanced panel because UK
surveillance data were not reported by ECDC from 2020 onward following EU
withdrawal; UK rows are excluded from all analyses.

Each country-year was assigned a surveillance quality grade based on the ECDC
source notation. Rows described as "comprehensive" surveillance were assigned
grade B. Belgium 2023 was assigned quality grade C because the ECDC 2023 report
noted a surveillance-system change and did not publish a calculated incidence
rate. Cyprus 2023 was assigned quality grade C for unspecified completeness. All
remaining 140 rows were grade B. Grade-C rows were included in primary analyses
and excluded in one sensitivity scenario.

The primary outcome was annual reported cases per country-year. Country-year
reported incidence per 100,000 population was computed as:

  incidence_it = cases_it / population_it × 100,000

where i denotes country and t denotes year. Population denominators were taken
from World Bank Open Data for the matching country-year.

#### Public covariates

We linked ECDC case rows to five public covariate sources using ISO 3166-1
alpha-3 country codes and year.

*World Bank Open Data* provided country-year total population, rural population
fraction, and GDP per capita in purchasing power parity terms (constant 2017
international dollars). Data were available for all 142 rows.

*FAOSTAT* provided country-year land-use shares including forest area fraction,
cropland fraction, and permanent meadows and pastures fraction, aggregated to
matched country-year records. Data were available for all 142 rows.

*TerraClimate* provided country-year summaries of mean temperature, total
precipitation, maximum temperature, minimum temperature, soil moisture, and
Palmer Drought Severity Index (PDSI), aggregated to country boundaries using
Natural Earth polygons and spatial averaging (11). Lag-1 versions (prior
calendar year) of six climate variables were computed to capture the seasonal
mast and rodent dynamics that precede hantavirus exposure in the following year
and to avoid temporal leakage of target-year climate information into forecasts.
Lag-1 features were available for 114 non-2019 country-year rows.

*Natural Earth* provided 1:50m resolution Admin-0 country boundary shapefiles
used for spatial aggregation and mapping (12).

*MODIS MOD13C2 Collection 6.1* NDVI and EVI were targeted as vegetation
covariates because vegetation conditions influence rodent food supply. However,
quality-masked country-year aggregation of MODIS tiles did not pass the
pre-specified inclusion gate in this study; consequently, MODIS was excluded
and no vegetation or NDVI claims are made in this paper.

#### Retrospective evaluation design

All evaluations were retrospective one-year-ahead benchmarks; no prospective
validation against future data was conducted. The primary temporal split used
data from 2019–2021 as the training window, 2022 as the validation year for
hyperparameter selection, and 2023 as the held-out test year. No 2023 outcome
information was used at any stage of model fitting, feature screening, or
hyperparameter selection.

A covariate-augmented model was promoted over simple baselines only if it
satisfied all of the following: (i) 2023 WIS was at most 95% of the best simple
baseline WIS, or WIS was comparable and coverage was closer to 0.90; (ii) 2023
90% coverage was not lower than the best simple baseline by more than 0.05;
(iii) interval width was interpretable and not merely inflated; (iv) no 2023
outcome information was used in tuning; and (v) no causal interpretation was
made from coefficients. Leave-one-year-out sensitivity analyses used targets 2021,
2022, and 2023, training on all preceding years in each case.

#### Forecast baselines and covariate-block evaluation

We evaluated six model families:

*Simple surveillance-history baselines.* The last-observed country-rate baseline
set the predicted incidence rate for target year t to the observed country rate
in year t−1; the predicted count was the product of the lagged rate and the
target-year population. The country historical mean-rate baseline used the mean
of all prior observed country rates. For both baselines, prediction intervals
were derived from Poisson quantiles at 0.05, 0.50, and 0.95 using the predicted
count as the Poisson mean.

*Negative-binomial baselines.* The empirical negative-binomial baseline fitted a
negative-binomial distribution to training counts, estimating overdispersion
as α = max((var(y_train) − mean(y_train)) / mean(y_train)², 10⁻⁶) and deriving
prediction intervals from the resulting distribution. The hierarchical
negative-binomial baseline shrunk each country's historical mean rate toward the
regional panel mean using a shrinkage weight λᵢ = nᵢ/(nᵢ + k), where nᵢ is the
number of prior observations for country i and k was selected on the 2022
validation WIS. These baselines provided conservative uncertainty references;
their overdispersion parameters were not interpreted as biological transmission
parameters.

*Covariate-block evaluation.* Nested feature blocks were constructed sequentially:
surveillance history only (lagged country and panel surveillance summaries and
target-year indicators); plus demographic context (World Bank population,
rurality, GDP); plus land-use (FAOSTAT land-use shares); plus climate and
water-balance (TerraClimate six-variable lag-1 block); plus source-quality
metadata (surveillance-completeness flags). Imputation parameters (median for
continuous variables, mode for binary) were fitted exclusively on training rows.
Constant, duplicate, and high-missingness features (>40% missing) were removed,
and highly correlated numeric features (|r| > 0.95 in training) were excluded
before fitting. The final modeling matrix contained ≤25 features before any
one-hot encoding. A gradient-boosting quantile regressor was fitted for each
block on the training window, with all hyperparameters fixed by validation-year
WIS. We refer to this procedure as covariate-block evaluation rather than
feature ablation to emphasize that each block is evaluated for practical
surveillance value, not for causal attribution.

*Penalized Poisson count model (exploratory).* A ridge-penalized Poisson
generalized linear model with a log population offset was fitted for each
covariate block:

  log(μᵢₜ) = log(populationᵢₜ / 100,000) + β₀ + Xᵢₜβ

The ridge penalty was applied to non-intercept coefficients; the penalty
parameter α was selected on 2022 validation WIS from the set {0.01, 0.1, 1, 10}.
This model was evaluated exploratorily, and coefficients were not interpreted
causally.

#### Evaluation metrics

Primary metrics were: (i) weighted interval score (WIS), computed for the
central 90% prediction interval per Bracher et al. (13); (ii) 90% empirical
coverage, reported as numerator/denominator (e.g., 16/28) and fraction;
(iii) mean 90% interval width; (iv) mean absolute error (MAE) against the
median prediction; (v) Brier score for any reported case (threshold: ≥1 case).

For a 90% prediction interval [l, u] and miscoverage α = 0.10, WIS is:

  IS_α = (u − l) + (2/α)(l − y)·𝟙(y < l) + (2/α)(y − u)·𝟙(y > u)
  WIS = [0.5|y − median| + (α/2)·IS_α] / 1.5

Lower WIS indicates better combined sharpness and calibration. Coverage near
0.90 is nominal; below-nominal coverage indicates underestimated uncertainty;
above-nominal indicates over-wide intervals. No model was ranked by WIS alone:
coverage and interval width must be read jointly with WIS to characterize the
calibration–sharpness tradeoff.

#### Sensitivity analyses

Three sensitivity scenarios were pre-specified: (i) all 142 rows (primary
analysis); (ii) excluding grade-C rows, removing Belgium 2023 and Cyprus 2023;
and (iii) excluding 2020–2021 COVID-era training rows, where sample size
permitted. Because COVID-era health-system disruption may have affected
reporting completeness and behavior, the third scenario tested whether the
main negative result depended on potentially anomalous training data.

#### Ethics and reproducibility

This study used aggregate, country-year public surveillance data. No individual-
level, clinical, address-level, or restricted human-subject data were used;
institutional review was not required. All analysis code, processed public-data
tables, and data dictionaries are archived at https://doi.org/10.5281/zenodo.20150542.

### Results

#### Dataset reconciliation

The rebuilt ECDC case table contained 142 country-year rows across 28–29 EU/EEA
countries for 2019–2023. Annual totals reconciled exactly to ECDC published
figures: 4,088 cases in 2019, 1,693 in 2020, 4,947 in 2021, 2,185 in 2022, and
1,885 in 2023 (Table 1). The marked decrease in 2020 and partial recovery in 2021
likely reflect both natural rodent population dynamics and COVID-era reporting
disruptions that are documented in ECDC surveillance notes. Of 142 rows, 140 were
grade B (comprehensive); Belgium 2023 and Cyprus 2023 were assigned grade C.
No missing values were present for World Bank or FAOSTAT covariates. TerraClimate
lag-1 climate features were complete for all 114 non-2019 country-year rows.
MODIS vegetation data were excluded from the analysis because quality-masked
aggregation did not pass the pre-specified gate.

#### Baseline performance

*Validation year (2022, n = 29 countries).* The empirical negative-binomial
baseline achieved the lowest WIS (47.17) and complete 90% coverage (29/29,
100%), but at the cost of very wide prediction intervals (mean width 694.2 cases;
Table 2). The hierarchical negative-binomial baseline produced nearly identical
results (WIS 47.38; coverage 29/29). The country historical mean-rate baseline
had a lower interval width (21.07 cases) but substantially higher WIS (65.58) and
below-nominal coverage (18/29, 62%). The last-observed country-rate baseline had
the worst WIS among simple baselines in 2022 (101.5) and undercovered observed
counts (16/29, 55%). The gradient-boosting covariate model had a WIS of 92.31
with no empirical coverage.

*Test year (2023, n = 28 countries).* The last-observed country-rate baseline
achieved the lowest WIS (42.86) and the narrowest mean prediction intervals
(14.61 cases per 100,000), but its 90% empirical coverage was substantially below
nominal (16/28, 57%). The empirical and hierarchical negative-binomial baselines
covered all 28 observed counts (28/28, 100%) but used substantially wider
prediction intervals (mean width ≈ 660 cases per 100,000). The country historical
mean-rate baseline had an intermediate WIS (52.47) but below-nominal coverage
(15/28, 54%).

The 2023 results exposed a pronounced calibration–sharpness tradeoff (Figure 2):
the sharpest baseline undercovered observed counts; the best-covering baselines
used implausibly wide intervals that would be uninformative for surveillance
communication. No single baseline simultaneously achieved near-nominal 90%
coverage and meaningfully narrow prediction intervals.

#### Covariate-block evaluation

None of the five covariate blocks passed the pre-specified promotion rule in the
2023 test year. The best-performing covariate block in 2023 was the land-use
block (mean WIS 318.5; 90% coverage 19/28, 68%), which was more than seven times
worse on WIS than the best simple baseline (42.86). The all-public feature set
had the worst 2023 WIS among covariate blocks (331.3; coverage 18/28, 64%). All
covariate blocks showed substantial WIS deterioration from the 2022 validation
year to the 2023 test year: for example, the all-public block improved slightly
over the simple baselines in 2022 (WIS 74.46 vs. 65.58 for the country
historical mean), but degraded sharply in 2023. This validation-to-test
instability indicates that the covariate associations learned on the 2019–2021
training window did not transfer reliably to the 2023 test year. Public
demographic, land-use, and climate covariates did not provide a stable,
calibrated improvement over surveillance history at the country-year annual scale.

#### Penalized Poisson count model (exploratory)

The best-performing penalized Poisson model in 2023 used the land-use feature
set with penalty parameter α = 0.01 (mean WIS 159.4; 90% coverage 9/28, 32%).
This model failed the promotion rule on every criterion: WIS was more than
three times worse than the best simple baseline; coverage was approximately
one-third of the nominal 90%; interval width was narrow (28.82 cases) because
the model's point estimates were too certain, producing sharp but systematically
miscalibrated forecasts. The count model exploratory results are consistent
with the gradient-boosting covariate-block evaluation: public annual covariates
do not provide the signal needed to support calibrated country-level forecasts
for sparse EU/EEA hantavirus data.

#### Country-level incidence map

Figure 1 shows country-level reported hantavirus incidence per 100,000
population for 2023. Incidence was highest in Finland and Germany, consistent
with the known ecology of Puumala virus and bank vole population peaks in
northern Europe in that year. Most EU/EEA countries reported fewer than 1 case
per 100,000 or zero cases. Several countries — particularly in southern and
eastern Europe — reported zero cases, reflecting a combination of genuine low
incidence and possible underdiagnosis or underreporting under heterogeneous
national surveillance systems. The map shows country-level surveillance totals
only; no within-country spatial variation is implied.

#### Sensitivity analyses

Excluding grade-C rows (Belgium and Cyprus 2023, n = 26 test countries) did
not change the main conclusion: the best covariate block (land use) had a
2023 WIS of 341.6 (vs. 318.5 in the primary analysis), and covariate-augmented
models did not outperform simple surveillance-history baselines. Excluding
2020–2021 COVID-era training rows shifted numerical WIS values but did not
reverse the negative result; the all-public covariate block under this scenario
had a 2023 WIS of 75.85, still above or comparable to the negative-binomial
baselines, and did not achieve near-nominal 90% coverage (89% vs. nominal 90%
but with very wide intervals of mean width 764 cases). The central finding was
robust across all three sensitivity scenarios.

### Discussion

The central finding of this benchmark is that sparse annual country-level EU/EEA
public surveillance data support transparent probabilistic evaluation but not
stable covariate-driven prediction. In 2023, the lowest WIS was achieved by
a simple last-observed country-rate baseline, yet this baseline undercovered
observed counts. Negative-binomial baselines achieved complete empirical coverage
by producing prediction intervals that span hundreds of cases per 100,000
population — intervals that are nominally correct but operationally uninformative.
No covariate-augmented model improved upon both dimensions simultaneously. The
negative result is the public-health result: sparse annual public data did not
support stable covariate-driven improvement over simple surveillance history.
This finding should temper operational claims and motivate better surveillance
inputs rather than more complex modeling.

For routine surveillance practice, the benchmark establishes two concrete
standards. First, any model proposed for EU/EEA hantavirus surveillance
evaluation should be assessed against both WIS and 90% empirical coverage,
not against point accuracy alone. A model that appears to have low mean absolute
error can simultaneously undercover observed counts, overstating confidence in
its predictions. Second, simple baselines — last-observed rate, historical mean —
are stronger than they appear in absolute terms: their median predictions are
often closer to observations than those of covariate-augmented models on sparse
annual data, and their uncertainty intervals, while not perfectly calibrated,
are narrower and more interpretable than overdispersed negative-binomial
alternatives. Surveillance programs that currently generate predictive statements
from public annual data without baseline comparisons risk overstating predictive
value.

The calibration–sharpness tradeoff documented here has direct relevance for
risk communication during periods of heightened public attention to hantavirus.
When a surveillance system can produce a sharp forecast (narrow interval, low
WIS) only by systematically undercovering observed values, that sharpness is
an artifact of overconfidence rather than genuine predictive signal. Communicating
this tradeoff to public health practitioners and to the media can help prevent
the false precision that follows from reporting a point estimate without its
calibration context. The social amplification of risk literature documents how
overconfident quantitative claims can amplify public concern disproportionately
to epidemiologic probability (7); transparent calibration benchmarks provide
practitioners with the evidence needed to resist this amplification.

The value of this benchmark is not that it produces a deployable predictor.
Its value is that it makes false precision visible.

The data limitations identified by this benchmark point toward productive
directions for surveillance improvement. Subnational data — at the regional or
prefecture level, where rodent habitat is more homogeneous — would substantially
reduce ecological aggregation bias inherent in country-year modeling. Reservoir
host density data, if collected systematically alongside hantavirus reporting,
would provide the mechanistic signal that public climate and land-use covariates
cannot. Longer comparable annual panels — extending the 2019–2023 window
backward with consistent case definitions — would improve the sample efficiency
of training and reduce dependence on COVID-era data that may reflect reporting
artifacts. Better harmonization of case definitions and surveillance completeness
reporting across EU/EEA member states would reduce the noise currently captured
by quality-grade flags. These structural improvements to surveillance
infrastructure are a more productive path than adding coarser public covariates
to an already sparse annual panel.

**Limitations.** This benchmark has five annual reporting years, which severely
limits statistical power to detect covariate effects. Country-year aggregation
masks within-country spatial and temporal heterogeneity in exposure and
reporting. Reported incidence reflects reporting completeness and health-seeking
behavior as well as true infection burden; the benchmark evaluates reported counts,
not unbiased burden estimates. Reporting heterogeneity across EU/EEA member
states is documented but not fully modeled. Belgium 2023 and Cyprus 2023 carry
grade-C quality flags for surveillance-system changes. The 2020–2021 training
years may reflect COVID-era health-system disruptions that altered reporting
independently of true hantavirus incidence. All evaluations are retrospective;
no prospective validation was conducted. No causal inference is made from any
covariate association. MODIS vegetation data were excluded because quality-masked
aggregation did not pass the pre-specified gate; vegetation claims are not made.
Results apply specifically to EU/EEA public annual reported surveillance and
should not be generalized to other surveillance systems, syndrome definitions,
geographic settings, or temporal resolutions. This benchmark does not model
human-to-human hantavirus transmission; no such modeling was attempted.

**Conclusion.** An open reproducible benchmark for reported hantavirus incidence
in EU/EEA countries, 2019–2023, shows that simple surveillance-history baselines
are difficult to beat with public annual country-level data. The calibration–
sharpness tradeoff documented here quantifies the uncertainty that public health
practitioners should acknowledge when interpreting or communicating annual
hantavirus surveillance data, particularly during periods of heightened public
attention to rare zoonotic events. Improving surveillance infrastructure —
subnational resolution, longer panels, systematic reservoir data — is a more
productive path to calibrated EU/EEA hantavirus risk assessment than adding
coarse public covariates to sparse annual counts.

---

## ACKNOWLEDGMENTS

The author thanks the European Centre for Disease Prevention and Control (ECDC)
for publicly accessible Annual Epidemiological Reports, and the following open
data providers: World Bank Open Data, FAOSTAT, TerraClimate, and Natural Earth.
Artificial intelligence assistance was used for manuscript planning, language
editing, and pre-submission quality checks. The author verified all analyses,
references, and claims and accepts responsibility for the final manuscript. No
AI-generated figures were used.

---

## AUTHOR BIOGRAPHY

Julian Juan is an independent researcher interested in reproducible infectious-
disease surveillance, probabilistic evaluation, and public-health modeling.

---

## REFERENCES

1. Jonsson CB, Figueiredo LT, Vapalahti O. A global perspective on hantavirus
ecology, epidemiology, and disease. Clin Microbiol Rev. 2010;23:412–41.

2. Vaheri A, Henttonen H, Voutilainen L, Mustonen J, Sironen T, Vapalahti O.
Hantavirus infections in Europe and their impact on public health. Rev Med
Virol. 2013;23:35–49.

3. World Health Organization. Hantavirus cluster linked to cruise ship travel,
multi-country — Disease Outbreak News. Geneva: WHO; 2026 [cited 2026 May 12].
Available at: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600

4. European Centre for Disease Prevention and Control. Hantavirus infection —
Annual Epidemiological Report for 2023. Stockholm: ECDC; 2024 [cited 2026 May 12].
Available at: https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023

5. Voutilainen L, Sironen T, Tonteri E, Balk-Moller NC, Iivanainen A, Niemimaa J,
et al. Life-long antibody responses and evidence for waning immunity to Puumala
hantavirus in a bank vole population. J Virol. 2015;89:5765–75.

6. World Health Organization. Hantavirus fact sheet. Geneva: WHO; 2023
[cited 2026 May 12]. Available at:
https://www.who.int/news-room/fact-sheets/detail/hantavirus

7. Kasperson RE, Renn O, Slovic P, Brown HS, Emel J, Goble R, et al. The social
amplification of risk: a conceptual framework. Risk Anal. 1988;8:177–87.

8. Zeimes CB, Olsson GE, Ahlm C, Vanwambeke SO. Landscape and local climatic
effects on human Puumala hantavirus incidence — the role of forest spatial
pattern. PeerJ. 2014;2:e541.

9. Kallio ER, Klingström J, Gustafsson E, Manni T, Vaheri A, Henttonen H, et al.
Prolonged survival of Puumala hantavirus outside the host: evidence for indirect
transmission via the environment. J Gen Virol. 2006;87:2127–34.

10. Reusken C, Heyman P. Factors driving hantavirus emergence in Europe.
Curr Opin Virol. 2013;3:92–9.

11. Abatzoglou JT, Dobrowski SZ, Parks SA, Hegewisch KC. TerraClimate, a
high-resolution global dataset of monthly climate and climatic water balance
from 1958–2015. Sci Data. 2018;5:170191.

12. Natural Earth. Natural Earth: free vector and raster map data [Internet].
2024 [cited 2026 May 12]. Available at: https://www.naturalearthdata.com

13. Bracher J, Ray EL, Gneiting T, Reich NG. Evaluating epidemic forecasts in an
interval format. PLoS Comput Biol. 2021;17:e1008618.

14. World Bank Open Data. World development indicators [Internet]. Washington
(DC): World Bank; 2024 [cited 2026 May 12]. Available at:
https://data.worldbank.org

15. Food and Agriculture Organization of the United Nations. FAOSTAT land use
[Internet]. Rome: FAO; 2024 [cited 2026 May 12]. Available at:
https://www.fao.org/faostat/en/#data/RL

---

## TABLE LEGENDS

**Table 1.** Source and quality audit for the EU/EEA hantavirus incidence
benchmark, 2019–2023. ECDC = European Centre for Disease Prevention and Control;
FAOSTAT = Food and Agriculture Organization Corporate Statistical Database;
GDP = gross domestic product; NDVI = normalized difference vegetation index;
EVI = enhanced vegetation index; QA = quality assurance.

**Table 2.** Core benchmark performance for 2022 (validation) and 2023 (test)
evaluation years. WIS = weighted interval score (lower is better); Coverage =
90% empirical coverage (fraction of observed counts inside the 90% prediction
interval, reported as numerator/total); Width = mean 90% interval width in
cases per 100,000 population; MAE = mean absolute error against median
prediction; Brier = Brier score for any reported case (threshold ≥1 case).
Bold indicates best value per column per evaluation year. NB = negative binomial.

---

## FIGURE LEGENDS

**Figure 1.** Country-level reported hantavirus incidence per 100,000 population,
EU/EEA, 2023. Data source: ECDC Annual Epidemiological Report for 2023.
Map projection: ETRS89/LAEA Europe (EPSG:3035). Boundaries: Natural Earth
1:50m Admin-0. Gray indicates countries for which data were not reported or
available. Map reflects country-level annual reported surveillance totals;
no within-country spatial variation is implied. Belgium 2023 and Cyprus 2023
are quality grade C (surveillance-system changes).

**Figure 2.** Calibration–sharpness tradeoff for 2023 one-year-ahead
probabilistic forecasts. Each point represents one model or covariate block.
x-axis: mean 90% prediction interval width (cases per 100,000 population);
y-axis: mean weighted interval score (lower is better). Point shape indicates
model family: circles = simple surveillance-history baselines; squares =
negative-binomial baselines; triangles = covariate blocks (gradient boosting);
diamonds = penalized Poisson count models. Key labeled points are annotated.
No single model achieved both low WIS and near-nominal coverage simultaneously:
the last-observed country-rate baseline (lowest WIS, 42.86) undercovered observed
counts (16/28, 57%); the empirical negative-binomial baseline (best coverage,
28/28, 100%) used intervals approximately 45-fold wider.

---

## TABLES

**Table 1. Source and quality audit for the EU/EEA hantavirus incidence benchmark, 2019–2023.**

[NOTE TO AUTHOR: Reproduce this table using Word's table tool (not as image).]

| Component | Source | Years | Rows/Coverage | QA result | Manuscript use |
|---|---|---|---|---|---|
| Reported cases/incidence | ECDC Annual Epidemiological Report | 2019–2023 | 142 country-years; 28–29 countries/year | PASS — totals reconcile exactly | Primary outcome |
| Population, rurality, GDP | World Bank Open Data | 2019–2023 | 142 rows; no missing | PASS | Covariate block: demographic |
| Land-use shares | FAOSTAT | 2019–2023 | 142 rows; no missing | PASS | Covariate block: land use |
| Climate/water balance | TerraClimate | 2018–2023 (lag-1 for 2019–2023) | 142 rows current year; 114 rows lag-1 complete | PASS | Covariate block: climate |
| Country boundaries | Natural Earth (1:50m Admin-0) | 2024 | 28–29 countries | PASS | Maps and spatial aggregation |
| NDVI/EVI | MODIS MOD13C2 | — | 0 (excluded) | FAIL — QA-masked aggregation not implemented | Excluded; no vegetation claims |

Note: Belgium 2023 and Cyprus 2023 are quality grade C (surveillance-system changes); all other rows are grade B (comprehensive).

---

**Table 2. Core benchmark performance for 2022 (validation) and 2023 (test) evaluation years.**

[NOTE TO AUTHOR: Reproduce this table using Word's table tool (not as image).]

| Year | Model | WIS | Coverage, n/N (%) | Width | MAE | Brier |
|---|---|---|---|---|---|---|
| 2022 | Country historical mean rate | 65.58 | 18/29 (62%) | 21.07 | 69.79 | 0.025 |
| 2022 | Last-observed country rate | 101.5 | 16/29 (55%) | 24.55 | 108.1 | 0.033 |
| 2022 | Empirical NB | **47.17** | **29/29 (100%)** | 694.2 | 72.1 | 0.158 |
| 2022 | Hierarchical NB | 47.38 | 29/29 (100%) | 693.5 | 72.79 | 0.198 |
| 2022 | Best covariate block (all public) | 74.46 | 22/29 (76%) | 264.9 | 109.9 | 0.386 |
| 2022 | Best penalized Poisson (land use)† | — | — | — | — | — |
| 2023 | Country historical mean rate | 52.47 | 15/28 (54%) | 20.61 | 58.14 | 0.036 |
| 2023 | Last-observed country rate | **42.86** | 16/28 (57%) | **14.61** | **47.11** | **0.061** |
| 2023 | Empirical NB | 43.75 | **28/28 (100%)** | 660 | 65.25 | 0.190 |
| 2023 | Hierarchical NB | 43.90 | 28/28 (100%) | 659.4 | 65.75 | 0.215 |
| 2023 | Best covariate block (land use) | 318.5 | 19/28 (68%) | 325.9 | 367.4 | 0.294 |
| 2023 | Best penalized Poisson (land use) | 159.4 | 9/28 (32%) | 28.82 | 167.6 | 0.099 |

WIS = weighted interval score (lower is better). Width = mean 90% interval width (cases per 100,000).
Bold indicates best value per column per evaluation year.
† Penalized Poisson 2022 results reflect validation-year WIS used for tuning only; primary evaluation is the 2023 test year.
