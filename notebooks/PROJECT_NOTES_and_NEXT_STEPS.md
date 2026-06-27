# Thesis Project — Session Notes & Next Steps

_Branch: `claude/code-explanation-xi7aov` · all work committed & pushed._

---

## PART 1 — What we did this session (in order)

1. **Reviewed all original notebooks** (01 baseline prep → 02 EDA → 03 processing → 04 ML modelling → 05 image CNN). Mapped the full pipeline.
2. **Compared the thesis draft to the code.** Found the preprocessing/EDA matched, but the modelling claims initially looked unsupported.
3. **Located `04_ML_Modelling_1`** — confirmed the thesis's 89% Random Forest, SMOTE, SVM/KNN/ANN results ARE real and reproducible. (Corrected my earlier assumption that they were fabricated.)
4. **Found the critical flaw: data leakage.** `04` split the data at the *visit* level, so the same patient appeared in train AND test.
   - 3-class diagnosis model: 89% → held up at ~88% under patient-grouped split (but is partly *circular* — uses CDRSB/FAQ, which define the diagnosis).
   - Early-detection model: ~82% → collapsed to ~34% (chance) under a fair patient-level split. The 82% was leakage.
5. **Rebuilt conversion prediction correctly** (notebook 06): one row per patient = baseline visit → predict future outcome. Leakage impossible by design.
6. **Investigated diagnostic reversion** (your catch): 123 patients (5.8%) improve at least once; 28 had CN→up→CN; clinically-impossible Dementia→lower cases exist = label noise.
7. **Agreed on confirmed-conversion labels** (Layer 1): a converter must show the worse stage on **≥2 consecutive visits**. Dropped 28 dementia-reversion patients.
8. **Built the sensitivity table** (Layer 3 receipts) showing converter counts under last-visit / ever / confirmed / 24mo / 36mo definitions.
9. **Diagnosed the cohort structure:** ADNI over-recruits prevalent MCI (enrollment bias) → MCI→Dementia is common, CN→MCI is rare/slow (median ~4 yrs). CN people don't skip to dementia.
10. **Built stratified + pooled models** (notebook 07): CN→progression, MCI→Dementia, Pooled→AD; excluded baseline DX from the pooled model so real biological predictors surface.
11. **Built survival analysis** (notebook 07): Kaplan-Meier + Cox for MCI→Dementia timing.
12. **Completed all remaining thesis-named methods** (notebook 08): 6-classifier comparison, feature selection (SelectKBest + RFE), clinical risk score, linear mixed-effects trajectories.

---

## PART 2 — What exists now (deliverables, all committed)

| File | What it contains |
|---|---|
| `notebooks/06_Early_Conversion_Prediction.ipynb` | First leakage-free conversion model (intro) |
| `notebooks/07_Stratified_AD_Predictors.ipynb` | 3 cohorts + predictors + **survival (KM/Cox)** |
| `notebooks/08_Model_Comparison_FeatSel_RiskScore.ipynb` | **6-model comparison, feature selection, risk score, mixed-effects** |
| `notebooks/RESULTS_early_conversion.md` | Summary for 06 |
| `notebooks/RESULTS_stratified_predictors.md` | Summary for 07 |
| `data/pre_modelling_data.csv` | Data so notebooks run as-is |

---

## PART 3 — Key results (the real, defensible numbers)

**Classification — ROC-AUC, 5-fold CV, patient-level, confirmed labels**
| Cohort | n | Events | Best AUC |
|---|---|---|---|
| CN → progression | 519 | 74 (14%) | ~0.70 (XGBoost) — under-powered |
| MCI → Dementia | 819 | 228 (28%) | ~0.83 (RF/XGB) |
| Pooled CN+MCI → AD | 1,338 | 244 (18%) | ~0.88 (RF) |

- **RF ≈ XGBoost ≈ Logistic** (ensembles do NOT clearly beat linear → signal largely linear).
- **Stage-dependent predictors (key finding):** CN stage = structure/memory (hippocampus, ICV, MOCA, LDELTOTAL); MCI stage = function/metabolism/amyloid (FAQ, FDG, AV45, ABETA).
- **Most defensible predictors (all methods agree):** FAQ, mPACCtrailsB, ADAS13, LDELTOTAL.

**Survival (MCI→Dementia):** APOE4+ converts faster (55% vs 80% dementia-free at 5 yrs). Cox: FAQ/ADAS13/AV45 speed conversion; hippocampus/memory/FDG slow it.

**Clinical risk score (7 vars):** AUC ≈ 0.81.

**Mixed-effects trajectories:** Dementia group declines fastest (ADAS13 ≈ +2.2 pts/yr).

---

## PART 4 — Decisions locked in
- ✅ Patient-level evaluation (no visit-level leakage).
- ✅ Confirmed conversion = worse stage on ≥2 consecutive visits.
- ✅ Drop clinically-impossible Dementia→lower cases (28).
- ✅ Stratify (CN, MCI) then pool; exclude baseline DX from pooled predictor model.
- ✅ Report ensembles ≈ logistic honestly (don't over-claim RF superiority).
- ✅ CNN deferred (future: default-mode-network project).

---

## PART 5 — NEXT STEPS (prioritized)

### ▶ START HERE next session:
**Step 1 — Generate figures** for the paper (none exist yet):
   - ROC curves (per cohort, all models)
   - Kaplan-Meier survival curves (by APOE4)
   - Predictor importance bar charts (per cohort)
   - Forest plot of Cox hazard ratios

**Step 2 — Rewrite Methods + Results** of the thesis to match the real numbers:
   - Replace the visit-level 89%/82% framing with patient-level, confirmed-label results.
   - Add the leakage discovery as a methodological strength.
   - State ensembles ≈ logistic; report the stage-dependent predictor finding.
   - Add the participant-flow / exclusion counts and the sensitivity table.

### Then:
**Step 3 — Reframe the thesis statement** around what the data actually shows (early predictors of AD + conversion, stratified, leakage-free).

**Step 4 — Update Limitations:** enrollment bias (prevalent MCI), CN cohort under-powered, diagnostic reversion/label noise, single-cohort (no external validation).

**Step 5 — Decide on cuts:** the thesis still *mentions* nothing now unbuilt EXCEPT the CNN — confirm CNN stays as "future work."

### Optional / stretch:
- Multi-state Markov model (rigorous handling of reversible CN↔MCI) — future work.
- External validation on a non-ADNI cohort.

---

## PART 6 — One-line orientation for "where do I begin?"
> **Open `07` and `08`, skim the Summary cells, then ask Claude to generate the figures (Step 1). After figures, do the Results rewrite (Step 2).** Everything analytical is done and committed; the remaining work is figures + writing.
