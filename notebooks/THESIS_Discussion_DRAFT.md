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
