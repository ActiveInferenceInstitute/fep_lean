# Background and Related Work {#sec:background_and_related_work}

## The Free Energy Principle and Its Mathematical Structure {#sec:the_free_energy_principle_and_its_mathematical_structure}

The Free Energy Principle (FEP) asserts that any bounded dynamical system that persists over time can be mathematically interpreted as performing approximate Bayesian inference [@friston2006free]. This foundational idea, first articulated formally by Karl Friston [@friston2010free] and extended into a comprehensive physics-of-self-organization program a decade later [@friston2019free], scales from simple single-cell homeostasis to complex human cognition via Active Inference [@friston2017active; @parr2022active]. Behind the claim lies a specific mathematical object—the variational free energy—and a specific operational claim: that the dynamics of a self-organizing system can be rewritten as a gradient flow on that object. Both halves must be formalized to speak precisely about what the FEP says.

### Variational Free Energy as an Evidence Lower Bound (ELBO) {#sec:vfe_as_elbo}

The machine learning literature [@blei2017variational] introduces the same quantity under the name *evidence lower bound* (ELBO). For a latent variable $z$, observation $x$, generative model $p(x, z)$, and variational posterior $q(z)$,

\begin{equation}\label{eq:bg_elbo}
\text{ELBO}(q) = \mathbb{E}_{q(z)}[\log p(x, z) - \log q(z)] = \log p(x) - \KL[q(z) \,\|\, p(z \mid x)].
\end{equation}

(Equation \ref{eq:bg_elbo}.) Identifying $z \leftrightarrow \psi$, $x \leftrightarrow s$, and $F = -\text{ELBO}$, the FEP variational free energy is exactly the negative ELBO. This equivalence is central: anything Mathlib4 proves about KL divergence and expectations under a dominating measure transfers directly to FEP statements.

### Formal Definition: Variational Free Energy {#sec:formal_definition_variational_free_energy}

The variational free energy $\FE$ for an agent with recognition density $q(\psi \mid m)$, generative model $p(s, \psi \mid m)$, and sensory observations $s$ is defined as:

\begin{equation}\label{eq:eq_1}
\FE[q, p] \;=\; \underbrace{\KL\!\bigl[q(\psi \mid m) \,\|\, p(\psi \mid s, m)\bigr]}_{\geq\, 0} \;-\; \underbrace{\log p(s \mid m)}_{\text{log-evidence}}
\end{equation}

Because KL divergence is non-negative by Gibbs' inequality, this immediately yields the **variational bound**:

\begin{equation}\label{eq:eq_2}
\FE[q, p] \;\geq\; -\log p(s \mid m) \;=\; \text{surprise}
\end{equation}

Equivalently, the free energy admits an **energy-entropy decomposition**:

\begin{equation}\label{eq:eq_3}
\FE[q, p] \;=\; \underbrace{\E_q\!\bigl[-\log p(s, \psi \mid m)\bigr]}_{\text{energy}} \;-\; \underbrace{\Ent\!\bigl[q(\psi \mid m)\bigr]}_{\text{entropy}}
\end{equation}

These dual decompositions—(1) as KL plus log-evidence and (3) as energy minus entropy—are the starting point for all subsequent formalisms in this paper. In Mathlib4 parlance, Eq.~\ref{eq:eq_3} is a statement about `∫ (fun ψ => -Real.log (p (s,ψ))) ∂(q)` together with `MeasureTheory.entropy q`; the mere act of writing this expression forces declaration of a measurable space `α` and an integrability hypothesis, neither of which typically appears in journal papers.

#### Three Equivalent Decompositions of Variational Free Energy {#sec:three_equivalent_decompositions}

Before proceeding to Active Inference, it is worth exhibiting the three algebraically equivalent forms of $\FE$ that appear throughout the FEP literature, since each form motivates a different slice of the Lean 4 catalogue. Let $o$ denote observations (written $s$ elsewhere), $s$ the hidden (latent) states (written $\psi$ elsewhere), $p(o, s)$ the generative model, and $q(s)$ the recognition density.

**(1) Surprise bound (posterior-tracking form).** Starting from Bayes' rule $p(s \mid o) = p(o, s)/p(o)$ and adding and subtracting $\log q(s)$ inside an expectation under $q$,

