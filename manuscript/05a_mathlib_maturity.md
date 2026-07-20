# Discussion: Ecosystem Maturity and Formalization Impacts {#sec:discussion}

Integrating LLM commentary (Hermes) with native Lean 4 compilation establishes a workflow for frontier theory: curated sketches in YAML, structured validation prose, and reproducible execution-integrity compiler traces. Pipeline **success** encompasses catalogue loading, environment validation, and artifact generation; native compilation of every sketch is a separate gate (§\ref{sec:native_lean_4_compilation_and_zero_direct_verification}). This section examines the implications for Mathlib, the strict execution-integrity mandate, and formal verification in theoretical neuroscience.

## Maturity Assessment of the Mathlib Ecosystem {#sec:maturity_assessment_of_the_mathlib_ecosystem}

The catalogue schema defines a **three-level maturity taxonomy** for Lean bodies:

1. **`real`** — the sketch compiles via `lake env lean` against the pinned toolchain and contains no `sorry`. This is the only level shipped in the current catalogue.
2. **`partial`** — the sketch compiles with at most 50% `sorry` coverage (staging concept for future drafts where infrastructure is close but not complete).
3. **`aspirational`** — the sketch is written as a structural skeleton with `sorry` placeholders, exercising the target statement shape without a compile guarantee (staging concept for prospective topics pending Mathlib4 infrastructure).

**Only `real` is shipped.** All {{total_topics}} catalogue rows carry **`mathlib_status: real`**; the `partial` and `aspirational` tags are reserved as staging states for in-progress work that has not yet passed the compilation gate. Each shipped sketch is a **topic-aligned, `sorry`-free** Mathlib lemma or definition (see `scripts/catalogue_sketches.py`); native `lake env lean` checks use the verifier preamble in `src/verification/lean_verifier.py`.

- **Scope**: Sketches are deliberately compact (e.g. measure nonnegativity, finset extrema, log identities, discrete updates). They typecheck and anchor the topic in Mathlib; they are **not** a guarantee that every natural-language catalogue title is fully proved at that statement strength.
- **Interpretation caveat**: A `real`-tagged sketch is a machine-checked *specification fragment*, not a complete end-to-end theorem for the informal FEP statement it anchors. The maturity label refers to Mathlib support for the *types and operations* invoked, not to the proof depth of the informal claim.
- **Separation of concerns**: The catalogue deliberately separates (a) informal natural-language statements, (b) Lean 4 sketch bodies, and (c) the Mathlib ecosystem that supports them. A mature Mathlib dependency enables sketch construction; a successful `lake env lean` pass provides the compilation gate; Hermes commentary documents the mathematical reading.

### Coverage by Area {#sec:coverage_by_area}

The five catalogue areas map onto distinct regions of Mathlib4 with varying degrees of infrastructure support:

| Area | Topics | Primary Mathlib modules | Coverage assessment |
|------|--------|------------------------|---------------------|
| FEP | {{areas.FEP.count}} | `MeasureTheory.Measure`, `Analysis.SpecialFunctions.Log`, `Algebra.BigOperators` | Strong: measure spaces, log/exp identities, and finset sums are mature |
| Active Inference | {{areas.ActiveInference.count}} | `Data.Finset`, `Algebra.BigOperators`, `MeasureTheory.Measure` | Strong for discrete models; continuous policy spaces lack SDE infrastructure |
| Information Geometry | {{areas.InfoGeometry.count}} | `Analysis.InnerProductSpace`, `Analysis.Calculus`, `Topology.MetricSpace` | Partial: inner products and calculus are available; Riemannian manifold API (`Geometry.Manifold`) exists but Fisher metric formalizations do not |
| Bayesian Mechanics | {{areas.BayesianMechanics.count}} | `Analysis.SpecialFunctions.Pow`, `Order.Monotone`, `Analysis.Calculus.Deriv` | Strong for algebraic structure; PDE-level solenoidal/dissipative decomposition is bespoke |
| Thermodynamics | {{areas.Thermodynamics.count}} | `Analysis.SpecialFunctions.Log`, `Algebra.BigOperators`, `Data.Finset` | Strong for discrete thermodynamic identities; continuous entropy functionals require integration theory beyond current Mathlib |

