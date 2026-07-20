## The `sorry` Mechanism and Formalization Maturity {#sec:the_sorry_mechanism_and_formalization_maturity}

### What `sorry` Does {#sec:what_sorry_does}

In Lean 4, `sorry` is a special tactic that admits any proof goal without actually proving it. The compiler then proceeds as if the goal were proven, while flagging the result as incomplete. Although convenient during incremental formalization, its presence signifies a fundamental failure to achieve mathematical verification.

```lean
-- This compiles, but Lean emits a warning: "declaration uses 'sorry'"
theorem expected_free_energy_decomposition (π : Policy) :
    EFE π = risk π + ambiguity π := by
  sorry  -- Proof to be completed
```

Crucially, `sorry` is *not* silently ignored. A file containing `sorry` compiles successfully but does not constitute a verified proof — analogous to a mathematical paper that states a lemma "without proof" and then uses it in subsequent arguments. Lean emits a warning at declaration time and attaches an axiom of the form `declaration uses 'sorry'` to the resulting constant; `#print axioms` reveals the unfilled hole.

### Three Maturity Levels {#sec:three_maturity_levels}

The taxonomy supports three maturity tags for formalization rows. **All {{maturity.real}} of {{total_topics}} shipped catalogue rows are tagged `real`** — every row in `config/topics.yaml` carries `mathlib_status: real`, every sketch compiles under the pinned Mathlib4 release (`{{mathlib_tag}}`), and every proof body is sorry-free. The `partial` (currently {{maturity.partial}}) and `aspirational` (currently {{maturity.aspirational}}) tags exist purely to stage future topics that are not yet in the catalogue (for example SDE-dependent rows awaiting native Mathlib4 stochastic integration). Each tag captures a distinct epistemic commitment, illustrated below with canonical Lean examples.

#### Level 1 — `real` (Fully Verified, Sorry-Free) {#sec:level_real}

A `real` sketch compiles under the pinned Lean 4 toolchain with zero occurrences of the `sorry` tactic. Every proof obligation is discharged by Mathlib4 lemmas, decision procedures, or explicit term construction. Topic **fep-001** is a canonical example:

```lean
import Mathlib.MeasureTheory.Measure.MeasureSpace

namespace FEP001
open MeasureTheory

theorem fep001_measure_mono {α : Type*} [MeasurableSpace α]
    (μ : Measure α) {s t : Set α} (h : s ⊆ t) :
    μ s ≤ μ t := by
  exact measure_mono h

theorem fep001_measure_union_le {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (s t : Set α) :
    μ (s ∪ t) ≤ μ s + μ t := by
  exact measure_union_le s t

end FEP001
```

This declaration references only `measure_mono` and `measure_union_le` from `Mathlib.MeasureTheory.Measure.MeasureSpace`, both of which exist in the pinned Mathlib4 release. No axioms are introduced beyond those of Mathlib4 itself, and `#print axioms fep001_measure_union_le` returns only the standard dependency set (`propext`, `Classical.choice`, `Quot.sound`).

#### Level 2 — `partial` (Structurally Correct With One or Two Holes) {#sec:level_partial}

A `partial` sketch states a theorem whose signature is type-correct and whose outer tactic structure is sound, but which contains one or two isolated `sorry` placeholders standing in for subgoals that depend on missing Mathlib4 infrastructure or on technical analytic lemmas outside the current scope. The surrounding proof *uses* the holes non-trivially; it is not a blanket `sorry`.

```lean
import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace FEP014Partial
open MeasureTheory

/-- Gibbs' inequality: KL divergence is non-negative. The outer structure is
    Jensen's inequality applied to the convex function `-log`; the hole is
    the appeal to convexity in the discrete setting. -/
theorem kl_nonneg_partial {α : Type*} [Fintype α]
    (q p : α → ℝ)
    (hq : ∀ x, 0 ≤ q x) (hp : ∀ x, 0 < p x) :
    0 ≤ ∑ x, q x * Real.log (q x / p x) := by
  have hlog : ∀ x, Real.log (q x / p x) ≤ q x / p x - 1 := by
    intro x
    sorry  -- Mathlib4: Real.log_le_sub_one_of_pos requires positive argument
  sorry  -- Close out via linear combination of hlog and the constraint ∑ q = 1
end FEP014Partial
```