\begin{equation}\label{eq:eq_F_surprise}
F[q] \;=\; -\log p(o) \;+\; \KL\!\bigl[q(s)\,\|\,p(s \mid o)\bigr] \;\geq\; -\log p(o).
\end{equation}

This is the "free energy bounds surprise" identity: the first term is the (negative log) model evidence—the Shannon surprise $-\log p(o)$ that the agent cannot change by rearranging beliefs—and the second is a non-negative KL gap that vanishes iff $q = p(\cdot \mid o)$.

**(2) Energy–entropy form.** Multiplying out the logarithm gives
\begin{equation}\label{eq:eq_F_energyentropy}
F[q] \;=\; \E_{q(s)}\!\bigl[-\log p(o, s)\bigr] \;+\; \E_{q(s)}\!\bigl[\log q(s)\bigr] \;=\; U_q \;-\; H[q],
\end{equation}
where $U_q := \E_{q}[-\log p(o, s)]$ is the (cross-)energy under the joint generative model and $H[q] := -\E_q[\log q(s)]$ is the Shannon entropy of the recognition density. This is the form most directly connected to statistical-mechanical free energy (Helmholtz $F = U - T S$, with $T = 1$ in natural units).

**(3) ELBO form.** Because $F[q] = \E_q[\log q(s) - \log p(o, s)]$, one has
\begin{equation}\label{eq:eq_F_elbo}
F[q] \;=\; -\text{ELBO}(q), \qquad \text{ELBO}(q) \;=\; \E_{q(s)}\!\bigl[\log p(o, s) - \log q(s)\bigr].
\end{equation}
This identity is what licenses the direct reuse of the machine-learning ELBO apparatus: variational Bayes, amortized inference, and the reparameterization trick all minimize $-\text{ELBO}$, which is exactly $F$.

**Why $F$ is the right object to minimize.** Eq.~\ref{eq:eq_F_surprise} exhibits $F$ as the sum of two non-negative terms (up to the sign of the evidence): a KL gap measuring *posterior error* and a surprise measuring *model error*. Minimizing $F$ with respect to $q$ with the model fixed drives the KL term to zero, so $q \to p(\cdot \mid o)$ (the exact Bayesian posterior); minimizing $F$ with respect to model parameters with $q$ fixed drives $-\log p(o)$ downward, so $\log p(o)$—the model evidence or *self-evidence*—is maximized. A single gradient step on $F$ therefore simultaneously performs *perception* (posterior tracking) and *evidence accumulation* (model fitting), which is precisely the dual role the FEP requires. In Lean 4 these two implications manifest as separate lemmas over separate measurable spaces (a posterior space and a parameter space), making it explicit where in the catalogue each role is discharged: posterior tracking draws on the KL-nonnegativity chain (fep-011, fep-035), while self-evidencing is anchored by the log and entropy lemmas (fep-012, fep-039).

### Predictive Coding as Precision-Weighted Prediction Error {#sec:predictive_coding_as_precision_weighted_prediction_error}

The FEP additionally predicts a specific microscopic form for belief updates. Assuming a generative model whose likelihood is a nonlinear Gaussian $p(x \mid s) = \mathcal{N}(x;\,g(s),\,\Sigma_\varepsilon)$ with precision $\Pi_\varepsilon = \Sigma_\varepsilon^{-1}$, a point-mass or Laplace recognition density concentrated at $\mu$, and differentiable $g$, the gradient of $F$ with respect to the mean takes the canonical precision-weighted prediction-error form
\begin{equation}\label{eq:eq_PC_update}
\dot{\mu} \;=\; -\frac{\partial F}{\partial \mu} \;=\; \bigl(\partial_\mu g(\mu)\bigr)^{\!\top} \Pi_\varepsilon\, \varepsilon \;-\; \Pi_s\,(\mu - \mu_{\text{prior}}),
\qquad \varepsilon := x - g(\mu),
\end{equation}
where $\varepsilon$ is the sensory prediction error, $\Pi_s$ is the prior precision on $\mu$, and $\mu_{\text{prior}}$ is the prior expectation. Here $\Pi_\varepsilon \cdot \varepsilon$ is the precision-weighted prediction error: each component of the error is rescaled by how confident the model is about that channel, so that more reliable sensory dimensions drive belief updates more aggressively. The first term on the right drives $\mu$ to reduce sensory prediction error; the second term anchors $\mu$ to its prior.

