## TITLE PAGE

**Title:**
Sparse Public Surveillance Limits Forecasting of Reported Hantavirus Incidence,
European Union and European Economic Area, 2019-2023

**Running head:** Hantavirus Forecasting Limits

**Author:** Julian Juan

**Affiliation:** Independent researcher

**ORCID:** 0009-0003-7234-2245

**Corresponding author:**
Julian Juan
Email: bubgaming3@gmail.com
Mailing address and phone: to be supplied in the submission portal.

**Word count (abstract):** 129

**Word count (text, excluding abstract, acknowledgments, references, tables,
figure legends):** 1,706

**One-sentence summary:**
Sparse annual public surveillance data did not support stable, calibrated
covariate-driven forecasts of reported EU/EEA hantavirus incidence.

**Keywords:** hantavirus; zoonoses; disease surveillance; European Union;
European Economic Area; probabilistic forecasting; calibration; public health
surveillance

---

## ABSTRACT

Public hantavirus surveillance reports are essential for public health
monitoring, but their ability to support country-level forecasting across
heterogeneous surveillance systems is unclear. We assembled a European
Union/European Economic Area country-year benchmark of reported hantavirus
incidence for 2019-2023 and linked labels to public demographic, land-use,
climate, and source-quality covariates. We compared surveillance baselines and
low-dimensional public-covariate models using one-year-ahead probabilistic
evaluation, weighted interval score, 90% empirical coverage, interval width,
mean absolute error, Brier score, and sensitivity analyses. Public covariates
did not provide stable, calibrated improvement on the 2023 test year; sharp
models undercovered observations, whereas overdispersed baselines used wide
intervals. Sensitivity, country-influence, calibration-localization, and
detectability analyses supported a conservative interpretation. Standardized
completeness metadata, longer comparable panels, and calibrated uncertainty
reporting are prerequisites for stronger pan-European hantavirus forecasting.

---

## TEXT

### Introduction

Hantaviruses are rodentborne viruses transmitted to humans primarily through
contact with infected rodent excreta (1). In Europe, most reported human disease
is hemorrhagic fever with renal syndrome, especially Puumala virus infection
linked to bank vole reservoirs in northern and central Europe (2). Public
surveillance is central to monitoring this zoonosis, but reported cases reflect
testing, ascertainment, case definitions, and national surveillance systems as
well as true infection pressure.

The European Centre for Disease Prevention and Control (ECDC) reported 1,885
confirmed and probable hantavirus infection cases from 28 EU/EEA countries in
2023, a notification rate of 0.4 cases per 100,000 population; Finland and
Germany accounted for 60.5% of reported cases (3). The 2023 and 2020
notification rates were the lowest in 2019-2023. ECDC also documented important
source-quality caveats: Belgium's 2023 surveillance system was no longer
comprehensive, Cyprus had unspecified surveillance context, Denmark and Iceland
did not report 2023 data, and the United Kingdom had no ECDC data from 2020
onward after EU withdrawal (3).

Forecasting is biologically plausible because hantavirus incidence is linked to
rodent host dynamics, mast events, weather, and land cover. However, high-signal
models usually rely on granular and internally consistent data. German Puumala
studies used district-level data and biologically specific predictors such as
weather and beech flowering; those studies reported useful outbreak warning
rules but also showed calibration challenges when later high-risk forecasts were
not confirmed (4,5). European mapping work demonstrates environmental
plausibility but does not answer whether annual public EU/EEA country-year data
can support calibrated forecasts (6).

Current public attention to hantavirus can also outpace what annual surveillance
data can resolve. In May 2026, WHO and ECDC reported a cruise-ship-associated
hantavirus cluster involving Andes virus, a setting and syndrome distinct from
European HFRS surveillance (7,8). Such events are not the target of this study,
but they illustrate why public health communication needs calibrated
uncertainty and clear limits on what surveillance data can support.

We asked whether public demographic, land-use, climate, and source-quality
covariates improved calibrated one-year-ahead forecasts of reported EU/EEA
country-year hantavirus incidence beyond simple surveillance-history baselines,
and whether performance failures were associated with sparse annual reporting
and surveillance-completeness caveats.

### Materials and Methods

We conducted a retrospective observational forecasting benchmark using public
aggregate surveillance data. We followed STROBE principles for observational
reporting and EID guidance for statistical and modeling manuscripts (9). The
unit of analysis was country-year reported hantavirus incidence, not individual
infection risk and not within-country risk.