### Module-Level Maturity and Compilation Outcomes {#sec:module_level_maturity}

Beyond the area-level view, the catalogue exposes a *module-level* dependency gradient. The table below groups the {{total_topics}} topics by their primary Mathlib4 dependency; empirical success rates are summarized by **`{{compile_rate.total}}`** and the per-area `compile_rate_area_*` keys in `manuscript_vars.yaml` (see §\ref{sec:aggregate_metrics}). First-time Mathlib setup: **`scripts/_maint_bootstrap_lean_toolchain.sh`** or repo **`scripts/00_setup_environment.py --project fep_lean`**.

| Mathlib4 module cluster | Topics using it | Typical constructs invoked | Observed compile rate |
|-------------------------|-----------------|-----------------------------|-----------------------|
| `MeasureTheory.Measure.*` | fep-001, fep-002, fep-006, fep-009, fep-015, fep-022, fep-027, fep-036, fep-042 | `Measure`, `IsProbabilityMeasure`, `measure_mono`, `measure_union_le` | ~9/9 mature — highest confidence cluster |
| `Algebra.BigOperators.*` | fep-003, fep-007, fep-017, fep-019, fep-033, fep-034, fep-039, fep-041, fep-047 | `Finset.sum`, `Finset.sum_nonneg`, `Finset.sum_le_sum` | ~9/9 mature — discrete-sum identities are rock solid |
| `Analysis.SpecialFunctions.*` | fep-010, fep-011, fep-012, fep-013, fep-016, fep-024, fep-026, fep-030, fep-031, fep-032, fep-035, fep-037, fep-040, fep-044, fep-050 | `Real.log`, `Real.exp`, `Real.rpow` | Strong — rare failures limited to elaborator timeouts on `positivity` |
| `Data.Finset.*` / `Order.Bounds.*` | fep-005, fep-008, fep-023, fep-028, fep-046 | `Finset.filter`, `Finset.exists_min_image`, `Finset.Nonempty` | Strong — the main risk is subtle `Decidable` instance drift |
| `Analysis.InnerProductSpace.*` | fep-004, fep-038 | `inner`, inner product positive-semidefiniteness | Adequate — formalized Fisher metric is missing; sketches encode the *positive-semidefiniteness anchor*, not the metric itself |
| `Analysis.Calculus.*` | fep-043 | `deriv`, `HasDerivAt` | Weaker — critical-point analyses that need `fderiv` on manifolds are not yet available |
| `LinearAlgebra.Matrix.*` | fep-025 | `Matrix.transpose`, skew-symmetry | Adequate — algebraic fragments compile; the PDE content that motivates them does not |
| `Topology.MetricSpace.*` | fep-018 | metric space axioms, geodesic anchors | Adequate — Riemannian manifold layer exists but is thinly populated |
| `Analysis.Convex.*` | fep-029 | convex combinations, Jensen-style inequalities | Adequate — Bregman divergence as a generic construct is absent |
| `Analysis.SpecialFunctions.Pow.*` | fep-016, fep-020, fep-032, fep-044 | `Real.rpow`, monotonicity of powers | Strong — but `rpow` elaboration is occasionally slow |

The pattern is unambiguous: **discrete, algebraic, and measure-theoretic modules are maximally mature**, while **continuous-time stochastic analysis, Riemannian geometry, and PDE infrastructure are comparatively under-populated**. This mirrors Mathlib4 priorities: the community has invested heavily in algebra, number theory, and measure-theoretic probability, while SDE theory and differential geometry remain growth areas (see §\ref{sec:identified_mathlib_gaps}).

These gap predictions align with the live verification results from `{{verify.run_id}}` (§\ref{sec:live_verification_error_taxonomy}): topics relying on discrete and algebraic clusters (`Finset`, `BigOperators`, `OrderedAlgebra`) compiled cleanly in both the original and Hermes-refined paths — never encountering genuine Mathlib gaps. Topics requiring stochastic analysis or Riemannian geometry (`MeasureTheory.Measure.Prod`, metric-space geodesics) required curator-level YAML improvements (e.g., `open MeasureTheory` directives, correct Mathlib API call signatures) to achieve clean Hermes-refined compilation, confirming the gap taxonomy as a predictor of formalization robustness: Mathlib maturity at the module cluster level is a reliable leading indicator of which sketches survive LLM pass-through intact versus requiring manual intervention.

