# Exploratory Data Analysis — Figure Interpretations (Draft)

> Research-format narrative for the five exploratory figures (EDA-1 … EDA-5). Written to slot into
> **Results §4.1 (Participant Flow and Cohort Construction)** as the descriptive/EDA subsection, or to
> stand alone as a short "Exploratory Data Analysis" section preceding the modeling results. Every
> number below was recomputed directly from the analytic dataset (`data/pre_modelling_data.csv`,
> baseline = each participant's first visit, N = 2,131) and reflects the corrected CSF p-tau181
> (Methods §3.12). Figures are at 300 DPI in `notebooks/figures/`.
>
> Style note: values are reported as **median [interquartile range]** because most features are skewed
> (see EDA-2); group differences use the Mann–Whitney *U* test, appropriate for non-normal distributions.
> Replace figure numbers with your final sequential numbering during layout.

---

## 4.1.x Exploratory data analysis

Before modeling, the baseline cohort was characterized descriptively to (a) document the sample and its
representativeness, (b) verify data quality and the plausibility of feature distributions, and (c)
establish, in an unadjusted view, which measures separate diagnostic groups and eventual converters.
These exploratory analyses motivate the feature set and the stratified design used in the modeling
chapters and are reported here as five figures.

### Figure EDA-1. Cohort composition and follow-up

**What the figure shows.** Six panels summarize the baseline sample of 2,131 participants: distribution
of baseline diagnosis, age, education, sex, *APOE* ε4 allele count, and number of longitudinal visits
per participant.

**Observations.** The cohort is weighted toward the impaired end of the cognitive spectrum: 969
participants (45.5%) were classified as mild cognitive impairment (MCI) at baseline, 792 (37.2%) as
cognitively normal (CN), and 370 (17.4%) as dementia. Participants were older adults (median age 73.4
years, IQR 68.3–78.4) and highly educated (median 16 years, IQR 14–18), with a slight male majority
(1,132 men, 999 women; 53.1% male). *APOE* ε4 — the principal common-variant genetic risk factor for
late-onset Alzheimer's disease — showed the expected dose gradient: 1,197 participants (56.2%) carried
no ε4 allele, 740 (34.7%) carried one, and 194 (9.1%) carried two. Follow-up was longitudinal but
right-skewed: most participants contributed a small number of visits, with a long tail of well-followed
individuals (up to ~15 visits), which is the repeated-measures structure that motivates participant-level
cross-validation (Methods §3.6).

**Interpretation.** The over-representation of MCI is a design feature of ADNI, a convenience cohort that
preferentially enrolls individuals with existing cognitive concern rather than a community-based random
sample. The high educational attainment and the skew toward cognitively impaired volunteers both limit
generalization to the general population and are carried forward as explicit limitations (Discussion
§5.7). The visible ε4 dose gradient is a first, reassuring internal validity check: a well-established
biological risk factor is distributed in the sample as the literature predicts.

### Figure EDA-2. Univariate distributions of the modeling features

**What the figure shows.** Histograms of sixteen key cognitive, MRI-volumetric, and fluid/PET biomarker
features at baseline, used to assess shape, skew, floor/ceiling effects, and outliers prior to modeling.

**Observations.** Three distributional patterns are evident and each has a modeling consequence.
(i) **Ceiling and floor effects** in screening instruments: MMSE is strongly left-skewed and piles up at
its maximum of 30 (a well-known ceiling effect in a cohort with many unimpaired participants), while the
functional (FAQ) and clinical-staging (CDRSB) scales floor near zero, since the large CN subgroup is by
definition functionally intact. (ii) **Right-skew in the fluid biomarkers**: total tau (TAU) and,
following correction, phosphorylated tau (PTAU) are right-skewed with a median PTAU of ~24 pg/mL on the
physiologically correct 8–120 pg/mL scale — confirming that the p-tau field is no longer a rescaled
duplicate of total tau (Methods §3.12). (iii) **Bimodality in amyloid measures**: both CSF Aβ42 (ABETA)
and amyloid-PET (AV45) show two modes, consistent with the biologically meaningful split between
amyloid-negative and amyloid-positive individuals; the ABETA spike at the upper bound reflects the assay
truncation at its ceiling (values above the measurable range recorded at the limit). MRI volumes
(Hippocampus, Entorhinal, WholeBrain, FDG metabolism) are approximately symmetric.

**Interpretation.** The mixed and often non-normal shapes justify two analytic choices: reporting central
tendency as medians with IQRs rather than means ± SD for the descriptive tables, and standardizing all
features before any distance- or gradient-based model (KNN, SVM, MLP, logistic regression). The amyloid
bimodality foreshadows why amyloid measures carry discriminative signal, and the corrected PTAU scale is
verified here visually before it enters the models.

### Figure EDA-3. Feature separation by baseline diagnosis

**What the figure shows.** Box plots of nine core features across the three baseline diagnostic groups
(CN, MCI, Dementia), giving an unadjusted view of how strongly each measure tracks disease stage.

**Observations.** Every feature displays a monotone gradient across CN → MCI → Dementia, and the
magnitude of separation orders the modalities. **Global cognition and function separate most sharply:**
ADAS13 rises from a median of 10.0 [7–13] in CN to 16.7 [12–21] in MCI to 29.7 [24–35] in dementia;
CDRSB moves from 0.0 [0–0] to 1.5 [1–2] to 4.5 [3.1–5.0]; FAQ from 0.0 to 1.0 to 13.0. **Memory** shows
the same ordering (LDELTOTAL 13 → 6 → 0; RAVLT-immediate 45 → 33 → 23). **Structural and metabolic
imaging** separate more modestly but consistently (hippocampal volume 7,434 → 6,706 → 5,614 mm³;
entorhinal 3,845 → 3,488 → 2,738; FDG 1.3 → 1.2 → 1.1). **Molecular pathology** tracks stage in the
expected directions: CSF Aβ42 falls (1,310 → 854 → 630 pg/mL, i.e. greater amyloid deposition), while
amyloid-PET SUVR, total tau, and corrected p-tau all rise (PTAU 20.2 → 25.2 → 35.1 pg/mL). *APOE* ε4
carriage climbs in parallel (29% of CN, 48% of MCI, 64% of dementia).

**Interpretation.** The uniform, biologically coherent staging across every modality confirms that the
features carry genuine disease signal and are correctly oriented — a critical data-quality gate before
modeling. It also previews a central finding of the thesis: the *degree* of separation is stage-dependent
(cognitive and functional scales dominate the visible group differences), which motivates modeling the
cohorts separately rather than pooling them (Methods §3.4; Results §4.5). Importantly, box-plot
separation by *current* diagnosis is not the same as *predictive* value for *future* conversion — the
latter is examined in EDA-5 and is a substantially harder problem.

### Figure EDA-4. Correlation structure of the feature set

**What the figure shows.** A Pearson correlation heat map of 26 baseline features, revealing redundancy
and natural feature "blocks" that inform feature selection and the interpretation of model importances.

**Observations.** The matrix organizes into coherent blocks. A **cognitive block** is strongly
inter-correlated — MMSE–MOCA r = +0.76, ADAS13–MMSE r = −0.74, ADAS13–LDELTOTAL r = −0.70, and the two
composite scores mPACCdigit–mPACCtrailsB r = +0.98 (near-duplicates by construction). A **medial-temporal
structural block** groups hippocampus–entorhinal (r = +0.70) with midtemporal and fusiform volumes, and
whole-brain–ICV track together (r = +0.72). A **molecular block** links the amyloid measures inversely
(ABETA–AV45 r = −0.73, i.e. lower CSF Aβ42 with higher amyloid-PET, as expected) and the tau measures
tightly (TAU–PTAU r = +0.98). Cross-block, higher global cognition (ADAS13) correlates with lower glucose
metabolism (ADAS13–FDG r = −0.65) and with smaller hippocampal volume (r = −0.55). Age is only weakly
correlated with most features (e.g., AGE–Hippocampus r = −0.43), and education weaker still.

**Interpretation.** The block structure explains two downstream results. First, the very high within-block
correlations (mPACC composites r = 0.98; TAU–PTAU r = 0.98) mean the feature set contains substantial
redundancy, so that a parsimonious model can recover most of the signal — the empirical basis for the
seven-variable risk score (Results §4.7) and the feature-group ablation, in which removing any single
imaging or biomarker modality barely changes performance (Results §4.11). Second, the near-perfect
TAU–PTAU correlation is exactly the pattern that the earlier data corruption had produced *artifactually*;
its persistence here at the corrected p-tau scale confirms the two tau species are genuinely
co-regulated, not that the correction reintroduced the error (Methods §3.12). High collinearity also
cautions against over-interpreting the coefficient of any single feature within a correlated block.

### Figure EDA-5. Baseline features by eventual outcome (converter vs. stable)

**What the figure shows.** Overlaid, density-normalized histograms of eight leading features for
participants who were **non-demented at baseline**, split by whether they later met the confirmed
conversion-to-dementia definition (a worse stage sustained across ≥2 consecutive visits; Methods §3.4)
versus remained stable. This is the exploratory analog of the prediction task itself.

**Observations.** Among the 1,761 participants non-demented at baseline, future converters and stable
participants show clearly offset — though substantially overlapping — baseline distributions, and every
displayed feature differs at p < 10⁻³⁷ (Mann–Whitney *U*). Future converters started with worse function
(FAQ median 4.0 vs 0.0), worse memory (LDELTOTAL 3.0 vs 10.0), worse global cognition (ADAS13 19.7 vs
12.0; MOCA 21.0 vs 24.9), lower glucose metabolism (FDG 1.2 vs 1.3), smaller hippocampi (6,180 vs 7,203
mm³), and a markedly more Alzheimer's-like molecular profile (AV45 1.4 vs 1.1; CSF Aβ42 668 vs 1,168
pg/mL). Critically, however, the two distributions **overlap heavily** for every feature — no single
baseline measure cleanly partitions converters from non-converters.