The outcome labels were manually reconstructed from ECDC Annual Epidemiological
Reports for 2019-2023. Rows were joined by ISO3 country code and year to World
Bank population, rurality, and GDP indicators; FAOSTAT land-use shares;
TerraClimate climate and water-balance summaries; and Natural Earth boundaries
(Table 1). MODIS NDVI/EVI was excluded because quality-masked country-year
aggregation did not pass the prespecified source-quality gate. All source and
model inputs, values/ranges, missingness rules, and lags are listed in Table 1
and the Appendix.

The primary temporal split trained models on 2019-2021 rows, used 2022 for
validation and tuning, and locked 2023 as the test year. Target-year case counts
were never used as predictors. Imputation parameters and feature screening were
estimated on training rows only. Candidate features were removed for high
missingness, constancy, duplication, or high training-set correlation before
model fitting.

We compared surveillance-history baselines, negative-binomial baselines,
covariate-block regression models, and an exploratory ridge-penalized Poisson
count model with a population offset. Covariate blocks were nested:
surveillance history only; plus demographic context; plus FAOSTAT land use; plus
TerraClimate climate and water balance; plus source-quality metadata. The
penalized Poisson model was tuned on 2022 validation weighted interval score
(WIS); coefficients were not interpreted causally.

Primary metrics were WIS for central 90% intervals, 90% empirical coverage,
mean interval width, mean absolute error, and Brier score for any reported case
(10). WIS rewards forecasts that are close to observations and have calibrated
uncertainty intervals; lower WIS is better. We did not rank models by WIS alone.
A covariate model could be promoted only if WIS improved without unacceptable
coverage loss, interval width remained interpretable, and sensitivity analyses
did not show dependence on flagged rows or high-incidence countries.

EID-specific sensitivity analyses tested exclusion of Belgium 2023, Cyprus
2023, both flagged rows, a retained flagged-row indicator, exclusion of 2020 and
2021 training rows, leave-one-country-out influence, calibration localization,
and a null-calibrated simulation-based detectability screen. The simulation
used the observed panel structure, actual populations, observed-like
overdispersion, observed-like missingness/flag patterns, and effect sizes from
none to large. It estimated the probability of selecting a covariate model over
a surveillance baseline and the false-positive selection rate when the true
effect was zero. These simulations do not validate model skill.

This study used aggregate public data only. No individual-level, clinical,
address-level, or restricted human-subject data were used; institutional review
was not required. Analysis code and public-data artifacts are archived at the
DOI listed in the Data and Code Availability statement; the DOI version must be
verified against the final clean submission archive before portal upload.

### Results

The benchmark contained 142 country-year rows. Annual totals reconciled exactly
to ECDC: 4,088 cases in 2019, 1,693 in 2020, 4,947 in 2021, 2,185 in 2022, and
1,885 in 2023. Belgium 2023 and Cyprus 2023 were the only grade-C source-quality
rows. World Bank and FAOSTAT covariates were complete for all rows; TerraClimate
lag-1 variables were complete for non-2019 rows.

In validation year 2022, the empirical negative-binomial baseline had the lowest
WIS, 47.17, and complete coverage, 29/29, but used wide intervals (mean width
694.2 cases). The country historical mean-rate baseline had narrower intervals
(21.07 cases) but lower coverage, 18/29. The best covariate block, all public
features, had WIS 74.46 and coverage 22/29 (Table 2).

In the 2023 test year, the last-observed country-rate baseline had the lowest
WIS, 42.86, and narrowest intervals (14.61 cases), but undercovered observed
counts, 16/28. Negative-binomial baselines covered all observations, 28/28, but
used intervals averaging approximately 660 cases. This produced a
calibration-sharpness tradeoff rather than a deployable forecasting model
(Figure 2).

No public-covariate block passed the promotion rule. The best covariate block in
2023 was land use, with WIS 318.55, coverage 19/28, and mean interval width
325.87 cases. The all-public block had WIS 331.31 and coverage 18/28. The
exploratory penalized Poisson land-use model improved over other Poisson
variants but failed calibration badly: WIS 159.37 and coverage 9/28. These
models were sharper than overdispersed baselines but too miscalibrated for
public-health use.

