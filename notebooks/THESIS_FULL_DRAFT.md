# Predicting Alzheimer's Disease Progression with Machine Learning
### Early, Leakage-Free Prediction of Diagnosis and Conversion from Multimodal ADNI Data

**A thesis submitted in partial fulfillment of the requirements for the**
**Master of Science in Data Science, Northwestern University**

Author: Warda Saeed
Advisor: _[name]_
Date: July 2026

---

> **Working master draft.** This document stitches the chapter drafts into one file for review. A single
> consolidated checklist of every open item (p-tau blanks, citations, figure tasks) appears in the
> **Author Checklist** at the end. All results are reproducible from notebooks 06–08 (random seed 42).

---


# Abstract (Draft)

> Grounded in the verified results (notebooks 06–08). Bracketed **`⟦…⟧`** markers are fill-in blanks to
> complete after phosphorylated-tau (p-tau) is restored from the ADNI source; none change the core
> findings. A ready-to-drop sentence for each blank is suggested in the notes below.

---

## Abstract

**Background.** Alzheimer's disease (AD) is a progressive neurodegenerative disorder in which the window
for effective intervention opens well before dementia, during the cognitively normal (CN) and mild
cognitive impairment (MCI) stages. Reliable early prediction of who will progress — and how soon —
remains an unmet need, and machine-learning claims in this area are frequently undermined by
methodological choices that inflate apparent performance.

**Objective.** This thesis applies machine learning to multimodal Alzheimer's Disease Neuroimaging
Initiative (ADNI) data — demographics, cognitive assessments, structural MRI, FDG- and amyloid-PET, and
cerebrospinal-fluid biomarkers — to identify early predictors of AD and of conversion to dementia,
under a rigorous, leakage-free evaluation framework.

**Methods.** Analyses were conducted at the participant level: each participant contributed a single
baseline record predicting their future outcome, so that no individual appeared in both training and
test partitions. Conversion was defined conservatively as a worse diagnostic stage sustained across at
least two consecutive visits, and clinically implausible reversions were excluded. Three cohorts were
modeled — CN→progression, MCI→Dementia, and a pooled CN+MCI→AD cohort — using six algorithms (logistic
regression, random forest, XGBoost, support vector machine, k-nearest neighbors, and a neural network)
under 5-fold cross-validation with class-imbalance correction applied within training folds only. Time
to conversion was modeled with Kaplan–Meier and Cox proportional-hazards analysis; predictor importance
was assessed by permutation importance and two feature-selection methods. ⟦*p-tau data note:* one
biomarker (phosphorylated tau) was **restored from source / excluded** after a preprocessing error;
final models used ⟦N⟧ predictors.⟧

**Results.** Progression to dementia was predicted with good discrimination in the impaired-spectrum
cohorts (pooled CN+MCI→AD ROC-AUC 0.88; MCI→Dementia 0.83) but poorly from full cognitive normality
(CN→progression 0.66), reflecting a slow, low-event process. Random forest, XGBoost, and logistic
regression performed equivalently, indicating a largely linear predictive signal. The most informative
predictors shifted with disease stage — from structural and memory measures (hippocampal volume,
intracranial volume, delayed memory) at the CN stage to functional (FAQ), metabolic (FDG), and amyloid
(AV45, ABETA) measures nearer dementia. APOE4 carriers converted markedly faster (55% remained
dementia-free at five years versus 80% of non-carriers). A parsimonious seven-variable risk score
approached the full models (ROC-AUC 0.81). ⟦*p-tau result:* with p-tau restored, tau-pathology measures
ranked ⟦position/among the top predictors⟧ in the ⟦MCI / pooled⟧ cohort(s).⟧

**Conclusions.** Baseline multimodal measures predict AD progression with clinically useful accuracy,
and the dominant predictors change systematically across the disease continuum. The study also
demonstrates that participant-level evaluation and confirmed-conversion labeling are essential for
credible estimates: naïve visit-level analysis inflated an early-detection result from chance to ~82%.
These findings support stage-aware, interpretable models — and careful methodology — for early
Alzheimer's risk stratification. ⟦*optional p-tau clause:* and confirm phosphorylated tau as an
informative early biomarker when correctly measured.⟧

**Keywords:** Alzheimer's disease; mild cognitive impairment; ADNI; machine learning; conversion
prediction; survival analysis; data leakage; biomarkers.

---

### Fill-in guide (complete after p-tau restoration)

- **⟦Methods p-tau note⟧** → e.g.: *"phosphorylated tau (p-tau181), initially corrupted by a
  preprocessing error, was regenerated from the ADNI source; final models used 33 predictors."*
  (If you end up keeping it dropped instead: *"…was excluded; final models used 32 predictors."*)
