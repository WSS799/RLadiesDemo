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