Surveillance-quality sensitivity did not rescue covariate models (Table 3).
Excluding Belgium 2023 and Cyprus 2023 left land use as the best covariate
block, but WIS worsened to 341.62 and coverage was 17/26. Excluding 2020-2021
training rows produced near-nominal coverage for the all-public block, 25/28,
but only with very wide intervals (mean width 764.02 cases) and WIS 75.85,
still above the best simple 2023 baseline. A flagged-row indicator did not
change the primary ranking.

Leave-one-country-out influence analysis showed that the conclusion was not
driven solely by Finland or Germany (Figure 3; Appendix). Removing Finland
reduced the best covariate-block WIS from 318.55 to 280.53 and kept the best
feature set as land use; removing Germany reduced WIS to 306.35 and also kept
land use as best. In neither case did a covariate block beat the best
surveillance baseline. Calibration localization showed that 2023 interval
failures were distributed across countries and model families rather than
limited to one flagged row.

The redesigned detectability screen reported a maximum null covariate-selection
probability of 0.000 across tested overdispersion and missingness settings. For
moderate and large simulated effects, selection probabilities increased under
some scenarios, indicating that the screen could detect strong injected effects
under its conservative selection rule. These simulations do not prove that
covariates have no biological effect; they indicate that the observed sample
structure has limited ability to justify promotion of modest covariate effects.

### Discussion

In this retrospective EU/EEA country-year benchmark, public covariates did not
provide stable, calibrated improvement over surveillance-history baselines for
one-year-ahead reported hantavirus incidence. The practical finding is not that
"modeling failed." The finding is that sparse annual public surveillance data
create a forecasting ceiling: sharp models undercovered observed counts, whereas
well-covered baselines required intervals too wide to guide operational
interpretation.

This result has public-health meaning. Before richer environmental covariates
can support credible pan-European annual forecasts, surveillance metadata must
better distinguish true incidence changes from reporting completeness,
case-definition, testing, and ascertainment changes. Standardized completeness
flags, harmonized source metadata, longer comparable panels, and explicit
uncertainty reporting are likely to improve public surveillance evaluation more
than adding coarse public covariates alone.

Our findings do not contradict high-resolution German Puumala warning systems.
Those studies used district-level German data and biologically relevant
predictors in a more internally consistent setting (4,5). This study tests a
harder and different question: what can be inferred from public EU/EEA
country-year annual reporting across heterogeneous surveillance systems? The
answer is intentionally conservative.

The benchmark also shows why baseline-standardized probabilistic evaluation is
valuable for public health forecasting design. EID has published infectious
disease forecast-evaluation work using WIS and baseline comparisons to assess
practical forecasting systems (11). Here, WIS alone would have favored a sharp
baseline in 2023, but coverage showed that the model was overconfident. Reading
WIS, coverage, and interval width together prevents false precision.

Limitations are substantial. The panel contains only five annual years and 142
country-year rows. Country-level aggregation masks subnational exposure,
reservoir ecology, and reporting heterogeneity. Reported cases are not true
infection burden. COVID-era years may reflect health-system disruption. Belgium
2023 and Cyprus 2023 have source-quality caveats. Covariates were public and
coarse; no nonpublic subnational surveillance or systematic reservoir data were
used. All evaluations were retrospective, and no prospective validation was
performed. No causal inference is made from any covariate association, and no
within-country risk map is implied by the figures.

An open benchmark for reported hantavirus incidence in EU/EEA countries,
2019-2023, shows that public country-year surveillance is valuable for
transparent evaluation but too sparse and heterogeneous for confident
covariate-driven forecasting claims. Standardized completeness metadata, longer
panels, and calibrated uncertainty reporting are prerequisites for stronger
pan-European hantavirus forecasting from public data.

---

## ACKNOWLEDGMENTS

The author thanks ECDC, World Bank Open Data, FAOSTAT, TerraClimate, and Natural
Earth for publicly accessible data. Artificial intelligence tools were used to
assist with manuscript planning, language editing, and pre-submission quality
checks. No confidential or nonpublic data were entered into AI tools. The author
verified all analyses, references, and claims and accepts responsibility for the
final manuscript. No AI-generated figures were used.

---

## BIOGRAPHICAL SKETCH

Julian Juan is an independent researcher interested in reproducible infectious
disease surveillance, probabilistic evaluation, and public-health modeling.

---

## REFERENCES

1. Jonsson CB, Figueiredo LT, Vapalahti O. A global perspective on hantavirus
ecology, epidemiology, and disease. Clin Microbiol Rev. 2010;23:412-41.

