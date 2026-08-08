# Early Prediction of Alzheimer's Conversion — Results Summary

Reproducible companion to `06_Early_Conversion_Prediction.ipynb`.

## What this addresses
The thesis goal is to use machine learning to identify **early predictors** of Alzheimer's
diagnosis and of conversion to dementia. The earlier modelling (`04_ML_Modelling_1`) evaluated the
early-detection task with a **visit-level** train/test split. Because each patient contributes
several visits with near-identical features and the same eventual-outcome label, that split leaks
the same patient into both train and test, inflating accuracy (~82%). Under a fair, patient-grouped
split the same model collapses to ~34% balanced accuracy (chance).

This analysis rebuilds the task **leakage-free**: one row per patient (their baseline visit),
predicting their future outcome, with every cross-validation fold splitting *patients*, never visits.

## Method
- **Unit of analysis:** one row per patient = earliest (baseline) visit. Patients with no follow-up
  are excluded (their outcome cannot be observed).
- **Target:** `Last_Visit_DX_Flag` (eventual diagnosis).
- **Validation:** 5-fold stratified cross-validation across patients.
- **Imbalance:** SMOTE applied **inside training folds only**; `class_weight='balanced'`.
- **Models:** Logistic Regression and Random Forest.
- **Importance:** permutation importance (drop in ROC-AUC) on held-out folds.

## Results (5-fold CV)

| Conversion task | Patients | Converters | ROC-AUC | Balanced acc | Sensitivity | Specificity |
|---|---|---|---|---|---|---|
| **MCI → Dementia** | 838 | 39% | **0.86** | 77% | 73–77% | 78–80% |
| **CN → MCI/Dementia** | 523 | 21% | **0.73** | 66% | 60% | 72% |

## Early predictors identified
- **MCI → Dementia:** FAQ (daily function), AV45 (amyloid PET), FDG (brain metabolism), CDRSB,
  ABETA, RAVLT-immediate and LDELTOTAL (memory), hippocampal volume.
- **CN → MCI/Dementia:** hippocampal volume, LDELTOTAL (delayed recall), MOCA, ventricular and
  intracranial volume, then FAQ / CDRSB.

## Interpretation
- The **MCI → Dementia** model is a genuine, defensible prognosis result (ROC-AUC 0.86) and directly
  supports the thesis: baseline functional, amyloid/metabolic, and memory measures predict who
  progresses to dementia.
- The **CN → MCI/Dementia** task is meaningfully harder (ROC-AUC 0.73), as expected when starting
  from fully normal cognition; structural and memory measures carry most of the early signal.
- These numbers are trustworthy because no individual appears in both train and test. They are the
  leakage-free counterpart to the visit-level results in `04_ML_Modelling_1`.

*Numbers are produced by the committed notebook on `data/pre_modelling_data.csv`; random seed = 42.*
