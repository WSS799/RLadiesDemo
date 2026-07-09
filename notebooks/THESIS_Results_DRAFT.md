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
enrollment pattern is discussed as a limitation (Section 5.7), as it inflates the apparent prevalence
of conversion relative to a community-based sample.

To respect the longitudinal structure of the data, all predictive models were built at the **patient
level**: each participant contributed a single record consisting of their **baseline (earliest) visit**,
and the model predicted that participant's **future** diagnostic outcome. Consequently, every
train/test partition separated *distinct individuals*, making it impossible for a given patient to
appear in both training and testing folds.

Table 4.1 summarizes baseline characteristics by diagnostic group. All cognitive, functional,
structural, and molecular markers worsened monotonically across the CN → MCI → Dementia continuum;
in particular, the corrected CSF p-tau181 increased across groups (21.4 → 27.9 → 36.5 pg/mL),
consistent with its role as a marker of tau pathology and confirming that the data-integrity
correction (Methods §3.12) restored a physiologically plausible measure. The distributions underlying
these summary values, the correlation structure among features, and the baseline separation between
eventual converters and non-converters are examined in the exploratory analysis (Section 4.2).

**Table 4.1 — Baseline characteristics by diagnostic group, mean (SD).**

| Characteristic | CN (n = 792) | MCI (n = 969) | Dementia (n = 370) |
|---|---|---|---|
| Age, years | 73.0 (6.2) | 72.9 (7.6) | 74.9 (7.9) |
| Education, years | 16.6 (2.6) | 15.9 (2.8) | 15.3 (3.0) |
| Sex, male / female | 354 / 438 | 571 / 398 | 207 / 163 |
| APOE4 alleles, mean | 0.32 | 0.59 | 0.84 |
| MMSE | 29.1 (1.1) | 27.6 (1.8) | 23.1 (2.1) |
| MoCA | 25.7 (2.4) | 22.5 (3.1) | 16.7 (3.8) |
| ADAS-13 | 10.3 (4.5) | 16.8 (6.7) | 30.2 (8.1) |
| CDR-SB | 0.0 (0.1) | 1.5 (0.9) | 4.4 (1.7) |
| FAQ | 0.2 (0.9) | 3.2 (4.1) | 13.2 (7.0) |
| Delayed memory (LDELTOTAL) | 13.2 (3.3) | 5.7 (3.4) | 1.4 (1.9) |
| Hippocampal volume (mm³) | 7,407 (824) | 6,724 (1,104) | 5,725 (975) |
| CSF Aβ (ABETA, pg/mL) | 1,248 (369) | 956 (397) | 674 (269) |
| CSF total tau (pg/mL) | 237 (69) | 289 (117) | 368 (123) |
| CSF p-tau181 (pg/mL) | 21.4 (7.0) | 27.9 (13.1) | 36.5 (13.3) |
| Amyloid-PET (AV45 SUVR) | 1.1 (0.2) | 1.2 (0.2) | 1.4 (0.2) |
| FDG-PET (SUVR) | 1.3 (0.1) | 1.2 (0.1) | 1.1 (0.1) |

## 4.2 Exploratory data analysis

