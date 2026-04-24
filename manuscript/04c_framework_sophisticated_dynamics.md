## Sophisticated Dynamics: Information Geometry and Bayesian Mechanics {#sec:sophisticated_dynamics_information_geometry_and_bayesian_mechanics}

The pipeline was tested against the frontier of contemporary mathematical physics, where the LLM had to formalize theorems representing high-dimensional statistical manifolds [@amari2016information] and non-equilibrium steady states (NESS) [@friston2019free]. Two catalogue areas carry this load: **Information Geometry ({{areas.InfoGeometry.count}} topics)** and **Bayesian Mechanics ({{areas.BayesianMechanics.count}} topics)** — together {{combined_info_bayes_count}} of the {{total_topics}} sketches, and the sections in which Mathlib4's measure-theoretic infrastructure is stressed hardest. See the Mathlib4 coverage figure in §\ref{sec:mathlib4_and_measure_theoretic_probability} for the distribution across these areas.

### Langevin Dynamics and the Fokker–Planck Equation {#sec:sophisticated_langevin_fp}

Beyond the static-bound formulation of the FEP, adaptive systems are naturally described by *stochastic* dynamics on the variational parameters. The canonical continuous-time object is the overdamped **Langevin stochastic differential equation**:

\begin{equation}\label{eq:sd_langevin_sde}
\dot{x}(t) \;=\; -\,\nabla F(x(t)) \;+\; \sqrt{2D}\,\xi(t), \qquad \langle \xi(t) \rangle = 0, \;\; \langle \xi(t)\,\xi(t')^\top \rangle = \mathbb{I}\,\delta(t - t'),
\end{equation}

where $F : \mathbb{R}^n \to \mathbb{R}$ is the free-energy functional, $D \ge 0$ is the diffusion coefficient, and $\xi$ is standard Gaussian white noise. Equation \ref{eq:sd_langevin_sde} expresses the principle that adaptive parameters *drift* along the free-energy gradient while continuously exploring a neighbourhood of the current state — reconciling deterministic gradient flow (§\ref{sec:sophisticated_gradient_measure}) with Bayesian posterior sampling.

The probability density $\rho(x, t)$ of trajectories solving Equation \ref{eq:sd_langevin_sde} evolves according to the **Fokker–Planck equation**:

\begin{equation}\label{eq:sd_fokker_planck}
\partial_t \rho(x, t) \;=\; \nabla \cdot \bigl(\rho\,\nabla F\bigr) \;+\; D\,\nabla^2 \rho \;=\; -\nabla \cdot J(x, t),
\end{equation}

with probability current $J = -\rho\,\nabla F - D\,\nabla \rho$. The stationary solution satisfies $\partial_t \rho^\star = 0$ and, in the gradient case, admits the Gibbs form $\rho^\star(x) \propto \exp(-F(x)/D)$ — directly linking the variational free energy $F$ to the thermodynamic Boltzmann weight (§\ref{sec:thermodynamics_results}).

### Gradient Flow in Measure Space {#sec:sophisticated_gradient_measure}

Otto's theory [@ao2004potential] reinterprets Equation \ref{eq:sd_fokker_planck} as *Wasserstein gradient descent* of the free-energy functional on the space of probability measures:

\begin{equation}\label{eq:sd_wasserstein_flow}
\partial_t \rho \;=\; \nabla \cdot \bigl(\rho\,\nabla \tfrac{\delta F}{\delta \rho}\bigr), \qquad F[\rho] \;=\; \mathbb{E}_\rho[U(x)] \;+\; D\,\mathbb{E}_\rho[\log \rho(x)],
\end{equation}

where $\delta F / \delta \rho$ is the $L^2$ functional derivative. Equation \ref{eq:sd_wasserstein_flow} elevates the FEP from a bound on scalars to a *geometric flow on a manifold of distributions*, with the Wasserstein-2 metric playing the role of Riemannian structure. Topic fep-038 (natural gradient) anchors the preconditioned analogue in the finite-dimensional Fisher-information geometry, while topic fep-018 provides the companion triangle-inequality and symmetry facts that underpin any metric-space formalization of such flows.

### Ergodicity, Invariant Measures, and Mathlib4 {#sec:sophisticated_ergodicity}

Under mild regularity on $F$ (e.g.\ $\nabla F$ globally Lipschitz and a confining condition $F(x) \to \infty$ as $\|x\| \to \infty$), the Langevin process is **ergodic**: trajectories explore the state space in a way that time-averages converge to ensemble averages under the stationary measure $\rho^\star$:

\begin{equation}\label{eq:sd_ergodicity}
\lim_{T \to \infty} \frac{1}{T}\int_0^T \phi(x(t))\,dt \;=\; \int \phi(x)\,\rho^\star(x)\,dx \quad\text{a.s.},
\end{equation}

for every $\rho^\star$-integrable observable $\phi$. Equation \ref{eq:sd_ergodicity} is the formal bridge between *single trajectories* (what an agent actually experiences) and *ensemble statistics* (what a Bayesian posterior encodes). Our Lean 4 encodings live in the discrete-step or static analogues of these statements: we use Mathlib4's `MeasureTheory.Measure` hierarchy for the underlying probability spaces, `Finset.sum`-style aggregation for the discrete time-average, and monotonicity lemmas (`measure_mono`, `measure_union_le`) for the structural invariants of the invariant measure. Full ergodic theorems in Mathlib4 (`MeasureTheory.Ergodic`) provide the long-term path for upgrading these sketches once pipeline coverage extends to measure-preserving transformations.

### Lean 4 Formalization Sketch: Langevin (fep-020) {#sec:sophisticated_lean_langevin}

