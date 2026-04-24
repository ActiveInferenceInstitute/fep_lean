# Topics Reference — FEP Lean formalization topics

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Full reference aligned with `config/topics.yaml` (50 topics as of April 2026). Per-topic sections below may not list every id; regenerate or extend this file when the catalogue grows.

> **Compilation status**: All 50 sketches compile cleanly under Lean v4.29.0 + Mathlib v4.29.0 on a green sweep. Run `uv run python scripts/03_lean_verify_only.py` for per-topic stdout; full JSON aggregates live in `output/reports/run_*/verification_manifest.json` when a pipeline run emits them.
>
> **Namespace wrapping**: Every committed sketch in `SKETCHES` (and therefore in `config/topics.yaml`) is wrapped `namespace FEPNNN ... end FEPNNN` so that theorem names across all 50 topics share no global scope. The illustrative snippets below are intentionally namespace-free for readability.

> [!IMPORTANT]
> **The Lean4 sketches below are pedagogical illustrations; committed catalogue data is authoritative.**
>
> - **Committed catalogue**: [`config/topics.yaml`](../config/topics.yaml) — every row is **mathlib_status: real** and `lean_sketch` matches `scripts/catalogue_sketches.py` `SKETCHES[id]` (enforced by `tests/test_catalogue_sketches_ssot.py`). Bodies are authored in `SKETCHES`; regenerate YAML with `scripts/_maint_build_topics_catalogue.py`. Each sketch compiles clean under the `LeanVerifier` preamble with `import Mathlib`, zero `sorry`, zero errors (verified: 50/50 on Lean v4.29.0 + Mathlib v4.29.0 with warm cache).
> - **Name drift**: The illustrative code fences below may use names like `variational_free_energy_bound` that do **not** exist in the shipped YAML. The actual shipped theorem/definition names (e.g. `fep001_measure_union_le`, `fep002_prob_measure_univ`, `fep002_elbo_bound`) and **`\Cref{eq:fep-NNN-k}`** targets surface in `manuscript/09z_unified_formalism_catalogue.md` after a pipeline run (same file: Lean fences + `equation` blocks with `\label{eq:…}`, plus `{#sec:…}` anchors).
> - **Mathlib hints**: The `Mathlib` field in each entry is a **navigation hint** (what concepts are relevant), not a literal import list. The sketch itself only imports `Mathlib` as an umbrella (see `LeanVerifier._wrap_lean_code`).
> - **To see the real Lean**: read `config/topics.yaml` directly, or run `uv run python scripts/03_lean_verify_only.py` which prints per-topic compile status for all 50.
> - **Partial pipeline runs**: optional env **`FEP_LEAN_MAX_TOPICS`** caps how many rows enter Gauss Sessions in `FEPPipeline` (the YAML file remains the full 50-topic canonical catalogue).

## Area Summary

Topic **ids** `fep-001` … `fep-050` are **not** contiguous by area: each id’s `area` field in `config/topics.yaml` is authoritative. For PDF injection, see auto-generated `manuscript/manuscript_vars.yaml` (`topics.<id>.area`).

Authoritative counts (derived from `config/topics.yaml` by `discover_projects` / `FEPTopicCatalogue` and regenerated on each `_maint_build_topics_catalogue.py` run):

| Area | Topic count |
|------|-------------|
| FEP | 14 |
| ActiveInference | 11 |
| BayesianMechanics | 10 |
| InfoGeometry | 8 |
| Thermodynamics | 7 |
| **Total** | **50** |

---

## FEP — Free Energy Principle (14 topics)

### fep-001 — Variational Free Energy Bound

**Mathlib**: `MeasureTheory, Probability.KL`

**Statement**: The variational free energy F[q,p] = KL[q(ψ|m) || p(ψ|s,m)] - E_q[log p(s|ψ,m)] upper-bounds surprise: F ≥ -log p(s|m).

**Lean4 sketch**:

```lean
theorem variational_free_energy_bound {q p : Measure ℝ} (hq : q.AeMeasurable) :
    variational_free_energy q p ≤
    -Real.log (∫ ψ, p.rnDeriv MeasureTheory.Measure.volume ψ
               ∂MeasureTheory.Measure.volume) := by
  exact kl_nonneg q p |>.trans_eq (by ring)
```

---

### fep-002 — Evidence Lower Bound (ELBO)

**Mathlib**: `MeasureTheory, Probability.KL, Analysis.SpecialFunctions.Log`

**Statement**: log p(s) = ELBO(q) + KL[q(ψ) || p(ψ|s)], so ELBO ≤ log p(s), and maximising ELBO with respect to q tightens the bound until KL = 0.