Before modeling, the baseline cohort (each participant's first visit, N = 2,131) was characterized
descriptively to (a) document the sample and its representativeness, (b) verify data quality and the
plausibility of feature distributions, and (c) establish, in an unadjusted view, which measures
separate diagnostic groups and eventual converters. These analyses motivate the feature set and the
stratified design used in the modeling sections and are reported as five figures. Because most features
are skewed (Figure EDA-2), values below are given as **median [interquartile range]** and group
differences use the Mann–Whitney *U* test; all values were computed from `data/pre_modelling_data.csv`
and reflect the corrected CSF p-tau181 (Methods §3.12).

**Figure EDA-1 — Cohort composition and follow-up.** Six panels summarize the baseline sample:
distribution of baseline diagnosis, age, education, sex, *APOE* ε4 allele count, and number of
longitudinal visits per participant. The cohort is weighted toward the impaired end of the spectrum:
969 participants (45.5%) were MCI at baseline, 792 (37.2%) CN, and 370 (17.4%) dementia. Participants
were older adults (median age 73.4 years, IQR 68.3–78.4) and highly educated (median 16 years, IQR
14–18), with a slight male majority (1,132 men, 999 women). *APOE* ε4 showed the expected dose gradient
(1,197 non-carriers, 740 with one allele, 194 with two). Follow-up was right-skewed: most participants
contributed a few visits, with a long tail up to ~15. The over-representation of MCI is a design
feature of ADNI, a convenience cohort that preferentially enrolls individuals with existing cognitive
concern; this, and the high educational attainment, limit generalization to the general population and
are carried forward as limitations (Section 5.7). The visible ε4 dose gradient is a first internal
validity check — a well-established risk factor is distributed as the literature predicts.

**Figure EDA-2 — Univariate distributions of the modeling features.** Histograms of sixteen key
cognitive, MRI-volumetric, and fluid/PET biomarker features reveal three distributional patterns, each
with a modeling consequence. (i) *Ceiling and floor effects*: MMSE piles up at its maximum of 30 (a
well-known ceiling effect in a cohort with many unimpaired participants), while FAQ and CDRSB floor
near zero. (ii) *Right-skew in the fluid biomarkers*: total tau and, after correction, phosphorylated
tau (median ~24 pg/mL on the correct 8–120 pg/mL scale) are right-skewed — confirming p-tau is no
longer a rescaled duplicate of total tau (Methods §3.12). (iii) *Bimodality in amyloid measures*: both
CSF Aβ42 and amyloid-PET (AV45) show two modes, consistent with the biological split between
amyloid-negative and amyloid-positive individuals; the ABETA spike at the upper bound reflects assay
truncation at its ceiling. MRI volumes and FDG are approximately symmetric. These shapes justify
reporting medians with IQRs for descriptive summaries and standardizing all features before any
distance- or gradient-based model (KNN, SVM, MLP, logistic regression).

**Figure EDA-3 — Feature separation by baseline diagnosis.** Box plots of nine core features across CN,
MCI, and Dementia give an unadjusted view of how strongly each measure tracks disease stage. Every
feature displays a monotone gradient, and the magnitude of separation orders the modalities. Global
cognition and function separate most sharply (ADAS13 median 10.0 [7–13] → 16.7 [12–21] → 29.7 [24–35];
CDRSB 0.0 → 1.5 → 4.5; FAQ 0.0 → 1.0 → 13.0); memory shows the same ordering (LDELTOTAL 13 → 6 → 0;
RAVLT-immediate 45 → 33 → 23). Structural and metabolic imaging separate more modestly but consistently
(hippocampus 7,434 → 6,706 → 5,614 mm³; FDG 1.3 → 1.2 → 1.1). Molecular pathology tracks stage in the
expected directions (CSF Aβ42 falls 1,310 → 854 → 630 pg/mL; corrected p-tau rises 20.2 → 25.2 → 35.1
pg/mL), and *APOE* ε4 carriage climbs in parallel (29% → 48% → 64%). This uniform, biologically
coherent staging confirms the features carry genuine, correctly oriented disease signal — a data-quality
gate before modeling — and previews a central finding: the *degree* of separation is stage-dependent,
which motivates modeling the cohorts separately rather than pooling them blindly (Methods §3.4; Section
4.6). Box-plot separation by *current* diagnosis, however, is not the same as *predictive* value for
*future* conversion, which is examined next.

**Figure EDA-4 — Correlation structure of the feature set.** A Pearson correlation heat map of 26
baseline features reveals coherent blocks. A *cognitive block* is strongly inter-correlated (MMSE–MOCA
r = +0.76; ADAS13–MMSE r = −0.74; the composites mPACCdigit–mPACCtrailsB r = +0.98, near-duplicates by
construction). A *medial-temporal structural block* groups hippocampus–entorhinal (r = +0.70) with
midtemporal and fusiform volumes, and whole-brain tracks with ICV (r = +0.72). A *molecular block*
links the amyloid measures inversely (ABETA–AV45 r = −0.73) and the tau measures tightly (TAU–PTAU
r = +0.98). Cross-block, higher ADAS13 correlates with lower FDG metabolism (r = −0.65) and smaller
hippocampal volume (r = −0.55); age is only weakly correlated with most features. This block structure
explains two downstream results: the high within-block redundancy means a parsimonious model can
recover most of the signal (the basis for the seven-variable risk score, Section 4.8, and the ablation
in Section 4.12, where removing any single imaging or biomarker modality barely changes performance);
and the near-perfect TAU–PTAU correlation is the pattern the earlier data corruption produced
*artifactually* — its persistence at the corrected scale confirms the two tau species are genuinely
co-regulated, not that the correction reintroduced the error (Methods §3.12). High collinearity also
cautions against over-interpreting any single feature's coefficient within a correlated block.

**Figure EDA-5 — Baseline features by eventual outcome (converter vs. stable).** Overlaid,
density-normalized histograms of eight leading features for participants non-demented at baseline, split
by whether they later met the confirmed conversion-to-dementia definition (Methods §3.4) versus remained
stable. Among the 1,761 non-demented-at-baseline participants, future converters and stable participants
show clearly offset — though substantially overlapping — baseline distributions, with every displayed
feature differing at p < 10⁻³⁷ (Mann–Whitney *U*). Future converters started with worse function (FAQ
median 4.0 vs 0.0), worse memory (LDELTOTAL 3.0 vs 10.0), worse global cognition (ADAS13 19.7 vs 12.0;
MOCA 21.0 vs 24.9), lower FDG metabolism (1.2 vs 1.3), smaller hippocampi (6,180 vs 7,203 mm³), and a
more Alzheimer's-like molecular profile (AV45 1.4 vs 1.1; CSF Aβ42 668 vs 1,168 pg/mL). Critically,
however, the two distributions overlap heavily for every feature — no single baseline measure cleanly
partitions converters from non-converters. This figure states visually both the promise and the
difficulty of early prediction: the consistent, highly significant shifts confirm baseline multimodal
information is genuinely predictive of *future* decline, but the pervasive overlap explains why
discrimination is good rather than perfect in the impaired-spectrum cohorts and genuinely hard from full
cognitive normality (Section 4.5). (This pooled non-demented view of 1,761 participants is the union of
the CN and MCI cohorts analyzed separately in the modeling sections — 74 confirmed CN converters and 228
confirmed MCI converters — under the same confirmed-conversion definition.)

## 4.3 Impact of evaluation design (data leakage)

Preliminary modeling that split the data at the visit level (i.e., treating each of a participant's
~4–5 visits as an independent record) produced optimistic accuracy estimates. For the early-detection
task, a Random Forest reported ~82% accuracy under visit-level splitting; however, under a correct
patient-grouped split the same model's balanced accuracy fell to ~34% (chance level for the outcome
distribution). The discrepancy arose because a participant's repeated visits carry near-identical
features and the same eventual-outcome label; a random visit-level split therefore allowed the model
to recognize individuals it had already seen rather than to generalize. All results reported below
use patient-level partitioning to avoid this bias.