This equation ties three separate strands of the catalogue together. (i) It is a **gradient flow** on $F$ and therefore shares the contraction structure formalized for quadratic descents in **fep-032** (`descent_contracts`, `grad_sq_nonneg`, `fixed_point`). (ii) Under the Laplace approximation introduced next, the energy $U_q$ reduces to a sum of quadratics in $\varepsilon$ weighted by the precisions $\Pi$; this is exactly the quadratic-minimum structure formalized in **fep-016** (`sq_nonneg`, `minimum at mode`, `precision-weighted quadratic`). (iii) Message passing across hierarchical layers of a predictive-coding network propagates the same form recursively, which is the structural content of **fep-045** (`ConjugateFamily`, `fold`, `single_update`) and the monotone-composition lemmas in **fep-048**. A reader who wants to know where in the Lean 4 catalogue the "prediction error" half of the FEP lives should therefore look at the intersection of these four rows.

### The Laplace Approximation and the Quadratic Form of $F$ {#sec:laplace_approximation}

The FEP in its most widely used form does not carry a fully nonparametric $q$; it typically employs the **Laplace assumption**—that $q$ is Gaussian, fully parameterized by its mean $\mu$ and covariance $\Sigma$:
\begin{equation}\label{eq:eq_laplace_q}
q(s) \;=\; \mathcal{N}\!\bigl(s;\,\mu,\,\Sigma\bigr).
\end{equation}
Inserting Eq.~\ref{eq:eq_laplace_q} into $F[q]$ and minimizing over $\Sigma$ at fixed $\mu$ yields the **Laplace fixed point**
\begin{equation}\label{eq:eq_laplace_cov}
\Sigma^{*} \;=\; \bigl(-H_F(\mu^{*})\bigr)^{-1},
\end{equation}
where $H_F(\mu) := \partial^2 F / \partial \mu \partial \mu^{\!\top}$ is the Hessian of $F$ at $\mu$; equivalently $\Sigma^{*}$ is the inverse observed information at the MAP estimate $\mu^{*}$. Substituting Eq.~\ref{eq:eq_laplace_cov} back into Eq.~\ref{eq:eq_F_energyentropy} collapses the entropy term to $\tfrac{1}{2}\log\det(2\pi e\,\Sigma^{*})$ and the energy term to a second-order Taylor expansion around $\mu^{*}$. The result is a **precision-weighted quadratic** in the prediction errors,
\begin{equation}\label{eq:eq_laplace_quadratic}
F_{\text{Laplace}}(\mu) \;\approx\; \tfrac{1}{2}\, \varepsilon^{\!\top} \Pi_\varepsilon\, \varepsilon \;+\; \tfrac{1}{2}\,(\mu - \mu_{\text{prior}})^{\!\top}\Pi_s\,(\mu - \mu_{\text{prior}}) \;-\; \tfrac{1}{2}\log\det\bigl(\Pi_\varepsilon\,\Pi_s\bigr) \;+\; \text{const},
\end{equation}
plus terms that vanish at $\mu^{*}$. This is the form of $F$ actually minimized in nearly every neural-predictive-coding and active-inference implementation, and it is also the form that **fep-016** formalizes: `sq_nonneg` provides the fundamental quadratic non-negativity lemma; `minimum at mode` certifies that the unique minimizer of a precision-weighted quadratic is the mode; `precision-weighted quadratic` assembles these into the canonical $\tfrac{1}{2} \varepsilon^{\!\top}\Pi\varepsilon$ shape. Because Eq.~\ref{eq:eq_laplace_quadratic} is an approximation, the catalogue keeps explicit algebraic scaffolding (Laplace quadratic $+$ descent contraction) separate from claims about the full $F$ functional, honoring the approximation's boundaries.

### The Active Inference Perception–Action Loop {#sec:ai_perception_action_loop}

Active Inference extends the FEP by positing that agents minimize not only present free energy but *expected* free energy under each available policy $\pi$:

\begin{equation}\label{eq:eq_4}
\EFE(\pi) = \underbrace{\mathbb{E}_{q(o, s \mid \pi)}[\log q(s \mid \pi) - \log q(s \mid o, \pi)]}_{\text{epistemic value}} - \underbrace{\mathbb{E}_{q(o \mid \pi)}[\log p(o \mid C)]}_{\text{pragmatic value}}
\end{equation}