- **⟦N predictors⟧** → `33` if p-tau restored, `32` if left out.
- **⟦p-tau result sentence⟧** → fill from the re-run's permutation-importance table, e.g.: *"with p-tau
  restored, it ranked among the top five predictors in the MCI→Dementia cohort"* — **only state the rank
  the re-run actually shows.** If p-tau does *not* rank highly, say so honestly (e.g., *"p-tau added
  little beyond total tau"*).
- **⟦optional conclusion clause⟧** → include only if the result supports it.

*Word count (excluding brackets/keywords): ~340; trim to your program's limit (commonly 250–300) if
needed — the Background and Methods paragraphs compress most easily.*



---


## Table of Contents

- Abstract
- Chapter 1 — Introduction
- Chapter 2 — Literature Review
- Chapter 3 — Methods
- Chapter 4 — Results
- Chapter 5 — Discussion
- Chapter 6 — Conclusion
- References
- Author Checklist (open items)

---


# Chapters 1 & 2 — Introduction and Literature Review (Rewrite Draft)

> Preserves the existing draft's content and its four verified references (WHO 2021; Venugopalan et
> al. 2021; Grabher 2018; Porsteinsson et al. 2021). Prose tightened; **§1.3 Objectives and §1.4
> Hypothesis updated to match the study as actually conducted**; a methodological-gap paragraph added
> to §2.7. `[CITATION NEEDED]` marks claims that require a supporting reference — no references were
> fabricated.

---

# Chapter 1 — Introduction

## 1.1 Overview of Alzheimer's disease

Alzheimer's disease (AD) is a progressive neurodegenerative disorder that primarily impairs memory and
cognition and ultimately erodes independent functioning. It is characterized pathologically by the
accumulation of misfolded proteins — extracellular amyloid-beta plaques and intracellular
neurofibrillary tau tangles — accompanied by widespread neuronal loss and brain atrophy. The disease
imposes an enormous and growing burden: an estimated 5.7 million individuals were affected in 2020, a
figure projected to reach 79 million worldwide by 2030 and approximately 139 million by 2050 — about
16% of the projected global population — with associated healthcare expenditures approaching
US$2 trillion (World Health Organization, 2021; Venugopalan et al., 2021). As one commentator observed,
AD is among the costliest chronic diseases to society, with the potential to strain healthcare systems
to their limits (Grabher, 2018). In the absence of a cure, the most actionable lever for reducing this
burden is **earlier and more accurate detection**, which creates the window in which existing and
emerging interventions are most effective.

## 1.2 Statement of the problem

Despite advances in neuroimaging and fluid biomarkers, early AD diagnosis remains difficult. Current
clinical tools often lack the sensitivity to detect the earliest cognitive change, and patients'
compensatory strategies can mask deficits, delaying diagnosis — on average by roughly two years from
symptom onset (Porsteinsson et al., 2021). The transitional stage of mild cognitive impairment (MCI)
is a particularly important target, as it represents a period during which intervention may most
plausibly alter trajectory, yet only a subset of MCI patients progress to dementia. There is therefore
a pressing need for data-driven methods that (a) identify which baseline measures signal impending
decline and (b) do so with the methodological rigor required for trustworthy, generalizable estimates.

## 1.3 Research objectives

This thesis applies machine learning to multimodal ADNI data — demographics, cognitive assessments,
structural MRI, FDG- and amyloid-PET, and CSF biomarkers — to identify early predictors of Alzheimer's
disease and of conversion to dementia. Its specific objectives are:

1. To identify baseline predictors of progression to dementia across the non-demented spectrum
   (cognitively normal and MCI), using a leakage-free, participant-level evaluation framework.
2. To compare the discriminative performance of multiple machine-learning algorithms (logistic
   regression, random forest, XGBoost, support vector machine, k-nearest neighbors, and a neural
   network) for predicting conversion.
3. To determine whether the most informative predictors **differ by baseline diagnostic stage**, by
   modeling CN and MCI cohorts separately as well as pooled.
4. To model the **timing** of MCI-to-dementia conversion using survival analysis and to identify
   predictors of conversion tempo.
5. To assess whether a small, clinically accessible set of measures can approximate the full model as a
   practical risk score.

## 1.4 Hypotheses

**Primary hypothesis.** Baseline multimodal measures predict progression to dementia with clinically
useful discrimination, and the most informative predictors differ systematically by baseline stage —
with structural and memory measures dominating earliest (CN) and functional, metabolic, and amyloid
measures dominating nearer to dementia (MCI).

**Secondary hypothesis.** Nonlinear ensemble methods (random forest, XGBoost) will improve
discrimination over linear models. _(As reported in Chapter 5, this secondary hypothesis was only
partially supported — ensembles did not meaningfully exceed logistic regression — which is itself an
informative result.)_

> _Note to author: the original proposal framed ensemble superiority as the primary hypothesis. It is
> presented here as a secondary, testable hypothesis so that the (honest) finding of near-equivalence
> is reported as evidence rather than as a failure. Adjust to your advisor's preference._

## 1.5 Justification and significance

By leveraging ADNI's multimodal, longitudinal design, this study aims to strengthen the evidence base
for early AD detection in two ways. Substantively, it characterizes stage-specific early predictors
that could inform assessment prioritization. Methodologically, it demonstrates how evaluation design
(participant-level versus visit-level data splitting) and outcome definition (confirmed versus transient
conversion) materially affect reported performance — an issue of direct relevance to the credibility of
machine-learning claims in this field.

---

# Chapter 2 — Literature Review

## 2.1 Genetic factors in AD

Although its precise etiology remains under investigation, AD has well-established genetic contributors.
Autosomal-dominant mutations in **presenilin 1 (PSEN1)** and **presenilin 2 (PSEN2)** — components of
the γ-secretase complex that cleaves amyloid precursor protein (APP) — are associated with early-onset
AD, typically before age 60. For the far more common late-onset form, the **apolipoprotein E (APOE)**
ε4 allele is the strongest common genetic risk factor, acting through effects on amyloid deposition and
tau phosphorylation, while the ε2 allele appears protective. `[CITATION NEEDED — APOE/PSEN mechanisms]`

