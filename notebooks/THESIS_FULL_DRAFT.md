# Predicting Alzheimer's Disease Progression with Machine Learning
### Early, Leakage-Free Prediction of Diagnosis and Conversion from Multimodal ADNI Data
> **Working master draft** (front matter now included, formatted to the SCS/MSPA guidelines). All results
> reproducible from notebooks 06–08 (seed 42); CSF p-tau181 correction complete (Methods §3.12); 33 features.

---



## 1. TITLE PAGE  *(unnumbered)*

<div align="center">

**Predicting Alzheimer's Disease Progression with Machine Learning: Early, Leakage-Free Prediction of Diagnosis and Conversion from Multimodal ADNI Data**

By

**Warda Saeed**

Thesis Project
Submitted in partial fulfillment of the
Requirements for the degree of

**MASTER OF SCIENCE IN DATA SCIENCE**
*(confirm exact degree wording with your program — the format guide reads "Predictive Analytics")*

[Month, Year of degree conferral — e.g., August 2026]

[First Reader Name], First Reader
[Second Reader Name], Second Reader

</div>

> *Title check (per guide): title case applied (articles/conjunctions/prepositions — "with, of, from,
> and" — lowercased; first word of title and subtitle capitalized); no special characters; "ADNI" kept
> as a standard field acronym. If your reviewers prefer the acronym spelled out, replace "ADNI" with
> "the Alzheimer's Disease Neuroimaging Initiative."*

---

## 2. ABSTRACT  *(page 2; ≤ 350 words, one page)*

<div align="center">

**ABSTRACT**

Predicting Alzheimer's Disease Progression with Machine Learning: Early, Leakage-Free Prediction of Diagnosis and Conversion from Multimodal ADNI Data

Warda Saeed

</div>

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

---

## 3. TABLE OF CONTENTS

| Section | Page |
|---|---|
| Abstract | — |
| List of Tables | — |
| List of Figures | — |
| **Chapter 1 — Introduction** | — |
| 1.1 Overview of Alzheimer's Disease | — |
| 1.2 Statement of the Problem | — |
| 1.3 Research Objectives | — |
| 1.4 Hypotheses | — |
| 1.5 Justification and Significance | — |
| **Chapter 2 — Literature Review** | — |
| 2.1 Genetic Factors in AD | — |
| 2.2 Neuropathology | — |
| 2.3 Brain Atrophy and Structural Change | — |
| 2.4 Diagnostic Methods and Biomarkers | — |
| 2.5 Benefits of Early Diagnosis | — |
| 2.6 The Role of ADNI | — |
| 2.7 Machine Learning in AD Prediction, and the Methodological Gap | — |
| **Chapter 3 — Methods** | — |
| 3.1 Study Design and Data Source | — |
| 3.2 Baseline Data Preparation | — |
| 3.3 Missing-Data Treatment and Encoding | — |
| 3.4 Cohort Construction and Unit of Analysis | — |
| 3.5 Feature Set | — |
| 3.6 Classification Models | — |
| 3.7 Predictor Identification | — |
| 3.8 Survival Analysis (Time to Conversion) | — |
| 3.9 Clinical Risk Score | — |
| 3.10 Cognitive-Decline Trajectories | — |
| 3.11 Software and Reproducibility | — |
| 3.12 Data-Integrity Correction: CSF p-tau (PTAU) | — |
| **Chapter 4 — Results** | — |
| 4.1 Participant Flow and Cohort Construction | — |
| 4.2 Exploratory Data Analysis | — |
| 4.3 Impact of Evaluation Design (Data Leakage) | — |
| 4.4 Conversion Labeling and Sensitivity Analysis | — |
| 4.5 Predictive Performance Across Cohorts and Algorithms | — |
| 4.6 Predictors of Conversion and Their Stage Dependence | — |
| 4.7 Time to Conversion (Survival Analysis) | — |
| 4.8 A Parsimonious Clinical Risk Score | — |
| 4.9 Cognitive Decline Trajectories | — |
| 4.10 Detailed Classification Performance and Calibration | — |
| 4.11 Subgroup and Fairness Analysis | — |
| 4.12 Feature-Group Contribution | — |
| **Chapter 5 — Discussion** | — |
| 5.1 Summary of Principal Findings | — |
| 5.2 Stage-Dependent Predictors | — |
| 5.3 Model Performance and the Study Hypothesis | — |
| 5.4 Timing of Conversion | — |
| 5.5 A Methodological Contribution: Evaluation Rigor and Label Quality | — |
| 5.6 Clinical Implications | — |
| 5.7 Limitations | — |
| 5.8 Future Directions | — |
| **Chapter 6 — Conclusion** | — |
| References | — |
| **Appendices** | — |
| Appendix A — Model Specifications and Hyperparameters | — |
| Appendix B — Feature Dictionary (33 Baseline Predictors) | — |
| Appendix C — Supplementary Results | — |

---

## 4. LIST OF TABLES

| Table | Title | Page |
|---|---|---|
| 4.1 | Baseline characteristics by diagnostic group | — |
| 4.2 | Converters by outcome definition | — |
| 4.3 | ROC-AUC by model and cohort (5-fold CV, mean ± SD) | — |
| 4.4 | Top early predictors by cohort (permutation-importance rank) | — |
| 4.5 | Kaplan–Meier: probability of remaining dementia-free | — |
| 4.6 | Detailed performance by cohort (AUC 95% CI, sensitivity, specificity, PPV, NPV, F1, Brier) | — |
| 4.7 | Pooled → AD ROC-AUC by subgroup | — |
| 4.8 | Feature-group ablation | — |

---

## 5. LIST OF FIGURES

| Figure | Title | Page |
|---|---|---|
| EDA-1 | Cohort overview: baseline demographics and follow-up | — |
| EDA-2 | Distributions of key cognitive, MRI, and biomarker features | — |
| EDA-3 | Key features by baseline diagnosis (CN / MCI / Dementia) | — |
| EDA-4 | Correlation matrix of baseline features | — |
| EDA-5 | Baseline feature distributions by eventual outcome (converter vs stable) | — |
| 1 | Receiver operating characteristic curves by cohort | — |
| 2 | Stage-dependent early predictors (permutation importance) | — |
| 3 | Kaplan–Meier estimates of remaining dementia-free, MCI cohort, by APOE4 status | — |
| 4 | Cox proportional-hazards model of time to MCI → Dementia conversion | — |
| 5 | Subgroup performance (Pooled → AD): fairness check | — |

*Note: figures are labeled EDA-1…EDA-5 (exploratory) and 1…5 (results); renumber sequentially (1–10)
during final layout if your reviewers prefer a single series.*

---

### Author to complete
- [ ] First Reader (Thesis Advisor) name; Second Reader (Final Reader) name
- [ ] Degree-conferral month/year on title page and the exact degree name (Data Science vs. Predictive Analytics)
- [ ] Paste the abstract body under the ABSTRACT header (from `THESIS_Abstract_DRAFT.md`)
- [ ] Page numbers in TOC / List of Tables / List of Figures (auto-generate in Word after layout)



---


# Chapters 1 & 2 — Introduction and Literature Review (Rewrite Draft)

> Preserves the existing draft's content and its four verified references (WHO 2021; Venugopalan et
> al. 2021; Grabher 2018; Porsteinsson et al. 2021). Prose tightened; **§1.3 Objectives and §1.4
> Hypothesis updated to match the study as actually conducted**; a methodological-gap paragraph added
> to §2.7. `[CITATION NEEDED]` marks claims that require a supporting reference — no references were
> fabricated.