where $o$ are predicted observations, $s$ are hidden states, and $C$ are prior preferences. The epistemic term rewards information gain (exploration); the pragmatic term rewards policies that realize preferred outcomes (exploitation). Policies are then selected by a softmax:

\begin{equation}\label{eq:bg_softmax_policy}
P(\pi) \propto \exp(-\gamma \cdot \EFE(\pi)),
\end{equation}

(Equation \ref{eq:bg_softmax_policy}.) with precision parameter $\gamma > 0$. Formalizing this loop in Lean 4 requires a `Fin n → Action` policy type, a measurable space of observations, and a summation over the (finite) policy set—all of which are available in `Algebra.BigOperators.Group.Finset` and `Data.Fin`.

### The Theoretical Landscape {#sec:the_theoretical_landscape}

The FEP ecosystem is heavily stratified mathematically, progressing from foundational variational calculus to cutting-edge stochastic physics. Each stratum is anchored by a distinguished mathematical object, and each object demands a different slice of Mathlib4:

1. **Foundational Variational Bounds** (Eqs.~\ref{eq:eq_1}--\ref{eq:eq_3}): Built upon basic Kullback–Leibler (KL) divergences and the Evidence Lower Bound (ELBO) originating in machine learning. The variational free energy $\FE$ serves as a tractable upper bound on surprise [@friston2007variational; @friston2008variational], and the generalized free energy extends these bounds to accommodate model uncertainty [@parr2019generalised]. Central object: the Boltzmann–Gibbs density $p^{*}(\Gamma) \propto \exp(-F(\Gamma))$, exhibiting free energy as a log-density on microstates $\Gamma$, in which statistical-mechanical "equilibrium" and Bayesian "posterior" coincide.

2. **Active Inference** (EFE and policy objectives; Eq.~\ref{eq:eq_4}): Introduces temporal policies in which organisms take physical action to minimize Expected Free Energy [@friston2015epistemic], decomposed into epistemic value (information gain) and pragmatic value (reward seeking) [@sajid2021active]. The Expected Free Energy $\EFE(\pi)$ selects policies that jointly minimize uncertainty and fulfill prior preferences. Recent work by Champion et al. [@champion2026reframing] theoretically unifies the EFE objective across four distinct published formulations (for example, risk-plus-ambiguity versus information-gain), providing a unified likelihood mapping amenable to Lean 4 formalization. Central object: the variational Bayes minimizer $q^{*} = \arg\min_{q} F[q, p]$, which at the algorithmic level becomes a policy selector $\pi^{*} = \arg\min_{\pi}\,\E[G(\pi)]$.

3. **Information Geometry** (§\ref{sec:information_geometry_results}, §\ref{sec:mathlib4_and_measure_theoretic_probability}): Models belief updates as traversal of statistical manifolds governed by the Fisher Information Metric and continuous natural gradients [@amari2016information]. The space of probability distributions becomes a Riemannian manifold whose curvature encodes the efficiency of inference. The Fisher Information Metric is defined as

\begin{equation}\label{eq:bg_fisher_metric}
g_{ij}(\theta) = \mathbb{E}_{p(x \mid \theta)}\!\left[\frac{\partial \log p(x \mid \theta)}{\partial \theta^i} \cdot \frac{\partial \log p(x \mid \theta)}{\partial \theta^j}\right],
\end{equation}

(Equation \ref{eq:bg_fisher_metric}.) Natural gradient descent replaces $\nabla F$ by $g^{-1}\nabla F$, which is invariant under reparameterizations. Central object: the natural gradient $\tilde{\nabla}_\theta F = g^{-1}(\theta)\,\nabla_\theta F$, which is the unique reparameterization-invariant direction of steepest descent on the statistical manifold.

4. **Bayesian Mechanics** (§\ref{sec:bayesian_mechanics_results}): Generalizes inference dynamics into Fokker–Planck equations, non-equilibrium steady states (NESS), and solenoidal flows defined by skew-symmetric boundaries (Markov blankets) [@parr2018markov; @friston2021stochastic]. Sakthivadivel (2023) [@sakthivadivel2023bayesian] formalized Bayesian mechanics as "a physics of and by beliefs," while Friston et al. (2023) [@friston2024path] provided the most mathematically precise treatment via path integrals and particular kinds. This layer connects cognitive inference to non-equilibrium statistical mechanics through the Helmholtz decomposition of probability flows. Central object: the Helmholtz-decomposed probability current $J(x) = -(D + Q(x))\,\nabla F(x)$ with $Q = -Q^{\!\top}$ (skew/solenoidal part) and $D$ symmetric positive-semidefinite (dissipative part), satisfying $\nabla \cdot J = 0$ at NESS.