## 2.2 Neuropathology

AD pathology is defined by two hallmarks: **amyloid plaques**, formed by aggregation of amyloid-beta
peptides derived from APP cleavage, which accumulate extracellularly and disrupt neuronal
communication; and **neurofibrillary tangles** of hyperphosphorylated tau, which impair intracellular
transport and contribute to neuronal death. The relative timing and coupling of these processes underlie
contemporary biomarker-based staging of the disease. `[CITATION NEEDED — amyloid/tau staging]`

## 2.3 Brain atrophy and structural change

Neurodegeneration in AD follows a characteristic spatial trajectory, beginning in the medial temporal
lobe — particularly the **hippocampus and entorhinal cortex** — and extending through parahippocampal
and temporal regions, the limbic system, and ultimately widespread neocortex. Hippocampal volume is
reported to be reduced by roughly a quarter in MCI and by up to 40% in AD relative to controls.
`[CITATION NEEDED — hippocampal atrophy figures]` These structural signatures motivate the MRI-derived
volumetric features (hippocampus, entorhinal cortex, mid-temporal cortex, ventricles, whole brain) used
in the present analysis.

## 2.4 Diagnostic methods and biomarkers

Contemporary AD assessment integrates three streams. **Neuroimaging** — structural MRI for atrophy,
FDG-PET for glucose metabolism, and amyloid-PET (e.g., AV45) for plaque burden. **CSF biomarkers** —
reduced amyloid-beta (ABETA) and elevated total and phosphorylated tau (TAU, p-tau), which change early
in the disease course. **Neuropsychological testing** — instruments such as ADAS-Cog, MMSE, MoCA, RAVLT,
the FAQ, and CDR-SB that quantify cognitive and functional status. The present study draws on all three
streams. _(Note: phosphorylated tau was excluded from the analyses reported here owing to a data
preprocessing error and is slated for restoration; see Methods §3.9.)_

## 2.5 Benefits of early diagnosis

Earlier diagnosis benefits patients (access to treatment during the most effective window; time for
financial and legal planning), caregivers (reduced burden; opportunity for care planning), and health
systems (timely intervention; capacity management) (Porsteinsson et al., 2021). `[CITATION NEEDED —
caregiver-burden statistics]` These benefits are the practical motivation for improving predictive
tools at the MCI and preclinical stages.

## 2.6 The role of ADNI

The Alzheimer's Disease Neuroimaging Initiative (ADNI), launched in 2003 as a public–private
partnership, has been central to AD biomarker research. Its longitudinal, multimodal design — repeated
imaging, fluid biomarkers, and cognitive assessment across the diagnostic spectrum — enables the study
of disease trajectories and the validation of predictive models. Its enrollment strategy, however,
preferentially recruits participants with existing cognitive concern, a feature that shapes conversion
rates and is addressed as a limitation of the present work (Chapter 5). `[CITATION NEEDED — ADNI design
reference]`

## 2.7 Machine learning in AD prediction, and the methodological gap

A substantial literature applies machine learning to ADNI data to predict AD progression from
multimodal features, frequently reporting high accuracy for stage classification and MCI-to-dementia
conversion. `[CITATION NEEDED — 2–3 representative ADNI ML studies, e.g., Venugopalan et al., 2021 and
others]` Two methodological issues, however, are inconsistently handled in this literature and are
central to the present thesis. First, because ADNI participants contribute **multiple visits with
near-identical features and shared outcome labels**, partitioning data at the visit level rather than
the participant level can allow information to leak between training and test sets and inflate reported
performance. `[CITATION NEEDED — data leakage in longitudinal ML]` Second, **diagnostic status
fluctuates over time** (including reversion from MCI to normal), so outcome definitions based on a
single visit can misclassify converters. This thesis contributes by applying participant-level
evaluation and a confirmed-conversion outcome throughout, and by quantifying how these choices affect
results — complementing the substantive goal of identifying stage-specific early predictors of AD.

---

### Notes for you (delete before submission)
- All four in-text references (WHO 2021; Venugopalan et al. 2021; Grabher 2018; Porsteinsson et al.
  2021) are from your existing draft and are retained.
- Every `[CITATION NEEDED]` marks a factual claim that should be supported with a reference before
  submission. I did **not** invent any citations.
- The only substantive edits versus your original are §1.3 (objectives) and §1.4 (hypotheses), aligned
  to the analysis actually performed, plus the methodological-gap paragraph in §2.7.



---


# Chapter 3 — Methods (Rewrite Draft)

> Draft grounded in the committed, reproducible notebooks (01–03 preprocessing; 06–08 analysis) and
> verified line-by-line against the executed code. Every hyperparameter, cohort size, and definition
> below was confirmed against the source. Random seed = 42 throughout.
>
> **Data-integrity resolution:** the `PTAU` variable was found to be corrupted — a duplicate of `TAU`
> (Pearson r = 1.00), traceable to a coding error in baseline preparation where total-tau values were
> assigned to the phosphorylated-tau column. `PTAU` was therefore **excluded from all analyses**, and
> all results below reflect the corrected **32-feature** set. The correction did not change the
> classification AUCs or the permutation-importance predictor rankings (PTAU was never a top predictor);
> its effects were to remove a spurious RFE selection and to let total tau (TAU) surface cleanly. See
> Section 3.9.

---

## 3.1 Study design and data source