## 4.4 Conversion labeling and sensitivity analysis

Because diagnostic status fluctuates in ADNI, the definition of "converter" materially affects the
analysis. Diagnostic reversion (an improvement between visits) occurred in 123 participants (5.8%),
predominantly MCI → CN (108 occurrences) with some Dementia → MCI (28). Twenty-eight participants
exhibited the CN → (MCI/Dementia) → CN pattern.

Table 4.2 reports the number of converters under alternative definitions. Requiring a **confirmed**
transition (worse stage sustained ≥2 consecutive visits) reduced converter counts by roughly a
quarter to a third relative to a naïve last-visit definition, removing single-visit fluctuations. The
confirmed definition was pre-specified as the primary outcome for all subsequent models.

**Table 4.2 — Converters by outcome definition**

| Definition | MCI→Dementia | CN→MCI/Dementia |
|---|---|---|
| Last-visit only | 329 (39%) | 110 (21%) |
| Ever reached worse stage | 340 (40%) | 120 (22%) |
| **Confirmed (≥2 visits) — primary** | **237 (28%)** | **78 (15%)** |
| Confirmed within 36 months | 181 (29% of eligible) | 27 (7% of eligible) |
| Confirmed within 24 months | 141 (20% of eligible) | 18 (4% of eligible) |