5. **Thermodynamic Foundations** (catalogue rows including **fep-013, fep-025, fep-030, fep-031, fep-037, fep-049, fep-050**): Extends the FEP to thermodynamic potentials, Gibbs free energy, the Jarzynski equality [@jarzynski1997nonequilibrium], and Landauer's principle [@landauer1961irreversibility]. These formalisms connect the variational framework to established results in statistical mechanics, providing a physical grounding for the information-theoretic constructs [@pavliotis2014stochastic]. Central object: the **free-energy bridge** $F_{\text{var}} = F_{\text{Helmholtz}} - kT\,\ln Z$, which identifies the variational free energy with the Helmholtz free energy up to an additive constant given by the log-partition function; this is the identity that makes FEP a bona fide physical theory rather than a purely information-theoretic one.

### The Formalization Gap {#sec:the_formalization_gap}

Despite this mathematical richness, the FEP's constructs have not previously been subjected to systematic machine-verified scrutiny. This is the **verification gap** introduced in §\ref{sec:the_verification_gap_in_mathematical_physics}: informal FEP mathematics—expressed in journal LaTeX with silent assumptions about measurability, dominating measures, and policy types—has lacked a kernel-checked counterpart in any dependent type theory. Table 1 summarizes the formalization status of key concepts prior to this work.

| FEP Concept | Informal Status | Formalized Here? | Computational Implementation |
|------------|----------------|:-----------------:|------------------------------|
| KL non-negativity | Textbook result | No (already in Mathlib4) | N/A (analytical) |
| Variational free energy bound | Core FEP claim | Yes | SPM/MATLAB, pymdp |
| EFE decomposition | Debated [@maheu2026reframing] | Yes | pymdp |
| Markov blanket partition | Critiqued [@biehl2021critique] | Yes | None formalized |
| Solenoidal/NESS decomposition | Advanced theory | Yes | Numerical only |
| Fisher information metric | Classical result | Yes | SymPy, JAX |
| Softmax policy selection | Standard ML | Yes | PyTorch, JAX |
| Conjugate prior update | Bayesian statistics | Yes | Stan, PyMC |

_Formalization status of key FEP concepts prior to this work. "Computational implementation" refers to numerical simulation; none represent formal verification._

## Interactive Theorem Proving: Lean 4 and Mathlib {#sec:interactive_theorem_proving_lean_4_and_mathlib}

Lean 4 is a functional programming language and interactive theorem prover (ITP) that provides a Calculus of Inductive Constructions for formalizing mathematics [@moura2021lean]. The Lean 4.0.0 release in 2023 coincided with Mathlib's port from Lean 3, establishing **Mathlib4** [@mathlib2020] as the single largest actively maintained formal mathematics library in use today—containing over 60,000 verified declarations for topology, measure theory, category theory, and geometry, and serving as the target of landmark formalization efforts including the Liquid Tensor Experiment for condensed mathematics [@scholze2022liquid] and the polynomial Freiman–Ruzsa proof in Lean 4 [@pfr2023lean]. The pinned toolchain for this work is **`{{lean_toolchain}}`** paired with Mathlib4 **`{{mathlib_tag}}`** at the corresponding revision (see `lean/lean-toolchain` and `lean/lakefile.lean`).

### Type Theory Foundations and Tactic Mode {#sec:type_theory_foundations}

Lean 4 rests on the Calculus of Inductive Constructions (CIC), a dependent type theory in which propositions and types are the same kind of object. A proof of proposition `P` is a term of type `P`; consequently, the kernel that type-checks terms is the same kernel that verifies proofs. Writing a proof in Lean is therefore identical to writing a program whose type is the statement of the theorem. Users rarely write proof terms directly; instead, they invoke *tactics*—metaprograms that incrementally build the term. A proof in tactic mode takes the following shape:

```lean
theorem kl_nonneg {α : Type*} [MeasurableSpace α] (μ ν : Measure α)
    (habs : μ ≪ ν) : 0 ≤ klDiv μ ν := by
  rw [klDiv]
  positivity
```