Under current policy, this sketch would be downgraded to a structural lemma with a weaker statement rather than shipped as `partial`.

#### Level 3 — `aspirational` (Signature Only) {#sec:level_aspirational}

An `aspirational` sketch states the theorem signature a formalization *aspires* to and defers the entire proof to a single `sorry`. The role is purely documentary: it records a target for future Mathlib4 PRs or project-internal lemma proofs.

```lean
import Mathlib.MeasureTheory.Measure.MeasureSpace

namespace FEPAspirational

/-- Non-equilibrium steady state: the stationary distribution of a Langevin
    dynamical system with skew-symmetric drift decomposes into symmetric
    (dissipative) and antisymmetric (circulating) flows. Aspirational — requires
    Mathlib4 infrastructure for stochastic differential equations. -/
theorem ness_decomposition_aspirational : True := by
  sorry

end FEPAspirational
```

### The Zero-`sorry` Policy {#sec:zero_sorry_policy}

We strictly enforce a zero-sorry maturity standard for all {{total_topics}} catalogue Lean bodies (orientation §\ref{sec:appendix_comprehensive_formalisms_overview}; per-topic Lean sketches and display-math equation ids juxtaposed in §\ref{sec:appendix_b_full_topic_lean_catalogue}). Under current policy, `config/topics.yaml` lists no `partial` or `aspirational` rows: every topic is tagged `mathlib_status: real` with a compiling sketch.

In the rendered manuscript, the count of {{maturity.real}} real rows is sourced directly from the `mathlib_status: real` field in `config/topics.yaml`, and this is the only acceptable state.

### The Compilation Gate: How Zero-Sorry Is Enforced {#sec:compilation_gate}

The zero-sorry policy is not a documentation convention — it is mechanically enforced at pipeline time by four distinct checks:

1. **Per-topic sketch compilation.** `scripts/03_lean_verify_only.py`, and the Gauss Sessions stage (`GaussRunner` + `LeanVerifier`) when workflows are enabled, iterate over every row in `config/topics.yaml`, wrap the `lean_sketch` string in a temporary file with `import Mathlib`, and invoke `lake env lean`. Per-row outcomes appear in logs or in `output/reports/run_*/verification_manifest.json`; the headline rate is reported in §`04e`.
2. **Sorry scan.** `scripts/03_lean_verify_only.py` loads each sketch and runs a textual scan (`re.search(r"\bsorry\b", sketch)`) before compilation. A positive hit raises a `CatalogueIntegrityError` and halts the sweep.
3. **Post-compile inspection.** `LeanVerifier.verify_sketch` sets `has_sorry=True` whenever the sketch text contains `sorry`, and the aggregate `verification_manifest.json` records the field. The manuscript's `verify.*` template variables propagate this aggregate outcome into the rendered PDF.
4. **Aggregate-file `grep` gate.** The CI step runs the literal command
   ```bash
   grep -n 'sorry' lean/FepSketches/fep_all.lean lean/FepSketches/Basic.lean
   ```
   against the concatenated batch files `fep_all.lean` and `Basic.lean`. Any non-comment `sorry` match (outside `--` or `/-` … `-/`) fails the build. This catches sketches that slip past per-row checks but introduce `sorry` when combined into the aggregate compilation.

In addition, `tests/test_fep_topics.py` asserts that every row of `config/topics.yaml` has `mathlib_status: real`, so any attempt to land a `partial` or `aspirational` row in the shipped catalogue fails at CI time.

