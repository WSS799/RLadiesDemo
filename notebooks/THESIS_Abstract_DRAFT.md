# Abstract (Draft)

> Grounded in the verified results (notebooks 06–08). The p-tau fill-in blanks have been **completed**
> following the CSF p-tau181 correction (Methods §3.9); the core findings are unchanged.

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
was assessed by permutation importance and two feature-selection methods. One biomarker, CSF
phosphorylated tau-181, had been corrupted by a preprocessing error and was corrected against the ADNI
source before analysis; final models used 33 predictors.

**Results.** Progression to dementia was predicted with good discrimination in the impaired-spectrum
cohorts (pooled CN+MCI→AD ROC-AUC 0.88; MCI→Dementia 0.83) but poorly from full cognitive normality
(CN→progression 0.65–0.69), reflecting a slow, low-event process. Random forest, XGBoost, and logistic
regression performed equivalently, indicating a largely linear predictive signal. The most informative
predictors shifted with disease stage — from structural and memory measures (hippocampal volume,
intracranial volume, delayed memory) at the CN stage to functional (FAQ), metabolic (FDG), and amyloid
(AV45, ABETA) measures nearer dementia. APOE4 carriers converted markedly faster (55% remained
dementia-free at five years versus 80% of non-carriers). A parsimonious seven-variable risk score
approached the full models (ROC-AUC 0.81). The corrected CSF p-tau181 measure entered as a mid-tier
predictor (importance rank ≈ 11–12 of 33) and left the conversion results unchanged.

**Conclusions.** Baseline multimodal measures predict AD progression with clinically useful accuracy,
and the dominant predictors change systematically across the disease continuum. The study also
demonstrates that participant-level evaluation and confirmed-conversion labeling are essential for
credible estimates: naïve visit-level analysis inflated an early-detection result from chance to ~82%.
These findings support stage-aware, interpretable models — and careful methodology — for early
Alzheimer's risk stratification, and they show that correctly measured CSF phosphorylated tau
contributes modest, non-redundant signal beyond total tau.

**Keywords:** Alzheimer's disease; mild cognitive impairment; ADNI; machine learning; conversion
prediction; survival analysis; data leakage; biomarkers.

---

### Note

p-tau blanks completed following the CSF p-tau181 correction (Methods §3.9): 33 predictors; corrected
PTAU is a mid-tier predictor (rank ≈ 11–12/33) and does not change the conversion results.

*Word count (excluding keywords): ~330; trim to your program's limit (commonly 250–300) if needed — the
Background and Methods paragraphs compress most easily.*