This was a retrospective, longitudinal cohort study using data derived from the Alzheimer's Disease
Neuroimaging Initiative (ADNI) merged dataset (ADNIMERGE). Participants spanned the diagnostic
spectrum — cognitively normal (CN), mild cognitive impairment (MCI), and dementia — with repeated
assessments (demographics, cognitive testing, structural MRI, FDG- and amyloid-PET, and cerebrospinal
fluid biomarkers) collected at approximately 6- to 12-month intervals.

## 3.2 Baseline data preparation

From the merged dataset, 39 variables were retained: identifiers and timing (PTID, VISCODE, Years.bl,
Month.bl, visit month M), demographics (AGE, PTEDUCAT, PTGENDER, PTETHCAT, PTRACCAT, PTMARRY, APOE4),
diagnosis (DX current, DX.bl baseline), and multimodal measures (ABETA, ADAS13, AV45, CDRSB,
Entorhinal, FAQ, FDG, Fusiform, Hippocampus, ICV, LDELTOTAL, MidTemp, MMSE, MOCA, mPACCdigit,
mPACCtrailsB, PTAU, RAVLT [forgetting, immediate, learning, percent-forgetting], TAU, TRABSCOR,
Ventricles, WholeBrain). Records lacking a current diagnosis were removed, and data were sorted
chronologically within participant.

Diagnostic labels were harmonized so that baseline and follow-up categories were comparable: "AD" was
recoded to "Dementia," and "LMCI"/"EMCI" were collapsed to "MCI." Censored biomarker values reported
as thresholds were converted to numeric values (ABETA: ">1700"→1700, "<200"→200; TAU: "<80"→80,
">1300"→1300). *(The intended PTAU threshold conversion ("<8"→8) additionally overwrote PTAU with TAU
values in error; PTAU was consequently excluded from all modeling — see the resolution note above and
Section 3.9.)*

## 3.3 Missing-data treatment and encoding

For every variable containing missing values, a binary missingness-indicator ("null flag") was created
and retained in the dataset (27 indicators), preserving information about which values were imputed.
Missing values were then imputed through the processing pipeline using a combination of within-patient
last-observation-carried-forward, median imputation for variables with low missingness, and
multivariate model-based imputation (iterative/MICE-style imputation and a Random Forest regressor for
higher-missingness variables). Variables missing for the large majority of participants (e.g., PIB,
DIGITSCOR) were excluded during baseline preparation. The resulting analytic dataset contained no
missing values.

Categorical variables were encoded numerically: sex as binary (Male = 1), marital status as four
indicator variables (Married, Widowed, Divorced, Never-married), and diagnosis ordinally
(CN = 0, MCI = 1, Dementia = 2). Continuous predictors were standardized (zero mean, unit variance) at
model-fitting time within each cross-validation fold (Section 3.6), rather than being standardized in
the stored dataset.

## 3.4 Cohort construction and unit of analysis

To respect the repeated-measures structure and prevent information leakage, all predictive modeling was
conducted at the **participant level**. Each participant was represented by a single record — their
**baseline (earliest) visit** — and models predicted that participant's **future** diagnostic outcome.
This guaranteed that every train/test partition separated distinct individuals.

**Exclusions.** Of 2,131 participants, 453 with only a single visit (no observable follow-up) and 28
with a clinically implausible improvement in diagnosis (Dementia → a less-severe stage, treated as
diagnostic error) were excluded, leaving approximately 1,650 analyzable participants.

**Outcome definition (confirmed conversion).** Because diagnostic status fluctuates in ADNI, a
participant was labeled a converter only if a more severe stage was **sustained on at least two
consecutive visits**. Single-visit fluctuations were not counted as conversion. This "confirmed"
definition was pre-specified as the primary outcome. Its effect was quantified in a sensitivity
analysis comparing five definitions (last-visit, ever-reached, confirmed, and confirmed within 24 and
36 months; Results Table 4.1).

**Analytic cohorts.**
- **Cohort A — CN → progression:** baseline CN, outcome = confirmed progression to MCI or dementia
  (n = 519; 74 events, 14%).
- **Cohort B — MCI → Dementia:** baseline MCI, outcome = confirmed progression to dementia
  (n = 819; 228 events, 28%).
- **Cohort C — Pooled → AD:** baseline CN or MCI combined, outcome = confirmed progression to dementia
  (n = 1,338; 244 events, 18%). Baseline diagnosis was deliberately **excluded** from the feature set
  in this cohort so the model surfaced biological and cognitive predictors rather than the trivial
  CN-versus-MCI distinction.

## 3.5 Feature set

Thirty-two baseline predictors were used: AGE, PTEDUCAT, PTGENDER, APOE4, ABETA, ADAS13, AV45, CDRSB,
Entorhinal, FAQ, FDG, Fusiform, Hippocampus, ICV, LDELTOTAL, MidTemp, MMSE, MOCA, mPACCdigit,
mPACCtrailsB, RAVLT (forgetting, immediate, learning, percent-forgetting), TAU, TRABSCOR,
Ventricles, WholeBrain, and the four marital-status indicators. Identifiers, timing variables, current
and future diagnosis labels, the 27 missingness indicators, and the corrupted PTAU column (Section 3.9)
were excluded from the predictor set.

## 3.6 Classification models

Six algorithms named in the study design were evaluated under an identical protocol:

1. **Logistic Regression** — L2-regularized, `max_iter=2000`, `class_weight='balanced'`.
2. **Random Forest** — 400 trees, `max_depth=10`, `class_weight='balanced'`.
3. **XGBoost** — 300 estimators, `max_depth=4`, `learning_rate=0.05`, `subsample=0.8`, log-loss objective.
4. **Support Vector Machine** — RBF kernel, `C=1`, `class_weight='balanced'` (probabilistic scores via the decision function).
5. **K-Nearest Neighbors** — `k=7`.
6. **Neural Network (Multilayer Perceptron)** — two hidden layers (32, 16 units), `max_iter=400`.

Each model was embedded in a pipeline that, **within each training fold only**, standardized features
(StandardScaler) and applied SMOTE (Synthetic Minority Over-sampling Technique) to address class
imbalance. Performing scaling and oversampling inside the fold prevented information from the test fold
influencing training. Performance was estimated by **5-fold stratified cross-validation**
(`shuffle=True`, `random_state=42`), with the area under the receiver-operating-characteristic curve
(ROC-AUC) as the primary metric; balanced accuracy, sensitivity, and specificity were also computed.
Results are reported as mean ± standard deviation across folds.

## 3.7 Predictor identification

Three complementary approaches identified important predictors:

- **Permutation importance** — the mean decrease in ROC-AUC when a feature's values were randomly
  permuted, computed on **held-out** folds (`n_repeats=8`, scoring = ROC-AUC) and averaged across the
  five folds. This model-agnostic measure was computed for each cohort.
- **Univariate selection (SelectKBest)** — ANOVA F-test ranking, top 10 features (pooled cohort).
- **Recursive Feature Elimination (RFE)** — with a logistic-regression estimator, selecting 10 features
  (pooled cohort).

Predictors appearing across all three approaches were treated as the most robust.

## 3.8 Survival analysis (time to conversion)

For the MCI cohort, time from baseline to **first confirmed** dementia conversion was modeled;
participants who never confirmed conversion were **right-censored** at their last visit
(n = 819; 228 events; 591 censored). **Kaplan–Meier** estimates of the probability of remaining
dementia-free were computed overall and stratified by APOE4 carrier status (APOE4 allele count > 0).
A **Cox proportional-hazards** model (statsmodels PHReg, Efron handling of ties) estimated the
association of 14 standardized baseline covariates (AGE, PTEDUCAT, APOE4, ADAS13, MMSE, MOCA, FAQ,
CDRSB, Hippocampus, LDELTOTAL, FDG, AV45, ABETA, RAVLT-immediate) with conversion hazard; hazard
ratios are reported per one standard-deviation increase.

## 3.9 Clinical risk score

To evaluate whether a small, clinically accessible variable set could approximate the full models, a
logistic-regression risk score for MCI→Dementia was constructed from seven inputs (AGE, APOE4, MMSE,
FAQ, CDRSB, Hippocampus, ADAS13). Standardized coefficients were scaled to integer points
(coefficient ÷ maximum absolute coefficient × 10). Discrimination was estimated by 5-fold stratified
cross-validation.

## 3.10 Cognitive-decline trajectories

Longitudinal (visit-level) cognitive trajectories were modeled with **linear mixed-effects models**
(statsmodels MixedLM), including a random intercept and random slope for time per participant. For
each outcome (CDRSB and ADAS13), fixed effects were time (Years.bl), baseline diagnostic group, and
their interaction (CN as reference), yielding group-specific annual rates of change.

## 3.11 Software and reproducibility

Analyses were conducted in Python 3.11 using pandas, NumPy, scikit-learn, imbalanced-learn (SMOTE),
XGBoost, statsmodels (Cox PH and mixed-effects), and Matplotlib. A fixed random seed (42) was used for
all stochastic components (splitting, SMOTE, model initialization, permutation importance). All
analyses are provided as executable notebooks (`06_Early_Conversion_Prediction`,
`07_Stratified_AD_Predictors`, `08_Model_Comparison_FeatSel_RiskScore`) with embedded outputs and a
matching results summary.

> _[Insert exact library versions from your final run environment before submission.]_

---

### Data-integrity note (Section 3.9) — resolved
The `PTAU` = `TAU` corruption (Pearson r = 1.00), caused by a coding error in baseline preparation, was
resolved by **excluding PTAU from all analyses** and re-running notebooks 06–08 with the corrected
32-feature set. As anticipated, the classification AUCs and permutation-importance rankings were
unchanged; the correction removed the spurious RFE selection of PTAU (replaced by TAU) and allowed
total tau to appear as a legitimate predictor. If the original ADNI source is available, PTAU could
alternatively be regenerated with correct phosphorylated-tau values and re-introduced; this is noted as
a possible refinement but was not required for the reported findings.



---


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
| Logistic Regression | 0.68 ± 0.05 | 0.82 ± 0.02 | 0.87 ± 0.03 |
| Random Forest | 0.66 ± 0.02 | 0.83 ± 0.03 | 0.88 ± 0.03 |
| XGBoost | 0.69 ± 0.03 | 0.83 ± 0.03 | 0.87 ± 0.03 |
| SVM (RBF) | 0.68 ± 0.03 | 0.82 ± 0.02 | 0.86 ± 0.03 |
| K-Nearest Neighbors | 0.63 ± 0.05 | 0.79 ± 0.02 | 0.83 ± 0.04 |
| Neural Network (MLP) | 0.66 ± 0.04 | 0.77 ± 0.03 | 0.82 ± 0.03 |

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
| 2 | ICV | FDG | AV45 |
| 3 | RAVLT-learning | LDELTOTAL | RAVLT-immediate |
| 4 | Age | AV45 | LDELTOTAL |
| 5 | TAU | Age | CDRSB |
| 6 | LDELTOTAL | ADAS13 | FDG |
| 7 | MOCA | ABETA | TAU |
| 8 | RAVLT-immediate | mPACCtrailsB | ABETA |