The two most stable regions for current FEP work are **Thermodynamics (`{{compile_rate.by_area.Thermodynamics}}` topics land cleanly on `Analysis.SpecialFunctions.*`, `Algebra.BigOperators.*`, and `Data.Finset.*`)** and the **measure-theoretic core of FEP (most topics route through the mature `MeasureTheory.Measure.*` cluster)**. These are the anchors against which less-mature areas should be benchmarked.

### The Mathlib Frontier for Deeper Formalization {#sec:mathlib_frontier_20_percent}

Although all {{total_topics}} shipped sketches compile, roughly a fifth of the catalogue achieves that compile status by reducing the informal claim to a discrete or algebraic surrogate rather than stating it over its native continuous, stochastic, or Riemannian object. Those rows sit on a short list of *frontier* Mathlib4 constructs that are not yet native:

- **Stochastic differential equations (SDE) and Fokker–Planck operators for non-equilibrium steady-state (NESS)** — needed for continuous-time Langevin dynamics (fep-020), gradient flows on beliefs (fep-032), fluctuation–dissipation (fep-037), and solenoidal/dissipative decompositions (fep-025, fep-049).
- **Riemannian manifold metric tensor (Fisher information metric)** — needed for fep-004 and fep-038; the inner-product anchor exists but the metric tensor on a statistical manifold does not.
- **Measure-theoretic conditional independence and conditional entropy** — needed for hierarchical models (fep-027), exploration-bonus information gain (fep-041), and mutual-information-based objectives.

**As Mathlib4's SDE layer matures, these frontier topics are tractable 6–18 month targets** for deeper formalization — each is bottlenecked on a well-defined Mathlib4 primitive rather than on an FEP-specific obstruction, so their upgrade from discrete surrogate to full statement will track the community's stochastic-analysis and differential-geometry roadmaps (see §\ref{sec:maturity_roadmap}).

### Identified Mathlib Gaps {#sec:identified_mathlib_gaps}

The catalogue's strict exclusion of incomplete mathematical mappings highlights the boundaries of contemporary proof assistants. We identify **five critical Mathlib gaps**, each with a precise impact on catalogue rows and a characterizable shape for the missing infrastructure. These are ordered by the number of catalogue rows they unlock and by the conceptual weight they carry in the FEP literature.

1. **Native `klDiv`.** Mathlib4 has `MeasureTheory.Measure.rnDeriv` (the Radon–Nikodym derivative) and a mature Bochner integration theory, but no dedicated `klDiv : Measure α → Measure α → ℝ≥0∞` function with an accompanying lemma library. Currently, KL must be assembled *ad hoc* from `rnDeriv` + `lintegral` + `log` — a four-step construction whose constants, measurability hypotheses, and absolute-continuity side-conditions must be re-derived each time it appears. Concretely, for $q \ll p$ one must instantiate
   \begin{equation}\label{eq:gap_kl_rnderiv}
   \KL[q \,\|\, p] \;=\; \int_{\Omega} \log\!\left(\frac{dq}{dp}\right) dq \;=\; \int_{\Omega} \left(\frac{dq}{dp}\right)\log\!\left(\frac{dq}{dp}\right) dp,
   \end{equation}
   together with positivity (Gibbs), the chain rule $\KL[q \,\|\, p] = \KL[q \,\|\, r] - \mathbb{E}_q[\log\, dp/dr]$, and the data-processing inequality — every single time. With a native `klDiv` API, theorems **fep-001, fep-002, fep-014, fep-024, fep-026** would simplify dramatically: each would reduce from a bespoke log-identity proof to a one- or two-line application of library lemmas (`klDiv_nonneg`, `klDiv_eq_zero_iff`, `klDiv_chain`), collapsing tens of lines of Radon–Nikodym bookkeeping per topic. The SLT project [@lean_slt2026] has an active PR towards this API; its merge is the single highest-leverage event on the roadmap.

