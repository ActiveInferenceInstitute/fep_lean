# FEP Background — Free Energy Principle, Active Inference & Bayesian Mechanics

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Overview

`fep_lean` formalizes **50 canonical theorems** spanning **five** deeply interconnected frameworks (counts mirror [`topics-reference.md`](topics-reference.md) and the YAML in [`config/topics.yaml`](../config/topics.yaml)):

| Framework | Count | Core Idea |
|-----------|-------|-----------|
| **Free Energy Principle (FEP)** | 14 | Self-organizing systems minimize variational free energy (a bound on surprise) |
| **Active Inference** | 11 | Agents act to minimize expected free energy over future trajectories |
| **Bayesian Mechanics** | 10 | Statistical-mechanics framing for systems that track probability distributions |
| **Information Geometry** | 8 | Riemannian geometry of probability distribution manifolds (Fisher metric) |
| **Thermodynamics** | 7 | Connection between FEP and classical thermodynamic free energy |

> Topic IDs are not strictly contiguous per area because the shipped catalogue is
> organized by topical coherence rather than area bands. See `topics-reference.md`
> for the authoritative ID-to-area mapping.


---

## 1. The Free Energy Principle

### Core Statement

Any self-organizing system that persists over time must minimize the **variational free energy** F[q]:

```
F[q] = KL[q(s) || p(s|o)] - log p(o)
```

In the literature's more symmetric form (with the generative joint `p(s, o)` expanded and the agent's variational density `q(ψ|s)`):

```
F[q,p] = KL[q(ψ) || p(ψ|s)] - log p(s)
        = KL divergence + negative log evidence
        ≥ -log p(s)          [since KL ≥ 0]
```

Where:

- `q(s)` / `q(ψ)` = the agent's internal (variational) distribution over hidden states
- `p(s|o)` / `p(ψ|s)` = the true posterior over hidden states given observations
- `p(o)` / `p(s)` = model evidence (marginal probability of observations / sensory data)
- `KL[q||p]` = Kullback-Leibler divergence from q to p

Minimizing F achieves two things simultaneously:

1. Makes q approximate the true posterior (perception = Bayesian inference)
2. Maximizes model evidence, i.e., minimizes surprise −log p(o) (adaptation)

### ELBO Connection

Variational free energy is the negative **Evidence Lower Bound (ELBO)**:

```
log p(s) = F[q,p] + KL[q||p^*]    where p^* = p(ψ|s)
         ≥ -F[q,p]                 (ELBO = -F)
```

Maximizing the ELBO (standard in variational inference) = minimizing free energy.

### Predictive Coding

The FEP gives rise to **predictive coding** — the brain generates predictions and updates beliefs based on **prediction errors** (residuals between predicted and actual sensory input). The Lean4 formalization of predictive coding (fep-006) captures the precision-weighted error minimization:

```
ε = s - g(μ)           (sensory prediction error)
Δμ ∝ -∂F/∂μ = Π·ε      (belief update proportional to precision-weighted error)
```

---

## 2. Active Inference

### From Perception to Action

Active Inference extends FEP to include actions. An agent not only updates beliefs (perception) but also selects **policies** π that minimize **expected free energy** G(π):

```
G(π) = E_q[log q(s_τ|π) - log p(s_τ, o_τ|π)]
     = E_q[log q(o,s|π) - log p(o,s|π)]
     = KL[q(s|π) || p(s|C)] - H[p(o|s)]     (pragmatic + epistemic value)
```

The subscript τ denotes a future time index: EFE is evaluated over the **expected trajectory** under π, rather than over past data. Minimizing G selects policies that jointly (a) bring predicted outcomes into alignment with preferences `p(s|C)` (pragmatic), and (b) resolve uncertainty about hidden states (epistemic).

Where:

- `p(s|C)` = prior preferences (what states the agent prefers)
- `H[p(o|s)]` = expected information gain (epistemic value / curiosity)
- `G(π)` = total expected free energy = pragmatic + epistemic value

### Belief Propagation

Policy selection in discrete-time Active Inference uses **belief propagation** / sum-product algorithms over factor graphs representing the generative model. The Lean4 formalization (fep-007) captures the fixed-point equations for belief updating.

### Epistemic vs. Pragmatic Value (fep-021)

```
-G(π) = Epistemic value (exploration) + Pragmatic value (exploitation)
       = E_q[log p(o|s)] - KL[q(s|π)||p(s|C)]
```

This decomposition is the formal basis for the exploration/exploitation trade-off in Active Inference.

---

## 3. Bayesian Mechanics

### Markov Blankets (fep-005)

A **Markov blanket** B of a system partitions the world into:

- **Internal states** μ (inside the blanket)
- **External states** η (outside the blanket)
- **Sensory states** s (blanket → internal)
- **Active states** a (internal → blanket)

The Markov blanket condition: μ ⊥ η | B (internal and external states are conditionally independent given the blanket). This is the formal basis for the FEP's claim about self-organization.

### NESS and Solenoidal Flow (fep-025)