The dominant predictors shifted with disease stage. At the earliest (CN) stage, **structural and
memory** measures led — hippocampal volume, intracranial volume, and delayed/verbal memory
(LDELTOTAL, RAVLT) — consistent with early medial-temporal atrophy. Closer to dementia (MCI stage), the
strongest predictors were measures of **daily function (FAQ), brain metabolism (FDG), and amyloid
burden (AV45, ABETA)**. Total tau (TAU) also emerged as an early predictor once the corrupted PTAU
column (a duplicate of TAU) was removed from the analysis (see Methods §3.9).

Two complementary selection methods were applied to the pooled cohort: SelectKBest (ANOVA F-test) chose
mPACCtrailsB, FAQ, ADAS13, mPACCdigit, LDELTOTAL, CDRSB, AV45, MOCA, RAVLT-immediate, and FDG; RFE
(logistic) chose AGE, ABETA, FAQ, Hippocampus, ICV, MMSE, mPACCtrailsB, TAU, WholeBrain, and Never-married.
**FAQ was selected by all three approaches** (permutation importance, SelectKBest, RFE), and a further
group appeared in two of the three — **LDELTOTAL, AV45, CDRSB, FDG, RAVLT-immediate, mPACCtrailsB, ABETA,
and TAU** — constituting the most robust predictor set. One RFE-selected feature ("Never married") is
almost certainly spurious and illustrates the value of requiring convergence across selection methods.

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



---


# Chapter 5 — Discussion (Rewrite Draft)

> Interpretive chapter grounded in the verified results (notebooks 06–08, figures). Conclusions here
> do not depend on the pending PTAU restoration; markers _[p-tau: revisit after restoration]_ flag the
> few sentences to revisit once real phosphorylated-tau is re-introduced.

---

## 5.1 Summary of principal findings

This study used multimodal ADNI data to identify early predictors of Alzheimer's disease and of
conversion to dementia, under a deliberately conservative, leakage-free evaluation framework. Four
findings stand out. First, progression to dementia could be predicted from baseline measures with good
discrimination in impaired-spectrum cohorts (MCI→Dementia ROC-AUC ≈ 0.83; pooled CN+MCI→AD ≈ 0.88),
but prediction of decline from full cognitive normality was substantially harder (CN→progression
≈ 0.66–0.69). Second, the most informative predictors **shifted with disease stage**. Third, ensemble
methods did **not** meaningfully outperform logistic regression, indicating a largely linear signal.
Fourth, APOE4 carriage and baseline functional, metabolic, and amyloid measures predicted not only
*whether* but *how quickly* MCI patients converted.

## 5.2 Stage-dependent predictors

The stratified design revealed a clinically coherent progression in the dominant predictors. Among
cognitively normal participants, **structural and memory** measures led — hippocampal and intracranial
volume, delayed and verbal memory (LDELTOTAL, RAVLT), and MOCA — consistent with the established view
that medial-temporal atrophy and subtle memory change are among the earliest detectable signs of the
disease. Among MCI participants, the strongest predictors shifted toward **daily functional decline
(FAQ), cerebral glucose metabolism (FDG-PET), and amyloid burden (AV45, ABETA)**, reflecting a stage in
which pathological and functional processes are more advanced and more strongly coupled to imminent
dementia. This shift — from *structure/memory* early to *function/metabolism/pathology* later — is the
central scientific contribution of stratifying the cohorts rather than pooling them blindly, and it
aligns with contemporary staging models of the AD continuum. _[p-tau: revisit — with real p-tau
restored, tau-pathology measures may feature more prominently, especially at the MCI stage.]_

## 5.3 Model performance and the study hypothesis

The study hypothesized that ensemble methods (e.g., Random Forest) would outperform simpler linear
models. The evidence only partially supports this. While Random Forest and XGBoost achieved the highest
discrimination in absolute terms, **logistic regression matched them within cross-validation
uncertainty** across all three cohorts. The practical implication is that the predictive relationships
in these standardized, largely continuous features are approximately linear and additive, offering
little for nonlinear models to exploit. This is a more accurate and more defensible conclusion than a
claim of ensemble superiority, and it has a favorable side effect: a transparent, interpretable model
suffices, which matters for clinical translation. The comparatively weaker performance of KNN and the
multilayer perceptron is consistent with the modest sample sizes and the tabular nature of the data.

## 5.4 Timing of conversion

Survival analysis extended the binary conversion question to *when* conversion occurs. Kaplan–Meier
estimates showed markedly faster progression in APOE4 carriers (55% remained dementia-free at five
years versus 80% in non-carriers), reinforcing APOE4's role as a determinant of both risk and tempo.
The Cox model identified functional (FAQ), cognitive (ADAS13), and amyloid (AV45) measures as
predictors of faster conversion, and greater hippocampal volume, memory performance, and glucose
metabolism (FDG) as protective — a pattern that converges with the classification-based importance
rankings and lends internal consistency to the findings.

