## Mathlib4 and Measure-Theoretic Probability {#sec:mathlib4_and_measure_theoretic_probability}

### What Is Mathlib4? A Short Orientation {#sec:what_is_mathlib4}

Mathlib4 [@mathlib2020] is the largest community-maintained library of formalized mathematics for Lean 4, containing over 60,000 verified declarations (as of March 2026) contributed by more than 770 mathematicians and computer scientists. It spans algebra, topology, analysis, number theory, category theory, and probability, and represents a multi-decade collaborative effort to digitize the foundations of modern mathematics into machine-checkable form.

For this project, Mathlib4 is the bedrock on which all {{total_topics}} FEP theorem sketches are constructed. Pinning the Lean 4 toolchain in `lean/lean-toolchain` and locking the Mathlib4 commit in `lean/lakefile.lean` guarantees reproducible compatibility with the verified formal-mathematics infrastructure. The pinned release used throughout this paper is **Mathlib4 `{{mathlib_tag}}`** with matching Lean toolchain `{{lean_toolchain}}`.

### Core Measure Theory and Stochastic Foundations {#sec:core_measure_theory}

The FEP is fundamentally a physics of probability measures. Mathlib4's measure-theory stack (`Mathlib.MeasureTheory`) supplies the formal substrate:

| Mathlib4 Type | Mathematical Object | FEP Usage |
|--------------|-------------------|-----------|
| `MeasurableSpace α` | $\sigma$-algebra on $\alpha$ | State/observation spaces |
| `Measure α` | Positive measure | Prior/posterior distributions |
| `Measure.volume` | Lebesgue measure | Reference measure |
| `AEStronglyMeasurable f μ` | $f$ is measurable a.e. | Integrability of free energy |
| `Measure.rnDeriv μ ν` | Radon-Nikodym derivative | Density ratios ($dq/dp$) |
| `∫ x, f x ∂μ` | Bochner integral | Expectations ($\mathbb{E}_q[f]$) |
| KL divergence (custom) | $\KL(q\|p)$ via `rnDeriv` + integral (native `klDiv` may land via SLT PRs) | Information geometry |

The compiler enforces that every operation respects its mathematical preconditions. You cannot compute $\KL(q\|p)$ without first proving absolute continuity ($q \ll p$) — an assumption routinely left implicit in the physics literature.

> **KL rows.** Several catalogue rows express Kullback–Leibler statements via `MeasureTheory.Measure.rnDeriv`, Bochner integrals, and `Real.log`, rather than a single named `klDiv` API. This keeps every proof explicit about absolute continuity and integrability. Discrete-support sketches use `Finset.sum` forms where that is the natural encoding.

### Key Mathlib4 Lemmas Referenced by the Catalogue {#sec:key_mathlib4_lemmas_referenced}

The {{total_topics}}-topic catalogue exercises a focused slice of Mathlib4's API surface. The table below lists the lemmas most frequently invoked across the compiling sketches, grouped by the Mathlib4 module family that exports them.

| Lemma / Definition | Mathlib4 Module | Representative FEP topics | Role in proof |
|-------------------|-----------------|--------------------------|---------------|
| `MeasureTheory.measure_union_le` | `MeasureTheory.Measure.MeasureSpace` | fep-001, fep-009, fep-014 | Countable subadditivity of measures (union bound) |
| `MeasureTheory.measure_mono` | `MeasureTheory.Measure.MeasureSpace` | fep-001, fep-009, fep-014 | Monotonicity under set inclusion |
| `MeasureTheory.measure_compl` | `MeasureTheory.Measure.MeasureSpace` | fep-002 | Complement rule for probability measures |
| `IsProbabilityMeasure.measure_univ` | `MeasureTheory.Measure.Typeclasses.Probability` | fep-002 | Probability measure sums to one |
| `Real.exp_pos` / `Real.exp_le_exp` | `Analysis.SpecialFunctions.Exp` | fep-010, fep-012, fep-031 | Strict positivity / monotonicity of `exp` |
| `Real.log_nonneg` / `Real.log_le_log` | `Analysis.SpecialFunctions.Log.Basic` | fep-011, fep-013, fep-024, fep-050 | Sign and monotonicity of `log` |
| `Real.sqrt_nonneg` | `Analysis.SpecialFunctions.Pow.Real` | fep-016, fep-038 | Non-negativity of square root |
| `Finset.sum_nonneg` / `Finset.sum_le_sum` | `Algebra.BigOperators.Group.Finset.Basic` + `Algebra.Order.BigOperators.Group.Finset` | fep-003, fep-007, fep-017, fep-039, fep-041 | Non-negativity / monotonicity of finite sums |
| `sq_nonneg` | `Algebra.Order.Ring.Basic` | fep-004, fep-016, fep-046 | $x^2 \geq 0$ for ordered rings |
| `mul_nonneg` | `Algebra.Order.Ring.Basic` | fep-021, fep-046, fep-049 | Product of non-negatives is non-negative |
| `mul_le_mul_of_nonneg_left` / `_right` | `Algebra.Order.Ring.Basic` | fep-031 | Monotonicity of multiplication |
| `mul_div_cancel₀` | `Algebra.Order.Field.Basic` | fep-030 | Cancellation in division (replaces wrong-arity `mul_div_cancel_left`) |
| `dist_triangle`, `dist_comm`, `dist_self` | `Topology.MetricSpace.Basic` | fep-018 | Symmetry, reflexivity, and triangle inequality |
| `inner_self_nonneg` (via `mul_self_nonneg`) | `Analysis.InnerProductSpace.Basic` / `…PiL2` | fep-004, fep-018, fep-038 | Inner product self-pairing non-negativity |
| `Measurable.const`/`add`/`mul`/`comp` | `MeasureTheory.MeasurableSpace.Basic` | fep-006, fep-014, fep-015 | Measurability of derived functions |
| `Matrix.transpose_transpose` | `LinearAlgebra.Matrix.Defs` | fep-025 | Transpose involution for NESS flows |
| `Finset.exists_min_image` / `_max_image` | `Data.Finset.Max` | fep-008, fep-023 | Existence of finite minimizers / maximizers |

