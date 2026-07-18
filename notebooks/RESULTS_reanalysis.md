# Leakage-Free Re-Analysis — Complete Results

Master record of the corrected analysis (scripts `10`–`14`). Every value is computed;
nothing is hand-entered. Seed = 42. Reproduce with:
`python3 10_leakage_free_reanalysis.py && python3 11_reanalysis_extended.py && python3 12_survival_riskscore.py && python3 13_subgroup_ablation.py && python3 14_figures.py`

## What changed vs. the original pipeline
1. **Fold-wise imputation.** The observed baseline was reconstructed (each imputed value
   is marked by a `null_flag`; those were set back to `NaN`). An `IterativeImputer`
   (MICE-style, BayesianRidge) is now fit **inside each training fold only** and applied
   to the held-out fold — no cross-fold and no future-visit leakage (only baseline rows
   are modeled). This makes the "leakage-free" claim defensible.
2. **ICV-residualized MRI.** Each brain volume is residualized on intracranial volume
   inside each training fold; raw ICV is dropped as a predictor (32 predictors, not 33).
   Removes the head-size confound (ICV previously ranked 2nd in the CN model).
3. **No-SMOTE primary** (class-weighting), SMOTE-NC kept as sensitivity.
4. **Calibration** reported (Brier + Brier skill score vs. a prevalence-only null).
5. **Paired model comparison** (bootstrap of out-of-fold AUC differences).
6. **Sensitivity analyses**: SMOTE-NC, complete-case, observed-only correlations.

---

## 1. Discrimination — 6 models × 3 cohorts (5-fold CV, out-of-fold, leakage-free)

**ROC-AUC (range across all six models):**
| Cohort | n / events | AUC range | Best (RF/LogReg) |
|---|---|---|---|
| CN → progression | 519 / 74 | 0.58–0.71 | RF 0.71 |
| MCI → Dementia | 819 / 228 | 0.78–0.83 | LogReg 0.83 |
| Pooled → AD | 1,338 / 244 | 0.83–0.88 | LogReg 0.88 |

Per-model AUC:
| Model | CN | MCI | Pooled |
|---|---|---|---|
| Logistic Regression | 0.68 | **0.83** | **0.88** |
| Random Forest | **0.71** | 0.83 | 0.88 |
| XGBoost | 0.69 | 0.83 | 0.88 |
| SVM (RBF) | 0.70 | 0.83 | 0.88 |
| K-Nearest Neighbors | 0.58 | 0.80 | 0.83 |
| Neural Net (MLP) | 0.63 | 0.78 | 0.84 |

**Headline: the MCI (0.83) and pooled (0.88) results are essentially unchanged from the
original global-imputation pipeline — the discrimination was NOT an imputation artifact.**
The CN model is modest (RF 0.71, others lower).

## 2. Detailed performance + calibration (Random Forest, out-of-fold)
| Cohort | AUC (95% CI) | Sens | Spec | PPV | NPV | F1 | Brier | Null Brier | Brier skill |
|---|---|---|---|---|---|---|---|---|---|
| CN → progression | 0.71 (0.64–0.78) | 23% | 93% | 34% | 88% | 0.27 | 0.130 | 0.122 | **−0.06** |
| MCI → Dementia | 0.83 (0.80–0.86) | 70% | 77% | 54% | 87% | 0.61 | 0.155 | 0.201 | +0.23 |
| Pooled → AD | 0.88 (0.86–0.90) | 73% | 86% | 54% | 94% | 0.62 | 0.113 | 0.149 | +0.25 |

**Key calibration finding (confirms reviewer):** the **CN model's Brier skill is negative
(−0.06)** — it is *worse-calibrated than a prevalence-only baseline*. The MCI and pooled
models are well-calibrated (skill +0.23, +0.25). Class-weighted linear models (LogReg/SVM)
produce poorly-calibrated probabilities by construction (Brier ≈ 0.21); the tree models are
the calibration-meaningful ones.

## 3. Stage-dependent predictors (permutation importance, ICV-residualized)
| Rank | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| 1 | WholeBrain | FAQ | FAQ |
| 2 | LDELTOTAL | FDG | AV45 |
| 3 | Hippocampus | mPACCtrailsB | ABETA |
| 4 | mPACCdigit | AV45 | CDRSB |
| 5 | RAVLT.learning | ADAS13 | FDG |
| 6 | CDRSB | AGE | ADAS13 |
| 7 | Entorhinal | RAVLT.immediate | mPACCtrailsB |
| 8 | RAVLT.forgetting | LDELTOTAL | AGE |