---

# Chapter 1 — Introduction

## 1.1 Overview of Alzheimer's disease

Alzheimer's disease (AD) is a progressive neurodegenerative disorder that primarily impairs memory and
cognition and ultimately erodes independent functioning. It is characterized pathologically by the
accumulation of misfolded proteins — extracellular amyloid-beta plaques and intracellular
neurofibrillary tau tangles — accompanied by widespread neuronal loss and brain atrophy. The disease
imposes an enormous and growing burden: an estimated 5.7 million individuals were affected in 2020, a
figure projected to reach 79 million worldwide by 2030 and approximately 139 million by 2050 — about
16% of the projected global population — with associated healthcare expenditures approaching
US$2 trillion (World Health Organization, 2021; Venugopalan et al., 2021). As one commentator observed,
AD is among the costliest chronic diseases to society, with the potential to strain healthcare systems
to their limits (Grabher, 2018). In the absence of a cure, the most actionable lever for reducing this
burden is **earlier and more accurate detection**, which creates the window in which existing and
emerging interventions are most effective.

## 1.2 Statement of the problem

Despite advances in neuroimaging and fluid biomarkers, early AD diagnosis remains difficult. Current
clinical tools often lack the sensitivity to detect the earliest cognitive change, and patients'
compensatory strategies can mask deficits, delaying diagnosis — on average by roughly two years from
symptom onset (Porsteinsson et al., 2021). The transitional stage of mild cognitive impairment (MCI)
is a particularly important target, as it represents a period during which intervention may most
plausibly alter trajectory, yet only a subset of MCI patients progress to dementia. There is therefore
a pressing need for data-driven methods that (a) identify which baseline measures signal impending
decline and (b) do so with the methodological rigor required for trustworthy, generalizable estimates.

## 1.3 Research objectives

This thesis applies machine learning to multimodal ADNI data — demographics, cognitive assessments,
structural MRI, FDG- and amyloid-PET, and CSF biomarkers — to identify early predictors of Alzheimer's
disease and of conversion to dementia. Its specific objectives are:

1. To identify baseline predictors of progression to dementia across the non-demented spectrum
   (cognitively normal and MCI), using a leakage-free, participant-level evaluation framework.
2. To compare the discriminative performance of multiple machine-learning algorithms (logistic
   regression, random forest, XGBoost, support vector machine, k-nearest neighbors, and a neural
   network) for predicting conversion.
3. To determine whether the most informative predictors **differ by baseline diagnostic stage**, by
   modeling CN and MCI cohorts separately as well as pooled.
4. To model the **timing** of MCI-to-dementia conversion using survival analysis and to identify
   predictors of conversion tempo.
5. To assess whether a small, clinically accessible set of measures can approximate the full model as a
   practical risk score.

## 1.4 Hypotheses

**Primary hypothesis.** Baseline multimodal measures predict progression to dementia with clinically
useful discrimination, and the most informative predictors differ systematically by baseline stage —
with structural and memory measures dominating earliest (CN) and functional, metabolic, and amyloid
measures dominating nearer to dementia (MCI).

**Secondary hypothesis.** Nonlinear ensemble methods (random forest, XGBoost) will improve
discrimination over linear models. _(As reported in Chapter 5, this secondary hypothesis was only
partially supported — ensembles did not meaningfully exceed logistic regression — which is itself an
informative result.)_

> _Note to author: the original proposal framed ensemble superiority as the primary hypothesis. It is
> presented here as a secondary, testable hypothesis so that the (honest) finding of near-equivalence
> is reported as evidence rather than as a failure. Adjust to your advisor's preference._

## 1.5 Justification and significance

By leveraging ADNI's multimodal, longitudinal design, this study aims to strengthen the evidence base
for early AD detection in two ways. Substantively, it characterizes stage-specific early predictors
that could inform assessment prioritization. Methodologically, it demonstrates how evaluation design
(participant-level versus visit-level data splitting) and outcome definition (confirmed versus transient
conversion) materially affect reported performance — an issue of direct relevance to the credibility of
machine-learning claims in this field.

---

# Chapter 2 — Literature Review

## 2.1 Genetic factors in AD

Although its precise etiology remains under investigation, AD has well-established genetic contributors.
Autosomal-dominant mutations in **presenilin 1 (PSEN1)** and **presenilin 2 (PSEN2)** — components of
the γ-secretase complex that cleaves amyloid precursor protein (APP) — are associated with early-onset
AD, typically before age 60. For the far more common late-onset form, the **apolipoprotein E (APOE)**
ε4 allele is the strongest common genetic risk factor, acting through effects on amyloid deposition and
tau phosphorylation, while the ε2 allele appears protective. `[CITATION NEEDED — APOE/PSEN mechanisms]`

## 2.2 Neuropathology

AD pathology is defined by two hallmarks: **amyloid plaques**, formed by aggregation of amyloid-beta
peptides derived from APP cleavage, which accumulate extracellularly and disrupt neuronal
communication; and **neurofibrillary tangles** of hyperphosphorylated tau, which impair intracellular
transport and contribute to neuronal death. The relative timing and coupling of these processes underlie
contemporary biomarker-based staging of the disease. `[CITATION NEEDED — amyloid/tau staging]`

## 2.3 Brain atrophy and structural change

Neurodegeneration in AD follows a characteristic spatial trajectory, beginning in the medial temporal
lobe — particularly the **hippocampus and entorhinal cortex** — and extending through parahippocampal
and temporal regions, the limbic system, and ultimately widespread neocortex. Hippocampal volume is
reported to be reduced by roughly a quarter in MCI and by up to 40% in AD relative to controls.
`[CITATION NEEDED — hippocampal atrophy figures]` These structural signatures motivate the MRI-derived
volumetric features (hippocampus, entorhinal cortex, mid-temporal cortex, ventricles, whole brain) used
in the present analysis.

## 2.4 Diagnostic methods and biomarkers

Contemporary AD assessment integrates three streams. **Neuroimaging** — structural MRI for atrophy,
FDG-PET for glucose metabolism, and amyloid-PET (e.g., AV45) for plaque burden. **CSF biomarkers** —
reduced amyloid-beta (ABETA) and elevated total and phosphorylated tau (TAU, p-tau), which change early
in the disease course. **Neuropsychological testing** — instruments such as ADAS-Cog, MMSE, MoCA, RAVLT,
the FAQ, and CDR-SB that quantify cognitive and functional status. The present study draws on all three
streams. _(Note: CSF phosphorylated tau was initially corrupted by a preprocessing error and was
corrected against the ADNI source before analysis; see Methods §3.12.)_

## 2.5 Benefits of early diagnosis