A common LLM-facing pitfall is arity drift: `HermesExplainer` sometimes suggests `measure_nonneg μ s` when the correct invocation in `Mathlib4 {{mathlib_tag}}` is simply `zero_le _` (measures land in `ENNReal`, where non-negativity is by construction). Similarly, `mul_div_cancel_left` has been renamed to `mul_div_cancel₀` in recent Mathlib4 refactors; topic fep-030 uses the current spelling. Both patterns are common enough that `classify_failure_kind` reports them under `renamed_identifier` and `arity_mismatch` respectively in `VerifyResult`.

### Coverage Map and Dependency Graph {#sec:coverage_map_and_dependency_graph}

![Ecosystem maturity of the {{total_topics}}-topic catalogue against the pinned Mathlib4 `{{mathlib_tag}}` release. Every topic currently carries `mathlib_status: real`, i.e. its sketch compiles `sorry`-free under `lake env lean`; the `partial` and `aspirational` staging tiers are reserved for future rows that would require still-absent Mathlib infrastructure (native SDEs, Fokker–Planck operators, general-measure KL, Riemannian metric tooling). The catalogue draws on `MeasureTheory`, `Analysis.SpecialFunctions`, `Analysis.InnerProductSpace`, `LinearAlgebra.Matrix`, and `Topology.MetricSpace`.](../output/figures/mathlib_coverage.png){#fig:mathlib_coverage width=80%}

The {{total_topics}}-topic FEP formalization induces a dense dependency graph within Mathlib4. The tables below map the five formalization areas against the verified infrastructure they rely on.

#### Coverage by FEP Area {#sec:coverage_by_fep_area}

The table below summarizes the primary Mathlib4 dependency per FEP theoretical area, along with the qualitative depth of coverage and the number of catalogue rows that draw on each area.

| FEP Area | Primary Mathlib4 Modules | Coverage Depth | Representative Lemmas |
|----------|-------------------------|----------------|----------------------|
| FEP core (measure / probability foundations) | `MeasureTheory.Measure.rnDeriv`, `MeasureTheory.MeasurableSpace`, `Analysis.SpecialFunctions.Log.Basic` | Deep | `measure_union_le`, `measure_mono`, `measure_compl`, `IsProbabilityMeasure.measure_univ` |
| Active Inference (policy selection, EFE) | `Algebra.BigOperators.Group.Finset`, `Data.Fin`, `Data.Finset.Basic`, `Order.Basic` | Broad | `Finset.sum_nonneg`, `Real.log_le_log`, softmax non-negativity |
| Bayesian Mechanics | `LinearAlgebra.Matrix.Transpose`, `Data.Finset.Basic`, `MeasureTheory.Measure.MeasureSpace` | Moderate | `inner_self_nonneg`, `sq_nonneg`, Fisher metric skeleton |
| Information Geometry | `Analysis.InnerProductSpace.Basic`, `Topology.MetricSpace.Basic`, `Analysis.SpecialFunctions.Pow.Real` | Moderate | `inner_self_nonneg`, `dist_triangle`, `Real.sqrt_nonneg` |
| Thermodynamics (Landauer, free energy) | `Analysis.SpecialFunctions.Log.Basic`, `MeasureTheory.Integral.Bochner` | Moderate | `Real.exp_pos`, `Real.log_le_log`, positivity of $kT \ln 2$ |

This five-area-by-three-module map is the authoritative dependency index for the catalogue: every sketch's `import` lines resolve into at least one module from its assigned row. The Dynamics sub-family (NESS, Langevin, Brownian) inherits Bayesian Mechanics' modules plus `Topology.MetricSpace.Basic` and does not yet have a stand-alone module spine, because SDE types remain aspirational in Mathlib4 (see §\ref{sec:gap_analysis}).

#### FEP and Active Inference ({{areas.FEP.count}} + {{areas.ActiveInference.count}} topics across areas) {#sec:fep_and_active_inference_coverage}

| Component | Status | Mathlib4 Module | Dependent Topics |
|-----------|--------|----------------|-----------------|
| Measure spaces | real | `MeasureTheory.Measure.MeasureSpace` | fep-001, fep-002, fep-006, fep-009, fep-014, fep-015 |
| Probability measure type-classes | real | `MeasureTheory.Measure.Typeclasses.Probability` | fep-002 |
| Discrete probability / EFE | real | `Algebra.BigOperators.Group.Finset.Basic` + `Algebra.Order.BigOperators.Group.Finset` | fep-003, fep-007, fep-008, fep-017, fep-039, fep-041 |
| Measurability / DPI scaffolds | real | `MeasureTheory.MeasurableSpace.Basic` | fep-014, fep-015 |
| KL-style statements | real | `Real.log` + measure-level lemmas (native `klDiv` not in Mathlib at pin) | fep-014, fep-024 |
| Belief propagation | real | Factor products + message aggregation (`Finset.sum_nonneg`, `mul_nonneg`) | fep-007 |
| Bayesian update | real | `mul_nonneg`, `Finset.sum_nonneg` | fep-017, fep-034 |

#### Geometry, Mechanics, and Thermodynamics ({{areas.InfoGeometry.count}} + {{areas.BayesianMechanics.count}} + {{areas.Thermodynamics.count}} topics) {#sec:geometry_mechanics_thermodynamics_coverage}

| Component | Status | Mathlib4 Module | Dependent Topics |
|-----------|--------|----------------|-----------------|
| Inner product spaces | real | `Analysis.InnerProductSpace.Basic` | fep-004, fep-038 |
| Matrix transpose/skew | real | `LinearAlgebra.Matrix.Transpose` | fep-025 |
| Metric spaces | real | `Topology.MetricSpace.Basic` | fep-018 |
| Exponential/log | real | `Analysis.SpecialFunctions.Exp` | fep-010, fep-020, fep-031 |
| Brownian motion | ○ Aspir.| Custom stochastic integration (future limit) | — |
| Langevin dynamics (SDE) | ○ Aspir. | Custom drift-diffusion SDE types | — |
| Non-Equilibrium SS (PDE)| ○ Aspir. | Custom divergence-free flow | — |

### The Import Pattern Strategy {#sec:the_import_pattern_strategy}

Every catalogue sketch begins with targeted Mathlib4 imports that constrain the formalization to specific, verified mathematical topologies.

```lean
-- Target: Information Geometry (fep-004, fep-038)
import Mathlib.Analysis.InnerProductSpace.Basic

-- Target: Bayesian Mechanics / NESS (fep-025)
import Mathlib.LinearAlgebra.Matrix.Transpose

-- Target: Thermodynamics (fep-031, fep-050)
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Order.Ring.Lemmas  -- required for mul_le_mul_of_nonneg_left
```

This selective-import strategy prevents the LLM from hallucinating non-existent API surfaces by grounding its generation window in the lemmas that each module actually exports. Crucially, `import` statements must appear at the top of the file, before any `namespace` declaration. Topics fep-042 and fep-045 initially failed compilation because Hermes emitted `import` statements inside a namespace block; in both cases the fix was a mechanical move of the imports to the file preamble.

### A Worked Example: KL Divergence and the ELBO {#sec:worked_example_kl_elbo}

The Evidence Lower Bound (ELBO) is the central object of variational free energy. For a generative model $p(x, z)$ and a variational posterior $q(z)$, the ELBO is:

\begin{equation}\label{eq:mathlib_elbo}
\mathrm{ELBO}(q) \;=\; \mathbb{E}_{q(z)}\!\bigl[\log p(x, z) - \log q(z)\bigr] \;=\; \log p(x) - \KL\!\bigl(q(z) \,\|\, p(z \mid x)\bigr).
\end{equation}

Equivalently, the variational free energy $F$ is the negative ELBO:

\begin{equation}\label{eq:mathlib_vfe_kl}
F(q) \;=\; \mathbb{E}_{q}\!\bigl[\log q(z) - \log p(x, z)\bigr] \;=\; \KL\!\bigl(q(z) \,\|\, p(z \mid x)\bigr) - \log p(x).
\end{equation}

The following Lean 4 sketch encodes the KL divergence over a finite state space using the discrete form (which avoids the absolute-continuity side conditions required by the Radon-Nikodym formulation):

```lean
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Algebra.BigOperators.Order

open Finset

namespace FEPExamples

/-- Discrete KL divergence between two distributions over a finite state space. -/
noncomputable def klDivDiscrete {α : Type*} [Fintype α] [DecidableEq α]
    (q p : α → ℝ) : ℝ :=
  ∑ x, q x * Real.log (q x / p x)

/-- Discrete ELBO for a generative model `logJoint` and variational posterior `q`. -/
noncomputable def elboDiscrete {α : Type*} [Fintype α]
    (logJoint : α → ℝ) (q : α → ℝ) : ℝ :=
  ∑ z, q z * (logJoint z - Real.log (q z))

/-- Non-negativity of KL for valid probability distributions (sketch). -/
theorem klDivDiscrete_nonneg {α : Type*} [Fintype α] [DecidableEq α]
    (q p : α → ℝ)
    (hq : ∀ x, 0 ≤ q x) (hp : ∀ x, 0 < p x)
    (hqsum : ∑ x, q x = 1) (hpsum : ∑ x, p x = 1) :
    0 ≤ klDivDiscrete q p := by
  -- Gibbs' inequality; full proof requires Jensen's inequality over Finset.sum.
  -- Mathlib provides convex_on_log and Finset.inner_mul_le_norm_mul_norm,
  -- but a sorry-free discrete Gibbs proof is a 20-30 line exercise.
  sorry

end FEPExamples
```

The theorem above is stated in a sketch; the catalogue's fep-014 row instead supplies *sorry-free* measure-theoretic ingredients used in standard KL/DPI proofs (`fep014_measure_mono`, `fep014_measure_union_le`, `fep014_dpi_measurable`, `fep014_compl_mass_le`, `fep014_measure_nonneg`), leaving the discrete Gibbs proof above as a pedagogical aspirational target.

### Gap Analysis: What Mathlib4 Does Not Yet Provide {#sec:gap_analysis}

Despite its breadth, Mathlib4 at the pinned release still leaves substantive gaps for a complete FEP formalization. The project deliberately downgrades sketches that would otherwise rely on unavailable infrastructure to sorry-free skeletons rather than chasing aspirational proofs behind a `sorry` hole.

| Missing Infrastructure | Impact on FEP formalization | Workaround in this catalogue |
|-----------------------|----------------------------|------------------------------|
| Native `klDiv` for general measures | fep-014, fep-024 use finite-support proxies | Discrete KL via `Finset.sum` and `Real.log` |
| Full Radon-Nikodym with sigma-finiteness automation | Continuous free energy proofs are skeletal | State theorems under explicit $q \ll p$ hypothesis |
| Itô / Stratonovich stochastic integral | Langevin dynamics (fep-025) lack SDE semantics | Replace $dW_t$ with deterministic drift skeleton |
| Fokker-Planck PDE for NESS | Non-equilibrium steady states (fep-025) | Prove algebraic identities on skew generator |
| Martingale convergence in $L^p$ | Ergodic steady-state arguments | Assume stationarity as hypothesis |
| Variational inequalities for PDE | Mean-field dynamics in large populations | Restrict to finite agent counts |
| Entropy for continuous measures (differential entropy) | fep-050 Landauer bound is discrete-only | Prove $kT \ln 2 > 0$ directly |
| Wasserstein distance and optimal transport | Information-geometric flows on $\mathcal{W}_2$ | Use $L^2$ metric as surrogate |
| Riemannian manifold ↔ Fisher information bridge | Fisher metric as pullback of a Riemannian metric tensor under the statistical-manifold embedding | State Fisher information as a bilinear form on tangent vectors (finite-parameter); skip the manifold-level equivalence |

**Aspirational gap — Fisher information on Riemannian manifolds.** The full information-geometric identification of Fisher information with a Riemannian manifold's metric tensor requires measure-theoretic integration of tensor-valued fields over a smooth manifold, and that combination is not yet composable in Mathlib4 at the pinned release. Mathlib4 carries `Geometry.Manifold.*` and `MeasureTheory.Integral.Bochner` in isolation, but the bridge — pullback of the Bochner integral of $\partial_i \log p \, \partial_j \log p$ along a smooth statistical embedding — has no off-the-shelf composable API. Catalogue rows fep-004 and fep-038 therefore encode the Fisher metric as a bilinear form on a finite-parameter tangent space (no manifold charts), which is sufficient for the local-geometry claims in Bayesian Mechanics but omits the global Riemannian structure.

These gaps are not obstacles to the present paper — they define its scope. Each compiling sketch in the catalogue is a verified claim inside the boundary of the pinned Mathlib4 release, and each aspirational extension is explicitly flagged for future Mathlib4 PRs.
