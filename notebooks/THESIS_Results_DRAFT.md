# Chapter 4 — Results (Rewrite Draft)

> Draft grounded entirely in the committed, reproducible notebooks (06–08) and figures.
> All modeling is patient-level and leakage-free; conversion is defined as a worse diagnostic
> stage sustained on ≥2 consecutive visits ("confirmed conversion"). Every number below is
> produced by `notebooks/07_*` and `notebooks/08_*` with random seed 42.
> Bracketed notes like _[Fig 1]_ mark where figures are inserted.

---

## 4.1 Participant flow and cohort construction

Of the 2,131 participants in the processed ADNI baseline dataset, 453 were excluded for having only
a single visit (no follow-up over which an outcome could be observed), and 28 were excluded for
containing a clinically implausible improvement in diagnosis (Dementia → a less severe stage), which
was treated as diagnostic error. This left approximately 1,650 analyzable participants with at least
two visits.

Because the Alzheimer's Disease Neuroimaging Initiative preferentially enrolls participants who
already show cognitive concern, the baseline diagnostic distribution was weighted toward impairment:
792 cognitively normal (CN), 969 mild cognitive impairment (MCI), and 370 dementia at baseline. This
enrollment pattern is discussed as a limitation (Section 5.5), as it inflates the apparent prevalence
of conversion relative to a community-based sample.

To respect the longitudinal structure of the data, all predictive models were built at the **patient
level**: each participant contributed a single record consisting of their **baseline (earliest) visit**,
and the model predicted that participant's **future** diagnostic outcome. Consequently, every
train/test partition separated *distinct individuals*, making it impossible for a given patient to
appear in both training and testing folds.

## 4.2 Impact of evaluation design (data leakage)

Preliminary modeling that split the data at the visit level (i.e., treating each of a participant's
~4–5 visits as an independent record) produced optimistic accuracy estimates. For the early-detection
task, a Random Forest reported ~82% accuracy under visit-level splitting; however, under a correct
patient-grouped split the same model's balanced accuracy fell to ~34% (chance level for the outcome
distribution). The discrepancy arose because a participant's repeated visits carry near-identical
features and the same eventual-outcome label; a random visit-level split therefore allowed the model
to recognize individuals it had already seen rather than to generalize. All results reported below
use patient-level partitioning to avoid this bias.

## 4.3 Conversion labeling and sensitivity analysis

Because diagnostic status fluctuates in ADNI, the definition of "converter" materially affects the
analysis. Diagnostic reversion (an improvement between visits) occurred in 123 participants (5.8%),
predominantly MCI → CN (108 occurrences) with some Dementia → MCI (28). Twenty-eight participants
exhibited the CN → (MCI/Dementia) → CN pattern.

Table 4.1 reports the number of converters under alternative definitions. Requiring a **confirmed**
transition (worse stage sustained ≥2 consecutive visits) reduced converter counts by roughly a
quarter to a third relative to a naïve last-visit definition, removing single-visit fluctuations. The
confirmed definition was pre-specified as the primary outcome for all subsequent models.

**Table 4.1 — Converters by outcome definition**

| Definition | MCI→Dementia | CN→MCI/Dementia |
|---|---|---|
| Last-visit only | 329 (39%) | 110 (21%) |
| Ever reached worse stage | 340 (40%) | 120 (22%) |
| **Confirmed (≥2 visits) — primary** | **237 (28%)** | **78 (15%)** |
| Confirmed within 36 months | 181 (29% of eligible) | 27 (7% of eligible) |
| Confirmed within 24 months | 141 (20% of eligible) | 18 (4% of eligible) |

Short fixed-horizon definitions (24/36 months) were inappropriate for the CN cohort because CN→MCI
conversion is slow (median time to confirmed conversion ≈ 4 years); the confirmed-any-time definition
was therefore used, with time-to-event modeled explicitly via survival analysis (Section 4.6).

## 4.4 Predictive performance across cohorts and algorithms

Three cohorts were modeled: (A) baseline **CN → progression** to MCI or dementia; (B) baseline
**MCI → Dementia**; and (C) a **pooled** CN+MCI cohort predicting progression to dementia, with
baseline diagnosis deliberately excluded from the feature set so that the model surfaced biological
and cognitive predictors rather than the trivial CN-vs-MCI distinction.

Six algorithms named in the study design were evaluated identically under 5-fold cross-validation
with SMOTE applied inside training folds only. Discrimination (ROC-AUC) is reported in Table 4.2 and
the receiver operating characteristic curves in _[Fig 1 — fig1_roc_cohorts.png]_.

**Table 4.2 — ROC-AUC by model and cohort (5-fold CV, mean ± SD)**

| Model | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| Logistic Regression | 0.69 ± 0.06 | 0.82 ± 0.02 | 0.87 ± 0.03 |
| Random Forest | 0.66 ± 0.02 | 0.83 ± 0.03 | 0.88 ± 0.03 |
| XGBoost | 0.70 ± 0.03 | 0.83 ± 0.04 | 0.87 ± 0.03 |
| SVM (RBF) | 0.68 ± 0.03 | 0.81 ± 0.02 | 0.86 ± 0.03 |
| K-Nearest Neighbors | 0.62 ± 0.05 | 0.77 ± 0.03 | 0.83 ± 0.03 |
| Neural Network (MLP) | 0.63 ± 0.05 | 0.79 ± 0.03 | 0.84 ± 0.04 |

