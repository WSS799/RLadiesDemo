# PTAU Correction — Data-Integrity Fix & Sensitivity Analysis

Companion note documenting the correction of the p-tau181 (PTAU) field and its (negligible) effect
on results. Applied to `data/pre_modelling_data.csv`; notebooks 07 and 08 now **include** PTAU.

## The bug
In earlier data processing, PTAU was corrupted two ways:
1. **Wrong detection limits.** Total-tau limits (`<80 → 80`, `>1300 → 1300`) were applied to p-tau181
   instead of its own limits (`<8 → 8`, `>120 → 120`). This inflated the PTAU ceiling ~10×.
2. **Cross-scale imputation.** The ~76% missing PTAU values were imputed on the total-tau scale, so the
   column became a near-perfect duplicate of TAU.

**Evidence:** in the pre-fix data, `PTAU` had median = 266.8, max = 1300, and `corr(PTAU, TAU) = 0.9995`
— i.e. PTAU carried no information distinct from TAU. The correct p-tau181 measuring range is 8–120 pg/mL
(ADNI documented observed range 8–108.5; source: `UPENNBIOMK_ROCHE_ELECSYS`, ADNIMERGE2 R package v0.1.1).

## The fix
- Reconstructed the real observed PTAU values from the source ADNI export with the **correct** detection
  limits (`<8 → 8`, `>120 → 120`), matched by `PTID` + `Month.bl`.
- Re-imputed the missing values with model-based (Random Forest) imputation restricted to the physiological
  range [8, 120], using correlated predictors (TAU, ABETA, AV45, FDG, cognitive measures, age, APOE4).
- Result: `PTAU` median = 24.6, max = 120.0, min = 8.0, `corr(PTAU, TAU) = 0.986` — on the correct scale,
  biologically plausible, and no longer a duplicate. Observed values preserved exactly; only gaps imputed.

## Sensitivity analysis — effect on results (patient-level, 5-fold CV, confirmed labels)

| Cohort | RF-AUC (PTAU excluded, original) | RF-AUC (PTAU included, fixed) | LR-AUC before → after |
|---|---|---|---|
| CN → progression | 0.661 ± 0.025 | 0.651 ± 0.033 | 0.685 → 0.691 |
| MCI → Dementia | 0.830 ± 0.031 | 0.829 ± 0.028 | 0.824 → 0.823 |
| Pooled CN+MCI → AD | 0.879 ± 0.031 | 0.880 ± 0.033 | 0.873 → 0.874 |

**Conclusion:** correcting PTAU does **not** change the conversion-prediction results (all AUCs within
run-to-run noise). Once corrected, PTAU is a legitimate **mid-tier predictor** — RF importance rank
≈ 11–12 of 33 features (~3.4–3.6%) in the MCI→Dementia and Pooled models — rather than a corrupted column
that had to be dropped.

**Why this matters for the thesis:** the correction restores a clinically meaningful CSF biomarker
(p-tau181) to the multimodal feature set without inflating performance, and the sensitivity check
demonstrates the main findings are robust to the fix. This is reported as a methodological strength.

_All numbers reproduced from the committed notebooks on the corrected `data/pre_modelling_data.csv`;
random seed = 42._