Short fixed-horizon definitions (24/36 months) were inappropriate for the CN cohort because CN→MCI
conversion is slow (median time to confirmed conversion ≈ 4 years); the confirmed-any-time definition
was therefore used, with time-to-event modeled explicitly via survival analysis (Section 4.7).

## 4.5 Predictive performance across cohorts and algorithms

Three cohorts were modeled: (A) baseline **CN → progression** to MCI or dementia; (B) baseline
**MCI → Dementia**; and (C) a **pooled** CN+MCI cohort predicting progression to dementia, with
baseline diagnosis deliberately excluded from the feature set so that the model surfaced biological
and cognitive predictors rather than the trivial CN-vs-MCI distinction.

Six algorithms named in the study design were evaluated identically under 5-fold cross-validation
with SMOTE applied inside training folds only. Discrimination (ROC-AUC) is reported in Table 4.3 and
the receiver operating characteristic curves in _[Fig 1 — fig1_roc_cohorts.png]_.

**Table 4.3 — ROC-AUC by model and cohort (5-fold CV, mean ± SD)**

| Model | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| Logistic Regression | 0.69 ± 0.05 | 0.82 ± 0.02 | 0.87 ± 0.03 |
| Random Forest | 0.65 ± 0.03 | 0.83 ± 0.03 | 0.88 ± 0.03 |
| XGBoost | 0.69 ± 0.04 | 0.82 ± 0.03 | 0.87 ± 0.03 |
| SVM (RBF) | 0.68 ± 0.03 | 0.81 ± 0.02 | 0.86 ± 0.03 |
| K-Nearest Neighbors | 0.64 ± 0.04 | 0.78 ± 0.03 | 0.83 ± 0.03 |
| Neural Network (MLP) | 0.62 ± 0.05 | 0.80 ± 0.02 | 0.84 ± 0.04 |

Cohort n / events: CN→progression 519 / 74 (14%); MCI→Dementia 819 / 228 (28%); Pooled 1,338 / 244 (18%).

Two patterns are notable. First, discrimination increased with baseline impairment: the pooled and
MCI cohorts achieved strong performance (AUC 0.83–0.88), whereas prediction of progression from full
cognitive normality was substantially harder and under-powered (AUC ≈ 0.65–0.69, 74 events). Second,
the top-performing algorithms — Random Forest, XGBoost, and Logistic Regression — were statistically
indistinguishable, with the simple linear model matching the ensembles. This indicates that the
predictive signal in these features is largely linear and does not require nonlinear modeling, which
qualifies the study hypothesis (Section 5.3).

## 4.6 Predictors of conversion and their stage dependence

Permutation importance (mean decrease in ROC-AUC on held-out folds) was used to rank predictors within
each cohort _[Fig 4 — fig4_predictors.png]_. This complements the exploratory finding that converters
and stable participants already separate at baseline on several of these measures (Section 4.2, Figure
EDA-5). Two complementary feature-selection methods were also applied to the pooled cohort: univariate
selection (ANOVA F-test, SelectKBest) and Recursive Feature Elimination with logistic regression.

**Table 4.4 — Top early predictors by cohort (permutation importance rank)**

| Rank | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| 1 | Hippocampus | FAQ | FAQ |
| 2 | ICV | FDG | AV45 |
| 3 | MOCA | LDELTOTAL | ABETA |
| 4 | Age | mPACCtrailsB | LDELTOTAL |
| 5 | LDELTOTAL | ADAS13 | RAVLT-immediate |
| 6 | MMSE | Age | FDG |
| 7 | FDG | ABETA | CDRSB |
| 8 | CDRSB | RAVLT-immediate | mPACCtrailsB |