Catalogue (YAML): probability measure identities plus `fep002_elbo_bound` (see manuscript `04a_framework_fep.md` table row fep-002).

Lean4 sketch (illustrative only):

```lean
theorem elbo_decomposition {p q : Measure ℝ} (hs : 0 < p.mass) :
    Real.log p.mass = elbo q p + KL q (p.cond :) := by
  rw [elbo, KL_def]; ring_nf; exact measure_decomp p q
```

---

### fep-003 — Expected Free Energy G(π) (ActiveInference)

**Mathlib**: `Probability.ConditionalExpectation, MeasureTheory`

**Statement**: G(π) = E_{q(o,s|π)}[log q(s|π) - log p(o,s|π)] decomposes into risk (KL from preferred outcomes) plus ambiguity (expected conditional entropy of observations given states).

**Lean4 sketch**:

```lean
theorem expected_free_energy_decomposition {π : Policy} {q p : Measure (O × S)} :
    G π q p = risk_term π q p + ambiguity_term π q p := by
  simp [G, risk_term, ambiguity_term]; rw [KL_split]; ring
```

---

### fep-004 — Fisher Information Metric (InfoGeometry)

**Mathlib**: `Geometry.Manifold, MeasureTheory.FisherInformation`

**Statement**: The Fisher information metric g_ij(θ) = -E_p[∂²log p(x;θ)/∂θᵢ∂θⱼ] defines a Riemannian metric on the statistical manifold of a parametric family.

**Lean4 sketch**:

```lean
theorem fisher_metric_positive_semidefinite
    {α : Type*} {Θ : Type*} [Fintype Θ]
    (p : Θ → Measure α) (θ : Θ) :
    PosSemidef (fisherMatrix p θ) := by
  exact fisherMatrix_pos_semidef p θ
```

---

### fep-005 — Markov Blanket Partition Theorem (BayesianMechanics)

**Mathlib**: `Probability.Kernel, MeasureTheory.Measure.Product`

**Statement**: Given a Markov blanket B of a system S, internal states μ are conditionally independent of external states η given blanket states b: p(μ,η|b) = p(μ|b)·p(η|b).

**Lean4 sketch**:

```lean
theorem markov_blanket_conditional_independence
    {Ω : Type*} [MeasurableSpace Ω]
    {μ η : Ω → ℝ} {b : Ω → ℝ}
    (hMarkov : IsMarkovBlanket b μ η) :
    IndepGiven μ η b := by
  exact hMarkov.to_indep
```

---

### fep-006 — Predictive Coding: Precision-Weighted Error Minimisation

**Mathlib**: `Analysis.Hessian, MeasureTheory`

**Statement**: The gradient of variational free energy with respect to mean μ equals the precision-weighted prediction error: ∂F/∂μ = -Π(s - g(μ)), where Π = -∂²F/∂ε² is the precision matrix.

**Lean4 sketch**:

```lean
theorem predictive_coding_gradient
    {μ : ℝ} {s : ℝ} {g : ℝ → ℝ} {Π : ℝ}
    (hΠ : Π = precision_from_hessian g μ) :
    gradient_F_wrt_μ g s μ = -Π * (s - g μ) := by
  simp [gradient_F_wrt_μ, hΠ, precision_from_hessian]; ring
```

---

### fep-007 — Belief Propagation / Sum-Product Algorithm (ActiveInference)

**Mathlib**: `Probability.ConditionalExpectation, Finset`

**Statement**: Marginal beliefs b(s_τ) are computed via the sum-product algorithm: b(s_τ) = σ(ln A^T ln o_τ + ln B^T ln b(s_{τ+1}) + ln B ln b(s_{τ-1})), where σ is softmax.

**Lean4 sketch**:

```lean
theorem belief_propagation_fixed_point
    {S O : Finset α} (A : O → S → ℝ) (B : S → S → ℝ)
    (o : O) (b_next b_prev : S → ℝ) :
    ∃ b : S → ℝ, IsFixedPoint (belief_update A B o b_next b_prev) b := by
  exact Brouwer.fixed_point_exists _
```

---

### fep-008 — Active Inference Optimal Policy (ActiveInference)

**Mathlib**: `Optimization.Convex, Probability.ConditionalExpectation`

**Statement**: The optimal policy π* minimizes G(π) = E_{q(o,s|π)}[log q(s|π) - log p(o,s|C)], equivalent to maximizing pragmatic (reward) and epistemic (information gain) value.

**Lean4 sketch**:

```lean
theorem optimal_policy_minimizes_G
    {Π : Type*} {q p : Π → Measure (O × S)} :
    ∃ π* : Π, ∀ π : Π, G q p π* ≤ G q p π := by
  exact exists_min_of_continuous_compact G continuous_G compact_Π
```

---

### fep-009 — Precision Weighting (Π = -∂²F/∂ε²)

**Mathlib**: `MeasureTheory, Analysis.Hessian`

**Statement**: Precision Π(ε) = -∂²F/∂ε² is the negative Hessian of free energy with respect to prediction errors ε and corresponds to the inverse covariance of prediction errors.

**Lean4 sketch**:

```lean
theorem precision_is_inverse_covariance
    {F : ℝ → ℝ} {ε : ℝ} (hF : TwiceDifferentiableAt ℝ F ε) :
    precision F ε = (variance_prediction_error F ε)⁻¹ := by
  simp [precision, variance_prediction_error, iteratedFDeriv]
```

---

### fep-010 — Path Integral Free Energy (BayesianMechanics)

**Mathlib**: `MeasureTheory.Measure.Product, Analysis.SpecialFunctions`

**Statement**: Action A[x(t)] = ∫₀ᵀ F(x(t), ẋ(t)) dt is minimized by the most-probable path under the variational density q, connecting FEP to Feynman path integrals.

**Lean4 sketch**:

```lean
theorem path_integral_extremal
    {F : ℝ → ℝ → ℝ} (hF : IsSmoothLagrangian F) :
    ∃ x : ℝ → ℝ, IsExtremal (pathIntegral F) x ∧
    SatisfiesEulerLagrange F x := by
  exact EulerLagrange.existence hF
```

---

### fep-011 — Renormalization Group Coarse-Graining (BayesianMechanics)

**Mathlib**: `MeasureTheory.Measure.Product`

**Statement**: Markov blanket hierarchies correspond to renormalization group (RG) coarse-graining: averaging over fast (fine-scale) variables yields effective dynamics for slow (coarse-scale) variables that still minimize free energy.

**Lean4 sketch**:

```lean
theorem rg_coarsegraining_preserves_fep
    {Ω_fine Ω_coarse : Type*}
    (π : Ω_fine → Ω_coarse) (p : Measure Ω_fine) :
    ∃ p_eff : Measure Ω_coarse,
    p_eff = p.map π ∧ FEPMinimiser p_eff := by
  exact ⟨p.map π, rfl, fep_preserved_under_marginalisation π p⟩
```

---

### fep-012 — Sentient Behaviour / Self-Evidencing

**Mathlib**: `MeasureTheory, Probability.KL`

**Statement**: A self-organizing system that acts to fulfill its generative model expectations exhibits sentient behavior in the FEP sense: it actively samples data that confirm its model (self-evidencing), thereby minimizing surprise.

**Lean4 sketch**:

```lean
theorem self_evidencing_minimizes_surprise
    {p : Measure S} {q : Measure S} (h : IsSelfEvidencing q p) :
    -Real.log (evidence p) ≤ variational_free_energy q p := by
  exact kl_nonneg q p |>.add_right _
```

---

### fep-013 — Helmholtz Free Energy Thermodynamic Connection (Thermodynamics)

**Mathlib**: `Analysis.Entropy, Topology.Algebra, MeasureTheory`

**Statement**: The Helmholtz free energy F = U - TS equals the variational free energy when the reference distribution is the Boltzmann distribution; minimizing F minimizes both thermodynamic free energy and informational surprise.

**Lean4 sketch**:

```lean
theorem helmholtz_equals_variational_at_boltzmann
    {U : ℝ → ℝ} {T : ℝ} (hT : 0 < T)
    (p_boltz : BoltzmannDistribution U T) :
    variational_free_energy p_boltz.q p_boltz.p =
    helmholtz_free_energy U T p_boltz.q := by
  simp [variational_free_energy, helmholtz_free_energy, BoltzmannDistribution]
  ring
```

---

### fep-014 — KL Divergence: Non-Negativity, Chain Rule, Monotonicity (InfoGeometry)

**Mathlib**: `MeasureTheory.KL, Analysis.SpecialFunctions.Log`

**Statement**: KL[q||p] ≥ 0 (Gibbs inequality); KL[q||p] = 0 iff q = p a.e.; KL satisfies the chain rule KL[q(x,y)||p(x,y)] = KL[q(x)||p(x)] + E_q[KL[q(y|x)||p(y|x)]].

**Lean4 sketch**:

```lean
theorem kl_chain_rule {p q : Measure (X × Y)} :
    KL q p = KL (q.map Prod.fst) (p.map Prod.fst) +
             KL.condKL q p := by
  exact Prob.kl_chain_rule q p
```

---

### fep-015 — Generative Model Joint Factorization

**Mathlib**: `Probability.Kernel, MeasureTheory.Measure.Product`

**Statement**: The generative model p(s,ψ|m) = p(s|ψ,m)·p(ψ|m) factorises into likelihood times prior. This factorisation is the foundation for variational inference: q approximates the intractable posterior p(ψ|s,m).

**Lean4 sketch**:

```lean
theorem generative_model_factorisation
    {S Ψ : Type*} [MeasurableSpace S] [MeasurableSpace Ψ]
    (likelihood : Kernel Ψ S) (prior : Measure Ψ) :
    (likelihood ⊗ₖ (Kernel.const Ψ prior)).prod_eq
    likelihood prior := by
  exact Kernel.prod_factorisation likelihood prior
```

---

### fep-016 — Laplace Approximation in FEP

**Mathlib**: `Analysis.Hessian, MeasureTheory`

**Statement**: Under the Laplace approximation, the variational density q(ψ) is approximated as Gaussian with mean μ* = argmin_ψ F(ψ) and precision Π = -∂²F/∂ψ², yielding closed-form updates.

**Lean4 sketch**:

```lean
theorem laplace_approximation_minimizes_kl
    {F : ℝ → ℝ} (hF : StrictlyConvex F) :
    ∃ μ : ℝ, ∃ Π : ℝ, 0 < Π ∧
    IsLocalMinimizer (fun q => KL q (gaussApprox F μ Π)) := by
  obtain ⟨μ, hμ⟩ := hF.hasUniqueMinimum
  exact ⟨μ, (-fderiv ℝ (fderiv ℝ F) μ).toReal, by positivity, hμ.to_kl_minimizer⟩
```

---

## ActiveInference — (remaining topics)

### fep-017 — Natural Gradient Descent on Free Energy (InfoGeometry)

**Mathlib**: `Geometry.Manifold, MeasureTheory.KL`

**Statement**: The natural gradient ∇̃F = F(θ)⁻¹·∇F, where F(θ) is the Fisher information matrix, provides the steepest descent direction on the statistical manifold, independent of parametrisation.

**Lean4 sketch**:

```lean
theorem natural_gradient_is_covariant
    {Θ : Type*} [FiniteDimensional ℝ Θ]
    {F : Θ → ℝ} {θ : Θ}
    (hF : DifferentiableAt ℝ F θ) :
    naturalGradient F θ = (fisherMatrix θ)⁻¹ • gradient F θ := by
  exact natural_gradient_def F θ
```

---

### fep-018 — Information Geometry: Geodesics & Parallel Transport (InfoGeometry)

**Mathlib**: `Geometry.Manifold, Analysis.InnerProductSpace`

**Statement**: On the statistical manifold (M, g_F), e-geodesics (exponential family) and m-geodesics (mixture family) are mutually dual under the Fisher metric, and parallel transport preserves the Fisher inner product.

**Lean4 sketch**:

```lean
theorem dual_geodesics_fisher_metric
    {M : Type*} [StatisticalManifold M]
    (γ_e γ_m : ℝ → M) (h_e : IsEGeodesic γ_e) (h_m : IsMGeodesic γ_m) :
    IsDualPair γ_e γ_m := by
  exact dual_structure_from_fisher h_e h_m
```

---

### fep-019 — Bayesian Model Comparison / Model Evidence (BayesianMechanics)

**Mathlib**: `Probability.Kernel, MeasureTheory.KL`

**Statement**: log p(s|m) = ELBO(q; m) + KL[q||p(·|s,m)] ≥ ELBO. Model comparison via log-evidence: model m₁ preferred over m₂ iff log p(s|m₁) > log p(s|m₂); Bayes factor = p(s|m₁)/p(s|m₂).

**Lean4 sketch**:

```lean
theorem bayesian_model_comparison
    {s : S} (m1 m2 : Model) :
    Prefers m1 m2 s ↔ Real.log (evidence m1 s) > Real.log (evidence m2 s) := by
  simp [Prefers, evidence]
```

---

### fep-020 — Continuous-Time Active Inference (Langevin) (ActiveInference)

**Mathlib**: `MeasureTheory.Measure.Product, Analysis.SpecialFunctions`

**Statement**: Continuous-time active inference is governed by generalised Langevin dynamics: dx = (f - Π⁻¹·∂F/∂x) dt + dW, where f is Prior flow, Π is precision, and W is Wiener noise.

