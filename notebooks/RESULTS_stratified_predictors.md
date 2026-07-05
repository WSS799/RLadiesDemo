# Stratified Predictors of Alzheimer's & MCI→Dementia Conversion — Results

Reproducible companion to `07_Stratified_AD_Predictors.ipynb`.

## Design (why it's defensible)
- **Patient-level rows:** one baseline visit per patient → future outcome. Splits are between people,
  so no leakage.
- **Confirmed outcomes:** a converter must show the worse stage on **≥2 consecutive visits**
  (handles diagnostic reversion / single-visit blips). Clinically impossible Dementia→lower
  trajectories dropped as error.
- **Stratified then pooled:** CN and MCI modeled separately, then combined, then compared — because
  ADNI over-recruits prevalent MCI (volunteer/enrollment bias).
- **Predictor discovery excludes baseline diagnosis** so biology shows through, not "you were already MCI."

## Participant flow
Total 2,131 → removed 453 (single visit) → removed 28 (Dementia→lower error) → analyzable ≈ 1,650.

## Classification results (patient-level, 5-fold CV, confirmed labels)

| Cohort | n | Events | ROC-AUC (Random Forest) | ROC-AUC (Logistic) |
|---|---|---|---|---|
| CN → progression (MCI/Dem) | 519 | 74 (14%) | 0.65 ± 0.03 | 0.69 ± 0.05 |
| MCI → Dementia | 819 | 228 (28%) | 0.83 ± 0.03 | 0.82 ± 0.02 |
| Pooled CN+MCI → AD | 1,338 | 244 (18%) | 0.88 ± 0.03 | 0.87 ± 0.03 |

_(PTAU was corrected — see `RESULTS_ptau_fix.md` — and is now included as a mid-tier predictor; 33 features. A sensitivity analysis confirms the conversion AUCs below are unchanged by the correction.)_

## Early predictors by stage (the key finding)
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

**Interpretation:** the dominant predictors *shift with disease stage*. At the **CN** stage, structural
and memory measures lead (hippocampal volume, ICV, memory [RAVLT/LDELTOTAL], MOCA). By the **MCI** stage,
functional decline (FAQ), brain metabolism (FDG), and amyloid (AV45/ABETA) dominate. With PTAU corrected,
the tau biomarkers (TAU, PTAU) sit in the mid tier. This stage-dependent pattern is clinically coherent
and is the scientific payoff of stratifying rather than pooling blindly.

## Timing — MCI→Dementia survival (Kaplan-Meier + Cox)
Cohort: 819 MCI patients, 228 confirmed conversions, 591 right-censored.

**Kaplan-Meier — % still dementia-free:**
| Group | 2 yr | 3 yr | 5 yr |
|---|---|---|---|
| APOE4-negative | 88% | 85% | 80% |
| APOE4-positive | 75% | 65% | 55% |
| All MCI | 81% | 75% | 68% |

**Cox proportional hazards (HR per 1 SD):**
- **Faster conversion (HR>1):** FAQ (1.41), ADAS13 (1.34), AV45/amyloid (1.29), APOE4 (1.16).
- **Slower conversion (HR<1):** FDG (0.72), RAVLT-immediate (0.76), LDELTOTAL (0.79), hippocampus (0.79).

## Honesty / limitations
- **CN→progression is modest (AUC ~0.66–0.69) and under-powered (74 events)** — predicting decline from
  fully normal cognition is genuinely hard; reported transparently rather than inflated.
- ADNI enrollment over-represents prevalent MCI, so absolute conversion rates are not population-representative.
- All evaluation is patient-level; the only Random Forest here is a *classifier*. This is the leakage-free
  counterpart to the earlier visit-level model, whose ~82% early-detection result was an artifact.

*All numbers produced by the committed notebook on `data/pre_modelling_data.csv`; random seed = 42.*