Earlier diagnosis benefits patients (access to treatment during the most effective window; time for
financial and legal planning), caregivers (reduced burden; opportunity for care planning), and health
systems (timely intervention; capacity management) (Porsteinsson et al., 2021). `[CITATION NEEDED —
caregiver-burden statistics]` These benefits are the practical motivation for improving predictive
tools at the MCI and preclinical stages.

## 2.6 The role of ADNI

The Alzheimer's Disease Neuroimaging Initiative (ADNI), launched in 2003 as a public–private
partnership, has been central to AD biomarker research. Its longitudinal, multimodal design — repeated
imaging, fluid biomarkers, and cognitive assessment across the diagnostic spectrum — enables the study
of disease trajectories and the validation of predictive models. Its enrollment strategy, however,
preferentially recruits participants with existing cognitive concern, a feature that shapes conversion
rates and is addressed as a limitation of the present work (Chapter 5). `[CITATION NEEDED — ADNI design
reference]`

## 2.7 Machine learning in AD prediction, and the methodological gap

A substantial literature applies machine learning to ADNI data to predict AD progression from
multimodal features, frequently reporting high accuracy for stage classification and MCI-to-dementia
conversion. `[CITATION NEEDED — 2–3 representative ADNI ML studies, e.g., Venugopalan et al., 2021 and
others]` Two methodological issues, however, are inconsistently handled in this literature and are
central to the present thesis. First, because ADNI participants contribute **multiple visits with
near-identical features and shared outcome labels**, partitioning data at the visit level rather than
the participant level can allow information to leak between training and test sets and inflate reported
performance. `[CITATION NEEDED — data leakage in longitudinal ML]` Second, **diagnostic status
fluctuates over time** (including reversion from MCI to normal), so outcome definitions based on a
single visit can misclassify converters. This thesis contributes by applying participant-level
evaluation and a confirmed-conversion outcome throughout, and by quantifying how these choices affect
results — complementing the substantive goal of identifying stage-specific early predictors of AD.

---

### Notes for you (delete before submission)
- All four in-text references (WHO 2021; Venugopalan et al. 2021; Grabher 2018; Porsteinsson et al.
  2021) are from your existing draft and are retained.
- Every `[CITATION NEEDED]` marks a factual claim that should be supported with a reference before
  submission. I did **not** invent any citations.
- The only substantive edits versus your original are §1.3 (objectives) and §1.4 (hypotheses), aligned
  to the analysis actually performed, plus the methodological-gap paragraph in §2.7.



---


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
folds; this prevents the optimistic bias documented in Section 4.2. Second, **standardization and SMOTE
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


# Chapter 4 — Results (Rewrite Draft)

> Draft grounded entirely in the committed, reproducible notebooks (06–08) and figures.
> All modeling is patient-level and leakage-free; conversion is defined as a worse diagnostic
> stage sustained on ≥2 consecutive visits ("confirmed conversion"). Every number below is
> produced by `notebooks/07_*` and `notebooks/08_*` with random seed 42.
> Bracketed notes like _[Fig 1]_ mark where figures are inserted.

---

## 4.1 Participant flow and cohort construction

Of the 2,131 participants in the processed ADNI baseline dataset, 453 were excluded for having only
a single visit (no follow-up over which an outcome could be observed), and 28 were excluded for
containing a clinically implausible improvement in diagnosis (Dementia → a less severe stage), which
was treated as diagnostic error. This left approximately 1,650 analyzable participants with at least
two visits.

Because the Alzheimer's Disease Neuroimaging Initiative preferentially enrolls participants who
already show cognitive concern, the baseline diagnostic distribution was weighted toward impairment.
Among the **full processed sample of 2,131** participants, 792 were cognitively normal (CN), 969 had
mild cognitive impairment (MCI), and 370 had dementia at baseline (the ~1,650 analyzable participants
noted above are the subset of this sample with at least two visits). This enrollment pattern is
discussed as a limitation (Section 5.7), as it inflates the apparent prevalence of conversion relative
to a community-based sample.

To respect the longitudinal structure of the data, all predictive models were built at the **patient
level**: each participant contributed a single record consisting of their **baseline (earliest) visit**,
and the model predicted that participant's **future** diagnostic outcome. Consequently, every
train/test partition separated *distinct individuals*, making it impossible for a given patient to
appear in both training and testing folds.

Table 4.1 summarizes baseline characteristics by diagnostic group. All cognitive, functional,
structural, and molecular markers worsened monotonically across the CN → MCI → Dementia continuum;
in particular, the corrected CSF p-tau181 increased across groups (21.4 → 27.9 → 36.5 pg/mL),
consistent with its role as a marker of tau pathology and confirming that the data-integrity
correction (Methods §3.12) restored a physiologically plausible measure. The distributions underlying
these summary values, the correlation structure among features, and the baseline separation between
eventual converters and non-converters are examined in the exploratory analysis (Section 4.2).

**Table 4.1 — Baseline characteristics by diagnostic group, mean (SD).**

| Characteristic | CN (n = 792) | MCI (n = 969) | Dementia (n = 370) |
|---|---|---|---|
| Age, years | 73.0 (6.2) | 72.9 (7.6) | 74.9 (7.9) |
| Education, years | 16.6 (2.6) | 15.9 (2.8) | 15.3 (3.0) |
| Sex, male / female | 354 / 438 | 571 / 398 | 207 / 163 |
| APOE4 alleles, mean | 0.32 | 0.59 | 0.84 |
| MMSE | 29.1 (1.1) | 27.6 (1.8) | 23.1 (2.1) |
| MoCA | 25.7 (2.4) | 22.5 (3.1) | 16.7 (3.8) |
| ADAS-13 | 10.3 (4.5) | 16.8 (6.7) | 30.2 (8.1) |
| CDR-SB | 0.0 (0.1) | 1.5 (0.9) | 4.4 (1.7) |
| FAQ | 0.2 (0.9) | 3.2 (4.1) | 13.2 (7.0) |
| Delayed memory (LDELTOTAL) | 13.2 (3.3) | 5.7 (3.4) | 1.4 (1.9) |
| Hippocampal volume (mm³) | 7,407 (824) | 6,724 (1,104) | 5,725 (975) |
| CSF Aβ (ABETA, pg/mL) | 1,248 (369) | 956 (397) | 674 (269) |
| CSF total tau (pg/mL) | 237 (69) | 289 (117) | 368 (123) |
| CSF p-tau181 (pg/mL) | 21.4 (7.0) | 27.9 (13.1) | 36.5 (13.3) |
| Amyloid-PET (AV45 SUVR) | 1.1 (0.2) | 1.2 (0.2) | 1.4 (0.2) |
| FDG-PET (SUVR) | 1.3 (0.1) | 1.2 (0.1) | 1.1 (0.1) |

## 4.2 Exploratory data analysis

