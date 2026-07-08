# Thesis Front Matter (formatted to SCS/MSPA Format Guidelines)

> Built to the format guide: Title Page → Abstract → Table of Contents → List of Tables → List of
> Figures. Bracketed `[…]` fields are for you to complete (reader names, date, degree name). Page
> numbers in the TOC/lists are shown as `—` and finalize during layout (Word/PDF). All table/figure
> titles below were verified three times against the actual chapter drafts and figure files.
>
> **Formatting reminders for the Word/PDF version (not shown in this Markdown):** US Letter (8.5×11),
> 1″ margins on all sides, double-spaced, every page numbered in the upper-right starting at **2** on
> the second page (title page unnumbered), APA or Chicago style throughout.

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

*(Insert the abstract text from `THESIS_Abstract_DRAFT.md` here — the Background/Objective/Methods/
Results/Conclusions paragraphs, ~330 words, no tables or formulas per the guide. Keywords may follow.)*

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
| 4.2 Impact of Evaluation Design (Data Leakage) | — |
| 4.3 Conversion Labeling and Sensitivity Analysis | — |
| 4.4 Predictive Performance Across Cohorts and Algorithms | — |
| 4.5 Predictors of Conversion and Their Stage Dependence | — |
| 4.6 Time to Conversion (Survival Analysis) | — |
| 4.7 A Parsimonious Clinical Risk Score | — |
| 4.8 Cognitive Decline Trajectories | — |
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
| Appendices *(optional)* | — |

---

## 4. LIST OF TABLES

| Table | Title | Page |
|---|---|---|
| 4.1 | Baseline characteristics by diagnostic group | — |
| 4.2 | Converters by outcome definition | — |
| 4.3 | ROC-AUC by model and cohort (5-fold CV, mean ± SD) | — |
| 4.4 | Top early predictors by cohort (permutation-importance rank) | — |
| 4.5 | Kaplan–Meier: probability of remaining dementia-free | — |

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
| 2 | Kaplan–Meier estimates of remaining dementia-free, MCI cohort, by APOE4 status | — |
| 3 | Cox proportional-hazards model of time to MCI → Dementia conversion | — |
| 4 | Stage-dependent early predictors (permutation importance) | — |

*Note: figures are labeled EDA-1…EDA-5 (exploratory) and 1…4 (results); renumber sequentially (1–9)
during final layout if your reviewers prefer a single series.*

---

### Author to complete
- [ ] First Reader (Thesis Advisor) name; Second Reader (Final Reader) name
- [ ] Degree-conferral month/year on title page and the exact degree name (Data Science vs. Predictive Analytics)
- [ ] Paste the abstract body under the ABSTRACT header (from `THESIS_Abstract_DRAFT.md`)
- [ ] Page numbers in TOC / List of Tables / List of Figures (auto-generate in Word after layout)
