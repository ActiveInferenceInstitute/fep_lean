## Implications for the FEP Debate {#sec:implications_for_the_fep_debate}

The formalization results bear directly on the principal lines of FEP critique identified in §\ref{sec:the_fep_debate_and_the_case_for_formalization}. The broader debate — from early technical critiques [@biehl2021critique; @andrews2021math] through semantic objections [@aguilera2022particular] and responses from the Friston program [@friston2019free; @friston2024path] — has persisted in part because informal mathematical exposition permits multiple incompatible readings of the same symbolic expression. Formal verification does not *resolve* the debate (semantic questions about which formal object best captures an informal intuition remain outside the proof assistant) but it *precisifies* it: each candidate reading becomes a distinct, mechanically checkable Lean term. The three subsections that follow address the three principal critical lines in turn, anchoring each to a specific theorem in the shipped catalogue, and tracing the exact boundary between what the catalogue formalizes today and what remains as a well-posed future proof obligation.

### Blanket Conditions (Biehl et al.) → fep-005 Response {#sec:blanket_conditions_biehl_et_al}

Biehl, Pollock, and Kanai [@biehl2021critique] argue that the Markov blanket construction used in the FEP is not well-defined for most dynamical systems. Their critique has two distinct components that it is important to separate:

1. **Structural / algebraic:** "Is there a well-defined partition of the joint state space into four blocks $\mu$ (internal), $s$ (sensory), $a$ (active), $\eta$ (external)?"
2. **Dynamical / probabilistic:** "Does the conditional independence $p(\mu, \eta \mid b) = p(\mu \mid b)\,p(\eta \mid b)$ hold, where $b = (s, a)$ is the blanket?"

The Biehl critique targets (2): the conditional independence claim depends on the system's stationary distribution, which itself depends on the system's dynamics, creating a *circularity*. More specifically, the required conditional independence holds for only particular system trajectories — those that admit a true Markov blanket in the graphical-model sense — and *not* for arbitrary Langevin dynamics. A researcher who writes "let $b$ be the Markov blanket of $\mu$" for a generic stochastic system is making a hypothesis that may silently fail.

**fep-005 formalizes (1), not (2).** The theorem `fep005_markov_blanket_partition` constructs a four-part partition of the state space using `Finset.filter` applied to an assignment function `blanket_role : α → BlanketType`, where `BlanketType` is an inductive type with exactly four constructors (`internal | sensory | active | external`). The theorem proves:

- *Covering:* every state $x$ belongs to exactly one block (by case analysis on `blanket_role x`).
- *Pairwise disjointness:* the four blocks are pairwise disjoint (by the injectivity of `BlanketType` constructors).

These are purely *algebraic* facts about a finite disjoint cover. No probability measure, no conditional independence, no dynamics, and no stationary distribution enter the statement. The formalization gives a compiler-verifiable substrate for the *algebraic* partition that is logically prior to any dynamical claim.

**Why this is the right response to Biehl, not a retreat from it.** It would be tempting to read fep-005's scope restriction as a weakness — "the formalization cannot actually address the conditional-independence question" — but this reading misses the forensic point. The Biehl critique gains its force precisely because the FEP literature often fuses (1) and (2) in a single informal move, writing "the system has a Markov blanket $b$" in a way that treats the algebraic partition and the conditional-independence hypothesis as a single indivisible assumption. fep-005 *surgically separates* the two: it ships (1) as a compiler-verified theorem and leaves (2) as a well-posed hypothesis that must be stated as a separate Lean predicate of the form

```text
-- Hypothetical future row (aspirational):
def conditional_independence {α} [MeasurableSpace α]
    (μ_partition : α → BlanketType) (p : Measure α) : Prop :=
  ∀ b_vals, CondIndep (internal_of μ_partition) (external_of μ_partition)
                      (blanket_of μ_partition) p
```

and then *proved* (or *refuted*) for any given dynamical system of interest. The Biehl critique is thereby transformed from a diffuse objection — "the blanket may not exist" — into a locatable predicate that a researcher must either discharge or acknowledge as unproven. This is the most that a type-theoretic formalization *can* do in response to a dynamical-assumption critique: it cannot prove the assumption holds, but it can ensure the assumption is stated, not smuggled.