Before modeling, the baseline cohort (each participant's first visit, N = 2,131) was characterized
descriptively to (a) document the sample and its representativeness, (b) verify data quality and the
plausibility of feature distributions, and (c) establish, in an unadjusted view, which measures
separate diagnostic groups and eventual converters. These analyses motivate the feature set and the
stratified design used in the modeling sections and are reported as five figures. Because most features
are skewed (Figure EDA-2), values below are given as **median [interquartile range]** and group
differences use the Mann–Whitney *U* test; all values were computed from `data/pre_modelling_data.csv`
and reflect the corrected CSF p-tau181 (Methods §3.12).

**Figure EDA-1 — Cohort composition and follow-up.** Six panels summarize the baseline sample:
distribution of baseline diagnosis, age, education, sex, *APOE* ε4 allele count, and number of
longitudinal visits per participant. The cohort is weighted toward the impaired end of the spectrum:
969 participants (45.5%) were MCI at baseline, 792 (37.2%) CN, and 370 (17.4%) dementia. Participants
were older adults (median age 73.4 years, IQR 68.3–78.4) and highly educated (median 16 years, IQR
14–18), with a slight male majority (1,132 men, 999 women). *APOE* ε4 showed the expected dose gradient
(1,197 non-carriers, 740 with one allele, 194 with two). Follow-up was right-skewed: most participants
contributed a few visits, with a long tail up to ~15. The over-representation of MCI is a design
feature of ADNI, a convenience cohort that preferentially enrolls individuals with existing cognitive
concern; this, and the high educational attainment, limit generalization to the general population and
are carried forward as limitations (Section 5.7). The visible ε4 dose gradient is a first internal
validity check — a well-established risk factor is distributed as the literature predicts.

**Figure EDA-2 — Univariate distributions of the modeling features.** Histograms of sixteen key
cognitive, MRI-volumetric, and fluid/PET biomarker features reveal three distributional patterns, each
with a modeling consequence. (i) *Ceiling and floor effects*: MMSE piles up at its maximum of 30 (a
well-known ceiling effect in a cohort with many unimpaired participants), while FAQ and CDRSB floor
near zero. (ii) *Right-skew in the fluid biomarkers*: total tau and, after correction, phosphorylated
tau (median ~24 pg/mL on the correct 8–120 pg/mL scale) are right-skewed — confirming p-tau is no
longer a rescaled duplicate of total tau (Methods §3.12). (iii) *Bimodality in amyloid measures*: both
CSF Aβ42 and amyloid-PET (AV45) show two modes, consistent with the biological split between
amyloid-negative and amyloid-positive individuals; the ABETA spike at the upper bound reflects assay
truncation at its ceiling. MRI volumes and FDG are approximately symmetric. These shapes justify
reporting medians with IQRs for descriptive summaries and standardizing all features before any
distance- or gradient-based model (KNN, SVM, MLP, logistic regression).

**Figure EDA-3 — Feature separation by baseline diagnosis.** Box plots of nine core features across CN,
MCI, and Dementia give an unadjusted view of how strongly each measure tracks disease stage. Every
feature displays a monotone gradient, and the magnitude of separation orders the modalities. Global
cognition and function separate most sharply (ADAS13 median 10.0 [7–13] → 16.7 [12–21] → 29.7 [24–35];
CDRSB 0.0 → 1.5 → 4.5; FAQ 0.0 → 1.0 → 13.0); memory shows the same ordering (LDELTOTAL 13 → 6 → 0;
RAVLT-immediate 45 → 33 → 23). Structural and metabolic imaging separate more modestly but consistently
(hippocampus 7,434 → 6,706 → 5,614 mm³; FDG 1.3 → 1.2 → 1.1). Molecular pathology tracks stage in the
expected directions (CSF Aβ42 falls 1,310 → 854 → 630 pg/mL; corrected p-tau rises 20.2 → 25.2 → 35.1
pg/mL), and *APOE* ε4 carriage climbs in parallel (29% → 48% → 64%). This uniform, biologically
coherent staging confirms the features carry genuine, correctly oriented disease signal — a data-quality
gate before modeling — and previews a central finding: the *degree* of separation is stage-dependent,
which motivates modeling the cohorts separately rather than pooling them blindly (Methods §3.4; Section
4.6). Box-plot separation by *current* diagnosis, however, is not the same as *predictive* value for
*future* conversion, which is examined next.

**Figure EDA-4 — Correlation structure of the feature set.** A Pearson correlation heat map of 26
baseline features reveals coherent blocks. A *cognitive block* is strongly inter-correlated (MMSE–MOCA
r = +0.76; ADAS13–MMSE r = −0.74; the composites mPACCdigit–mPACCtrailsB r = +0.98, near-duplicates by
construction). A *medial-temporal structural block* groups hippocampus–entorhinal (r = +0.70) with
midtemporal and fusiform volumes, and whole-brain tracks with ICV (r = +0.72). A *molecular block*
links the amyloid measures inversely (ABETA–AV45 r = −0.73) and the tau measures tightly (TAU–PTAU
r = +0.98). Cross-block, higher ADAS13 correlates with lower FDG metabolism (r = −0.65) and smaller
hippocampal volume (r = −0.55); age is only weakly correlated with most features. This block structure
explains two downstream results: the high within-block redundancy means a parsimonious model can
recover most of the signal (the basis for the seven-variable risk score, Section 4.8, and the ablation
in Section 4.12, where removing any single imaging or biomarker modality barely changes performance);
and the near-perfect TAU–PTAU correlation is the pattern the earlier data corruption produced
*artifactually* — its persistence at the corrected scale confirms the two tau species are genuinely
co-regulated, not that the correction reintroduced the error (Methods §3.12). High collinearity also
cautions against over-interpreting any single feature's coefficient within a correlated block.

**Figure EDA-5 — Baseline features by eventual outcome (converter vs. stable).** Overlaid,
density-normalized histograms of eight leading features for participants non-demented at baseline, split
by whether they later met the confirmed conversion-to-dementia definition (Methods §3.4) versus remained
stable. Among the **1,761 participants non-demented at baseline** (792 CN + 969 MCI), **257** later
showed a confirmed conversion to dementia and **1,504** remained stable. Future converters and stable
participants show clearly offset — though substantially overlapping — baseline distributions, with every
displayed feature differing at p < 10⁻³⁷ (Mann–Whitney *U*). Future converters started with worse
function (FAQ
median 4.0 vs 0.0), worse memory (LDELTOTAL 3.0 vs 10.0), worse global cognition (ADAS13 19.7 vs 12.0;
MOCA 21.0 vs 24.9), lower FDG metabolism (1.2 vs 1.3), smaller hippocampi (6,180 vs 7,203 mm³), and a
more Alzheimer's-like molecular profile (AV45 1.4 vs 1.1; CSF Aβ42 668 vs 1,168 pg/mL). Critically,
however, the two distributions overlap heavily for every feature — no single baseline measure cleanly
partitions converters from non-converters. This figure states visually both the promise and the
difficulty of early prediction: the consistent, highly significant shifts confirm baseline multimodal
information is genuinely predictive of *future* decline, but the pervasive overlap explains why
discrimination is good rather than perfect in the impaired-spectrum cohorts and genuinely hard from full
cognitive normality (Section 4.5). (This figure is descriptive and uses all 1,761 non-demented baseline
participants with a to-dementia outcome. The modeling sections instead use the subset with follow-up
eligibility and cohort-specific outcomes — CN n = 519 with 74 confirmed progressions to MCI **or**
dementia, and MCI n = 819 with 228 confirmed progressions to dementia — so the descriptive converter
count here, 257, is not expected to equal the sum of the two modeling-cohort event counts.)

## 4.3 Impact of evaluation design (data leakage)

Preliminary modeling that split the data at the visit level (i.e., treating each of a participant's
~4–5 visits as an independent record) produced optimistic accuracy estimates. For the early-detection
task, a Random Forest reported ~82% accuracy under visit-level splitting; however, under a correct
patient-grouped split the same model's balanced accuracy fell to ~34% (chance level for the outcome
distribution). The discrepancy arose because a participant's repeated visits carry near-identical
features and the same eventual-outcome label; a random visit-level split therefore allowed the model
to recognize individuals it had already seen rather than to generalize. All results reported below
use patient-level partitioning to avoid this bias.

