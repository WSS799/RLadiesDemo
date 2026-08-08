# Chapter 3 — Methods (Rewrite Draft)

> Draft grounded in the committed, reproducible notebooks (01–03 preprocessing; 06–08 analysis) and
> verified line-by-line against the executed code. Every hyperparameter, cohort size, and definition
> below was confirmed against the source. Random seed = 42 throughout.
>
> **Data-integrity resolution:** the `PTAU` (CSF phosphorylated tau-181) variable was found to be
> corrupted — total-tau detection limits (`<80/>1300`) and cross-scale imputation had been applied to it,
> making it a near-duplicate of `TAU` (Pearson r ≈ 1.00) on the wrong (~10×) scale. It was **corrected**
> by reconstructing observed values from the ADNI source on p-tau181's true 8–120 pg/mL scale
> (`UPENNBIOMK_ROCHE_ELECSYS`, ADNIMERGE2) and re-imputing gaps within range; final models use the
> corrected **33-feature** set. A sensitivity analysis (Section 3.12) confirms the correction leaves the
> conversion AUCs unchanged; corrected PTAU enters as a mid-tier predictor. See Section 3.12.

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
">1300"→1300; PTAU: correctly "<8"→8, ">120"→120 after the correction described in Section 3.12). *(An
earlier version of the pipeline had applied total-tau limits to PTAU and imputed it on the wrong scale;
this was corrected before the analyses reported here — see Section 3.12.)*

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
36 months; Results Table 4.2).

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

Thirty-three baseline predictors were used: AGE, PTEDUCAT, PTGENDER, APOE4, ABETA, ADAS13, AV45, CDRSB,
Entorhinal, FAQ, FDG, Fusiform, Hippocampus, ICV, LDELTOTAL, MidTemp, MMSE, MOCA, mPACCdigit,
mPACCtrailsB, PTAU, RAVLT (forgetting, immediate, learning, percent-forgetting), TAU, TRABSCOR,
Ventricles, WholeBrain, and the four marital-status indicators (PTAU included after the correction in
Section 3.12). Identifiers, timing variables, current and future diagnosis labels, and the 27
missingness indicators were excluded from the predictor set.

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

**Evaluation metrics.** Discrimination was summarized by the **area under the ROC curve (ROC-AUC)** —
the probability that a randomly chosen converter receives a higher predicted risk than a randomly chosen
non-converter (0.5 = chance, 1.0 = perfect ranking). At a 0.5 probability threshold, four count-based
measures were derived from the confusion matrix: **sensitivity** (recall; true positives ÷ all true
converters), **specificity** (true negatives ÷ all true non-converters), **positive predictive value**
(PPV; true positives ÷ all predicted converters), and **negative predictive value** (NPV; true negatives
÷ all predicted non-converters). The **F1 score** (harmonic mean of PPV and sensitivity) summarized the
balance between them, and **balanced accuracy** (mean of sensitivity and specificity) provided an
imbalance-robust accuracy. Probability **calibration** — whether predicted risks match observed
frequencies — was quantified with the **Brier score**, the mean squared difference between predicted
probability and outcome (lower is better). ROC-AUC was the primary metric because it is
threshold-independent and insensitive to class prevalence, both important given the low conversion base
rates. For the survival models, the **concordance index (C-index)** — the survival analogue of ROC-AUC —
and **hazard ratios** (the multiplicative change in instantaneous conversion risk per one-standard-
deviation increase in a covariate; >1 faster, <1 slower) were reported.

**Interval estimation.** Because held-out event counts were modest, 95% confidence intervals for ROC-AUC
were obtained by **bootstrap resampling** of the out-of-fold predictions (1,000 resamples with
replacement; 2.5th–97.5th percentiles). Cross-validation point estimates are reported as the mean across
the five folds, with the standard deviation as a dispersion measure.

**Subgroup (fairness) analysis.** To probe generalizability, pooled-model out-of-fold AUC was recomputed
within strata defined by sex, APOE4 carriage (0 vs ≥ 1 allele), education (< 16 vs ≥ 16 years), and age
(< 75 vs ≥ 75 years). Strata with fewer than 30 participants or a single outcome class were not
evaluated. Comparable AUCs across strata indicate equitable performance; systematic gaps identify
subgroups for which the model is less reliable.