Here `by` enters tactic mode, `rw` rewrites by the definition of `klDiv`, and `positivity` closes goals of the form `0 ≤ _` for a broad class of expressions. This style is introduced in depth in §\ref{sec:lean_4_a_primer_for_active_inference_researchers}.

### Why Lean 4 for Physical Theories? {#sec:why_lean_4_for_physical_theories}

Lean 4 offers four properties critical for formalizing the FEP:

1. **Dependent types with universe polymorphism**: Types can depend on values, enabling precise encoding of parameterized families of probability measures, finite policy spaces, and transition kernels. Universe polymorphism avoids the size issues that plague set-theoretic foundations when formalizing measure theory.

2. **Mathlib4's measure-theoretic stack**: The library provides formalized Bochner integration, Radon–Nikodym derivatives (`MeasureTheory.Measure.rnDeriv`), σ-algebra constructions, and probability kernels. Because a native `klDiv` primitive is not yet in Mathlib4—it is under active development via the Statistical Learning Theory project [@lean_slt2026]—KL divergence in our catalogue is constructed as the Radon–Nikodym-derivative integral $\int \log (dq/dp)\, dq$ (i.e., `∫ x, Real.log ((μ.rnDeriv ν) x) ∂μ`), which requires only absolute continuity $\mu \ll \nu$ and integrability of the log-density. This infrastructure directly supports the variational calculus underlying the FEP.

3. **Advanced proof automation**: The pinned Lean 4 `{{lean_toolchain}}` toolchain and Mathlib4 `{{mathlib_tag}}` supply automation including the `grind` tactic (SMT-style), `positivity`, and related solvers. These capabilities expand the range of FEP theorems that can be verified without manual proof construction; newer releases add further improvements.

4. **Active LLM–ITP ecosystem**: The Lean 4 community has attracted the most LLM-integration tooling of any proof assistant, including LeanDojo [@yang2024leandojo], Lean Copilot [@song2025copilot], LEGO-Prover [@xin2024lego], and compatibility with AlphaProof-style reinforcement learning approaches.

Modern physical theories, however, often outpace formalized repositories. Many concepts in Bayesian Mechanics—such as particular formulations of Langevin dynamics [@pavliotis2014stochastic] or curl-free vector fields—sit on the leading edge of physics, which renders them "aspirational" targets that require custom local axioms to satisfy the Lean compiler.

### Lean 4 Release Cadence and Tactic Evolution {#sec:lean4_release_cadence}

Lean 4 has maintained a rapid release cadence. The repository pins **`{{lean_toolchain}}`** in `lean/lean-toolchain`; later releases add further automation and ergonomics beyond what this paper's lemmas rely on.

This evolution directly shapes our pipeline's capabilities: each new tactic and automation improvement expands the set of FEP theorems that can be upgraded from "partial" (containing `sorry`) to "real".

### Prior Formalization Work in Adjacent Domains {#sec:prior_formalization_work}

A range of prior efforts have formalized parts of cognitive science, statistical mechanics, or information theory in interactive theorem provers. None targets the FEP directly, but each offers methodological lessons:

| Project | System | Domain | Scope | Relevance to FEP |
|---------|--------|--------|-------|------------------|
| Hammers for Helmholtz [@avigad2017] | Lean 3 | Real analysis / measure theory | Foundational | Provides the measure-theoretic backbone reused in Mathlib4 |
| Information-theoretic inequalities [@mehtaMetaIT2021] | Isabelle/HOL | Classical information theory | Shannon entropy, mutual information | Complementary to KL-based FEP work |
| Formalized statistical mechanics [@paulson2022thermo] | Isabelle/HOL | Classical thermodynamics | Partition functions, entropy | Thermodynamic catalogue rows build on analogous ideas |
| LeanDojo [@yang2024leandojo] | Lean 4 | Proof search benchmarks | Retrieval-augmented LLM | Demonstrates tractability of LLM ↔ Lean interfaces |
| Statistical Learning Theory in Lean [@lean_slt2026] | Lean 4 | ML theory | KL divergence, concentration | Direct upstream target for our KL usage |
| Categorical ontology / classical simulation [@namjoshi2026fundamentals] | Lean 4 | Foundations | Definitions of classical / quantum systems | Adjacent formalization of physical theories |