## 4.4 Conversion labeling and sensitivity analysis

Because diagnostic status fluctuates in ADNI, the definition of "converter" materially affects the
analysis. Diagnostic reversion (an improvement between consecutive visits) occurred in 123 participants
(5.8% of the full sample), comprising **136 reversion events** — 108 MCI → CN and 28 Dementia → MCI
(the difference reflects 13 participants who reverted more than once). The 28 Dementia → MCI cases are
the clinically implausible improvements excluded during cohort construction (§3.4). A further 18
participants exhibited the CN → (MCI/Dementia) → CN pattern.

Table 4.2 reports the number of converters under alternative outcome definitions, all computed on the
**same eligible cohorts used for modeling** (MCI n = 819; CN n = 519), so the confirmed row matches the
event counts carried into every subsequent analysis. Requiring a **confirmed** transition (worse stage
sustained ≥2 consecutive visits) reduced converter counts by roughly 30% relative to a naïve last-visit
definition, removing single-visit fluctuations. The confirmed definition was pre-specified as the
primary outcome for all subsequent models.

**Table 4.2 — Converters by outcome definition** (denominators: eligible MCI n = 819, CN n = 519)

| Definition | MCI→Dementia | CN→MCI/Dementia |
|---|---|---|
| Last-visit only | 321 (39%) | 106 (20%) |
| Ever reached worse stage | 321 (39%) | 116 (22%) |
| **Confirmed (≥2 visits) — primary** | **228 (28%)** | **74 (14%)** |
| Confirmed within 36 months | 177 (22%) | 26 (5%) |
| Confirmed within 24 months | 138 (17%) | 17 (3%) |

For the MCI cohort, the last-visit and ever-reached counts coincide (321) because dementia is a
near-absorbing state once the implausible reversions are removed. Short fixed-horizon definitions
(24/36 months) were inappropriate for the CN cohort because CN→MCI conversion is slow (median time to
confirmed conversion ≈ 4 years); the confirmed-any-time definition was therefore used, with time-to-event
modeled explicitly via survival analysis (Section 4.7).

## 4.5 Predictive performance across cohorts and algorithms

Three cohorts were modeled: (A) baseline **CN → progression** to MCI or dementia; (B) baseline
**MCI → Dementia**; and (C) a **pooled** CN+MCI cohort predicting progression to dementia, with
baseline diagnosis deliberately excluded from the feature set so that the model surfaced biological
and cognitive predictors rather than the trivial CN-vs-MCI distinction.

Six algorithms named in the study design were evaluated identically under 5-fold cross-validation
with SMOTE applied inside training folds only. Discrimination (ROC-AUC) is reported in Table 4.3 and
the receiver operating characteristic curves in _[Fig 1 — fig1_roc_cohorts.png]_.

**Table 4.3 — ROC-AUC by model and cohort (5-fold CV, mean ± SD)**

| Model | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| Logistic Regression | 0.69 ± 0.05 | 0.82 ± 0.02 | 0.87 ± 0.03 |
| Random Forest | 0.65 ± 0.03 | 0.83 ± 0.03 | 0.88 ± 0.03 |
| XGBoost | 0.69 ± 0.04 | 0.82 ± 0.03 | 0.87 ± 0.03 |
| SVM (RBF) | 0.68 ± 0.03 | 0.81 ± 0.02 | 0.86 ± 0.03 |
| K-Nearest Neighbors | 0.64 ± 0.04 | 0.78 ± 0.03 | 0.83 ± 0.03 |
| Neural Network (MLP) | 0.62 ± 0.05 | 0.80 ± 0.02 | 0.84 ± 0.04 |

Cohort n / events: CN→progression 519 / 74 (14%); MCI→Dementia 819 / 228 (28%); Pooled 1,338 / 244 (18%).

Two patterns are notable. First, discrimination increased with baseline impairment: the pooled and
MCI cohorts achieved strong performance (AUC 0.83–0.88), whereas prediction of progression from full
cognitive normality was substantially harder and under-powered (AUC ≈ 0.65–0.69, 74 events). Second,
the top-performing algorithms — Random Forest, XGBoost, and Logistic Regression — were statistically
indistinguishable, with the simple linear model matching the ensembles. This indicates that the
predictive signal in these features is largely linear and does not require nonlinear modeling, which
qualifies the study hypothesis (Section 5.3).

## 4.6 Predictors of conversion and their stage dependence

Permutation importance (mean decrease in ROC-AUC on held-out folds) was used to rank predictors within
each cohort _[Fig 2 — fig2_predictors.png]_. This complements the exploratory finding that converters
and stable participants already separate at baseline on several of these measures (Section 4.2, Figure
EDA-5). Two complementary feature-selection methods were also applied to the pooled cohort: univariate
selection (ANOVA F-test, SelectKBest) and Recursive Feature Elimination with logistic regression.

**Table 4.4 — Top early predictors by cohort (permutation importance rank)**

| Rank | CN → progression | MCI → Dementia | Pooled → AD |
|---|---|---|---|
| 1 | Hippocampus | FAQ | FAQ |
| 2 | ICV | FDG | AV45 |
| 3 | MOCA | LDELTOTAL | ABETA |
| 4 | Age | mPACCtrailsB | LDELTOTAL |
| 5 | LDELTOTAL | ADAS13 | RAVLT-immediate |
| 6 | MMSE | Age | FDG |
| 7 | FDG | ABETA | CDRSB |
| 8 | CDRSB | RAVLT-immediate | mPACCtrailsB |

The dominant predictors shifted with disease stage. At the earliest (CN) stage, **structural and
memory** measures led — hippocampal volume, intracranial volume, memory (LDELTOTAL), and global
cognition (MOCA, MMSE) — consistent with early medial-temporal atrophy. Closer to dementia (MCI stage),
the strongest predictors were measures of **daily function (FAQ), brain metabolism (FDG), and amyloid
burden (AV45, ABETA)**. The corrected CSF phosphorylated-tau measure (PTAU) entered the models as a
**mid-tier predictor**: it ranked ≈ 11th–12th of 33 features by Random Forest permutation importance in
the MCI→Dementia model and 9th in the pooled model — mid-pack in both cases, consistent with its known
but partly redundant relationship to total tau (Methods §3.12).