2. **Conditional entropy and mutual information.** $H(X\mid Y)$ and $I(X;Y)$ are not in Mathlib4 as first-class objects (as of `{{mathlib_tag}}`). Concretely, the definitions
   \begin{equation}\label{eq:gap_cond_entropy_mutual}
   H(X \mid Y) \;=\; -\sum_{x,y} p(x,y)\log p(x\mid y), \qquad I(X;Y) \;=\; \KL[p(x,y) \,\|\, p(x)p(y)] \;=\; H(X) - H(X\mid Y)
   \end{equation}
   require a coupled treatment of joint measures, marginals, and conditional kernels that Mathlib4 has as scattered primitives but not as a unified information-theoretic layer.    This gap directly blocks **fep-021** — the decomposition
   \begin{equation}\label{eq:gap_efe_risk_ambiguity}
   \EFE(\pi) \;=\; \underbrace{\KL[q(o_\tau\mid\pi)\,\|\,p(o_\tau)]}_{\text{risk}} \;+\; \underbrace{\mathbb{E}_{q(o_\tau\mid\pi)}\,H[p(o_\tau\mid s_\tau)]}_{\text{ambiguity}} \;=\; \text{pragmatic} + \text{epistemic},
   \end{equation}
   whose epistemic term *is* the mutual information $I(s_\tau;\, o_\tau \mid \pi)$ — and **fep-041**, whose exploration bonus is precisely the non-negativity claim $I(s;o\mid\pi) \geq 0$. Without `condEntropy` and `mutualInfo`, these rows must be stated at the level of finite-sum log identities rather than as instances of a general theorem.

3. **Itô stochastic integrals and Brownian motion.** `SDE.lean` is not in Mathlib4. The Langevin equation at the heart of FEP path-integral formulations,
   \begin{equation}\label{eq:gap_langevin_sde}
   dx \;=\; -\nabla F(x)\, dt \;+\; \sqrt{2\beta^{-1}}\, dW_t,
   \end{equation}
   requires the Itô integral $\int_0^t \sigma(X_s)\, dW_s$ and its isometry $\mathbb{E}\!\left[\left(\int_0^t \sigma\, dW\right)^{\!2}\right] = \mathbb{E}\!\left[\int_0^t \sigma^2\, ds\right]$ for rigorous formalization. Mathlib4 supplies the martingale prerequisites (`MeasureTheory.Martingale`, optional stopping) but not the Itô construction itself. This gap blocks **fep-020** (Langevin sampling) from being promoted beyond its current algebraic-step form, and secondarily constrains **fep-032** (gradient flows on beliefs) and **fep-037** (fluctuation–dissipation) to finite-step statements.

4. **Fokker–Planck operator.** The Fokker–Planck PDE governing the evolution of the density $p(x,t)$ under the Langevin equation above,
   \begin{equation}\label{eq:gap_fokker_planck_ness}
   \partial_t p \;=\; \nabla\!\cdot\!\big((D\,\nabla F)\, p\big) \;-\; \nabla\!\cdot\!\big((Q\,\nabla F)\, p\big),
   \end{equation}
   has no Mathlib4 formalization of the underlying differential operator $\mathcal{L} = \nabla\!\cdot\!\big(D(\cdot) + Q(\cdot)\big)$ with $D$ symmetric positive-semidefinite (dissipative) and $Q$ skew-symmetric (solenoidal). While `MeasureTheory.Measure.Lebesgue` and vector-calculus fragments exist, the divergence operator acting on measure-density pairs is not assembled. This blocks full NESS statements (**fep-025**) and entropy-production identities (**fep-049**) from being promoted to their native Fokker–Planck form; both currently ship as algebraic anchors at the level of skew-symmetric matrices.