The dominant predictors shifted with disease stage. At the earliest (CN) stage, **structural and
memory** measures led — hippocampal volume, intracranial volume, memory (LDELTOTAL), and global
cognition (MOCA, MMSE) — consistent with early medial-temporal atrophy. Closer to dementia (MCI stage),
the strongest predictors were measures of **daily function (FAQ), brain metabolism (FDG), and amyloid
burden (AV45, ABETA)**. The corrected CSF phosphorylated-tau measure (PTAU) entered the models as a
**mid-tier predictor** (Random Forest importance rank ≈ 11–12 of 33; ranked 9th in the pooled cohort),
consistent with its known but partly redundant relationship to total tau (Methods §3.12).

Two complementary selection methods were applied to the pooled cohort: SelectKBest (ANOVA F-test) chose
mPACCtrailsB, FAQ, ADAS13, mPACCdigit, LDELTOTAL, CDRSB, AV45, MOCA, RAVLT-immediate, and FDG; RFE
(logistic) chose AGE, ABETA, FAQ, Hippocampus, ICV, mPACCtrailsB, PTAU, TAU, WholeBrain, and Never-married.
**FAQ was selected by all three approaches** (permutation importance, SelectKBest, RFE), and a further
group appeared in two of the three — **LDELTOTAL, AV45, CDRSB, FDG, RAVLT-immediate, mPACCtrailsB, and
ABETA** — constituting the most robust predictor set. That RFE retained both PTAU and TAU indicates
each tau species carries some non-redundant signal once PTAU is correctly scaled. One RFE-selected
feature ("Never married") is almost certainly spurious and illustrates the value of requiring
convergence across selection methods.

## 4.7 Time to conversion (survival analysis)

For the MCI cohort (819 participants; 228 confirmed conversions; 591 right-censored at last visit),
time from baseline to first confirmed dementia was modeled. Kaplan–Meier estimates stratified by APOE4
status _[Fig 2 — fig2_km_apoe4.png]_ showed markedly faster progression among APOE4 carriers:

**Table 4.5 — Kaplan–Meier: probability of remaining dementia-free**

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

## 4.8 A parsimonious clinical risk score

To assess whether a small set of clinically accessible variables could approximate the full models, a
logistic-regression risk score was built for MCI→Dementia from seven inputs (age, APOE4, MMSE, FAQ,
CDRSB, hippocampal volume, ADAS13). This parsimonious score achieved ROC-AUC ≈ 0.81 ± 0.03 — nearly
matching the full multivariable models — indicating that a handful of routine measures (led by ADAS13,
FAQ, hippocampal volume, and APOE4) capture most of the available predictive signal.

## 4.9 Cognitive decline trajectories

Linear mixed-effects models (random intercept and slope per participant) characterized the rate of
cognitive decline by baseline group. All groups worsened over time, and the dementia group declined
fastest: ADAS13 increased by ≈ +2.2 points/year in the dementia group versus ≈ +1.7 points/year in
the CN group; CDRSB showed the same ordering. Absolute CN slopes should be interpreted with caution,
as the CN group contains future converters, but the relative ordering is consistent with expected
disease progression.

## 4.10 Detailed classification performance and calibration

Table 4.6 reports discrimination (ROC-AUC with bootstrap 95% confidence intervals from 1,000 resamples)
alongside threshold-based operating characteristics at a 0.5 cut-point (sensitivity, specificity,
positive and negative predictive value, F1) and probability calibration (Brier score) for each cohort.

**Table 4.6 — Detailed performance by cohort (patient-level out-of-fold predictions).**

| Cohort | ROC-AUC (95% CI) | Sens. | Spec. | PPV | NPV | F1 | Brier |
|---|---|---|---|---|---|---|---|
| CN → progression | 0.65 (0.58–0.72) | 24% | 89% | 28% | 88% | 0.26 | 0.147 |
| MCI → Dementia | 0.82 (0.80–0.85) | 65% | 80% | 56% | 86% | 0.60 | 0.155 |
| Pooled → AD | 0.88 (0.86–0.90) | 67% | 88% | 55% | 92% | 0.61 | 0.113 |