**Feature-group ablation.** To attribute predictive value to data modalities, the pooled model was refit
(i) using each predefined feature group in isolation and (ii) with each group removed, comparing the
resulting cross-validated AUC to the full-model AUC. Groups were cognitive/functional, MRI-volumetric,
PET, CSF, and demographic/genetic. A large decrease when a group is removed indicates non-redundant
signal; a negligible decrease indicates the group's information is largely captured by the remaining
features.

**Rationale for the modeling protocol.** Three design choices warrant emphasis. First, all resampling
was performed at the **participant level**, so that no individual appeared in both training and test
folds; this prevents the optimistic bias documented in Section 4.3. Second, **standardization and SMOTE
were fit only on training folds** and then applied to the held-out fold, so that no information from the
test data influenced preprocessing (a common and subtle source of leakage). Third, class imbalance was
addressed with SMOTE and balanced class weights **rather than by discarding majority cases**, preserving
all available data. Together these choices prioritize unbiased, reproducible estimates over headline
accuracy.

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

Analyses were conducted in Python 3.11.15 (CPython) on a 64-bit Linux platform. The complete software
stack, with the exact versions used for the final run, was: NumPy 2.4.6, pandas 3.0.3,
scikit-learn 1.9.0 (classification models, cross-validation, permutation importance, feature
selection, and metrics), imbalanced-learn 0.14.2 (SMOTE), XGBoost 3.2.0 (gradient-boosted trees),
statsmodels 0.14.6 (Cox proportional-hazards regression and linear mixed-effects models),
SciPy 1.17.1 (bootstrap resampling and statistical tests), and Matplotlib 3.11.0 (figures). Kaplan–Meier
estimation and the confirmed-conversion labeling were implemented directly in NumPy/pandas rather than
through an external survival package, so that the exact censoring and labeling logic remains inspectable
in the notebook source.

A fixed random seed (42) was applied to every stochastic component — the participant-level
cross-validation splitter, SMOTE, model initialization (Random Forest, XGBoost, and the multilayer
perceptron), and permutation importance — so that all reported numbers are exactly reproducible from the
notebooks. All analyses are provided as executable notebooks (`06_Early_Conversion_Prediction`,
`07_Stratified_AD_Predictors`, `08_Model_Comparison_FeatSel_RiskScore`, and
`09_Performance_Fairness_Ablation`) with embedded outputs and matching results summaries, run against a
single, version-controlled analytic dataset (`data/pre_modelling_data.csv`).

---

## 3.12 Data-integrity correction: CSF p-tau (PTAU)
The CSF phosphorylated-tau (PTAU, p-tau181) field had been corrupted in earlier processing in two ways:
total-tau detection limits (`<80/>1300` rather than p-tau181's `<8/>120`) were applied, and its ~76%
missing values were imputed on the total-tau scale — leaving PTAU a near-duplicate of TAU (r ≈ 1.00,
median ≈ 267, max 1300, i.e. ~10× too high). It was **corrected** by reconstructing the observed
p-tau181 values from the ADNI source (`UPENNBIOMK_ROCHE_ELECSYS`, ADNIMERGE2 R package) on the true
8–120 pg/mL scale, matched by PTID and visit month, and re-imputing the remaining gaps with model-based
(Random Forest) imputation restricted to the physiological range. The corrected PTAU has median 24.6,
max 120, and r(PTAU, TAU) = 0.986 — biologically plausible and no longer a duplicate. A sensitivity
analysis (5-fold CV, patient-level) confirmed the correction leaves the conversion AUCs essentially
unchanged (MCI→Dementia RF 0.830→0.829; pooled 0.879→0.880), with corrected PTAU entering as a mid-tier
predictor (RF importance rank ≈ 11–12 of 33). The correction is reported as a methodological strength:
it restores a clinically meaningful biomarker without inflating performance and demonstrates robustness
of the main findings.