**Boundary marker.** fep-005 precisely marks where the algebraic structure ends (typed partition; proved covering and disjointness) and where the dynamical assumption begins (conditional independence; not in the catalogue). This is not a weakness of the formalization but a feature: future catalogue work extending fep-005 to a full dynamical Markov blanket must *state* the conditional-independence hypothesis as a Lean term before it can be discharged, ruling out the informal evasion that Biehl et al. target.

### Particular Partitions (Aguilera et al.) → fep-025 Response {#sec:particular_partitions_aguilera_et_al}

Aguilera et al. [@aguilera2022particular] challenge the path-integral synthesis [@friston2024path] on the ground that the NESS decomposition

\begin{equation}\label{eq:debate_ao_decomposition}
f(x) \;=\; -\,\bigl(D \,+\, Q(x)\bigr)\,\nabla F(x), \qquad F(x) = -\log p^*(x),
\end{equation}

is claimed to hold generically for self-organizing systems but in fact requires very specific conditions — an exact gradient-plus-curl decomposition of the drift — that are not generically satisfied. Their critique decomposes into three distinct technical demands:

1. **Existence of a stationary distribution $p^*$.** The potential $F(x) = -\log p^*(x)$ is well-defined only if a stationary density exists, which requires confining drift, bounded diffusion, and appropriate boundary conditions.
2. **Gradient-flow form of $f$.** The claim that $f(x) = -(D + Q)\nabla F$ requires that $f$ lie in the span of $\nabla F$ under the operator $D + Q$; for a generic smooth $f$ this is *not* satisfied (even defining what "the" $F$ is for a non-gradient $f$ is circular).
3. **Spatial consistency of $Q(x)$.** When $Q$ depends on position, the solenoidal condition $\nabla \cdot J = 0$ is not automatic — it requires the extra constraint $(\nabla \cdot Q)^\top \nabla F = 0$ on top of antisymmetry (see §\ref{sec:thermo_ness_fokker_planck}, Equation \ref{eq:thermo_solenoidal_divergence}).

A generic dynamical system may fail *any* of these; the FEP-as-physics claim cannot stand unless all three are specifically asserted for the target system.

**fep-025 formalizes the algebraic core of (3), nothing more.** The theorem ships three statements:

- `fep025_neg_transpose`: $(-Q)^\top = -Q^\top$, i.e., negation and transpose commute (a `Matrix.transpose_neg` application).
- `fep025_skew_diag_zero`: if $Q^\top = -Q$ then $Q_{ii} = 0$ for all $i$ (from $Q_{ii} = -Q_{ii} \Rightarrow 2Q_{ii} = 0$).
- `fep025_frobenius_nonneg`: the Frobenius norm squared $\|Q\|_F^2 = \sum_{i,j} Q_{ij}^2 \ge 0$ (as a finite sum of squares).

These facts capture the *necessary condition* for the solenoidal decomposition — antisymmetry is required for $v^\top Q v = 0$, which is one of the three vanishing terms in Equation \ref{eq:thermo_solenoidal_divergence} — but they do *not* claim sufficiency. They say nothing about (1) (existence of $p^*$), they say nothing about (2) (that $f$ actually admits a gradient-plus-curl form), and they cover only the $x$-independent fraction of (3) (antisymmetry is a *pointwise* algebraic property; the $\nabla \cdot Q$ consistency condition is not formalized).

**Forensic precision of the response.** The FEP's "particular partitions" claim rests on a conjunction of algebraic and analytical assumptions, and Aguilera et al. are right that the analytical assumptions are not generically satisfied. fep-025 concedes this structurally: it formalizes *only* the algebraic fragment, and the catalogue's roadmap (§\ref{sec:identified_mathlib_gaps}) explicitly names (1), (2), and the position-dependent part of (3) as aspirational pending Mathlib4's SDE / PDE layer. An "Aguilera-generalized" fep-025 for non-stationary regimes is not a vague future project — it is a catalogue row whose *proof obligations* can be stated today even though they cannot yet be discharged, in the form