Stage-dependence holds and is now **cleaner**: with the ICV head-size artifact removed, the
CN stage is led by genuine **brain-volume (WholeBrain, Hippocampus, Entorhinal, residualized)
and memory** measures; MCI/pooled by **function (FAQ), metabolism (FDG), and amyloid (AV45,
ABETA)**.

## 4. Survival (MCI cohort; n = 819, 228 events, 591 censored)
- **Kaplan–Meier by APOE4 (OBSERVED-only genotype; 1 imputed excluded):** dementia-free at
  5 yr = **80% (non-carriers) vs 55% (carriers)**; log-rank **p = 7.2×10⁻¹²**. (Unchanged;
  APOE4 was essentially fully observed in this cohort.)
- **Cox PH (HR per 1 SD, ICV-residualized):** faster conversion — AV45 1.43, FAQ 1.38,
  ADAS13 1.25 (all p<0.05); slower — FDG 0.73, Hippocampus 0.75, RAVLT-immediate 0.75
  (all p<0.05). Same directions as before.

## 5. Parsimonious risk score (MCI → Dementia)
7 variables, fold-wise imputed, cross-validated **AUC = 0.81**. Points per +1 SD:
ADAS13 +10, FAQ +10, Hippocampus −10, APOE4 +6, CDR-SB +4, MMSE −3, Age −3.

## 6. Sensitivity analyses (robustness)
- **SMOTE-NC vs. no-SMOTE:** near-identical (MCI 0.831/0.831; pooled 0.882/0.886; CN
  0.718/0.716). SMOTE did not drive results; the redundant SMOTE + class-weight combination
  was dropped.
- **Complete-case (zero imputation):** AUCs are *higher*, not lower (CN 0.75, MCI 0.90,
  pooled 0.93) — directly refuting the concern that missingness/imputation manufactured the
  signal. (Complete cases are a biomarker-complete subset with fewer events, so this is a
  robustness check, not the primary estimate.)
- **Observed-only PTAU–TAU correlation = 0.978** (n = 2,103 both-observed), vs 0.986 with
  imputed values — the tau–tau correlation is genuine, not an imputation artifact.
- **Paired model comparison (bootstrap AUC difference):** in MCI and pooled, logistic
  regression was the top or tied-top model; in CN, RF vs LogReg difference 95% CI
  [−0.03, +0.09] includes 0. **No model significantly outperformed logistic regression.**

## 7. Subgroup / fairness (Pooled → AD; overall 0.88)
| Subgroup | n | events | AUC |
|---|---|---|---|
| Male | 737 | 142 | 0.88 |
| Female | 601 | 102 | 0.88 |
| APOE4-negative | 771 | 83 | 0.88 |
| APOE4-positive | 567 | 161 | 0.85 |
| Education < 16 yr | 447 | 92 | 0.84 |
| Education ≥ 16 yr | 891 | 152 | 0.90 |
| Age < 75 yr | 767 | 134 | 0.91 |
| Age ≥ 75 yr | 571 | 110 | 0.84 |
Equitable by sex; lower for less-educated, older, and APOE4-positive participants (unchanged).

## 8. Feature-group ablation (Pooled → AD; full 0.88)
| Group | AUC alone | AUC removed | Δ if removed |
|---|---|---|---|
| Cognitive / functional | 0.854 | 0.850 | −0.032 |
| MRI volumetric | 0.770 | 0.875 | −0.006 |
| PET | 0.788 | 0.883 | +0.002 |
| CSF | 0.761 | 0.884 | +0.003 |
| Demographic / genetic | 0.658 | 0.878 | −0.004 |
Cognitive/functional carries most of the signal; other modalities largely redundant (unchanged).

---

## Bottom line for the thesis
- The central discrimination findings (MCI 0.83, pooled 0.88, stage-dependent predictors,
  APOE4 survival, ~0.81 risk score) **survive a fully leakage-free re-analysis** with
  fold-wise imputation, ICV-residualized MRI, and no SMOTE. The "leakage-free" claim is now
  earned rather than asserted.
- **New, honest limitations to report:** the CN model is under-powered *and* poorly
  calibrated (negative Brier skill); it should not be described as clinically useful.
- Sensitivity analyses (SMOTE, complete-case, observed-only) all support robustness.