5. **Fisher information metric as a Riemannian metric.** `Geometry.Manifold.SmoothManifoldWithCorners` and `Analysis.InnerProductSpace` exist in Mathlib4, but the construction of a *statistical manifold* $\{p_\theta\,:\,\theta \in \Theta\}$ as a smooth manifold equipped with the Fisher metric
   \begin{equation}\label{eq:gap_fisher_metric}
   g_{ij}(\theta) \;=\; \mathbb{E}_{x \sim p_\theta}\!\left[\frac{\partial \log p_\theta(x)}{\partial \theta^i}\,\frac{\partial \log p_\theta(x)}{\partial \theta^j}\right]
   \end{equation}
   remains aspirational — the chart data, the smoothness of $\theta \mapsto p_\theta$, and the positive-definiteness of $g$ must be assembled manually. This blocks **fep-004, fep-018, fep-038** from reaching their full geometric form: without the Fisher metric as a first-class `RiemannianMetric` instance, natural-gradient and geodesic claims reduce to inner-product-positive-semidefiniteness anchors rather than full statements on the information manifold.

**Implication for the Mathlib community.** These gaps identify concrete formalization targets. A native `klDiv`, a conditional-entropy / mutual-information layer, an Itô integral, a Fokker–Planck operator, or a Fisher–Riemannian metric would each unlock multiple catalogue topics for stronger formalizations. The five gaps are moreover *nested by dependency*: `condEntropy` and `mutualInfo` build on `klDiv`; Fokker–Planck builds on Itô; Fisher–Riemannian builds on the inner-product-space infrastructure plus a statistical-manifold chart layer. The pipeline's modular structure means new Mathlib infrastructure can be adopted per-topic without restructuring the catalogue; each upgrade is a one-sketch edit plus a regeneration of `scripts/catalogue_sketches.py`.

An adjacent, lower-urgency gap is the **generalized Radon–Nikodym theorem for non-σ-finite pairs** (relevant to singular priors and Bayesian nonparametric models such as fep-046). Mathlib4 covers the σ-finite case; the non-σ-finite extension remains folklore. Closing this gap would unblock empirical-Bayes and stick-breaking formalizations currently stated over discrete approximations, but — unlike the five gaps above — it would not affect a cluster of core FEP theorems.

### A 6–12 Month Maturity Roadmap {#sec:maturity_roadmap}

Given current Mathlib4 development velocity and the specific gaps above, a tractable 6–12 month roadmap for FEP-relevant maturity looks as follows. Each phase is keyed to a concrete Mathlib4 or SLT artefact and to the catalogue rows it upgrades; where an upstream PR is not yet available, we route through the SLT project's shim namespace rather than block the catalogue.

1. **Months 1–3 — `klDiv` adoption.** Adopt the SLT project's `FormalML.klDiv` shim (not upstream yet; tracking PR `#NNN` in the SLT repository) as a namespaced alias, so catalogue rows can transparently retarget to the upstream `MeasureTheory.klDiv` once it merges. Refactor **fep-001, fep-002, fep-014, fep-024, fep-026** to call `klDiv_nonneg`, `klDiv_eq_zero_iff`, and the chain rule directly; the four- to five-step Radon–Nikodym constructions collapse into single-line applications. Expected payoff: five topics shrink substantially, and the `log`-identity lemmas they currently encode become *corollaries* of the `klDiv` API rather than bespoke proofs. Resolves five topics.
2. **Months 3–6 — conditional entropy and mutual information.** PR a `condEntropy` definition to Mathlib4 via `ProbabilityTheory.condEntropy`, built directly on `klDiv` and the existing `ProbabilityTheory.kernel` / `Measure.condKernel` machinery. Derive `mutualInfo` as the symmetric difference $I(X;Y) = H(X) - H(X\mid Y)$ or, equivalently, as `klDiv` of the joint against the product of marginals. Refactor **fep-021** (EFE = risk + epistemic = pragmatic + ambiguity; epistemic term is the mutual information $I(s_\tau; o_\tau \mid \pi)$) and **fep-041** (exploration bonus as the non-negativity $I(s;o\mid\pi) \geq 0$) to instantiate these. This phase does not require new measure-theoretic foundations — it is a natural follow-on to SLT's KL work, and it resolves the EFE epistemic term that is the most-cited informal identity in the Active Inference literature.
3. **Months 6–9 — Itô integral prototype.** Prototype an Itô stochastic integral on the real line using Lean 4's existing `MeasureTheory.Martingale` infrastructure as the discrete-time scaffolding, together with `Measure.restrict` for the elementary simple-process construction, then pass to the $L^2$ limit via the Itô isometry. The prototype need only be strong enough to state $dX_t = b(X_t)\, dt + \sigma(X_t)\, dW_t$ with $b,\sigma$ Lipschitz; this is sufficient for **fep-020** (Langevin sampling) to be promoted from its current algebraic-step form to a genuinely continuous-time statement, and it supplies the substrate needed by fep-032 and fep-037 in subsequent phases. Resolves the Langevin and diffusion sketches.
4. **Months 9–12 — Fokker–Planck operator.** Formalize the Fokker–Planck operator $\mathcal{L} = \nabla\!\cdot\!\big(D(\cdot) + Q(\cdot)\big)$ via the existing `MeasureTheory.Measure.Lebesgue` infrastructure and the divergence theorem, specializing the Kolmogorov forward equation to the Langevin setting above. Use it to upgrade **fep-025** (solenoidal NESS) and **fep-049** (entropy production) from skew-symmetric-matrix anchors to full solenoidal/dissipative decompositions, and to give fep-027 (hierarchical NESS) its native PDE form. Resolves the NESS and entropy-production sketches.