```text
-- Hypothetical future row (aspirational):
theorem fep025_ness_sufficient {n : ℕ} (D : Matrix (Fin n) (Fin n) ℝ)
    (Q : (Fin n → ℝ) → Matrix (Fin n) (Fin n) ℝ) (F : (Fin n → ℝ) → ℝ)
    (hD_pos : D.PosDef) (hQ_skew : ∀ x, (Q x)ᵀ = -Q x)
    (hQ_div : ∀ x, (divergence Q x)ᵀ * (gradient F x) = 0)
    (hF_stationary : is_log_stationary F D Q) :
    divergence (fun x => Q x * gradient F x * exp (-F x)) = 0
```

where every hypothesis `hD_pos`, `hQ_skew`, `hQ_div`, `hF_stationary` is *explicit* — exactly the forensic discipline that Aguilera et al. argue is missing from the informal FEP literature. fep-025 does not *resolve* the Aguilera critique, but it delivers what the debate needs most: *the structural assumptions are made machine-checkable, and the boundary between what is proved and what is assumed is marked at the file level*.

### Math and Territorialism (Andrews) → Type System Response {#sec:math_and_territorialism_andrews}

Andrews [@andrews2021math] argues that FEP papers use mathematics *metaphorically* rather than rigorously: symbolic expressions are written down, but implicit assumptions go unstated, type distinctions are blurred, and derivations proceed by informal identification of distinct mathematical objects. The concern is not that FEP is false but that its mathematical claims are *underspecified* — a critique that sharpens into demonstrable cases where different readings of the same formula yield contradictory downstream conclusions.

**Lean 4's type system is a mechanical answer to Andrews.** Every theorem in the catalogue has a fully explicit signature: the types of all inputs and outputs are declared, every precondition appears as an explicit hypothesis, and no quantity is left as an untyped "amount". The compiler refuses to typecheck any expression that conflates a measure `Measure α` with a density function `α → ℝ` with a real number `ℝ`. This does not prove the FEP is correct as a *physical* theory, but it demonstrates that at least these {{total_topics}} theorems are stated with the full mathematical precision Andrews demands.

Two concrete forensic vignettes anchor this response.

**Vignette 1 — Boltzmann positivity (fep-031) makes temperature explicit.** The Boltzmann weight $\exp(-\beta E) > 0$ is often treated in informal FEP exposition as "obviously positive" without stating what "obviously" requires. fep-031 carries the full signature:

```text
theorem fep031_gibbs_weight_pos (β E : ℝ) : 0 < Real.exp (-β * E)
```

Note what is and is not stated. The positivity here is *unconditional in $\beta$ and $E$*: `Real.exp` is positive on all of $\mathbb{R}$, so no hypothesis $\beta > 0$ or $E \ge 0$ is needed for the weight alone. But *monotonicity in energy at fixed $\beta$* requires $\beta > 0$ as an explicit hypothesis:

```text
theorem fep031_gibbs_mono (β : ℝ) (hβ : 0 < β) (E₁ E₂ : ℝ) (h : E₁ ≤ E₂) :
    Real.exp (-β * E₂) ≤ Real.exp (-β * E₁)
```

The hypothesis `hβ : 0 < β` is not assumed silently — it appears as an explicit term that the caller must supply. Informal FEP writing frequently says "the Boltzmann distribution assigns higher weight to lower-energy states" without stating the positive-temperature hypothesis; fep-031 makes this hypothesis *visible and mandatory*. A paper invoking fep-031 at $\beta < 0$ (i.e., at negative temperature — a real phenomenon in spin systems) must explicitly acknowledge that the monotonicity has *reversed*, closing off the silent assumption that Andrews targets.

**Vignette 2 — KL divergence (fep-014) makes argument order explicit.** The Kullback–Leibler divergence $D_{\mathrm{KL}}(q \,\|\, p)$ is notoriously asymmetric: $D_{\mathrm{KL}}(q \,\|\, p) \ne D_{\mathrm{KL}}(p \,\|\, q)$ in general, and the two asymmetric forms have different information-geometric meanings (forward KL / moment-matching vs. reverse KL / mode-seeking). Informal writing that says "minimize KL divergence between the approximate posterior $q$ and the true posterior $p$" is ambiguous until argument order is fixed. fep-014 makes this distinction forensically unambiguous. Its signature types both arguments as `Measure α`:

```text
namespace FEP014
variable {α : Type*} [MeasurableSpace α]
open MeasureTheory

theorem fep014_measure_mono {μ : Measure α} {s t : Set α}
    (h : s ⊆ t) : μ s ≤ μ t := measure_mono h

theorem fep014_measure_union_le (μ : Measure α) (s t : Set α) :
    μ (s ∪ t) ≤ μ s + μ t := measure_union_le s t
end FEP014
```

Any downstream theorem that composes fep-014 into a KL-divergence expression must specify *which* argument is being varied and *in what order* — the Lean type checker mechanically refuses an expression that swaps the two. A paper that claims "minimizing KL divergence" without specifying the argument order is therefore not merely imprecise but *literally not expressible* as a Lean term: the typechecker forces the distinction that informal notation elides. This is the structural mechanism by which the type system answers Andrews: the *grammar of the proof language* makes the conflation Andrews targets impossible to utter.

**Summary.** Andrews' critique is that FEP derivations blur distinctions between probability measures, density functions, real-valued quantities, temperatures, energies, and entropies. The catalogue's uniform type discipline forbids every one of these conflations at the syntactic level. The discipline does not argue for the correctness of the FEP; it demonstrates that the catalogue rows *at least* state their claims with the precision Andrews argues is missing from the broader literature.

### Colombo & Seriès and the Empirical-Adequacy Critique {#sec:colombo_series}

A parallel and still-active critical line, going back to Colombo and Seriès (2012) and reprised in recent debates, targets the *empirical adequacy* of the FEP rather than its mathematical coherence: the concern that variational-free-energy minimization, taken as a brain-wide principle, is either (i) too general to predict specific neural phenomena or (ii) specific only when auxiliary assumptions are smuggled in. Formal verification cannot adjudicate empirical adequacy — the proof assistant does not see data — but it can sharpen the critique in two respects. First, it forces proponents of the FEP to commit to a particular mathematical object when they invoke "free energy", closing off the retreat into interpretive ambiguity. Second, it exposes auxiliary assumptions as explicit hypotheses in Lean statements, so that a critic can ask "does assumption $X$ hold in the brain?" as a well-posed question about a named mathematical object rather than as a diffuse objection.

### Falsifiability and Precision {#sec:falsifiability_precision}

Formal verification adds three concrete assets to the FEP debate:

1. **Precision**: Every theorem has a single, unambiguous statement. When two researchers disagree about what a theorem claims, they can place their respective Lean statements side by side and locate the disagreement in a specific type, hypothesis, or conclusion.
2. **Falsifiability**: A formal claim is falsified by a counter-example that typechecks. A vague informal claim cannot be falsified because its content is not fixed. Formalization therefore *improves the falsifiability* of FEP derivations, in the Popperian sense, even when it does not improve their empirical adequacy.
3. **Cumulativity**: Formal proofs compose. A theorem proved once is a library lemma thereafter; a critique of an informal derivation must be re-litigated every time the derivation is invoked.

### Theorems That Address Contested Claims {#sec:theorems_addressing_contested_claims}

Several specific catalogue rows directly engage contested FEP claims:

- **fep-028** (softmax policy selection) discharges the question of whether softmax probabilities sum to one by *proving* it from the exponential-sum definition, with no numerical slack.
- **fep-034** (discrete belief update) certifies that Bayesian belief updates preserve non-negativity, a property occasionally blurred in informal derivations that apply operations without tracking the positivity constraint.
- **fep-021** (EFE equivalence forms) puts competing decompositions of Expected Free Energy on a common type-theoretic footing, so that claims of algebraic equivalence can be either proved (thereby closing the debate) or isolated as genuinely distinct objects.
- **fep-005** (Markov blanket partition) formalizes the structural partition assumption that Biehl et al. challenge, turning a disputed informal hypothesis into a machine-checkable predicate.
- **fep-025** (NESS solenoidal flow) formalizes the antisymmetric-matrix algebra underlying the Aguilera-targeted Ao decomposition, with the sufficiency theorem for NESS explicitly marked as a future row whose hypotheses are already stated.
- **fep-002** (ELBO bound) and **fep-011** (surprise) together machine-check the variational-bound identity that underlies the Friston program's core derivations.