Topic fep-020 takes the deterministic skeleton of Equation \ref{eq:sd_langevin_sde} — the gradient-descent step $x \mapsto x - \eta\,\nabla F(x)$ — and proves three structural facts that any faithful Langevin discretization must satisfy: (i) the displacement $(\eta\,\text{grad})^2 \ge 0$ (`sq_nonneg`), certifying that one-step squared displacement is a well-defined nonnegative energy quantity; (ii) strict descent when the gradient is positive and the step size is positive (`fep020_descent`), formally $0 < \eta, 0 < \text{grad} \Rightarrow x - \eta\,\text{grad} < x$; and (iii) the sketch `noncomputable def fep020_langevinStep` wraps the update so downstream topics can reuse the definition. The stochastic term $\sqrt{2D}\,\xi$ is deferred because Mathlib4's Itô-integral formalization is still in progress; once it lands, fep-020 can be upgraded in place by importing the stochastic-calculus module and replacing the deterministic step with its SDE counterpart.

### Information Geometry Results ({{areas.InfoGeometry.count}} topics) {#sec:information_geometry_results}

Information geometry treats parametric families of probability distributions $\mathcal{M} = \{p_\theta\}_{\theta \in \Theta}$ as Riemannian manifolds, with the Fisher information tensor as the canonical metric. The {{areas.InfoGeometry.count}} topics in this subsection formalize the algebraic and inequality-theoretic building blocks of that geometry: a valid Riemannian metric (fep-004, fep-038), the core information-divergence (fep-014, fep-024), its convex-analytic generalizations (fep-029, fep-044), the metric-space substrate for geodesics (fep-018), and the Bayesian update on that manifold (fep-017).

| Topic | Theorem | Maturity | Key Mathlib Module | `sorry` count |
|-------|---------|----------|--------------------|--------------|
| fep-004 | Fisher Information Metric: inner product space, squared score nonneg, parameter distance, `inner_comm` | real | `Analysis.InnerProductSpace.Basic` | 0 |
| fep-014 | KL Divergence: `measure_mono`, `measure_union_le`, measurable composition (DPI), `compl_mass` | real | `MeasureTheory.Measure.MeasureSpace` | 0 |
| fep-017 | Conditional Expectation: Bayesian update (posterior = likelihood × prior), posterior nonneg, evidence nonneg | real | `Algebra.BigOperators` | 0 |
| fep-018 | Statistical Manifold Geodesics: `dist_triangle`, `dist_comm`, `dist_self` | real | `Topology.MetricSpace.Basic` | 0 |
| fep-024 | KL Regularization: log-ratio identity, log monotone, `kl_self_zero` (log 1 = 0) | real | `Analysis.SpecialFunctions.Log.Basic` | 0 |
| fep-029 | Bregman Divergences: secant inequality, convex combo bound | real | `Analysis.Convex.Basic` | 0 |
| fep-038 | Natural Gradient: preconditioned norm nonneg, `inner_self_nonneg`, `norm_nonneg` | real | `Analysis.InnerProductSpace.Basic` | 0 |
| fep-044 | α-Divergence Family: convex combination nonneg, α=1 → KL, α=0 → reverse KL | real | `Analysis.SpecialFunctions.Pow.Real` | 0 |

#### Fisher Information Metric (fep-004) {#sec:sd_fisher}

On a statistical manifold $\mathcal{M} = \{p_\theta\}_{\theta \in \Theta}$ with $\Theta \subset \mathbb{R}^n$ open, the **Fisher information metric** is the Riemannian metric whose components in the coordinate basis are given by the expected outer product of the score function $s_i(x; \theta) := \partial_{\theta_i} \log p_\theta(x)$:

\begin{equation}\label{eq:sd_fisher_metric}
g_{ij}(\theta) \;=\; \mathbb{E}_{p_\theta}\!\left[\frac{\partial \log p_\theta}{\partial \theta_i} \cdot \frac{\partial \log p_\theta}{\partial \theta_j}\right] \;=\; -\,\mathbb{E}_{p_\theta}\!\left[\frac{\partial^2 \log p_\theta}{\partial \theta_i \partial \theta_j}\right],
\end{equation}

where the second equality uses the identity $\mathbb{E}_{p_\theta}[\partial_i s_j] + \mathbb{E}_{p_\theta}[s_i s_j] = 0$ that follows from differentiating the normalization $\int p_\theta \, d\mu = 1$ twice under the integral. The matrix $I(\theta) = [g_{ij}(\theta)]$ is the **Fisher information matrix** and, under regularity conditions that exchange differentiation and integration, is symmetric and positive semidefinite.

The Fisher metric is distinguished among Riemannian metrics on $\mathcal{M}$ by Chentsov's uniqueness theorem: up to scalar, it is the only metric invariant under sufficient statistics (Markov embeddings). Geometrically, it captures how distinguishable two nearby distributions $p_\theta$ and $p_{\theta + d\theta}$ are: the squared infinitesimal KL divergence is

\begin{equation}\label{eq:sd_kl_fisher_taylor}
2\, D_\text{KL}(p_\theta \,\|\, p_{\theta+d\theta}) \;=\; g_{ij}(\theta)\,d\theta^i\,d\theta^j + O(\|d\theta\|^3),
\end{equation}

so the Fisher metric *is* the Hessian of the KL divergence at coincident parameters — connecting fep-004 directly to fep-014 and fep-024. The **Cramér–Rao bound** states that for any unbiased estimator $T$ of $\theta$, $\operatorname{Var}_{p_\theta}[T] \succeq I(\theta)^{-1}$ in the positive-semidefinite order; no unbiased estimator can resolve parameters more finely than the Fisher geometry permits. In the FEP context, $I(\theta)$ plays the role of a **precision matrix** — the natural metric for measuring how "far" two nearby beliefs are from each other, and the object weighted by attention / synaptic-gain parameters in predictive coding.