**Lean4 sketch**:

```lean
theorem continuous_active_inference_sde
    {F : ℝ → ℝ} {f : ℝ → ℝ} {Π : ℝ} (hΠ : 0 < Π) :
    ∃ x : ℝ → ℝ, SatisfiesGeneralisedLangevin F f Π x := by
  exact SDE.existence_uniqueness (langevin_drift F f Π) standard_diffusion
```

---

### fep-021 — Epistemic vs Pragmatic Value Decomposition (ActiveInference)

**Mathlib**: `Probability.ConditionalExpectation, Finset`

**Statement**: -G(π) = Epistemic value + Pragmatic value = E_q[log p(o|s,π)] - KL[q(s|π)||p(s|C)], separating information gain (curiosity) from goal-directed behavior.

**Lean4 sketch**:

```lean
theorem epistemic_pragmatic_decomposition
    {π : Policy} (q p : Measure (O × S)) :
    -G q p π = epistemicValue q p π + pragmaticValue q p π := by
  simp [G, epistemicValue, pragmaticValue]; ring
```

---

### fep-022 — Hierarchical Generative Model (Deep Temporal Model) (FEP)

**Mathlib**: `Probability.Kernel, MeasureTheory.Measure.Product`

**Statement**: A hierarchical generative model p(s, ψ¹, ..., ψᴸ|m) = p(s|ψ¹)·∏ₗ p(ψˡ|ψˡ⁺¹) factorises level-by-level; variational free energy decomposes as sum of level-wise free energies.

**Lean4 sketch**:

```lean
theorem hierarchical_free_energy_decomposition
    {L : ℕ} (p : HierarchicalGenerativeModel L) (q : HierarchicalVariational L) :
    F_hier q p = ∑ l : Fin L, F_level l q p := by
  induction L with
  | zero => simp [F_hier]
  | succ n ih => simp [F_hier, F_level]; rw [← ih]; ring
```

---

### fep-023 — Affordance: Reachable Distributions under Policy (ActiveInference)

**Mathlib**: `Probability.ConditionalExpectation, Finset`

**Statement**: An affordance is a reachable posterior distribution over states under a given policy: q(s_T|π) = ∑_{s₀} p(s_T|s₀, π)·b(s₀). Only policies leading to preferred distributions p(s|C) have low G(π).

**Lean4 sketch**:

```lean
theorem affordance_reachable_posterior
    {S : Finset α} (b : S → ℝ) (T : S → S → ℝ) (π : Policy) :
    reachablePosterior b T π ∈ AffordanceSet π := by
  exact lift_policy_to_distribution b T π
```

---

### fep-024 — Surprise Minimisation = Long-Run Entropy (BayesianMechanics)

**Mathlib**: `Analysis.Entropy, MeasureTheory`

**Statement**: Time-averaged surprise (1/T)∫₀ᵀ -log p(s_t|m) dt → H[p(s|m)] as T → ∞ by ergodicity; minimising long-run surprise = minimising entropy of the sensory marginal = self-organisation into low-entropy states.

**Lean4 sketch**:

```lean
theorem time_average_surprise_is_entropy
    {p : Measure S} (hErg : IsErgodic p) :
    Filter.Tendsto (fun T => (1/T) * ∫ x in Set.Icc 0 T,
                   -Real.log (p.density x) ∂MeasureTheory.Measure.lebesgue)
    Filter.atTop (nhds (entropy p)) := by
  exact ergodic_theorem_for_log p hErg
```

---

### fep-025 — Solenoidal Flow & NESS Steady-State (Thermodynamics)

**Mathlib**: `Probability.Kernel, MeasureTheory.Measure.Product`

**Statement**: At non-equilibrium steady state (NESS), the probability current J = (-D·∇ + Q)·p decomposes into gradient flow (free energy minimisation) plus solenoidal part Q (irreversible cycling), maintaining the steady state while dissipating entropy.

**Lean4 sketch**:

```lean
theorem ness_solenoidal_decomposition
    {D Q : Matrix ℝ ℝ} (hD : PosDef D) (hQ : Q.IsSkewSymm)
    (p : Measure ℝ) (hNESS : IsNESS D Q p) :
    (probabilityCurrent D Q p).solenoidalPart = Q.mulVec (gradient (logDensity p)) := by
  exact NESS.decomposition D Q p hNESS
```

---

## Navigation

- [← FEP Background](fep-background.md)
- [← Lean4 Context](lean4.md)
- [← docs/README.md](README.md)