Cohort n / events: CN→progression 519 / 74 (14%); MCI→Dementia 819 / 228 (28%); Pooled 1,338 / 244 (18%).

Two patterns are notable. First, discrimination increased with baseline impairment: the pooled and
MCI cohorts achieved strong performance (AUC 0.83–0.88), whereas prediction of progression from full
cognitive normality was substantially harder and under-powered (AUC ≈ 0.66–0.70, 74 events). Second,
the top-performing algorithms — Random Forest, XGBoost, and Logistic Regression — were statistically
indistinguishable, with the simple linear model matching the ensembles. This indicates that the
predictive signal in these features is largely linear and does not require nonlinear modeling, which
qualifies the study hypothesis (Section 5.3).

## 4.5 Predictors of conversion and their stage dependence

Permutation importance (mean decrease in ROC-AUC on held-out folds) was used to rank predictors within
each cohort _[Fig 4 — fig4_predictors.png]_. Two complementary feature-selection methods were also
applied to the pooled cohort: univariate selection (ANOVA F-test, SelectKBest) and Recursive Feature
Elimination with logistic regression.

**Table 4.3 — Top early predictors by cohort (permutation importance rank)**

| Rank | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| 1 | Hippocampus | FAQ | FAQ |
| 2 | ICV | FDG | LDELTOTAL |
| 3 | Age | LDELTOTAL | AV45 |
| 4 | MOCA | mPACCtrailsB | FDG |
| 5 | LDELTOTAL | Age | ABETA |
| 6 | RAVLT-learning | RAVLT-immediate | CDRSB |
| 7 | ADAS13 | ADAS13 | RAVLT-immediate |
| 8 | FDG | ABETA | mPACCtrailsB |

The dominant predictors shifted with disease stage. At the earliest (CN) stage, **structural and
memory** measures led — hippocampal volume, intracranial volume, and delayed verbal memory
(LDELTOTAL) — consistent with early medial-temporal atrophy. Closer to dementia (MCI stage), the
strongest predictors were measures of **daily function (FAQ), brain metabolism (FDG), and amyloid
burden (AV45, ABETA)**. Predictors that recurred across all methods (permutation importance,
SelectKBest, and RFE) — **FAQ, mPACCtrailsB, ADAS13, and LDELTOTAL** — are considered the most robust.
One RFE-selected feature ("Never married") is almost certainly spurious and illustrates the value of
requiring convergence across selection methods.

## 4.6 Time to conversion (survival analysis)

For the MCI cohort (819 participants; 228 confirmed conversions; 591 right-censored at last visit),
time from baseline to first confirmed dementia was modeled. Kaplan–Meier estimates stratified by APOE4
status _[Fig 2 — fig2_km_apoe4.png]_ showed markedly faster progression among APOE4 carriers:

**Table 4.4 — Kaplan–Meier: probability of remaining dementia-free**

| Group | 2 years | 3 years | 5 years |
|---|---|---|---|
| APOE4 negative | 88% | 85% | 80% |
| APOE4 positive | 75% | 65% | 55% |
| All MCI | 81% | 75% | 68% |

A Cox proportional-hazards model (features standardized; hazard ratios per 1 SD) identified independent
predictors of conversion timing _[Fig 3 — fig3_cox_forest.png]_. Higher **FAQ (HR ≈ 1.41), ADAS13
(1.34), and amyloid AV45 (1.29)** were associated with faster conversion, while higher **FDG (0.72),
verbal memory (RAVLT-immediate 0.76; LDELTOTAL 0.79), and hippocampal volume (0.79)** were associated
with slower conversion. These timing predictors align with the classification-based importance
rankings, providing convergent evidence.

## 4.7 A parsimonious clinical risk score

To assess whether a small set of clinically accessible variables could approximate the full models, a
logistic-regression risk score was built for MCI→Dementia from seven inputs (age, APOE4, MMSE, FAQ,
CDRSB, hippocampal volume, ADAS13). This parsimonious score achieved ROC-AUC ≈ 0.81 ± 0.03 — nearly
matching the full multivariable models — indicating that a handful of routine measures (led by ADAS13,
FAQ, hippocampal volume, and APOE4) capture most of the available predictive signal.

## 4.8 Cognitive decline trajectories

Linear mixed-effects models (random intercept and slope per participant) characterized the rate of
cognitive decline by baseline group. All groups worsened over time, and the dementia group declined
fastest: ADAS13 increased by ≈ +2.2 points/year in the dementia group versus ≈ +1.7 points/year in
the CN group; CDRSB showed the same ordering. Absolute CN slopes should be interpreted with caution,
as the CN group contains future converters, but the relative ordering is consistent with expected
disease progression.

---

### Notes for you (delete before submission)
- Every number here is traceable to notebooks 07/08 and the four figures in `notebooks/figures/`.
- The 89% 3-class result from the original `04` notebook is intentionally **not** presented as an early-detection
  result — if you want to keep it, present it in a short subsection as *concurrent diagnostic classification*
  and note its circularity (it uses CDRSB/FAQ, which partly define the diagnosis).
- Figures are referenced as [Fig 1–4]; place the PNGs from `notebooks/figures/` at those points.