Two complementary selection methods were applied to the pooled cohort: SelectKBest (ANOVA F-test) chose
mPACCtrailsB, FAQ, ADAS13, mPACCdigit, LDELTOTAL, CDRSB, AV45, MOCA, RAVLT-immediate, and FDG; RFE
(logistic) chose AGE, ABETA, FAQ, Hippocampus, ICV, mPACCtrailsB, PTAU, TAU, WholeBrain, and Never-married.
**FAQ was selected by all three approaches** (permutation importance, SelectKBest, RFE), and a further
group appeared in two of the three — **LDELTOTAL, AV45, CDRSB, FDG, RAVLT-immediate, mPACCtrailsB, and
ABETA** — constituting the most robust predictor set. That RFE retained both PTAU and TAU indicates
each tau species carries some non-redundant signal once PTAU is correctly scaled. One RFE-selected
feature ("Never married") is almost certainly spurious and illustrates the value of requiring
convergence across selection methods.

## 4.7 Time to conversion (survival analysis)

For the MCI cohort (819 participants; 228 confirmed conversions; 591 right-censored at last visit),
time from baseline to first confirmed dementia was modeled. Kaplan–Meier estimates stratified by APOE4
status _[Fig 3 — fig3_km_apoe4.png]_ showed markedly faster progression among APOE4 carriers:

**Table 4.5 — Kaplan–Meier: probability of remaining dementia-free**

| Group | 2 years | 3 years | 5 years |
|---|---|---|---|
| APOE4 negative | 88% | 85% | 80% |
| APOE4 positive | 75% | 65% | 55% |
| All MCI | 81% | 75% | 68% |

A Cox proportional-hazards model (features standardized; hazard ratios per 1 SD) identified independent
predictors of conversion timing _[Fig 4 — fig4_cox_forest.png]_. Higher **FAQ (HR ≈ 1.41), ADAS13
(1.34), and amyloid AV45 (1.29)** were associated with faster conversion, while higher **FDG (0.72),
verbal memory (RAVLT-immediate 0.76; LDELTOTAL 0.79), and hippocampal volume (0.79)** were associated
with slower conversion. These timing predictors align with the classification-based importance
rankings, providing convergent evidence.

## 4.8 A parsimonious clinical risk score

To assess whether a small set of clinically accessible variables could approximate the full models, a
logistic-regression risk score was built for MCI→Dementia from seven inputs (age, APOE4, MMSE, FAQ,
CDRSB, hippocampal volume, ADAS13). This parsimonious score achieved ROC-AUC ≈ 0.81 ± 0.03 — nearly
matching the full multivariable models — indicating that a handful of routine measures (led by ADAS13,
FAQ, hippocampal volume, and APOE4) capture most of the available predictive signal.

## 4.9 Cognitive decline trajectories

Linear mixed-effects models (random intercept and slope per participant) characterized the rate of
cognitive decline by baseline group. All groups worsened over time, and the dementia group declined
fastest: ADAS13 rose by ≈ +2.22 points/year in the dementia group, versus ≈ +1.73 (CN) and ≈ +1.62
(MCI); CDRSB showed the same pattern (Dementia +0.67, CN +0.49, MCI +0.46 points/year). The dementia
group is clearly the fastest-declining, while the CN and MCI group slopes are essentially
indistinguishable from each other.

These absolute slopes should be interpreted with strong caution and are **not** comparable to
community-based estimates of cognitive decline in healthy older adults (where cognitively normal ADAS13
slopes are typically well under +0.5 points/year). The magnitude here is inflated by two features of the
design: ADNI's CN group is an enriched, help-seeking sample that includes a substantial fraction of
future converters, and the random-slope model attributes the accelerating decline of those eventual
converters to the group-average slope. The finding should therefore be read as a within-study relative
ordering, not as an epidemiological decline rate.

## 4.10 Detailed classification performance and calibration

Table 4.6 reports discrimination (ROC-AUC with bootstrap 95% confidence intervals from 1,000 resamples)
alongside threshold-based operating characteristics at a 0.5 cut-point (sensitivity, specificity,
positive and negative predictive value, F1) and probability calibration (Brier score) for each cohort.

**Table 4.6 — Detailed performance by cohort (patient-level out-of-fold predictions).**

| Cohort | ROC-AUC (95% CI) | Sens. | Spec. | PPV | NPV | F1 | Brier |
|---|---|---|---|---|---|---|---|
| CN → progression | 0.65 (0.58–0.72) | 24% | 89% | 28% | 88% | 0.26 | 0.147 |
| MCI → Dementia | 0.82 (0.80–0.85) | 65% | 80% | 56% | 86% | 0.60 | 0.155 |
| Pooled → AD | 0.88 (0.86–0.90) | 67% | 88% | 55% | 92% | 0.61 | 0.113 |

The pooled and MCI models combined high specificity with high negative predictive value (NPV 86–92%):
a low predicted risk reliably identified non-converters, which is clinically useful for ruling out
imminent progression. Positive predictive value was more modest (55–56%), an expected consequence of the
low conversion base rate. Brier scores of 0.11–0.16 indicate reasonable probability calibration. The CN
model's low sensitivity at the default threshold (24%) reflects its limited statistical power; where
early flagging is prioritized, a lower decision threshold would trade specificity for sensitivity.

## 4.11 Subgroup and fairness analysis

To assess generalizability across patient subgroups, pooled-model discrimination was recomputed within
strata defined by sex, APOE4 status, education, and age (Table 4.7, Figure 5).

**Table 4.7 — Pooled → AD ROC-AUC by subgroup.**

| Subgroup | n | Events | ROC-AUC |
|---|---|---|---|
| Male | 737 | 142 | 0.87 |
| Female | 601 | 102 | 0.88 |
| APOE4-negative | 771 | 83 | 0.87 |
| APOE4-positive | 567 | 161 | 0.84 |
| Education < 16 yr | 447 | 92 | 0.83 |
| Education ≥ 16 yr | 891 | 152 | 0.90 |
| Age < 75 yr | 767 | 134 | 0.91 |
| Age ≥ 75 yr | 571 | 110 | 0.82 |

Performance was equivalent by sex (0.87 vs 0.88). Two disparities were notable: the model discriminated
better for more-educated participants (0.90 vs 0.83) and for younger participants (0.91 vs 0.82), and
modestly worse for APOE4 carriers (0.84 vs 0.87). These gaps — likely reflecting ADNI's education-skewed
enrollment and the greater clinical heterogeneity of older and higher-genetic-risk patients — matter for
equitable deployment and are discussed in Section 5.7.

## 4.12 Feature-group contribution

To quantify each data modality's contribution, the pooled model was refit using each feature group in
isolation and, separately, with each group removed (Table 4.8).

**Table 4.8 — Feature-group ablation (Pooled → AD; full-model AUC 0.88).**

| Feature group | AUC (group alone) | AUC (group removed) | Δ if removed |
|---|---|---|---|
| Cognitive / functional | 0.855 | 0.838 | −0.042 |
| MRI volumetric | 0.747 | 0.877 | −0.003 |
| PET (AV45, FDG) | 0.791 | 0.879 | −0.001 |
| CSF (ABETA, TAU, PTAU) | 0.755 | 0.877 | −0.003 |
| Demographic / genetic | 0.659 | 0.876 | −0.004 |

