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
streams. _(Note: phosphorylated tau was excluded from the analyses reported here owing to a data
preprocessing error and is slated for restoration; see Methods §3.9.)_

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