The pooled and MCI models combined high specificity with high negative predictive value (NPV 86–92%):
a low predicted risk reliably identified non-converters, which is clinically useful for ruling out
imminent progression. Positive predictive value was more modest (55–56%), an expected consequence of the
low conversion base rate. Brier scores of 0.11–0.16 indicate reasonable probability calibration. The CN
model's low sensitivity at the default threshold (24%) reflects its limited statistical power; where
early flagging is prioritized, a lower decision threshold would trade specificity for sensitivity.

## 4.11 Subgroup and fairness analysis

To assess generalizability across patient subgroups, pooled-model discrimination was recomputed within
strata defined by sex, APOE4 status, education, and age (Table 4.7, Figure 5).

**Table 4.7 — Pooled → AD ROC-AUC by subgroup.**

| Subgroup | n | Events | ROC-AUC |
|---|---|---|---|
| Male | 737 | 142 | 0.87 |
| Female | 601 | 102 | 0.88 |
| APOE4-negative | 771 | 83 | 0.87 |
| APOE4-positive | 567 | 161 | 0.84 |
| Education < 16 yr | 447 | 92 | 0.83 |
| Education ≥ 16 yr | 891 | 152 | 0.90 |
| Age < 75 yr | 767 | 134 | 0.91 |
| Age ≥ 75 yr | 571 | 110 | 0.82 |

Performance was equivalent by sex (0.87 vs 0.88). Two disparities were notable: the model discriminated
better for more-educated participants (0.90 vs 0.83) and for younger participants (0.91 vs 0.82), and
modestly worse for APOE4 carriers (0.84 vs 0.87). These gaps — likely reflecting ADNI's education-skewed
enrollment and the greater clinical heterogeneity of older and higher-genetic-risk patients — matter for
equitable deployment and are discussed in Section 5.7.

## 4.12 Feature-group contribution

To quantify each data modality's contribution, the pooled model was refit using each feature group in
isolation and, separately, with each group removed (Table 4.8).

**Table 4.8 — Feature-group ablation (Pooled → AD; full-model AUC 0.88).**

| Feature group | AUC (group alone) | AUC (group removed) | Δ if removed |
|---|---|---|---|
| Cognitive / functional | 0.855 | 0.838 | −0.042 |
| MRI volumetric | 0.747 | 0.877 | −0.003 |
| PET (AV45, FDG) | 0.791 | 0.879 | −0.001 |
| CSF (ABETA, TAU, PTAU) | 0.755 | 0.877 | −0.003 |
| Demographic / genetic | 0.659 | 0.876 | −0.004 |

Cognitive and functional measures alone reached an AUC of 0.855 — close to the full multimodal model
(0.88) — and their removal produced by far the largest degradation (−0.042). Removing any single
imaging, biomarker, or demographic block barely changed performance (−0.001 to −0.004), because those
modalities are substantially correlated with the cognitive measures and with one another (Section 4.2,
Figure EDA-4). This redundancy explains why the parsimonious clinical score (Section 4.8) approaches the
full model, and it indicates that, for conversion prediction in this cohort, cognitive-functional
assessment carries most of the actionable signal.

---

### Notes for you (delete before submission)
- Every number here is traceable to notebooks 06–08 and the figures in `notebooks/figures/`.
- **Section map after adding EDA:** §4.1 sample/flow + Table 4.1 → §4.2 exploratory data analysis
  (Figures EDA-1–EDA-5) → §4.3 data leakage → §4.4 labeling → §4.5 performance → §4.6 predictors →
  §4.7 survival → §4.8 risk score → §4.9 trajectories → §4.10 detailed metrics → §4.11 fairness →
  §4.12 ablation. Tables keep their numbers (4.1–4.8); figures are EDA-1…EDA-5 and 1…5.
- The 89% 3-class result from the original `04` notebook is intentionally **not** presented as an
  early-detection result — if you want to keep it, present it as *concurrent diagnostic classification*
  and note its circularity (it uses CDRSB/FAQ, which partly define the diagnosis).