The landscape shows that adjacent domains have proven tractable, but no prior work has attempted a systematic, catalogue-scale formalization of the FEP specifically.

## The LLM–ITP Bridge {#sec:the_llm_itp_bridge}

The integration of Large Language Models with interactive theorem provers has accelerated dramatically since 2023, yielding several landmark systems:

| System | Year | Approach | Benchmark | Key innovation |
|--------|------|----------|-----------|----------------|
| LeanDojo [@yang2024leandojo] | 2024 | Retrieval-augmented | LeanDojo Benchmark | Grounded tactic suggestion via premise retrieval |
| Baldur [@first2023draft] | 2023 | Whole-proof generation | miniF2F | End-to-end proof generation + repair |
| LEGO-Prover [@xin2024lego] | 2024 | Modular growing libraries | miniF2F | Reusable lemma construction |
| DeepSeek-Prover [@deepseek2024prover] | 2024 | RL from proof feedback | miniF2F | RLPAF — reinforcement learning from proof assistant feedback |
| AlphaGeometry [@trinh2024alphageometry] | 2024 | Neuro-symbolic | IMO Geometry | Synthetic data + symbolic deduction |
| AlphaProof [@alphaproof2024] | 2024 | Gemini + AlphaZero | IMO 2024 | Silver-medal level problem solving |
| Lean Copilot [@song2025copilot] | 2025 | Editor integration | N/A | Real-time tactic suggestion in VSCode |
| DeepSeek-Prover-V2 [@deepseek2025proverv2] | 2025 | RL + subgoal decomposition | miniF2F, ProofNet | Reinforcement learning for structured proof planning |

These systems share a common focus: they solve _existing_ mathematical problems within established libraries. The challenge of _axiomatizing a physical theory_—where the target concepts (Markov blankets, solenoidal flows, Expected Free Energy decompositions) may not yet have formal counterparts in any library—is fundamentally different. Our work addresses this axiomatization challenge, using LLMs not to find proofs but to translate informal mathematical physics into well-typed formal specifications.

### The Axiomatization vs. Problem-Solving Distinction {#sec:the_axiomatization_vs_problem_solving_distinction}

The distinction between proof search and theory axiomatization is worth making precise:

- **Proof search** (LeanDojo, DeepSeek-Prover): given a well-typed theorem statement, find a proof term. The statement already exists in a formal language; the challenge is navigating the proof space.
- **Theory axiomatization** (this work): given an informal mathematical theory (published in journals, written in natural language with embedded LaTeX), produce well-typed theorem statements, definitions, and structural lemmas. The challenge is _translation from informal to formal_, not proof search.

This distinction explains why our pipeline emphasizes `sorry`-based maturity assessment rather than proof-completion rates: the primary contribution is demonstrating that FEP constructs _can be stated_ in Lean 4's type system, not that they have been fully proven.

## The FEP Debate and the Case for Formalization {#sec:the_fep_debate_and_the_case_for_formalization}

The mathematical status of the FEP has been actively debated in the literature, along three principal lines of critique:

1. **Blanket conditions.** The partition of states into internal, external, sensory, and active components is not always well-defined for arbitrary dynamical systems ([@biehl2021critique]). Specifically, Biehl et al. demonstrate that *"various definitions of the 'Markov blanket' proposed in different works are not equivalent"* and that crucial vector-field rewritings are not generally correct absent previously unstated assumptions. The canonical Markov-blanket claim is that the state space admits a factorization $X = \Psi \times B \times H$ (external, blanket, internal) such that the blanket $b = (s, a)$ renders external and internal states conditionally independent,
\begin{equation}\label{eq:eq_markov_blanket}
p(\psi, \eta \mid b) \;=\; p(\psi \mid b)\,p(\eta \mid b)\qquad\text{(conditional independence given the blanket)}.
\end{equation}
Eq.~\ref{eq:eq_markov_blanket} is a *statistical* condition about a specific family of joint densities, and whether a given dynamical system satisfies it depends on the system's drift, diffusion, and steady-state structure—properties that are not determined by the choice of state-space partition alone. The blanket partition sits at the intersection of two very different objects: an algebraic/set-theoretic decomposition of the state space, and a measure-theoretic conditional-independence statement about its dynamics. Conflating the two is precisely the locus of Biehl et al.'s critique. Accordingly, **fep-005** in our catalogue formalizes only the *algebraic* side—that $X$ admits a 4-part disjoint cover $\{\Psi, S, A, H\}$ with $\Psi \cup S \cup A \cup H = X$ and pairwise empty intersections—without asserting the dynamical conditional-independence in Eq.~\ref{eq:eq_markov_blanket}. This is a deliberately modest formal claim: it renders transparent which portion of the Markov-blanket machinery is settled by partition bookkeeping and which portion requires additional hypotheses about the system's transition kernel, separating honest structural content from aspirational dynamical content.

