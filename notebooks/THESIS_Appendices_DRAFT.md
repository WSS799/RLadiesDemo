# Appendices

> Supplementary material for the thesis. Every value here was extracted directly from the executable
> notebooks (`06`–`09`) and the analytic dataset (`data/pre_modelling_data.csv`); nothing is estimated.
> Random seed = 42 throughout. Place after the References.

---

## Appendix A — Model specifications and hyperparameters

All six classifiers were evaluated under an identical pipeline: within each training fold only, features
were standardized (`StandardScaler`) and the minority class was oversampled with SMOTE
(`random_state = 42`); performance was estimated by stratified 5-fold cross-validation
(`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`). Scaling and oversampling were fit on
training folds and applied to the held-out fold, so no test-fold information entered preprocessing.
The exact estimator settings (all other parameters at their scikit-learn / XGBoost defaults) were:

**Table A1 — Classifier hyperparameters.**

| Model | Library | Key hyperparameters |
|---|---|---|
| Logistic Regression | scikit-learn | L2 penalty; `max_iter = 2000`; `class_weight = 'balanced'` |
| Random Forest | scikit-learn | `n_estimators = 400`; `max_depth = 10`; `class_weight = 'balanced'`; `random_state = 42` |
| XGBoost | xgboost | `n_estimators = 300`; `max_depth = 4`; `learning_rate = 0.05`; `subsample = 0.8`; `eval_metric = 'logloss'`; `random_state = 42` |
| Support Vector Machine | scikit-learn | RBF kernel; `C = 1`; `class_weight = 'balanced'`; scores via `decision_function` |
| K-Nearest Neighbors | scikit-learn | `n_neighbors = 7` |
| Neural Network (MLP) | scikit-learn | `hidden_layer_sizes = (32, 16)`; `max_iter = 400`; `random_state = 42` |

*Preprocessing (all models):* `StandardScaler` → `SMOTE(random_state = 42)` → estimator, chained in an
`imblearn` pipeline so both steps are re-fit inside every training fold.

Survival models (Appendix C) used `statsmodels` `PHReg` (Cox proportional hazards, Efron handling of
ties); cognitive-trajectory models used `statsmodels` `MixedLM` with a random intercept and random slope
for time per participant. Kaplan–Meier estimation and the confirmed-conversion labeling were implemented
directly in NumPy/pandas.

---

## Appendix B — Feature dictionary (33 baseline predictors)

The modeling feature set comprised 33 baseline predictors (baseline diagnosis excluded by design). The
"% imputed" column is the fraction of **baseline** values that were originally missing and filled by the
imputation pipeline (Methods §3.3); a missingness indicator was retained for each. Note that all-visit
missingness is higher for several fluid/PET biomarkers (e.g., CSF measures are collected in a subset of
visits; see §3.12). Ranges are observed baseline min–max.

**Table B1 — Feature dictionary.**