**Interpretation.** This figure is the visual statement of both the promise and the difficulty of early
prediction. The consistent, highly significant shifts confirm that baseline multimodal information is
genuinely predictive of *future* decline — converters are already biologically and cognitively distinct
years before diagnosis. But the pervasive overlap explains why discrimination is good rather than perfect
in the impaired-spectrum cohorts (AUC ≈ 0.83–0.88) and why prediction from full cognitive normality is
genuinely hard (AUC ≈ 0.66–0.69; Results §4.4): the separating signal is real but distributed across many
correlated, individually imperfect markers, which is precisely the regime in which multivariable models
add value over any single biomarker. The offsets also preview the specific predictors that dominate the
modeling importances — function (FAQ), memory (LDELTOTAL), amyloid (AV45/ABETA), and metabolism (FDG).

---

### Notes for you (delete before submission)
- All medians/IQRs, correlations, and *p*-values above were recomputed from `pre_modelling_data.csv`
  (baseline = first visit per participant) and reflect the corrected PTAU. Numbers match the figures.
- The EDA-5 sample here is *non-demented at baseline* (1,761 participants) pooled; the modeling chapters
  report the CN and MCI cohorts separately (74 confirmed CN converters; 228 confirmed MCI converters).
  If a reviewer asks, the pooled EDA view and the stratified modeling view are consistent — the pooled
  count is simply the union across strata under the confirmed-conversion definition.
- No claims here exceed what was computed; there are no citations to add in this subsection (it is
  descriptive), though you may wish to cite the ADNI cohort-design reference and the *APOE*/ceiling-effect
  literature where flagged in the surrounding chapters.