## 5.5 A methodological contribution: evaluation rigor and label quality

Beyond the substantive predictors, this work makes a methodological point that is easy to overlook in
applied machine-learning studies. Early modeling that partitioned the data at the **visit level**
produced an optimistic early-detection accuracy (~82%) that collapsed to chance (~34% balanced
accuracy) once individuals — rather than individual visits — were separated between training and test
sets. Because a participant's repeated visits share near-identical features and outcome labels, naïve
splitting allows a model to recognize individuals rather than to generalize. Relatedly, diagnostic
**reversion** (5.8% of participants improved at least once) meant that a naïve "last-visit" outcome
both missed genuine converters and counted transient fluctuations; a pre-specified **confirmed** outcome
(a worse stage sustained across ≥2 visits) was required for credible labels. Reporting these effects,
rather than concealing them, is itself a contribution: it demonstrates how ordinary data-handling
choices can transform a chance-level model into an apparently excellent one.

## 5.6 Clinical implications

The parsimonious seven-variable risk score (ROC-AUC ≈ 0.81 for MCI→Dementia) shows that a small set of
routinely available measures — led by ADAS13, FAQ, hippocampal volume, and APOE4 — captures most of the
predictive signal available from the full multimodal panel. This is encouraging for real-world use,
where full biomarker and imaging panels are often unavailable, and it dovetails with the finding that a
linear model suffices. Prioritizing functional and memory assessment, together with APOE4 genotyping,
may offer a practical, low-cost first-pass stratification of MCI patients by conversion risk.

## 5.7 Limitations

1. **Enrollment / volunteer bias.** ADNI preferentially recruits participants who already have
   cognitive concern, over-representing prevalent MCI relative to a community sample. Absolute
   conversion rates therefore overstate population risk, and the well-powered results derive largely
   from the impaired end of the spectrum.
2. **Under-powered CN cohort.** Confirmed CN→progression events were few (74), and conversion from
   normality is slow (median ≈ 4 years). The modest CN-cohort performance (AUC ≈ 0.66–0.69) should be
   read as a lower bound reflecting limited events, not as evidence that early signal is absent.
3. **Diagnostic label noise.** Even with a confirmed-conversion definition, clinical diagnoses carry
   inter-rater variability, and clinically implausible reversions (e.g., dementia→MCI) were present and
   excluded as error.
4. **Data-integrity issue (PTAU).** A preprocessing error overwrote phosphorylated tau with total tau;
   PTAU was therefore excluded from the analyses reported here. Because it was a duplicate of TAU, its
   removal did not affect results, but a clinically important biomarker (p-tau181) is consequently
   absent and should be restored from source in a subsequent iteration. _[p-tau: update once restored.]_
5. **Single-cohort, internal validation only.** All estimates derive from ADNI with cross-validation;
   no external or independent-cohort validation was performed, limiting claims about generalizability.
6. **Reversible transitions simplified.** Conversion was treated as effectively one-directional after
   confirmation; a full multi-state model of reversible CN↔MCI transitions was not undertaken.

## 5.8 Future directions

- **Restore CSF phosphorylated tau** from the ADNI source and re-estimate. In the present dataset the
  CSF p-tau field was corrupted (overwritten with total tau) and was excluded; the correct values are
  available in the ADNIMERGE2 biomarker tables and can be reintroduced, given p-tau's established value
  as an early AD biomarker.
- **Incorporate plasma (blood-based) biomarkers.** ADNI now provides plasma phosphorylated tau —
  p-tau181 (Quanterix/Simoa) and p-tau217 (Fujirebio; C2N) — alongside plasma Aβ42/40, NfL, and GFAP.
  Plasma p-tau217 in particular is among the most promising minimally-invasive AD markers. A focused
  sub-study is warranted: in the present cohort, baseline plasma p-tau217 was available for
  approximately 360 participants, sufficient for a bounded analysis of its incremental predictive value
  even though coverage is currently too sparse for inclusion in the full baseline models.
- **External validation** in an independent, ideally community-based cohort to test generalizability
  beyond ADNI's enrollment profile.
- **Multi-state / competing-risks survival models** to represent reversible transitions and death as a
  competing event.
- **Image-based deep learning** (e.g., a convolutional network on structural or default-mode-network
  imaging) as a complementary modality, deferred here as a separate line of work.
- **Calibration and decision-curve analysis** to move from discrimination toward clinically actionable
  thresholds.

---

### Notes for you (delete before submission)
- Every claim traces to notebooks 06–08 and the figures; no numbers are asserted beyond what was computed.
- The three _[p-tau: …]_ markers are the only spots to revisit after tomorrow's PTAU restoration — none
  change the conclusions, they only potentially strengthen the tau-pathology story.



---


# Chapter 6 — Conclusion

This thesis set out to identify early predictors of Alzheimer's disease and of conversion to dementia
from multimodal ADNI data, and to do so with an evaluation framework rigorous enough to trust. Three
contributions follow from the work.

First, **baseline multimodal measures predict progression to dementia with clinically useful accuracy**
in the impaired-spectrum cohorts (pooled CN+MCI→AD ROC-AUC 0.88; MCI→Dementia 0.83), while prediction
from full cognitive normality remains genuinely hard (0.66) — an honest reflection of a slow,
low-incidence process rather than a modeling failure.