The upshot is that a row can only be promoted to `mathlib_status: real` after all gates pass: syntactic (no literal `sorry` in per-row or aggregate files), semantic (Lean accepts the term), compositional (no unresolved `#print axioms` entries beyond Mathlib4's base set), and policy-level (`test_fep_topics.py` enforces `real` as the only shipped label).

#### ✓ Real (Fully Verified) {#sec:real_fully_verified}

A catalogue sketch is **real** when all of the following checkable conditions hold:

- The fragment compiles without `sorry` (zero proof gaps in the sketch).
- All imported constants and lemmas are present in the pinned Mathlib4 version; no local axioms or admitted theorems are used in the sketch.
- No definitions or theorems in the sketch rely on opaque fixtures representing missing mathematics.

**Catalogue count (YAML `mathlib_status: real`): {{maturity.real}} of {{total_topics}} topics.** The Lean statement in each row is machine-checked; the natural-language `title` remains the research-facing claim and may call for stronger formalizations as Mathlib4 coverage expands (see §\ref{sec:maturity_assessment_of_the_mathlib_ecosystem}). Sketches vary in depth: some topics prove multiple substantive properties (for example fep-028 defines softmax and proves both non-negativity and normalization; fep-050 defines the Landauer bound $kT \ln 2$ and proves its positivity; fep-005 constructs a four-part partition with a disjoint cover), while others anchor simpler structural lemmas such as measure monotonicity or exponential identities. All sketches are unique — no two topics share identical proof bodies — and each uses a Mathlib4 API that is idiomatic for its domain. Sketches typecheck and anchor the topic in Mathlib4, but they do not by themselves guarantee that every natural-language catalogue title is fully proved at its maximum statement strength.

![Proof maturity distribution across all {{total_topics}} topics. Under current policy all topics are `real` (sorry-free, compiling sketches). The donut chart shows the zero-sorry policy in effect; the taxonomy retains `partial` and `aspirational` categories for future rows that may require incomplete formalizations as Mathlib4 grows.](../output/figures/sorry_distribution.png)

### Migration From `partial` to `real`: A Worked Example {#sec:migration_partial_to_real}

Promotion to `real` is a mechanical story on this codebase: missing imports, Mathlib4 lemma renames between releases, or arity mismatches surface as `lake env lean` errors and are fixed in small diffs. Topic **fep-031** is a canonical import-fix case — the monotonicity step needs `mul_le_mul_of_nonneg_left` from `Mathlib.Algebra.Order.Ring.Lemmas`:

```lean
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Algebra.Order.Ring.Lemmas

theorem fep031_exp_monotone (a b c : ℝ) (ha : 0 ≤ a) (h : b ≤ c) :
    a * Real.exp b ≤ a * Real.exp c := by
  exact mul_le_mul_of_nonneg_left (Real.exp_le_exp_of_le h) ha
```

Before the extra import, the same proof block fails with an unknown identifier for `mul_le_mul_of_nonneg_left`. Similar migrations in the catalogue have included lemma renames (for example `mul_div_cancel_left` → `mul_div_cancel₀`) and hypothesis-arity fixes at `measure_nonneg` call sites. Headline catalogue health is summarized by the compile rate `{{compile_rate.total}}` after each verifier sweep (§\ref{sec:quantitative_execution_metrics}), not by ad-hoc per-area failure counts in prose.

### Maturity by FEP Area {#sec:maturity_by_area}

Under current policy every shipped row is `mathlib_status: real`. If a future Mathlib4 bump breaks individual sketches, failures are expected to cluster along the *import graph* (shared `MeasureTheory` or `Analysis.SpecialFunctions` paths) rather than along narrative areas alone. Per-area headline rates are still reported via the `compile_rate_area_*` variables in `manuscript_vars.yaml` whenever the verifier can attribute rows cleanly to an area.

### Why Aspirational Proofs Are Rejected {#sec:why_aspirational_proofs_are_rejected}

Some pipelines tolerate "aspirational" sketches that consist of `sorry` gaps as structural blueprints. This project explicitly rejects that approach for four reasons:

1. **Illusion of formalization.** Allowing `sorry` gaps creates a false impression of verified physics and undermines the core purpose of an interactive theorem prover.
2. **Type-level dishonesty.** Natural-language ambiguity is often merely transferred into an ill-founded local axiom, bypassing the rigor of formal mathematics rather than engaging with it.
3. **Strict truthfulness.** We maintain a zero-hallucination constraint: unproven statements are not allowed in the final verified corpus.
4. **Migration discipline.** Rejecting `aspirational` forces the pipeline to confront Mathlib4 gaps head-on, either by narrowing the claim to a provable sub-statement or by flagging the gap in §\ref{sec:gap_analysis} for a future Mathlib4 PR. An `aspirational` bucket would let gaps persist silently.