Cognitive and functional measures alone reached an AUC of 0.855 — close to the full multimodal model
(0.88) — and their removal produced by far the largest degradation (−0.042). Removing any single
imaging, biomarker, or demographic block barely changed performance (−0.001 to −0.004), because those
modalities are substantially correlated with the cognitive measures and with one another (Section 4.2,
Figure EDA-4). This redundancy explains why the parsimonious clinical score (Section 4.8) approaches the
full model, and it indicates that, for conversion prediction in this cohort, cognitive-functional
assessment carries most of the actionable signal.

---

### Notes for you (delete before submission)
- Every number here is traceable to notebooks 06–08 and the figures in `notebooks/figures/`.
- **Section map after adding EDA:** §4.1 sample/flow + Table 4.1 → §4.2 exploratory data analysis
  (Figures EDA-1–EDA-5) → §4.3 data leakage → §4.4 labeling → §4.5 performance → §4.6 predictors →
  §4.7 survival → §4.8 risk score → §4.9 trajectories → §4.10 detailed metrics → §4.11 fairness →
  §4.12 ablation. Tables keep their numbers (4.1–4.8); figures are EDA-1…EDA-5 and 1…5.
- The 89% 3-class result from the original `04` notebook is intentionally **not** presented as an
  early-detection result — if you want to keep it, present it as *concurrent diagnostic classification*
  and note its circularity (it uses CDRSB/FAQ, which partly define the diagnosis).


# Chapter 5 — Discussion (Rewrite Draft)

> Interpretive chapter grounded in the verified results (notebooks 06–08, figures). Conclusions here
> do not depend on the PTAU correction (now completed, Methods §3.12); the former p-tau markers flag the
> few sentences to revisit once real phosphorylated-tau is re-introduced.

---

## 5.1 Summary of principal findings

This study used multimodal ADNI data to identify early predictors of Alzheimer's disease and of
conversion to dementia, under a deliberately conservative, leakage-free evaluation framework. Four
findings stand out. First, progression to dementia could be predicted from baseline measures with good
discrimination in impaired-spectrum cohorts (MCI→Dementia ROC-AUC ≈ 0.83; pooled CN+MCI→AD ≈ 0.88),
but prediction of decline from full cognitive normality was substantially harder (CN→progression
≈ 0.65–0.69). Second, the most informative predictors **shifted with disease stage**. Third, ensemble
methods did **not** meaningfully outperform logistic regression, indicating a largely linear signal.
Fourth, APOE4 carriage and baseline functional, metabolic, and amyloid measures predicted not only
*whether* but *how quickly* MCI patients converted.

## 5.2 Stage-dependent predictors

The stratified design revealed a clinically coherent progression in the dominant predictors. Among
cognitively normal participants, **structural and memory** measures led — hippocampal and intracranial
volume, delayed and verbal memory (LDELTOTAL, RAVLT), and MOCA — consistent with the established view
that medial-temporal atrophy and subtle memory change are among the earliest detectable signs of the
disease. Among MCI participants, the strongest predictors shifted toward **daily functional decline
(FAQ), cerebral glucose metabolism (FDG-PET), and amyloid burden (AV45, ABETA)**, reflecting a stage in
which pathological and functional processes are more advanced and more strongly coupled to imminent
dementia. This shift — from *structure/memory* early to *function/metabolism/pathology* later — is the
central scientific contribution of stratifying the cohorts rather than pooling them blindly, and it
aligns with contemporary staging models of the AD continuum. Once the corrupted CSF p-tau181 measure
was corrected (Methods §3.12), it entered the models as a mid-tier predictor rather than a leading one —
consistent with its strong correlation with, and only partly non-redundant signal beyond, total tau.

## 5.3 Model performance and the study hypothesis

The study hypothesized that ensemble methods (e.g., Random Forest) would outperform simpler linear
models. The evidence only partially supports this. While Random Forest and XGBoost achieved the highest
discrimination in absolute terms, **logistic regression matched them within cross-validation
uncertainty** across all three cohorts. The practical implication is that the predictive relationships
in these standardized, largely continuous features are approximately linear and additive, offering
little for nonlinear models to exploit. This is a more accurate and more defensible conclusion than a
claim of ensemble superiority, and it has a favorable side effect: a transparent, interpretable model
suffices, which matters for clinical translation. The comparatively weaker performance of KNN and the
multilayer perceptron is consistent with the modest sample sizes and the tabular nature of the data.

## 5.4 Timing of conversion

Survival analysis extended the binary conversion question to *when* conversion occurs. Kaplan–Meier
estimates showed markedly faster progression in APOE4 carriers (55% remained dementia-free at five
years versus 80% in non-carriers), reinforcing APOE4's role as a determinant of both risk and tempo.
The Cox model identified functional (FAQ), cognitive (ADAS13), and amyloid (AV45) measures as
predictors of faster conversion, and greater hippocampal volume, memory performance, and glucose
metabolism (FDG) as protective — a pattern that converges with the classification-based importance
rankings and lends internal consistency to the findings.

## 5.5 A methodological contribution: evaluation rigor and label quality

Beyond the substantive predictors, this work makes a methodological point that is easy to overlook in
applied machine-learning studies. Early modeling that partitioned the data at the **visit level**
produced an optimistic early-detection accuracy (~82%) that collapsed to chance (~34% balanced
accuracy) once individuals — rather than individual visits — were separated between training and test
sets. Because a participant's repeated visits share near-identical features and outcome labels, naïve
splitting allows a model to recognize individuals rather than to generalize. Relatedly, diagnostic
**reversion** (5.8% of participants improved at least once) meant that a naïve "last-visit" outcome
both missed genuine converters and counted transient fluctuations; a pre-specified **confirmed** outcome
(a worse stage sustained across ≥2 visits) was required for credible labels. Reporting these effects,
rather than concealing them, is itself a contribution: it demonstrates how ordinary data-handling
choices can transform a chance-level model into an apparently excellent one.

## 5.6 Clinical implications

The parsimonious seven-variable risk score (ROC-AUC ≈ 0.81 for MCI→Dementia) shows that a small set of
routinely available measures — led by ADAS13, FAQ, hippocampal volume, and APOE4 — captures most of the
predictive signal available from the full multimodal panel. This is encouraging for real-world use,
where full biomarker and imaging panels are often unavailable, and it dovetails with the finding that a
linear model suffices. Prioritizing functional and memory assessment, together with APOE4 genotyping,
may offer a practical, low-cost first-pass stratification of MCI patients by conversion risk. The
feature-group ablation (Section 4.12) reinforces this: cognitive and functional measures alone reached
an AUC of 0.855 versus 0.88 for the full multimodal panel, and removing any single imaging or biomarker
modality barely changed performance. Because these modalities are substantially inter-correlated, the
more expensive and invasive assessments (PET, lumbar puncture) added little *incremental* discrimination
here — an economically meaningful finding for resource-limited settings, though those modalities retain
value for mechanism, staging, and confirmation.

## 5.7 Limitations

1. **Enrollment / volunteer bias.** ADNI preferentially recruits participants who already have
   cognitive concern, over-representing prevalent MCI relative to a community sample. Absolute
   conversion rates therefore overstate population risk, and the well-powered results derive largely
   from the impaired end of the spectrum.