| # | Feature | Modality | Description (direction) | Units | % imputed (baseline) | Baseline range (min–max) |
|---|---|---|---|---|---|---|
| 1 | AGE | Demographic | Age at baseline | years | 0% | 54.4 – 91.4 |
| 2 | PTEDUCAT | Demographic | Years of education | years | 0% | 4 – 20 |
| 3 | PTGENDER | Demographic | Sex (Male = 1, Female = 0) | binary | 0% | 0 – 1 |
| 4 | APOE4 | Genetic | Number of *APOE* ε4 alleles | count (0–2) | 4% | 0 – 2 |
| 5 | ABETA | CSF | Amyloid-β 1-42 (lower = more pathology) | pg/mL | 43% | 200 – 1700 |
| 6 | ADAS13 | Cognitive | ADAS-Cog 13-item (higher = worse) | points | 1% | 0 – 56 |
| 7 | AV45 | PET | Florbetapir amyloid-PET (higher = more plaque) | SUVR | 52% | 0.81 – 2.03 |
| 8 | CDRSB | Clinical | Clinical Dementia Rating–Sum of Boxes (higher = worse) | points | 0% | 0 – 10 |
| 9 | Entorhinal | MRI | Entorhinal cortex volume | mm³ | 31% | 1,143 – 5,896 |
| 10 | FAQ | Functional | Functional Activities Questionnaire (higher = worse) | points | 1% | 0 – 30 |
| 11 | FDG | PET | FDG-PET glucose metabolism (lower = worse) | SUVR | 37% | 0.69 – 1.70 |
| 12 | Fusiform | MRI | Fusiform gyrus volume | mm³ | 31% | 8,991 – 29,950 |
| 13 | Hippocampus | MRI | Hippocampal volume | mm³ | 30% | 2,991 – 11,068 |
| 14 | ICV | MRI | Intracranial volume | mm³ | 19% | 1,100,687 – 2,110,294 |
| 15 | LDELTOTAL | Cognitive (memory) | Logical Memory delayed recall (higher = better) | points | 0% | 0 – 23 |
| 16 | MidTemp | MRI | Middle temporal gyrus volume | mm³ | 31% | 9,375 – 32,189 |
| 17 | MMSE | Cognitive | Mini-Mental State Exam (higher = better) | points (0–30) | 0% | 17 – 30 |
| 18 | MOCA | Cognitive | Montreal Cognitive Assessment (higher = better) | points (0–30) | 40% | 4 – 30 |
| 19 | mPACCdigit | Cognitive (composite) | modified PACC, Digit-Symbol variant (higher = better) | composite | 0% | −23.4 – 6.3 |
| 20 | mPACCtrailsB | Cognitive (composite) | modified PACC, Trails-B variant (higher = better) | composite | 0% | −23.4 – 7.4 |
| 21 | PTAU | CSF | Phosphorylated tau-181 (higher = more pathology; corrected, §3.12) | pg/mL | 43% | 8 – 120 |
| 22 | RAVLT.forgetting | Cognitive (memory) | RAVLT forgetting score | points | 0% | −28 – 15 |
| 23 | RAVLT.immediate | Cognitive (memory) | RAVLT immediate recall, trials 1–5 (higher = better) | points | 0% | 0 – 71 |
| 24 | RAVLT.learning | Cognitive (memory) | RAVLT learning score (higher = better) | points | 0% | −8 – 12 |
| 25 | RAVLT.perc.forgetting | Cognitive (memory) | RAVLT percent forgetting (higher = worse) | % | 1% | −400 – 100 |
| 26 | TAU | CSF | Total tau (higher = more pathology) | pg/mL | 43% | 80 – 1300 |
| 27 | TRABSCOR | Cognitive (executive) | Trail Making Test B completion time (higher = worse) | seconds | 2% | 0 – 300 |
| 28 | Ventricles | MRI | Ventricular volume (higher = more atrophy) | mm³ | 23% | 5,650 – 150,432 |
| 29 | WholeBrain | MRI | Whole-brain volume | mm³ | 21% | 669,364 – 1,486,036 |
| 30 | Married | Demographic | Marital status = married (indicator) | binary | 0% | 0 – 1 |
| 31 | Widowed | Demographic | Marital status = widowed (indicator) | binary | 0% | 0 – 1 |
| 32 | Divorced | Demographic | Marital status = divorced (indicator) | binary | 0% | 0 – 1 |
| 33 | Never_married | Demographic | Marital status = never married (indicator) | binary | 0% | 0 – 1 |

*RAVLT percent-forgetting has an extreme negative floor (−400) arising when the delayed-recall
denominator is very small; the value was retained as recorded and standardized with the other features.*

---

## Appendix C — Supplementary results

### C1 — Full Cox proportional-hazards model (MCI → Dementia)

Hazard ratios per one standard-deviation increase in each standardized covariate (Efron ties); 819
participants, 228 confirmed conversions, 591 right-censored. HR > 1 indicates *faster* conversion, HR < 1
*slower*. This is the complete 14-covariate model summarized in Section 4.7.

**Table C1 — Cox proportional-hazards results.**

| Covariate | Hazard ratio (per 1 SD) | p-value |
|---|---|---|
| FAQ | 1.409 | < 0.001 |
| ADAS13 | 1.340 | 0.005 |
| AV45 | 1.291 | 0.016 |
| APOE4 | 1.161 | 0.051 |
| CDRSB | 1.146 | 0.069 |
| PTEDUCAT | 1.089 | 0.213 |
| MOCA | 0.952 | 0.649 |
| AGE | 0.925 | 0.309 |
| MMSE | 0.917 | 0.293 |
| ABETA | 0.820 | 0.120 |
| Hippocampus | 0.794 | 0.016 |
| LDELTOTAL | 0.786 | 0.011 |
| RAVLT.immediate | 0.761 | 0.020 |
| FDG | 0.717 | < 0.001 |