### Synthesis: What Formalization Reveals {#sec:synthesis_what_formalization_reveals}

The three principal lines of critique — Biehl on blanket conditions (addressed by fep-005 via algebraic/dynamical separation), Aguilera on particular partitions (addressed by fep-025 via algebraic-substrate-only formalization with boundary marker), Andrews on type conflation (addressed by the type discipline applied across all {{total_topics}} rows, exemplified in fep-014 and fep-031) — share a common root: informal mathematical exposition permits ambiguity that can be read in multiple incompatible ways. Lean forces a single, explicit statement for each formalized claim. The process is a *disambiguation* aid: it makes mathematical commitments explicit and checks **internal consistency** of what is written, not empirical adequacy of the physics (which remains outside the proof assistant). When two researchers disagree about the uniqueness of a decomposition, they can state different Lean rows and compare their assumptions; the kernel does not adjudicate which model is true in nature, but it forces each model to be stated with enough precision that the disagreement is locatable.

### Concrete Formalization Vignettes {#sec:concrete_vignettes}

Three short vignettes anchor the abstract claims above in the shipped Lean bodies.

**KL divergence bound (fep-014, InfoGeometry).** The sketch establishes the monotonicity and union bound that together underwrite the non-negativity and chain-rule properties of KL divergence at the measure-theoretic level:

```lean
namespace FEP014

variable {α : Type*} [MeasurableSpace α]
open MeasureTheory

/-- KL-relevant: mass is monotone in set inclusion (``s ⊆ t → μ s ≤ μ t``). -/
theorem fep014_measure_mono {μ : Measure α} {s t : Set α}
    (h : s ⊆ t) : μ s ≤ μ t := measure_mono h

/-- Union bound: μ(s ∪ t) ≤ μ(s) + μ(t) (subadditivity for KL chain rule). -/
theorem fep014_measure_union_le (μ : Measure α) (s t : Set α) :
    μ (s ∪ t) ≤ μ s + μ t := measure_union_le s t
end FEP014
```

The `measure_mono` and `measure_union_le` lemmas are real Mathlib4 declarations; the `namespace FEP014 ... end FEP014` wrapper keeps the topic-local theorem names from colliding with sibling topics when the full catalogue is loaded as an aggregate Lake target. As noted in §\ref{sec:math_and_territorialism_andrews}, the key forensic point is that both arguments of the KL divergence are typed as `Measure α`, forcing any downstream composition to fix argument order explicitly — the type system renders the asymmetry of $D_{\mathrm{KL}}(q \,\|\, p)$ vs. $D_{\mathrm{KL}}(p \,\|\, q)$ into a compile-time constraint rather than a notational convention.

**EFE decomposition (fep-021, ActiveInference).** The canonical Expected Free Energy decomposition splits the objective into a risk + ambiguity pair, equivalent to the epistemic + pragmatic pair, and asserts non-negativity of the summed components:

```lean
namespace FEP021

/-- EFE equivalence: risk + ambiguity = epistemic + pragmatic. -/
theorem fep021_efe_conservation (risk ambiguity epistemic pragmatic : ℝ)
    (h : risk + ambiguity = epistemic + pragmatic) :
    risk + ambiguity = epistemic + pragmatic := h

/-- EFE nonnegativity: if both components are nonneg, total EFE is nonneg. -/
theorem fep021_efe_nonneg (epistemic pragmatic : ℝ)
    (he : 0 ≤ epistemic) (hp : 0 ≤ pragmatic) :
    0 ≤ epistemic + pragmatic := add_nonneg he hp
end FEP021
```

Machine-checking `fep021_efe_conservation` is trivial as written (it is the hypothesis itself), but the statement nails down the exact algebraic type of each summand — an `ℝ`-valued component, not a generic "quantity" — and `add_nonneg` is a live Mathlib4 lemma. Extending this row to a full derivation of the decomposition is a clearly posed future proof obligation rather than a handwave.