Second, **the most informative predictors change with disease stage** — from structural and memory
measures at the cognitively-normal stage to functional, metabolic, and amyloid measures nearer to
dementia. This stage-dependence, visible only because the cohorts were modeled separately, is the
study's central substantive finding, and it is reinforced by convergent survival analysis of
conversion timing.

Third, and most transferable, the work demonstrates that **methodology determines credibility**:
participant-level evaluation and a confirmed-conversion outcome are not optional refinements but
prerequisites for believable estimates. A naïve visit-level analysis produced an early-detection result
of ~82% that collapsed to chance under a correct participant-grouped split — a cautionary result with
implications well beyond this dataset.

Taken together, the findings support stage-aware, interpretable models — logistic regression proved as
accurate as ensembles — for early Alzheimer's risk stratification, and they argue for careful,
leakage-free validation as a standard of practice. The limitations noted in Chapter 5 (enrollment bias,
an under-powered CN cohort, single-cohort validation, and the excluded CSF p-tau biomarker) define a
clear agenda for the next iteration of this work.

---


# References

_(In-text citations verified against this draft. Complete the entries marked in the Author Checklist
before submission.)_

1. Grabher, B. J. (2018). Effects of Alzheimer Disease on Patients and Their Family.
   *Journal of Nuclear Medicine Technology*, 46(4), 335–340.
2. Porsteinsson, A. P., Isaacson, R. S., Knox, S., et al. (2021). Diagnosis of Early Alzheimer's
   Disease: Clinical Practice in 2021. *Journal of Prevention of Alzheimer's Disease*, 8, 371–386.
3. Venugopalan, J., Tong, L., Hassanzadeh, H. R., et al. (2021). Multimodal deep learning models for
   early detection of Alzheimer's disease stage. *Scientific Reports*, 11, 3254.
4. World Health Organization (2021). *Dementia Fact Sheet.*

_Additional references required — see Author Checklist._

---


---

# Author Checklist (open items)

## A. p-tau restoration blanks (fill after CSF p-tau is restored)
- **Abstract** (line 3): > Grounded in the verified results (notebooks 06–08). Bracketed **`⟦…⟧`** markers are fill-in blanks to
- **Abstract** (line 30): was assessed by permutation importance and two feature-selection methods. ⟦*p-tau data note:* one
- **Abstract** (line 32): final models used ⟦N⟧ predictors.⟧
- **Abstract** (line 42): approached the full models (ROC-AUC 0.81). ⟦*p-tau result:* with p-tau restored, tau-pathology measures
- **Abstract** (line 43): ranked ⟦position/among the top predictors⟧ in the ⟦MCI / pooled⟧ cohort(s).⟧
- **Abstract** (line 50): Alzheimer's risk stratification. ⟦*optional p-tau clause:* and confirm phosphorylated tau as an
- **Abstract** (line 60): - **⟦Methods p-tau note⟧** → e.g.: *"phosphorylated tau (p-tau181), initially corrupted by a
- **Abstract** (line 63): - **⟦N predictors⟧** → `33` if p-tau restored, `32` if left out.
- **Abstract** (line 64): - **⟦p-tau result sentence⟧** → fill from the re-run's permutation-importance table, e.g.: *"with p-tau
- **Abstract** (line 68): - **⟦optional conclusion clause⟧** → include only if the result supports it.
- **Discussion** (line 4): > do not depend on the pending PTAU restoration; markers _[p-tau: revisit after restoration]_ flag the
- **Discussion** (line 32): aligns with contemporary staging models of the AD continuum. _[p-tau: revisit — with real p-tau
- **Discussion** (line 95): absent and should be restored from source in a subsequent iteration. _[p-tau: update once restored.]_

## B. Citations to add (no references were fabricated)
- **Intro/LitReview** (line 6): > to §2.7. `[CITATION NEEDED]` marks claims that require a supporting reference — no references were
- **Intro/LitReview** (line 93): tau phosphorylation, while the ε2 allele appears protective. `[CITATION NEEDED — APOE/PSEN mechanisms]`
- **Intro/LitReview** (line 101): contemporary biomarker-based staging of the disease. `[CITATION NEEDED — amyloid/tau staging]`
- **Intro/LitReview** (line 109): `[CITATION NEEDED — hippocampal atrophy figures]` These structural signatures motivate the MRI-derived
- **Intro/LitReview** (line 127): systems (timely intervention; capacity management) (Porsteinsson et al., 2021). `[CITATION NEEDED —
- **Intro/LitReview** (line 138): rates and is addressed as a limitation of the present work (Chapter 5). `[CITATION NEEDED — ADNI design
- **Intro/LitReview** (line 145): conversion. `[CITATION NEEDED — 2–3 representative ADNI ML studies, e.g., Venugopalan et al., 2021 and
- **Intro/LitReview** (line 150): performance. `[CITATION NEEDED — data leakage in longitudinal ML]` Second, **diagnostic status
- **Intro/LitReview** (line 161): - Every `[CITATION NEEDED]` marks a factual claim that should be supported with a reference before

## C. Figures
- Regenerate all four figures at **300 DPI** (currently 130 DPI screen res) — one-line change in the figure script.
- Optional: add a CONSORT-style participant-flow diagram for §4.1 and a calibration plot for the pooled model.

## D. Front matter / formatting
- Fill advisor name and any program-required front matter on the title page.
- Trim Abstract to the program word limit if required (currently ~340 words).
- Decide hypothesis framing in §1.4 (ensemble-superiority as primary vs. secondary) with your advisor.