Five covariates reached significance at α = 0.05: higher FAQ, ADAS13, and AV45 predicted faster
conversion; higher hippocampal volume, delayed memory (LDELTOTAL), immediate memory (RAVLT.immediate),
and FDG metabolism predicted slower conversion (FDG and FAQ most strongly).

### C2 — Full permutation-importance rankings (top 10 by cohort)

Mean decrease in ROC-AUC when each feature is permuted, averaged across held-out folds (Random Forest,
`n_repeats = 8`). Section 4.6 (Table 4.4) shows the top 8; the full top 10 is given here.

**Table C2 — Top-10 predictors by cohort (permutation-importance rank).**

| Rank | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| 1 | Hippocampus | FAQ | FAQ |
| 2 | ICV | FDG | AV45 |
| 3 | MOCA | LDELTOTAL | ABETA |
| 4 | AGE | mPACCtrailsB | LDELTOTAL |
| 5 | LDELTOTAL | ADAS13 | RAVLT.immediate |
| 6 | MMSE | AGE | FDG |
| 7 | FDG | ABETA | CDRSB |
| 8 | CDRSB | RAVLT.immediate | mPACCtrailsB |
| 9 | RAVLT.forgetting | CDRSB | PTAU |
| 10 | ADAS13 | AV45 | Hippocampus |

Corrected CSF p-tau (PTAU) appears at rank 9 in the pooled model, confirming its mid-tier standing
(Section 4.6).

### C3 — Feature-selection convergence (pooled cohort)

Two additional selection methods were applied to the pooled cohort on standardized features.

**Table C3 — Feature selection, pooled → AD.**

| Method | Selected features (10) |
|---|---|
| Univariate (SelectKBest, ANOVA F-test) | mPACCtrailsB, FAQ, ADAS13, mPACCdigit, LDELTOTAL, CDRSB, AV45, MOCA, RAVLT.immediate, FDG |
| Recursive Feature Elimination (logistic) | AGE, ABETA, FAQ, Hippocampus, ICV, mPACCtrailsB, PTAU, TAU, WholeBrain, Never_married |
| **Convergent (both methods)** | **FAQ, mPACCtrailsB** |

Combined with permutation importance, **FAQ** was selected by all three approaches. That RFE retained
both PTAU and TAU indicates each tau species carries some non-redundant signal once PTAU is correctly
scaled; the RFE-selected "Never_married" indicator is almost certainly spurious and illustrates the value
of requiring convergence across methods.

### C4 — Parsimonious clinical risk score (MCI → Dementia)

Logistic-regression score from seven routinely available inputs; cross-validated ROC-AUC = 0.81 ± 0.03
(Section 4.8). Integer points are standardized coefficients scaled to the largest absolute coefficient
(coefficient ÷ max|coefficient| × 10); positive points increase predicted dementia risk.

**Table C4 — Risk-score points (per +1 SD).**

| Variable | Points |
|---|---|
| ADAS13 | +10 |
| FAQ | +9 |
| Hippocampus | −8 |
| APOE4 | +6 |
| CDRSB | +4 |
| MMSE | −2 |
| AGE | −2 |

Higher ADAS13 and FAQ contribute most to predicted risk; larger hippocampal volume is the strongest
protective term — consistent with the permutation-importance and Cox results.

---

### Notes for you (delete before submission)
- Every value here traces to notebooks `06`–`09` (seed 42) and `pre_modelling_data.csv`. Table A1 matches
  the `models()` definitions in notebook `08`; Tables C1–C4 are the printed notebook outputs.
- Consider adding these to the front-matter **List of Tables** as A1, B1, C1–C4 if your program wants
  appendix tables enumerated (some do not).
- Appendix B "% imputed (baseline)" is deliberately baseline-level; if a reader asks about the ~76%
  figure cited for PTAU in §3.12, that is all-visit missingness, not baseline.