At **Non-Equilibrium Steady State (NESS)**, the system's probability flow decomposes:

```
J(x) = -D · ∇F(x) + Q(x) · ∇F(x)
```

Where:

- `D` = diffusion (noise) term
- `Q` = solenoidal (curl) flow — the NESS component that prevents equilibration
- `F(x)` = non-equilibrium free energy (potential function)

The solenoidal component ensures the system remains far from equilibrium while minimizing free energy on average.

### Surprise Minimization = Entropy Minimization (fep-024)

Over long time scales:

```
E_τ[-log p(s_τ)] → H[p(s)]    (time-average surprise → entropy)
```

Minimizing long-run average surprise is equivalent to minimizing the entropy of the agent's sensory marginal — self-organization into low-entropy (ordered) states.

---

## 4. Information Geometry

### Fisher Information Metric (fep-004)

The **Fisher information metric** gives the natural Riemannian geometry on probability distribution manifolds:

```
g_ij(θ) = -E_p[∂²log p(x;θ)/∂θᵢ∂θⱼ] = E_p[(∂log p/∂θᵢ)(∂log p/∂θⱼ)]
```

This metric defines geodesics (shortest paths between distributions) and natural gradients.

### Natural Gradient Descent (fep-017)

Standard gradient descent on F is slow when parameters have correlated effects. **Natural gradient** uses the Fisher metric:

```
θ_{t+1} = θ_t - η · F(θ)^{-1} · ∇F
```

where `F(θ)` is the Fisher information matrix. Natural gradient descent is invariant to reparametrization of the distribution family.

---

## 5. Thermodynamics Connection (fep-013)

The **Helmholtz free energy** in classical thermodynamics:

```
F_thermo = U - T·S    (internal energy minus temperature × entropy)
```

connects to variational free energy:

```
F_variational = E_q[U(ψ)] - H[q] = E_q[U(ψ)] + KL[q||p_0]
```

where `p_0` is a reference (prior) distribution. Both minimize a same-form functional — the FEP is the information-theoretic generalization of classical thermodynamic free energy minimization.

### Langevin dynamics connection

Gradient descent on a free-energy surface `F(x)` with thermal noise is described by the **overdamped Langevin equation**:

```
dx = -∇F(x) dt + √(2β⁻¹) dW
```

where `β = 1/(k_B·T)` is the inverse temperature and `dW` is a standard Wiener increment. This is the stochastic-differential-equation form of the FEP's gradient-descent-on-surprise story: the drift `−∇F` pulls the system toward free-energy minima, while the `√(2β⁻¹) dW` noise prevents pathological convergence and generates the correct Boltzmann stationary distribution `p_∞(x) ∝ exp(−β·F(x))`. Continuous-time Active Inference (topic fep-020) generalizes this with a precision-weighted drift and (in Bayesian mechanics) an additive solenoidal term `Q·∇F` to describe NESS flow (topic fep-025).

---

## Mathlib modules per area

The Lean 4 sketches lean on these Mathlib4 modules; see [lean4.md](lean4.md#mathlib4-modules-used-in-fep_lean) for full coverage status.

| Area | Primary Mathlib modules |
|------|-------------------------|
| **FEP** | `MeasureTheory.Measure.rnDeriv`, `MeasureTheory.MeasurableSpace` |
| **ActiveInference** | `MeasureTheory.Integral.Bochner`, `Topology.MetricSpace.Basic` |
| **BayesianMechanics** | `MeasureTheory.Decomposition.Lebesgue`, `Analysis.MeanInequalities` |
| **InfoGeometry** | `Analysis.InnerProductSpace.Basic`, `Geometry.Manifold.Basic` |
| **Thermodynamics** | `Analysis.SpecialFunctions.Log.Basic`, `MeasureTheory.Measure.Haar` |

These are the modules most frequently `import`ed (via the umbrella `import Mathlib`) across the 50-topic catalogue. Per-topic hints live in the `mathlib` field of `config/topics.yaml`.

---

## Key References

1. **Friston, K.** (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
2. **Friston, K. et al.** (2016). Active inference and learning. *Neuroscience & Biobehavioral Reviews*, 68, 862-879. DOI: [10.1016/j.neubiorev.2016.06.022](https://doi.org/10.1016/j.neubiorev.2016.06.022).
3. **Parr, T., Pezzulo, G., Friston, K.** (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*. MIT Press.
4. **Ramstead, M., Sakthivadivel, D., Friston, K.** (2023). On Bayesian mechanics: a physics of and by beliefs. *Interface Focus*, 13(3).
5. **Amari, S.** (2016). *Information Geometry and Its Applications*. Springer.

---

## How the catalogue is processed

For execution order (template `run.sh`, Stage 02 script discovery, subprocess timeouts, workflow flags), see [pipeline.md](pipeline.md) and [configuration.md](configuration.md).

---

## Navigation

- [Lean4 context →](lean4.md)
- [Topics reference →](topics-reference.md)
- [← docs/README.md](README.md)