This roadmap is deliberately *conservative*: it prioritises infrastructure that benefits multiple catalogue rows and aligns with existing Mathlib4 community workstreams rather than proposing bespoke FEP-only extensions. The five critical gaps in §\ref{sec:identified_mathlib_gaps} are nested by dependency — `condEntropy`/`mutualInfo` on top of `klDiv`, Fokker–Planck on top of Itô, Fisher–Riemannian on the inner-product layer — so each phase reduces the remaining gap surface for the next. The Fisher–Riemannian metric (gap 5) is deliberately deferred beyond the 12-month horizon: it requires a statistical-manifold chart layer that is substantial in its own right, and its impact is concentrated in three catalogue rows rather than dispersed across the catalogue.

### Comparison to Other Mathlib4 Formalization Projects {#sec:comparison_other_formalisation_projects}

FEP formalization is not Mathlib4's first encounter with a physically motivated theory. The comparison below contextualises its maturity against other flagship formalization efforts:

| Project | Domain | Mathlib4 maturity of core dependencies | Depth reached |
|---------|--------|-----------------------------------------|---------------|
| **Liquid Tensor Experiment** [@scholze2022liquid] | Condensed mathematics / homological algebra | Category theory, homological algebra: *very mature* by 2022 | Full theorem proved (Scholze's challenge met) |
| **Perfectoid spaces** [@buzzard2020] | p-adic geometry / number theory | Topology, completions, nonarchimedean fields: *mature* | Definitions formalized; theorems a work-in-progress |
| **PhysLean / HEPLean** [@toobysmith2024] | High-energy physics / tensor index notation | Linear algebra, tensor products: *mature*; physics-specific: *bespoke* | Index notation and contractions formalized |
| **Lean SLT** [@lean_slt2026] | Statistical learning theory | Measure theory: *mature*; KL/entropy: *active development* | Foundational definitions; `klDiv` PR in progress |
| **FEP Lean (this work)** | Free Energy Principle / Active Inference | Measure theory, big operators, special functions: *mature*; SDE / Riemannian geometry: *weak* | {{total_topics}}-sketch catalogue; sketches are `sorry`-free specification fragments |

Two lessons follow. First, successful Mathlib4 formalizations of contested physical theories (Liquid Tensor Experiment, perfectoid spaces) depended on *pre-existing* maturity in their core algebraic infrastructure; the FEP catalogue sits in a similar position for its *discrete* and *measure-theoretic* core, but not yet for its *stochastic-dynamical* frontier. Second, the catalogue's current depth (specification fragments rather than end-to-end proofs) tracks the early stages of other large formalization efforts — the Perfectoid and Liquid Tensor projects began as definition-and-statement skeletons before the proofs accumulated.