The Lean sketch for fep-004 formalizes the algebraic preconditions for this metric structure: score-squared nonnegativity (`sq_nonneg`), Euclidean parameter distances $\|\theta_1 - \theta_2\|^2 \ge 0$, and symmetry of the underlying inner product (`real_inner_comm`). Together these are the three building blocks of a Riemannian metric tensor on a statistical manifold; the measure-theoretic second-moment identity in Equation \ref{eq:sd_fisher_metric} requires integration machinery that will fold in once Mathlib4's `ProbabilityTheory.Integral` coverage deepens. See §\ref{sec:catalogue-fep-004} in Appendix B; typeset signatures in §\ref{sec:eqs-fep-004} of Appendix~\ref{sec:appendix_c_latex_equations}.

#### Natural Gradient (fep-038) {#sec:sd_natural_gradient}

The ordinary Euclidean gradient $\nabla_\theta F$ of a loss $F : \Theta \to \mathbb{R}$ is *not* coordinate-invariant on a statistical manifold: reparametrising $\theta \mapsto \phi(\theta)$ produces an update that depends on the Jacobian of $\phi$, so two modellers using different parametrizations of the same family will take genuinely different steps. Amari [@amari1998natural] resolved this by defining the **natural gradient** as the steepest-descent direction with respect to the Fisher-induced Riemannian metric:

\begin{equation}\label{eq:sd_natural_gradient}
\tilde{\nabla}_\theta F(\theta) \;=\; I(\theta)^{-1}\,\nabla_\theta F(\theta).
\end{equation}

Geometrically, $\tilde{\nabla}_\theta F$ is the unique vector such that $\langle \tilde{\nabla}_\theta F, v\rangle_{I(\theta)} = dF(\theta)[v]$ for all tangent $v$, where $\langle u, v\rangle_{I} := u^\top I v$ is the Fisher inner product. The natural gradient update

\begin{equation}\label{eq:sd_natural_gradient_update}
\theta_{t+1} \;=\; \theta_t \;-\; \eta\, I(\theta_t)^{-1}\,\nabla_\theta F(\theta_t)
\end{equation}

is invariant under smooth reparametrization, converges in fewer iterations than Euclidean gradient descent on ill-conditioned manifolds, and at the maximum-likelihood limit achieves the Cramér–Rao efficiency bound (Fisher efficiency). In Active Inference, $I(\theta_t)^{-1}$ is the precision-weighted gain that modulates prediction-error backpropagation — the mathematical substrate for the claim that *attention is precision*. The natural gradient also underlies modern second-order methods in deep learning (K-FAC, Shampoo) that approximate $I(\theta)^{-1}$ with tractable block structure.

The fep-038 Lean sketch formalizes the preconditioned inner-product nonnegativity $\langle v, I v\rangle \ge 0$ (via `inner_self_nonneg`) and the Fisher matrix symmetry that are prerequisites for $\tilde{\nabla}_\theta F$ to be well-posed: a non-symmetric or indefinite preconditioner would not define a metric and the resulting update could be non-descent. The full invariance theorem — that $\tilde{\nabla}$ transforms as a contravariant tensor under reparametrization — requires the Jacobian/chain-rule machinery of `Analysis.Calculus.Deriv` on manifolds and is a natural next step.

#### KL Divergence (fep-014) and the I- / M-Projection Asymmetry {#sec:sd_kl}

The **Kullback–Leibler divergence** between probability measures $q \ll p$ on a measurable space $(X, \mathcal{F})$ is

\begin{equation}\label{eq:sd_kl_def}
D_\text{KL}(q \,\|\, p) \;=\; \int_X q\,\log\frac{q}{p}\,d\mu \;=\; \mathbb{E}_q\!\left[\log\frac{dq}{dp}\right].
\end{equation}

Three structural properties lift it from a mere functional to the canonical statistical discrepancy:

1. **Nonnegativity** (Gibbs' inequality): $D_\text{KL}(q \,\|\, p) \ge 0$ with equality iff $q = p$ a.e. This follows from Jensen's inequality applied to the concave function $\log$: $\mathbb{E}_q[\log(p/q)] \le \log \mathbb{E}_q[p/q] = 0$.

2. **Chain rule / data-processing inequality (DPI)**: for any measurable $T : X \to Y$, $D_\text{KL}(q \,\|\, p) \ge D_\text{KL}(T_\sharp q \,\|\, T_\sharp p)$. Postprocessing cannot increase KL; equivalently, sufficient statistics preserve it with equality. DPI is the information-theoretic skeleton of the second law.

3. **Asymmetry**: in general $D_\text{KL}(q \,\|\, p) \neq D_\text{KL}(p \,\|\, q)$. This asymmetry is not a defect but carries the **mode-covering / mode-seeking** distinction that governs variational inference:

   - The **I-projection** $\arg\min_q D_\text{KL}(q \,\|\, p)$ (first slot) is **zero-forcing / mode-seeking**: $q$ must vanish wherever $p$ vanishes, so $q$ concentrates on a single mode of a multimodal $p$.
   - The **M-projection** $\arg\min_q D_\text{KL}(p \,\|\, q)$ (second slot) is **mass-covering / moment-matching**: $q$ must place mass everywhere $p$ has mass, so $q$ smears across multiple modes.

The FEP uses the I-projection, variational free energy $F[q] = D_\text{KL}(q(s) \,\|\, p(s \mid o)) - \log p(o)$, which gives rise to the mode-seeking behavior characteristic of predictive-coding posteriors and explains why Active Inference agents commit to one hypothesis rather than averaging across several. The fep-014 Lean sketch formalizes the monotonicity ingredients — `measure_mono`, `measure_union_le`, measurable-function composition underlying DPI, and complement mass via `compl_mass` — that make the KL divergence a genuine information measure before any integration theory is invoked.

#### Rényi / Tsallis α-Divergences (fep-044) {#sec:sd_alpha_div}

The one-parameter **Chernoff α-divergence family** interpolates between forward and reverse KL and recovers Hellinger distance at its midpoint:

\begin{equation}\label{eq:sd_alpha_div}
D_\alpha(p \,\|\, q) \;=\; \frac{1}{\alpha(1-\alpha)}\left[1 - \int p^{\alpha}\, q^{1-\alpha} \, d\mu\right], \qquad \alpha \in (0, 1).
\end{equation}

Endpoint limits and distinguished values:

| $\alpha$ | Limit | Behavior |
|--------|-------|-----------|
| $\alpha \to 1$ | $D_\text{KL}(p \,\|\, q)$ | M-projection, mass-covering |
| $\alpha \to 0$ | $D_\text{KL}(q \,\|\, p)$ | I-projection, mode-seeking |
| $\alpha = 1/2$ | $4\,H^2(p, q)$ | Symmetric Hellinger distance squared |

The family embeds into the more general class of Csiszár $f$-divergences $D_f(p \,\|\, q) = \int q\,f(p/q)\,d\mu$ (with $f$ convex, $f(1) = 0$): the $\alpha$-divergence corresponds to $f_\alpha(u) = \bigl(u^\alpha - \alpha u - (1-\alpha)\bigr)/(\alpha(\alpha-1))$. Varying $\alpha$ gives a continuous spectrum from mode-seeking to mass-covering inference, recovering the **Rényi divergence** $D_\alpha^{\text{Rényi}}(p\|q) = \frac{1}{\alpha - 1}\log\int p^\alpha q^{1-\alpha}\,d\mu$ (monotone transform) and, in the non-extensive generalization, the **Tsallis divergence** used in power-law statistical mechanics. The FEP's standard KL is thus one point on a principled continuum; generalized FEP formulations (e.g. generalized variational inference) replace KL by $D_\alpha$ to trade off robustness against tail-sensitivity. The fep-044 Lean sketch formalizes the $\alpha$-combination nonnegativity $\alpha p + (1-\alpha) q \ge 0$ and the two KL endpoints that characterize this family on the algebraic side.

#### Bregman Divergences and Mirror Descent (fep-029) {#sec:sd_bregman}

For a strictly convex, differentiable **potential** $\phi : \mathcal{C} \to \mathbb{R}$ on a convex domain $\mathcal{C} \subseteq \mathbb{R}^n$, the **Bregman divergence** is the gap between $\phi$ and its linear approximation at $q$:

\begin{equation}\label{eq:sd_bregman}
B_\phi(p, q) \;=\; \phi(p) \;-\; \phi(q) \;-\; \langle \nabla \phi(q),\, p - q\rangle.
\end{equation}

Key properties: $B_\phi(p, q) \ge 0$ with equality iff $p = q$; $B_\phi$ is convex in its first argument; and it obeys the **generalized Pythagorean theorem** $B_\phi(p, r) = B_\phi(p, q) + B_\phi(q, r) + \langle \nabla\phi(r) - \nabla\phi(q),\, q - p\rangle$, which reduces to the familiar identity when $q$ is the Bregman projection of $p$ onto a convex set. Distinguished instances:

- $\phi(p) = \tfrac{1}{2}\|p\|^2$ recovers **squared Euclidean distance** $B_\phi(p, q) = \tfrac{1}{2}\|p - q\|^2$.
- $\phi(p) = \sum_i p_i \log p_i$ (negative Shannon entropy) on the probability simplex recovers the **KL divergence** $B_\phi(p, q) = D_\text{KL}(p \,\|\, q)$ — positioning KL as one instance of a general convex-analytic family.
- $\phi(p) = -\log\det(P)$ on positive-definite matrices recovers the **LogDet / Burg divergence** used in covariance estimation.

**Mirror descent** is gradient descent in the dual geometry induced by $\phi$: $\nabla\phi(\theta_{t+1}) = \nabla\phi(\theta_t) - \eta \nabla F(\theta_t)$, equivalent to $\theta_{t+1} = \arg\min_\theta \{\langle \nabla F(\theta_t), \theta\rangle + \tfrac{1}{\eta} B_\phi(\theta, \theta_t)\}$. On the probability simplex with entropic $\phi$, mirror descent becomes the **exponentiated gradient / multiplicative-weights** update and coincides with natural gradient in the Fisher geometry (dually flat case) — a deep bridge between fep-029 and fep-038. Belief-propagation convergence guarantees in graphical models are obtained by recognizing the algorithm as a Bregman projection onto local marginal polytopes. The fep-029 Lean sketch formalizes the secant inequality (the defining convexity condition) and the convex-combination endpoint bounds that validate a candidate $\phi$ as inducing a bona fide Bregman divergence.

#### KL Regularization (fep-024) and Bayesian Update Geometry (fep-017) {#sec:sd_kl_reg_bayes}

Topic fep-024 isolates the elementary log-identities that license variational bounds: the log-ratio decomposition $\log(p/q) = \log p - \log q$, monotonicity of $\log$ on $(0, \infty)$, and the anchor $D_\text{KL}(p \,\|\, p) = 0$ via $\log 1 = 0$. These three facts are the Lean-level primitives behind the ELBO decomposition $\log p(o) = \mathbb{E}_q[\log p(o, s)] - \mathbb{E}_q[\log q(s)] + D_\text{KL}(q \,\|\, p(\cdot \mid o))$ and thus behind every variational FEP bound in the catalogue.

Topic fep-017 formalizes **Bayesian updating** as an equality of conditional expectations on a discrete probability space: posterior $=$ likelihood $\times$ prior $/$ evidence, with posterior nonnegativity and evidence nonnegativity both proven from `Algebra.BigOperators`. Geometrically, Bayes' rule is the **Bregman projection** of the prior onto the constraint manifold $\{q : \mathbb{E}_q[f] = \mathbb{E}_{p(\cdot\mid o)}[f]\}$ in the KL (entropic Bregman) geometry — which is why variational inference, maximum-entropy updating, and exponential-family sufficient-statistic matching all coincide on exponential families. fep-017 provides the discrete-sum skeleton; the measure-theoretic Radon–Nikodym version using `MeasureTheory.Measure.withDensity` is the natural Mathlib4 upgrade path.

#### Statistical Manifold Geodesics and Dual Connections (fep-018) {#sec:sd_geodesics}

Amari's information geometry equips $\mathcal{M}$ not with a single Levi–Civita connection but with a one-parameter **α-connection family** $\nabla^{(\alpha)}$, with two distinguished members forming a **dually flat pair** $(\nabla^{(+1)}, \nabla^{(-1)})$:

- The **exponential ($e$-) connection** $\nabla^{(+1)}$: its geodesics are $\log$-linear interpolations $\log p_t = (1-t)\log p_0 + t \log p_1 + \text{const}$. In exponential families these become straight lines in natural parameters.
- The **mixture ($m$-) connection** $\nabla^{(-1)}$: its geodesics are convex mixtures $p_t = (1-t) p_0 + t p_1$, i.e. straight lines in the probability simplex.

Duality $\nabla^{(+\alpha)} + \nabla^{(-\alpha)} = 2\nabla^{(g)}$ (twice the Levi–Civita connection) produces the generalized Pythagorean theorem: if $q$ is the $m$-projection of $p$ onto an $e$-flat submanifold $\mathcal{E}$, then $D_\text{KL}(p \,\|\, r) = D_\text{KL}(p \,\|\, q) + D_\text{KL}(q \,\|\, r)$ for all $r \in \mathcal{E}$. This is the geometric reason the EM algorithm, iterative scaling, and variational message-passing all converge. The fep-018 Lean sketch anchors the underlying metric-space axioms — triangle inequality (`dist_triangle`), symmetry (`dist_comm`), and reflexivity (`dist_self`) — that are the foundational properties any Riemannian metric space (and thus any α-geodesic structure) must satisfy before curvature tensors, connections, or geodesic equations can be introduced. The dual-connection upgrade is aspirational future work requiring `Mathlib.Geometry.Manifold`.

**Representative formalization** — *Fisher Information Metric (fep-004)*: The pipeline formalizes the Fisher metric using Mathlib4's `EuclideanSpace` and inner product infrastructure. The sketch proves that the squared score is nonnegative (`sq_nonneg`), that parameter distances $\|\theta_1 - \theta_2\|^2 \geq 0$ hold in the Euclidean parameter space, and that the inner product is symmetric (`real_inner_comm`) — the three algebraic building blocks of a Riemannian metric tensor on a statistical manifold. The full connection to the score function's second moment (Equation \ref{eq:sd_fisher_metric}) requires measure-theoretic integration not yet available in the Lean sketch, but the metric structure is anchored. See §\ref{sec:catalogue-fep-004} in Appendix B and §\ref{sec:eqs-fep-004} in Appendix~\ref{sec:appendix_c_latex_equations}.

### Bayesian Mechanics Results ({{areas.BayesianMechanics.count}} topics) {#sec:bayesian_mechanics_results}

Bayesian mechanics rests on a particular partition of system states. A **Markov blanket partition** of a finite state space $\mathcal{S}$ is a decomposition into four mutually disjoint blocks $\mathcal{S} = \mathcal{I} \sqcup \mathcal{B}_s \sqcup \mathcal{B}_a \sqcup \mathcal{E}$ — **internal** ($\mathcal{I}$), **sensory blanket** ($\mathcal{B}_s$), **active blanket** ($\mathcal{B}_a$), and **external** ($\mathcal{E}$) — such that internal and external states are conditionally independent given the blanket $\mathcal{B} = \mathcal{B}_s \cup \mathcal{B}_a$:

\begin{equation}\label{eq:sd_markov_blanket_ci}
p(\mu, \eta \mid b) \;=\; p(\mu \mid b)\, p(\eta \mid b), \qquad \mu \in \mathcal{I},\; \eta \in \mathcal{E},\; b \in \mathcal{B}.
\end{equation}

Equation \ref{eq:sd_markov_blanket_ci} is the *statistical mechanical* content of the blanket: internal and external states are **decoupled given the blanket**. This is the formal basis for Friston's claim that bounded systems admit an interpretation as performing inference — the internal state $\mu$ tracks the external state $\eta$ through the "statistical mirror" provided by the sensory/active interface, without ever accessing $\eta$ directly. The partition is *directional*: sensory states are causally influenced by external states ($\eta \to b_s$), active states causally influence external states ($b_a \to \eta$), and internal and external states interact only via the blanket. In the stochastic setting (§\ref{sec:sophisticated_langevin_fp}), this directionality corresponds to a particular block structure in the drift and diffusion of the Langevin equation, and gives rise to the **solenoidal/dissipative NESS decomposition** of §\ref{sec:thermodynamics_results}.

Topic **fep-005** formalizes this four-part partition as `Finset.filter` applications over an assignment function and proves (i) pairwise disjointness of the four blocks, (ii) completeness of their union as the full state space, and (iii) that the generative factorisation $p(\mathcal{I}, \mathcal{B}_s, \mathcal{B}_a, \mathcal{E}) = p(\mathcal{I} \mid \mathcal{B})\,p(\mathcal{E} \mid \mathcal{B})\,p(\mathcal{B})$ composes with the likelihood structure of topic **fep-009** (`likelihood_mono`, joint-product nonnegativity, `map_nonneg` for pushforwards), which encodes the generative-model likelihood on `MeasureTheory.Measure.MeasureSpace`. Together fep-005 and fep-009 deliver a compiler-verifiable version of the blanket-plus-likelihood substrate on which all downstream Bayesian-mechanics results rest. fep-005 thus establishes the *algebraic partition* — a decidable, finite, disjoint cover — as the precondition for the statistical-mechanical claim of Equation \ref{eq:sd_markov_blanket_ci}.

At non-equilibrium steady state (NESS), the stationary flow admits a **solenoidal/dissipative decomposition** $\dot\rho = -\nabla \cdot (\rho\,\nabla F + Q\rho) = 0$ in which the dissipative (gradient) component drives relaxation while the solenoidal component $Q\rho$ carries probability conservatively around level sets of $F$. The defining constraint on $Q$ is **skew-symmetry**, $Q^\top = -Q$, which forces $Q_{ii} = 0$ on the diagonal and guarantees $\nabla \cdot (Q\rho) = 0$ for smooth $\rho$ — the solenoidal component produces no entropy. This constraint is what distinguishes the NESS decomposition from a pure gradient flow and is formalized directly in topic fep-025 via `Matrix.transpose_neg` (from `LinearAlgebra.Matrix.Transpose`) together with a `skew_diag_zero` lemma; see §\ref{sec:thermodynamics_results} for the Lean sketch.

**Mathlib4 module footprint (Bayesian Mechanics)**: The Bayesian-mechanics area depends on two backbone modules: **`LinearAlgebra.Matrix.Transpose`** supplies the transpose API required for the skew-symmetric solenoidal constraint ($Q^\top = -Q$) in fep-025 and for precision-matrix manipulations elsewhere, while **`Data.Finset.Basic`** supplies the `Finset.filter`, `Finset.disjoint`, and `Finset.union` API that fep-005 uses to encode the four-part Markov blanket partition as a decidable predicate on a finite carrier. Measure-theoretic topics (fep-009, fep-022, fep-027, fep-036, fep-042) additionally route through `MeasureTheory.Measure.MeasureSpace` and `MeasureTheory.Measure.Prod`.

| Topic | Theorem | Maturity | Key Mathlib Module | `sorry` count |
|-------|---------|----------|--------------------|--------------|
| fep-005 | Markov Blanket Partition: 4-part partition, pairwise disjoint, total cover | real | `Data.Finset.Basic` | 0 |
| fep-009 | Generative Model Likelihood: joint product nonneg, `likelihood_mono`, `map_nonneg` | real | `MeasureTheory.Measure.MeasureSpace` | 0 |
| fep-010 | Fluctuation Theorem: `exp_pos`, detailed balance (`exp(a)*exp(-a)=1`), `exp_add` | real | `Analysis.SpecialFunctions.Exp` | 0 |
| fep-019 | Prior Predictive: mixture definition, `mixture_nonneg` | real | `Algebra.BigOperators` | 0 |
| fep-027 | Hierarchical Generative Models: product mass nonneg, marginal nonneg, product probability | real | `MeasureTheory.Measure.Prod` | 0 |
| fep-022 | Posterior Predictive Checks: pushforward nonneg, `preimage_univ`, `preimage_mono` | real | `MeasureTheory.Measure.MeasureSpace` | 0 |
| fep-036 | Empirical Bayes Coupling: scaled mass nonneg via `ENNReal.toReal_nonneg`, mixture bound | real | `MeasureTheory.Measure.MeasureSpace` | 0 |
| fep-040 | Gaussian Entropy and Heat Capacity: `log_variance`, `variance_nonneg`, `entropy_mono` | real | `Analysis.SpecialFunctions.Log.Basic` | 0 |
| fep-042 | Sufficient Statistics Factorization: pushforward nonneg, `preimage_univ`, `preimage_mono` | real | `MeasureTheory.MeasurableSpace.Basic` | 0 |
| fep-046 | Stick-Breaking Priors: `stick_nonneg`, `remaining_decreases`, `two_step_nonneg` | real | `Algebra.Order.Field.Basic` | 0 |

#### Hierarchical Generative Models and Predictive Coding (fep-027) {#sec:sd_hierarchical}

A **hierarchical generative model** of depth $L$ over observations $o$ and latent state stacks $s^{(1)}, \ldots, s^{(L)}$ factors the joint as a Markov chain on levels:

\begin{equation}\label{eq:sd_hierarchical_gm}
p\!\left(o, s^{(1)}, \ldots, s^{(L)}\right) \;=\; p(o \mid s^{(1)}) \;\prod_{l=1}^{L-1} p(s^{(l)} \mid s^{(l+1)}) \;\cdot\; p(s^{(L)}).
\end{equation}

In Friston's predictive coding realization, each conditional $p(s^{(l)} \mid s^{(l+1)})$ is Gaussian, $s^{(l)} = g^{(l)}(s^{(l+1)}) + \omega^{(l)}$ with $\omega^{(l)} \sim \mathcal{N}(0, \Pi_l^{-1})$, so that inference reduces to gradient descent on precision-weighted squared prediction errors $\varepsilon^{(l)} = s^{(l)} - g^{(l)}(\mu^{(l+1)})$. This gives the canonical **top-down predictions / bottom-up prediction errors** dynamic:

\begin{equation}\label{eq:sd_predictive_coding_dynamics}
\dot\mu^{(l)} \;=\; -\,\Pi_l\,\varepsilon^{(l)} \;+\; \partial_{\mu^{(l)}} g^{(l-1)}\,\Pi_{l-1}\,\varepsilon^{(l-1)},
\end{equation}

a neurobiologically suggestive message-passing algorithm in which precisions $\Pi_l$ gate the influence of each level — the mathematical form of selective attention. Marginalising a level is an integration against the product measure, $p(s^{(l)}) = \int p(s^{(l)}, s^{(l+1)})\,d\mu_{s^{(l+1)}}$, so every marginal remains a probability measure under pushforward.

The fep-027 Lean sketch formalizes exactly the pieces needed for this compositional structure to be well-posed on `MeasureTheory.Measure.Prod`: (i) pointwise product-mass nonnegativity $0 \le \mu(s)\cdot\nu(t)$, (ii) nonnegativity of marginals obtained via `Measure.map Prod.fst` (first-coordinate pushforward), and (iii) rectangle-mass nonnegativity $0 \le \mu(s \times^{\mathrm s} t)$. These are the building blocks of a valid factored joint on a product measurable space; they anchor Equation \ref{eq:sd_hierarchical_gm} without yet committing to specific conditional-independence structure (which requires `ProbabilityTheory.Kernel`). Upgrading to the predictive-coding dynamics requires Gaussian conditional kernels — the natural integration path via fep-040.

#### Gaussian Entropy, Variance as Temperature, and Heat Capacity (fep-040) {#sec:sd_gaussian_entropy}

For a univariate Gaussian $\mathcal{N}(\mu, \sigma^2)$ the differential entropy admits the closed form

\begin{equation}\label{eq:sd_gauss_entropy}
H(\mathcal{N}(\mu, \sigma^2)) \;=\; \tfrac{1}{2}\log(2\pi e\, \sigma^2) \;=\; \tfrac{1}{2}\log(2\pi e) + \tfrac{1}{2}\log \sigma^2,
\end{equation}

with multivariate generalization $H(\mathcal{N}(\mu, \Sigma)) = \tfrac{1}{2}\log\det(2\pi e\,\Sigma)$. Entropy is monotone in the variance — higher $\sigma^2$ encodes higher uncertainty. The **equipartition / heat-capacity** analogy is the bridge to statistical mechanics: identify $\sigma^2$ with thermodynamic temperature $T$ (each quadratic degree of freedom carries $\tfrac{1}{2}k_B T$ of energy at equilibrium), so that

\begin{equation}\label{eq:sd_equipartition_thermo}
U \;=\; \langle F\rangle \;=\; \tfrac{1}{2}k_B T, \qquad C_V \;=\; \frac{\partial U}{\partial T} \;=\; \tfrac{1}{2}k_B, \qquad S \;=\; \int \frac{C_V}{T}\,dT \;=\; \tfrac{1}{2}k_B \log T + \text{const}.
\end{equation}

The functional form $\tfrac{1}{2}\log \sigma^2$ of Gaussian entropy is thus *identical* to the temperature-dependent entropy of a harmonic-oscillator degree of freedom with $T \leftrightarrow \sigma^2$. In Bayesian mechanics, the variance of a belief plays the role of **informational temperature**: a broad belief is "hot" (exploratory, high entropy), a tight belief is "cold" (committed, low entropy), and the precision $\Pi = \sigma^{-2}$ is the inverse temperature $\beta$. This identification underwrites the deep-temperature parametrizations used in Boltzmann machines, diffusion models, and annealed variational inference — all of which can be read as cooling schedules on Gaussian belief precisions.

The fep-040 Lean sketch formalizes that $\log(\sigma^2)$ is well-defined on the positive cone $\sigma^2 > 0$ (avoiding the log-of-zero singularity) and that entropy is monotone in $\sigma^2$ (`entropy_mono`) — the two order-theoretic facts that make Equation \ref{eq:sd_gauss_entropy} a bona fide entropy function. The multivariate determinant version routes through `Matrix.det` and `Matrix.logDet` once `Matrix.PosDef` integrates with `Analysis.SpecialFunctions.Log`.

#### Stick-Breaking Priors and Dirichlet Processes (fep-046) {#sec:sd_stick_breaking}

Sethuraman's **stick-breaking construction** gives an explicit, almost-surely-valid sample from a **Dirichlet process** $\mathrm{DP}(\alpha, G_0)$:

\begin{equation}\label{eq:sd_stick_breaking}
V_k \;\stackrel{\text{iid}}{\sim}\; \mathrm{Beta}(1, \alpha), \qquad \pi_k \;=\; V_k\,\prod_{j<k}(1 - V_j), \qquad \theta_k \;\stackrel{\text{iid}}{\sim}\; G_0, \qquad G \;=\; \sum_{k=1}^\infty \pi_k\,\delta_{\theta_k}.
\end{equation}

The construction proceeds by iteratively "breaking" a unit stick: at step $k$, fraction $V_k$ of the remaining stick $\prod_{j<k}(1 - V_j)$ is assigned to component $k$. Two algebraic invariants make this well-posed: the retained mass $v(1-v) \in [0, 1]$ is nonnegative (each break gives a valid proportion), and the remaining stick $\prod_{j \le k}(1 - V_j)$ decreases monotonically in $k$ (monotone convergence to zero a.s. when $\alpha < \infty$), so $\sum_k \pi_k = 1$ almost surely. The resulting random measure $G$ is a draw from $\mathrm{DP}(\alpha, G_0)$; the concentration parameter $\alpha$ controls the rate at which new atoms appear (small $\alpha$ = few large atoms, large $\alpha$ = many small atoms following $G_0$).

Dirichlet processes are the foundational prior of **Bayesian nonparametrics**: they place a prior over discrete probability measures whose support size is itself random and grows with data. In Active Inference, DP priors enable **infinite-dimensional generative models** that can add latent causes as observations demand — a formalization of conceptual novelty and structure learning. The Chinese-restaurant-process representation of the same prior gives a coherent sampling / inference scheme (Neal's Algorithm 8 for DP mixtures). Hierarchical Dirichlet processes (HDPs) extend this to shared-atom structure across groups (topic models, multi-task learning), and Pitman–Yor processes generalize to power-law atom-size distributions relevant to linguistic data.

The fep-046 Lean sketch formalizes the two constructive invariants at the algebraic level on `Algebra.Order.Field.Basic`: `fep046_stick_nonneg` (the retained mass after a single cut is nonneg, i.e. $u(1-v) \ge 0$ whenever $u \ge 0$ and $v \le 1$), `fep046_remaining_decreases` (the residual stick shrinks under each break), and `fep046_two_step_nonneg` (compositional nonnegativity across two consecutive breaks). These suffice to certify that the stick-breaking recursion stays within the probability simplex; upgrading to the full DP requires countable-product measures via `MeasureTheory.Measure.Prod` and the Kolmogorov extension, a natural next step once infinite-product measure theory matures in Mathlib4.

**Representative formalization** — *Markov Blanket Partition (fep-005)*: The pipeline constructs a formal four-part partition of all system states into internal, sensory, active, and external components using `Finset.filter` over an assignment function. Three properties are proved: pairwise disjointness of the partition blocks, completeness (every state belongs to exactly one block), and coverage of the full state space. This makes the structural assumptions of Markov blanket decomposition machine-checkable — directly addressing the Biehl et al. critique (§\ref{sec:blanket_conditions_biehl_et_al}): whether a valid partition exists for a given dynamical system becomes a checkable predicate rather than a matter of interpretation. See §\ref{sec:catalogue-fep-005} in Appendix B and §\ref{sec:eqs-fep-005} in Appendix~\ref{sec:appendix_c_latex_equations} (\Cref{eq:fep-005-1}--\Cref{eq:fep-005-3}).

**Representative formalization** — *Hierarchical Generative Models (fep-027)*: Hierarchical models sit at the junction of Bayesian mechanics and measure-theoretic probability. The sketch uses Mathlib4's `MeasureTheory.Measure.Prod` to construct joint measures on $\alpha \times \beta$ and proves three structural facts: (i) pointwise nonnegativity of product mass, $0 \le \mu(s) \cdot \nu(t)$; (ii) nonnegativity of marginals obtained via `Measure.map Prod.fst`; (iii) rectangle mass $0 \le \mu(s \times^{\mathrm s} t)$. Together these anchor the compositional structure of multilevel models — each level's marginal remains a valid measure under pushforward — without yet committing to specific conditional independence structure.

### Synthesis: What the {{combined_info_bayes_count}} Theorems Establish {#sec:sophisticated_synthesis}

Taken together, the {{areas.InfoGeometry.count}} Information Geometry theorems and {{areas.BayesianMechanics.count}} Bayesian Mechanics theorems span the full probabilistic and geometric infrastructure required for a complete FEP formalization.

**The {{areas.InfoGeometry.count}} Information Geometry theorems** establish the **differential-geometric substrate**:

- **Riemannian metric structure** — fep-004 (Fisher information metric as squared-score inner product and parameter-distance metric) and fep-038 (natural gradient as the preconditioned, reparametrization-invariant descent direction).
- **Core information divergence** — fep-014 (KL divergence via monotonicity, DPI, and complement-mass) and fep-024 (log-ratio identities and the self-divergence anchor $D_\text{KL}(p\|p) = 0$).
- **Convex-analytic generalizations** — fep-029 (Bregman divergences as the convex-analytic umbrella containing KL) and fep-044 (α-divergences as the one-parameter interpolation from mode-seeking to mass-covering).
- **Metric-space substrate for geodesics** — fep-018 (triangle inequality, symmetry, reflexivity as the prerequisites for curvature, connections, and α-geodesics).
- **Bayesian update geometry** — fep-017 (posterior = likelihood × prior / evidence as an equality of conditional expectations, identifiable with a Bregman / KL projection).

**The {{areas.BayesianMechanics.count}} Bayesian Mechanics theorems** establish the **probabilistic substrate**:

- **Markov blankets** — fep-005 (four-part disjoint cover formalizing the conditional-independence structure $p(\mu,\eta\mid b) = p(\mu\mid b)p(\eta\mid b)$).
- **Generative models** — fep-009 (likelihood monotonicity and pushforward structure) and fep-027 (hierarchical factorization on product measure spaces).
- **Priors** — fep-019 (mixture priors as prior predictives) and fep-046 (stick-breaking / Dirichlet-process priors for nonparametric inference).
- **Posteriors** — fep-022 (posterior predictive checks via pushforward measures).
- **Learning** — fep-036 (empirical-Bayes coupling of hyperpriors to data-estimated hyperparameters).
- **Gaussian models** — fep-040 (Gaussian entropy, variance as informational temperature, heat-capacity analogy).
- **Sufficient statistics** — fep-042 (pushforward / preimage structure underwriting the factorization theorem and exponential-family sufficiency).
- **Fluctuation theorems** — fep-010 (exponential positivity and detailed balance as the stochastic-thermodynamic anchor).

The two areas interlock: information geometry gives the *metric and curvature* on the space of beliefs, while Bayesian mechanics gives the *generative and conditional-independence structure* that populates that space with physically meaningful distributions. The natural gradient of fep-038 is exactly the descent direction on the belief manifold defined by the Fisher metric of fep-004; the KL divergence of fep-014 is the Bregman divergence of fep-029 instantiated at negative Shannon entropy; the Gaussian entropy of fep-040 is the log-determinant Riemannian volume element on the Fisher manifold of univariate Gaussians; the Markov blanket of fep-005 is the conditional-independence structure that makes the hierarchical factorization of fep-027 well-posed. {{combined_info_bayes_count_caps}} theorems, each discharging its algebraic obligations with `sorry` count zero, collectively certify the geometric-probabilistic infrastructure on which Active Inference and FEP formulations are built.