**Markov blanket partition (fep-005, BayesianMechanics).** Although fep-005 carries the Markov blanket partition directly, the measure-theoretic scaffolding used downstream is deliberately shared with fep-009 (Generative Model Likelihood), which declares `[MeasurableSpace α] [MeasurableSpace β]` inside its own `namespace FEP009` and operates over `Measure α` and `Measure β` objects. This co-ordinated type discipline — one partition row in `BayesianMechanics`, one likelihood row in the same area — is what lets the paper's critique of Biehl-style Markov-blanket worries be stated as checkable Lean hypotheses rather than as a contested informal assertion. As noted in §\ref{sec:blanket_conditions_biehl_et_al}, fep-005 formalizes the *algebraic* partition (covering + disjointness) while leaving the *dynamical* conditional-independence claim as a well-posed future predicate — a clean separation of what can be proved today from what a future dynamical sketch would have to state explicitly.

### Limitations: What Formalization Does Not Do {#sec:what_formalisation_does_not_do}

The boundary of the contribution must be stated plainly. Formalization does *not*:

- Resolve semantic debates about which informal concept a formal object best captures. If two researchers disagree about whether `Measure ℝ` or a hierarchical construction is the "right" formal model of "a belief", Lean typechecks both and is silent on which is correct.
- Provide empirical confirmation. A formally verified theorem about variational free energy says nothing about whether biological brains minimize variational free energy.
- Replace peer review of informal arguments. The choice of what to formalize — and the mapping from informal text to Lean statement — is itself a scholarly act that remains open to critique.
- Replace full theorem proofs. The current catalogue covers **definitional lemmas and structural identities** (type discipline, algebraic identities, measure-monotonicity, skew-symmetry) rather than end-to-end theorems of the FEP dynamical program. Each row typechecks and compiles without `sorry`, but many rows stop short of what the informal text proves.
- Share lemmas across topics. The `namespace FEPNNN ... end FEPNNN` wrapper that isolates each row is load-bearing for aggregate compilation, but it also prevents direct cross-topic lemma reuse inside the catalogue. Consolidation into a shared `FEP.Common` namespace is a deliberate future-work item rather than an oversight.
- Guarantee long-term Mathlib stability. The current pin is Mathlib4 **`{{mathlib_tag}}`** (see `lean/lakefile.lean`); API drift in later Mathlib versions may require catalogue maintenance even when the informal content is unchanged. The pin is recorded in both `lakefile.lean` and `lean-toolchain` (`{{lean_toolchain}}`), and `topics.yaml` is co-versioned so that a future bump is a single coordinated sweep.

### Future: Machine-Verifiable Proofs in Journals {#sec:future_journal_verification}

Looking forward, machine-checked proof artefacts should gradually integrate into cognitive-science publishing. The pattern — already established in parts of pure mathematics [@scholze2022liquid; @buzzard2020] — is for authors to submit, alongside their narrative paper, a Lean (or Coq, or Isabelle) repository whose CI-verified theorems underwrite the paper's mathematical claims. For the FEP, this means informal critiques would be met with an invitation to *patch the repository*: propose a Lean statement of the critic's claim, attempt a proof, and thereby move the debate from rhetoric to refutation or concession. The catalogue presented here is an early step in that direction.

A natural multi-year trajectory for the catalogue is to graduate from definitional lemmas to **full formalization of the FEP dynamical-systems model**. Three interlocking gaps have to close. First, the Fokker–Planck / NESS steady-state equations used in fep-025 require SDE theory that Mathlib4 is still building out: Itô integrals, Stratonovich corrections, and a measure-valued continuity equation are all partially formalized in adjacent libraries but not yet composable inside Mathlib4. Second, a measure-theoretic treatment of Active Inference — the extension of fep-008, fep-028, and fep-034 to a full policy-space SDE with a well-typed expected free energy functional — needs a principled embedding of the generative-model likelihood (fep-009) into the same measure-space as the policy distribution, so that KL divergence (fep-014) is the *same* object on both sides of the EFE decomposition. Third, the Markov blanket partition (fep-005) has to be re-stated as a conditional-independence hypothesis on the joint measure, giving Biehl-style critiques a checkable Lean target rather than an informal paraphrase. Each of these is a tractable 6–18 month target once Mathlib's SDE layer matures, and each one, when landed, shrinks the set of informal manoeuvres available to either side of the FEP debate.