2. Vaheri A, Henttonen H, Voutilainen L, Mustonen J, Sironen T, Vapalahti O.
Hantavirus infections in Europe and their impact on public health. Rev Med
Virol. 2013;23:35-49.

3. European Centre for Disease Prevention and Control. Hantavirus infection.
In: ECDC. Annual Epidemiological Report for 2023. Stockholm: ECDC; 2025
[cited 2026 May 14]. https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023

4. Kazasidis O, Jacob J. Machine learning identifies straightforward early
warning rules for human Puumala hantavirus outbreaks. Sci Rep. 2023;13:3989.

5. Kazasidis O, Geduhn A, Jacob J. High-resolution early warning system for
human Puumala hantavirus infection risk in Germany. Sci Rep. 2024;14:9474.

6. Zeimes CB, Olsson GE, Ahlm C, Vanwambeke SO. Landscape and regional
environmental analysis of the spatial distribution of hantavirus human cases in
Europe. Front Public Health. 2015;3:54.

7. World Health Organization. Hantavirus cluster linked to cruise ship travel,
Multi-country. Geneva: WHO; 2026 [cited 2026 May 14].
https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600

8. European Centre for Disease Prevention and Control. Hantavirus-associated
cluster of illness on a cruise ship: ECDC assessment and recommendations.
Stockholm: ECDC; 2026 [cited 2026 May 14].
https://www.ecdc.europa.eu/en/publications-data/hantavirus-associated-cluster-illness-cruise-ship-ecdc-assessment-and

9. von Elm E, Altman DG, Egger M, Pocock SJ, Gotzsche PC, Vandenbroucke JP. The
Strengthening the Reporting of Observational Studies in Epidemiology (STROBE)
statement: guidelines for reporting observational studies. PLoS Med.
2007;4:e296.

10. Bracher J, Ray EL, Gneiting T, Reich NG. Evaluating epidemic forecasts in an
interval format. PLoS Comput Biol. 2021;17:e1008618.

11. Fox SJ, Slayton RB, Johansson MA, Biggerstaff M, Reich NG. Optimizing
disease outbreak forecast ensembles. Emerg Infect Dis. 2024;30:1801-9.

12. World Bank Open Data. World development indicators [Internet]. Washington
(DC): World Bank; 2024 [cited 2026 May 14]. https://data.worldbank.org

13. Food and Agriculture Organization of the United Nations. FAOSTAT land use
[Internet]. Rome: FAO; 2024 [cited 2026 May 14].
https://www.fao.org/faostat/en/#data/RL

14. Abatzoglou JT, Dobrowski SZ, Parks SA, Hegewisch KC. TerraClimate, a
high-resolution global dataset of monthly climate and climatic water balance
from 1958-2015. Sci Data. 2018;5:170191.

15. Natural Earth. Natural Earth: free vector and raster map data [Internet].
2024 [cited 2026 May 14]. https://www.naturalearthdata.com

---

## TABLE LEGENDS

**Table 1.** Public data sources and model inputs for reported hantavirus
incidence forecasting, European Union and European Economic Area, 2019-2023.
The complete variable-level table appears in the Appendix.

**Table 2.** Core benchmark performance for 2022 validation and 2023 test
evaluation years. WIS = weighted interval score; Width = mean 90% interval
width in reported cases; MAE = mean absolute error; NB = negative binomial.

**Table 3.** EID-specific sensitivity summary for 2023 test-year covariate-block
models. Coverage is reported as numerator/denominator and fraction.

---

## FIGURE LEGENDS

**Figure 1.** Country-level reported hantavirus incidence per 100,000
population, European Union and European Economic Area, 2023. Map reflects
country-level annual reported surveillance totals; no within-country spatial
variation is implied. Belgium 2023 and Cyprus 2023 carry source-quality caveats.

**Figure 2.** Calibration-sharpness tradeoff for 2023 one-year-ahead
probabilistic forecasts. Each point represents one model or covariate block.
Lower WIS is better; interval width and coverage must be interpreted jointly.

**Figure 3.** Surveillance-quality sensitivity, Finland/Germany influence, and
calibration-localization summary. These panels test whether the main conclusion
depends on flagged rows, high-incidence countries, or localized coverage
failures.

---

## TABLES

**Table 1. Public data sources and model inputs for reported hantavirus
incidence forecasting, European Union and European Economic Area, 2019-2023.**