2. **Under-powered CN cohort.** Confirmed CN→progression events were few (74), and conversion from
   normality is slow (median ≈ 4 years). The modest CN-cohort performance (AUC ≈ 0.65–0.69) should be
   read as a lower bound reflecting limited events, not as evidence that early signal is absent.
3. **Diagnostic label noise.** Even with a confirmed-conversion definition, clinical diagnoses carry
   inter-rater variability, and clinically implausible reversions (e.g., dementia→MCI) were present and
   excluded as error.
4. **Data-integrity correction (PTAU).** A preprocessing error had placed CSF p-tau181 on the wrong
   scale, making it a near-duplicate of total tau. This was identified and corrected against the ADNI
   source (Methods §3.12); a sensitivity analysis confirmed the conversion results were unchanged, and
   corrected PTAU entered as a mid-tier predictor. This is reported as a resolved data-integrity check
   rather than a limitation, though it underscores the importance of biomarker-scale validation.
5. **Subgroup performance disparities.** Discrimination was equitable by sex but lower for
   less-educated participants (AUC 0.83 vs 0.90), older participants (0.82 vs 0.91 at age ≥ 75), and
   APOE4 carriers (0.84 vs 0.87; Section 4.11). These gaps likely reflect ADNI's education-skewed
   enrollment and greater heterogeneity among older, higher-risk patients. They caution against uniform
   deployment and motivate subgroup-aware calibration and validation before clinical use.
6. **Single-cohort, internal validation only.** All estimates derive from ADNI with cross-validation;
   no external or independent-cohort validation was performed, limiting claims about generalizability.
7. **Reversible transitions simplified.** Conversion was treated as effectively one-directional after
   confirmation; a full multi-state model of reversible CN↔MCI transitions was not undertaken.

## 5.8 Future directions

- **Incorporate plasma (blood-based) biomarkers.** ADNI now provides plasma phosphorylated tau —
  p-tau181 (Quanterix/Simoa) and p-tau217 (Fujirebio; C2N) — alongside plasma Aβ42/40, NfL, and GFAP.
  Plasma p-tau217 in particular is among the most promising minimally-invasive AD markers. A focused
  sub-study is warranted: in the present cohort, baseline plasma p-tau217 was available for
  approximately 360 participants, sufficient for a bounded analysis of its incremental predictive value
  even though coverage is currently too sparse for inclusion in the full baseline models.
- **External validation** in an independent, ideally community-based cohort to test generalizability
  beyond ADNI's enrollment profile.
- **Multi-state / competing-risks survival models** to represent reversible transitions and death as a
  competing event.
- **Image-based deep learning** (e.g., a convolutional network on structural or default-mode-network
  imaging) as a complementary modality, deferred here as a separate line of work.
- **Calibration and decision-curve analysis** to move from discrimination toward clinically actionable
  thresholds.

---

### Notes for you (delete before submission)
- Every claim traces to notebooks 06–08 and the figures; no numbers are asserted beyond what was computed.
- The p-tau markers have been resolved following the CSF p-tau181 correction (Methods §3.12) — none
  change the conclusions, they only potentially strengthen the tau-pathology story.


# Chapter 6 — Conclusion

This thesis set out to identify early predictors of Alzheimer's disease and of conversion to dementia
from multimodal ADNI data, under an evaluation framework rigorous enough to trust. Three contributions
follow. First, baseline multimodal measures predict progression to dementia with clinically useful
accuracy in the impaired-spectrum cohorts (pooled CN+MCI→AD ROC-AUC 0.88; MCI→Dementia 0.83), while
prediction from full cognitive normality remains genuinely hard (≈ 0.65–0.69). Second, the most
informative predictors change with disease stage — from structural and memory measures at the
cognitively-normal stage to functional, metabolic, and amyloid measures nearer dementia — a
stage-dependence visible only because the cohorts were modeled separately. Third, and most transferable,
the work shows that methodology determines credibility: participant-level evaluation and a
confirmed-conversion outcome are prerequisites for believable estimates, as a naïve visit-level analysis
produced an early-detection result of ~82% that collapsed to chance under a correct participant-grouped
split. Together the findings support stage-aware, interpretable models — logistic regression proved as
accurate as ensembles — and argue for leakage-free validation as a standard of practice. The limitations
in Chapter 5 (enrollment bias, an under-powered CN cohort, single-cohort validation) define the agenda
for the next iteration.

---


# References

_(APA/Chicago style to be finalized; complete the entries flagged in the Author Checklist. At least
seven scholarly sources with two published within the last ten years are required per the format guide.)_

Grabher, B. J. (2018). Effects of Alzheimer disease on patients and their family. *Journal of Nuclear
Medicine Technology, 46*(4), 335–340.

Porsteinsson, A. P., Isaacson, R. S., Knox, S., et al. (2021). Diagnosis of early Alzheimer's disease:
Clinical practice in 2021. *Journal of Prevention of Alzheimer's Disease, 8*, 371–386.

Venugopalan, J., Tong, L., Hassanzadeh, H. R., et al. (2021). Multimodal deep learning models for early
detection of Alzheimer's disease stage. *Scientific Reports, 11*, 3254.

World Health Organization. (2021). *Dementia fact sheet.*

---


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

---


# Author Checklist (open items)

## A. p-tau — COMPLETE
The CSF p-tau181 correction is done (Methods §3.12); 33 features; p-tau is a mid-tier predictor. No open p-tau blanks remain.

## B. Citations to add (no references were fabricated)
- **Intro/LitReview** (line 6): > to §2.7. `[CITATION NEEDED]` marks claims that require a supporting reference — no references were
- **Intro/LitReview** (line 93): tau phosphorylation, while the ε2 allele appears protective. `[CITATION NEEDED — APOE/PSEN mechanisms]`
- **Intro/LitReview** (line 101): contemporary biomarker-based staging of the disease. `[CITATION NEEDED — amyloid/tau staging]`
- **Intro/LitReview** (line 109): `[CITATION NEEDED — hippocampal atrophy figures]` These structural signatures motivate the MRI-derived
- **Intro/LitReview** (line 127): systems (timely intervention; capacity management) (Porsteinsson et al., 2021). `[CITATION NEEDED —
- **Intro/LitReview** (line 138): rates and is addressed as a limitation of the present work (Chapter 5). `[CITATION NEEDED — ADNI design
- **Intro/LitReview** (line 145): conversion. `[CITATION NEEDED — 2–3 representative ADNI ML studies, e.g., Venugopalan et al., 2021 and
- **Intro/LitReview** (line 150): performance. `[CITATION NEEDED — data leakage in longitudinal ML]` Second, **diagnostic status
- **Intro/LitReview** (line 161): - Every `[CITATION NEEDED]` marks a factual claim that should be supported with a reference before

## C. Figures
- Regenerate all four figures at **300 DPI** (currently 130 DPI) — one-line change in the figure script.
- Optional: CONSORT-style participant-flow diagram (§4.1) and a calibration plot (pooled model).

## D. Front matter / formatting
- Fill advisor name and program-required front matter on the title page.
- Trim Abstract to the program word limit if required (~330 words).
- Confirm hypothesis framing in §1.4 with your advisor.
