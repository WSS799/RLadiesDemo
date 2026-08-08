# Figure Layout & Plan — Results Figures

Two deliverables:
1. **Shareable gallery** (for advisor/committee review): `figures_gallery.html` — a self-contained page
   with all four figures, captions, and an at-a-glance stat strip. Published as an Artifact.
2. **In-thesis placement plan** (this document): where each figure goes and its caption.

Source PNGs live in `notebooks/figures/` and are reproducible from notebooks 07–08 (seed 42).

---

## Figure inventory & placement

**Exploratory / descriptive figures** (place early — Results §4.1 or an EDA subsection):
| Fig | File | Shows | Goes in |
|---|---|---|---|
| EDA-1 | `eda1_cohort_overview.png` | Baseline diagnosis, age, education, sex, APOE4, visits/patient | §4.1 |
| EDA-2 | `eda2_feature_distributions.png` | Distributions of 16 key cognitive/MRI/biomarker features | §4.1 / EDA |
| EDA-3 | `eda3_by_diagnosis.png` | Key features by baseline diagnosis (CN/MCI/Dementia) box plots | §4.1 / EDA |
| EDA-4 | `eda4_correlation_matrix.png` | Correlation matrix of 26 baseline features | §4.1 / EDA |
| EDA-5 | `eda5_predictors_by_outcome.png` | Baseline feature distributions: Converter vs Stable | §4.3 / EDA |

**Results figures** (renumbered to match citation order in Chapter 4):
| Fig | File | Goes in | Referenced at |
|---|---|---|---|
| 1 | `fig1_roc_cohorts.png` | Results §4.5 (performance) | after Table 4.3 |
| 2 | `fig2_predictors.png` | Results §4.6 (predictors) | after Table 4.4 |
| 3 | `fig3_km_apoe4.png` | Results §4.7 (survival) | after Table 4.5 |
| 4 | `fig4_cox_forest.png` | Results §4.7 (survival) | after the Cox paragraph |
| 5 | `fig5_subgroup_fairness.png` | Results §4.11 (fairness) | after Table 4.7 |

*(Figures are now numbered in first-citation order: Fig 1 → 2 → 3 → 4 → 5. Files were renamed to match,
so `fig2_*` is predictors, `fig3_*` is Kaplan–Meier, `fig4_*` is Cox. The standalone
`figures_gallery.html` artifact still uses the earlier ordering and can be regenerated if needed.)*

---

## Final captions (thesis-ready)

**Figure 1. Receiver operating characteristic curves by cohort.** Random Forest, participant-level
5-fold cross-validation, pooled out-of-fold predictions. Cross-validated ROC-AUC: pooled CN+MCI→AD 0.88,
MCI→Dementia 0.83, CN→progression 0.66 (0.65–0.69 across models). No participant contributes to both
training and test partitions.

**Figure 2. Stage-dependent early predictors.** Permutation importance (mean decrease in ROC-AUC on
held-out folds) for the three cohorts. Structural and memory measures dominate at the CN stage;
functional, metabolic, and amyloid measures dominate at the MCI stage.

**Figure 3. Kaplan–Meier estimates of remaining dementia-free, MCI cohort, by APOE4 status.**
819 participants; 228 confirmed conversions; 591 right-censored. At five years, 55% of APOE4-positive
versus 80% of APOE4-negative participants remained dementia-free.

**Figure 4. Cox proportional-hazards model of time to MCI→Dementia conversion.** Hazard ratios per one
standard-deviation increase (points) with 95% confidence intervals (lines); dashed line at HR = 1.
Higher FAQ, ADAS13, and AV45 predict faster conversion; higher hippocampal volume, memory, and FDG
predict slower conversion.

---

## Formatting notes for submission
- Export at ≥300 DPI for print (current PNGs are 130 DPI screen resolution — **regenerate at
  `dpi=300` before final submission**; one-line change in the figure script).
- Consistent colorblind-safe palette already applied across all four.
- If the program requires greyscale-safe figures, Fig 1/2 rely on line separation (fine); Fig 4 uses
  color only for cohort separation (already in separate panels, so safe).

## Still to add (optional, if time permits)
- **Calibration plot** for the pooled model (predicted vs observed risk) — strengthens clinical claims.
- **Participant-flow (CONSORT-style) diagram** for §4.1 — boxes for 2,131 → exclusions → analytic cohorts.