| Input group | Main variables | Source | Training range or values | Lag/missingness rule | Use |
|---|---|---|---|---|---|
| Outcome | cases; incidence_per_100k | ECDC; World Bank population | cases 0-1,740; incidence 0-26.99/100,000 | outcome only | reported-incidence label |
| Population denominator | population | World Bank | 39,182-83,196,000 persons | none | rate/count conversion and offsets |
| Surveillance history | country_last_rate; country_historical_rate; regional and panel rates | derived from prior ECDC rows | 0-22.75/100,000 for country rates | prior years only | simple baselines and surveillance-only block |
| Demographic context | rural population; GDP per capita | World Bank | rurality 4.82%-47.39%; GDP 10,354-116,860 current US dollars | lag 1 year; training-only imputation | context block |
| Land use | agricultural, cropland, forest, pasture, other land shares | FAOSTAT | shares 0.0007-0.8088 | lag 1 year; training-only imputation | land-use block |
| Climate/water balance | deficit, precipitation, soil moisture, maximum/minimum temperature, vapor pressure deficit | TerraClimate | precipitation 362.7-1,594.0 mm; temperature -1.21-24.51 C | lag 1 year; training-only imputation | climate block |
| Source quality | EU/EEA status; surveillance completeness; quality grade | ECDC and manual source audit | categorical | no imputation for primary labels | all-public block and sensitivity |
| Boundary display | country boundaries | Natural Earth | not a predictor | not used in models | national-scale maps only |
| Excluded candidate | NDVI/EVI | MODIS MOD13C2 | not used | excluded because QA-masked aggregation not implemented | no vegetation claims |

**Table 2. Core benchmark performance for 2022 validation and 2023 test evaluation years.**

| Year | Model | WIS | Coverage, n/N (%) | Width | MAE | Brier |
|---|---|---:|---|---:|---:|---:|
| 2022 | Country historical mean rate | 65.58 | 18/29 (62%) | 21.07 | 69.79 | 0.025 |
| 2022 | Last-observed country rate | 101.46 | 16/29 (55%) | 24.55 | 108.07 | 0.033 |
| 2022 | Empirical NB | 47.17 | 29/29 (100%) | 694.21 | 72.10 | 0.158 |
| 2022 | Hierarchical NB | 47.38 | 29/29 (100%) | 693.52 | 72.79 | 0.198 |
| 2022 | Best covariate block, all public | 74.46 | 22/29 (76%) | 264.92 | 109.89 | 0.386 |
| 2023 | Country historical mean rate | 52.47 | 15/28 (54%) | 20.61 | 58.14 | 0.036 |
| 2023 | Last-observed country rate | 42.86 | 16/28 (57%) | 14.61 | 47.11 | 0.061 |
| 2023 | Empirical NB | 43.75 | 28/28 (100%) | 660.00 | 65.25 | 0.190 |
| 2023 | Hierarchical NB | 43.90 | 28/28 (100%) | 659.39 | 65.75 | 0.215 |
| 2023 | Best covariate block, land use | 318.55 | 19/28 (68%) | 325.87 | 367.44 | 0.294 |
| 2023 | Best penalized Poisson, land use | 159.37 | 9/28 (32%) | 28.82 | 167.64 | 0.099 |

**Table 3. Sensitivity summary for 2023 covariate-block models.**

| Scenario | Best covariate block | WIS | Coverage, n/N (%) | Width | Promotion rule passed |
|---|---|---:|---|---:|---|
| Primary all rows | Land use | 318.55 | 19/28 (68%) | 325.87 | No |
| Exclude Belgium 2023 | Land use | 329.37 | 18/27 (67%) | 324.12 | No |
| Exclude Cyprus 2023 | Land use | 329.95 | 18/27 (67%) | 329.04 | No |
| Exclude Belgium and Cyprus 2023 | Land use | 341.62 | 17/26 (65%) | 327.36 | No |
| Retain flagged rows with indicator | Land use | 318.55 | 19/28 (68%) | 325.87 | No |
| Exclude 2020 training rows | All public | 138.27 | 25/28 (89%) | 593.23 | No |
| Exclude 2021 training rows | Surveillance only | 27.93 | 26/28 (93%) | 304.32 | No |
| Exclude 2020-2021 training rows | All public | 75.85 | 25/28 (89%) | 764.02 | No |