2. **Particular partitions.** The broader applicability of the "particular physics" framework has been questioned, with arguments that certain assumptions about steady-state densities are unduly restrictive ([@aguilera2022particular]). Concretely, the "particular-physics" construction assumes that a stochastic system with dynamics $\mathrm{d}x = f(x)\mathrm{d}t + \sigma\,\mathrm{d}W_t$ admits a non-equilibrium steady-state (NESS) density $p^{*}(x)$ such that the probability current decomposes as
\begin{equation}\label{eq:eq_helmholtz_current}
J(x) \;=\; -\bigl(D + Q(x)\bigr)\,\nabla F(x),\qquad F(x) := -\log p^{*}(x),
\end{equation}
with $D$ symmetric positive-semidefinite (the dissipative component), $Q(x)$ **antisymmetric**, i.e. $Q(x)^{\!\top} = -Q(x)$ (the solenoidal component), and the steady-state divergence condition $\nabla \cdot J(x) = 0$. Establishing all three conditions simultaneously requires both an *algebraic* fact (skew-symmetry of $Q$) and an *analytic/stochastic* fact (existence of the NESS density satisfying Eq.~\ref{eq:eq_helmholtz_current}). **fep-025** in our catalogue formalizes the algebraic piece precisely—namely, that if $Q$ is antisymmetric then $(-Q)^{\!\top} = -Q^{\!\top}$, equivalently $Q^{\!\top} = -Q \iff (-Q)^{\!\top} = -Q^{\!\top}$—and honestly labels this as a *necessary* algebraic condition for solenoidal structure rather than a full NESS proof. The sketch docstring explicitly defers the existence of $p^{*}$ and the divergence-free property to aspirational work; this again makes transparent which part of the critique (the algebraic part) is settled and which part (the stochastic-analytic part) still requires dedicated Fokker–Planck machinery that is absent from Mathlib4 at the pinned revision.

3. **Math and territorialism** (a deliberate nod to the classic "map and territory" distinction and to the "territorialism" of notational regionalisms across fields). It has been argued that FEP derivations sometimes conflate distinct mathematical objects—using the same notation for different quantities in different contexts ([@andrews2021math]). Lean 4's strict type system makes such conflations impossible: a `Measure ℝ` is computationally distinct from an $\mathbb{R}$-valued function, and the compiler rigidly enforces this isolation at every step.

These debates motivate the present work: formal verification in Lean 4 does not adjudicate the underlying semantic disagreements, but it does force every assumption to be explicit and every inference step to be machine-checked, so that disputes separate cleanly into those that survive formalization and those that do not.

## Recent Developments (2024–2026) {#sec:recent_developments_20242026}

Recent developments reveal a widening gap between the FEP's theoretical ambitions and its interactive formalization. On the theoretical side, 2024–2026 produced significant advances: path-integral and geometric reframings of Bayesian mechanics [@sakthivadivel2023bayesian; @friston2024path], unification of divergent Expected Free Energy formulations [@champion2026reframing], and extensions of Active Inference into phenomenological and cognitive modeling domains. Meanwhile, Lean 4's formalization community has concentrated on discrete mathematics, polynomial reasoning, and statistical learning theory rather than continuous physical theories. No substantive intersection between these macroscopic generative models and interactive type verification materialized during this period. This structural gap motivates the present work: bridging informal FEP mathematics to Lean 4's type system requires a dedicated translation pipeline, not a repurposing of existing proof-search tools. By anchoring each informal construct to a compiler-verified Lean 4 sketch, the catalogue supplies the formal axiomatization infrastructure needed to rigorously evaluate competing formalizations as the theory continues to evolve — transforming what are currently aesthetic or rhetorical disputes about mathematical rigor into machine-checkable proof obligations with unambiguous pass/fail outcomes.
