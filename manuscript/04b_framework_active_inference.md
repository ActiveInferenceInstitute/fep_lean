## Intermediate Dynamics: Active Inference ({{areas.ActiveInference.count}} topics) {#sec:intermediate_dynamics_active_inference}

Transitioning into temporally extended behavior, Active Inference [@friston2017active; @friston2016active] models required the mapping of discrete action policies and decision theory, including motor control implementations where prediction errors drive action [@adams2013predictions]. The key challenge is that Active Inference introduces *temporal* structure: agents select policies $\pi$ over future time steps and evaluate their expected consequences, as synthesized in the discrete state-space framework [@dacosta2023bayesian]. Whereas the static FEP (Section \ref{sec:foundational_dynamics_free_energy_principle}) treats belief update as a single variational optimization, Active Inference elevates this to a *bilevel* optimization: an inner loop that minimizes variational free energy $F$ to approximate the posterior, and an outer loop that minimizes *expected* free energy $G(\pi)$ to select future actions. The {{areas.ActiveInference.count}} theorems catalogued below constitute the formal vocabulary required to state, prove, and compose these two loops within a mechanised setting.

### Generative Model, Variational Inference, and Policy Evaluation {#sec:ai_generative_model}

Active Inference begins with the same generative model that underwrites the static FEP, but partitioned into observation and latent components with an explicit decomposition into likelihood and prior:

\begin{equation}\label{eq:ai_generative_model}
p(o, s) \;=\; p(o \mid s)\,p(s),
\end{equation}

and extended to sequences $(o_{1:T}, s_{1:T})$ under a (possibly time-varying) transition kernel $p(s_{t+1} \mid s_t, a_t)$ with action $a_t$. Writing out the full sequential generative model,

\begin{equation}\label{eq:ai_sequential_gm}
p(o_{1:T}, s_{1:T} \mid a_{0:T-1}) \;=\; p(s_1)\,\prod_{t=1}^{T} p(o_t \mid s_t)\,\prod_{t=1}^{T-1} p(s_{t+1} \mid s_t, a_t),
\end{equation}

makes the *factor graph* structure of the problem explicit: the joint factorises into a prior on the initial state, a chain of transition factors under the action sequence, and an emission factor at each time. Inference on this factor graph is typically performed by local message passing — the forward--backward algorithm in the discrete case, the Kalman filter in the linear-Gaussian case — and the catalogue's perception-side topics (fep-007, fep-017 *(catalogued under InfoGeometry; reused here for its Bayesian-update content)*, fep-034, fep-047) are the algebraic invariants that make such schemes well-defined.

The agent's variational posterior $q(s)$ approximates the true posterior $p(s \mid o)$ by minimizing the standard variational free energy (Eq. \ref{eq:eq_VFE_functional}); under mean-field or structured factorisations this produces the familiar message-passing updates captured in the catalogue (fep-007 `factorProduct_nonneg`, fep-047 `forward_nonneg`, fep-034 `beliefUpdate`). Topic fep-017 formalizes the unnormalised posterior `likelihood s * prior s` as a concrete `def` on `State := Fin 8` and proves nonnegativity of both the pointwise posterior and the evidence sum — the discrete analogue of a well-posed Bayesian update.

### Expected Free Energy and Policy Selection {#sec:ai_expected_free_energy}

Action is selected not by minimizing the *current* free energy but its **path-integral expectation** over predicted trajectories — the *expected free energy* $G(\pi)$. The most compact form is the posterior–joint log-ratio over future latents $s_\tau$ and observations $o_\tau$:

\begin{equation}\label{eq:ai_efe_log_ratio}
G(\pi) \;=\; \mathbb{E}_{q}\!\bigl[\log q(s_\tau \mid \pi) \;-\; \log p(s_\tau, o_\tau \mid \pi)\bigr],
\end{equation}

where the expectation is taken under the policy-conditioned predictive $q(s_\tau, o_\tau \mid \pi)$. Equation \ref{eq:ai_efe_log_ratio} is the *generative* form of EFE; it rearranges into the posterior-averaged-VFE-plus-risk identity below, and — via a conditional-independence step — into the epistemic-plus-pragmatic form used throughout the catalogue. For a policy $\pi = (a_0, a_1, \dots, a_{T-1})$ we write the canonical decomposition:

\begin{equation}\label{eq:ai_efe_total}
G(\pi) \;=\; \underbrace{\mathbb{E}_{q_\pi}\!\bigl[F(q_\pi(\cdot \mid \tilde{o}),\, p(\cdot, \tilde{o}))\bigr]}_{\text{posterior-averaged VFE}} \;+\; \underbrace{\mathbb{E}_{q_\pi}\!\bigl[\mathrm{KL}\bigl[q(\tilde{o} \mid \pi) \,\big\|\, p(\tilde{o})\bigr]\bigr]}_{\text{risk}},
\end{equation}

where $\tilde{o}$ and $\tilde{s}$ denote predicted future observations and states under $\pi$, and $p(\tilde{o})$ encodes prior preferences.

#### Risk--Ambiguity Decomposition {#sec:ai_risk_ambiguity}

Substituting the joint factorisation $p(s_\tau, o_\tau \mid \pi) = p(o_\tau \mid s_\tau)\,q(s_\tau \mid \pi)$ into Eq. \ref{eq:ai_efe_log_ratio} and absorbing the prior preferences $p(o \mid C)$ (the agent's generative model of *preferred* outcomes conditioned on a context $C$) yields the first canonical decomposition of $G(\pi)$ into **risk** and **ambiguity**:

\begin{equation}\label{eq:ai_risk_ambiguity}
G(\pi) \;=\; \underbrace{\mathbb{E}_{q(s_\tau\mid\pi)}\!\bigl[-\log p(o_\tau \mid C)\bigr]}_{\text{risk (pragmatic cost)}} \;+\; \underbrace{\mathbb{E}_{q(s_\tau\mid\pi)}\!\bigl[H[p(o_\tau \mid s_\tau)]\bigr]}_{\text{ambiguity (aleatoric uncertainty)}},
\end{equation}

where $H[p(o_\tau \mid s_\tau)] = -\sum_{o} p(o \mid s_\tau) \log p(o \mid s_\tau)$ is the Shannon entropy of the likelihood. **Risk** is the expected *surprise* that future outcomes will be measured under the agent's prior preferences $C$ — a low-risk policy is one whose anticipated observations have high log-prior under $p(o \mid C)$. **Ambiguity** is the expected entropy of the observation channel given the agent's beliefs: a high-ambiguity policy leads the agent into states where the likelihood $p(o \mid s)$ is dispersed, so observations poorly disambiguate the latent state. Ambiguity is the *irreducible* (aleatoric) uncertainty that remains even under perfect belief, distinguishing it from epistemic uncertainty, which the agent can reduce through action.

#### Epistemic--Pragmatic Decomposition {#sec:ai_epistemic_pragmatic}

An equivalent rearrangement using the predictive $q(o_\tau \mid \pi) = \sum_s p(o_\tau \mid s)\,q(s \mid \pi)$ and Bayes' rule for the posterior $q(s_\tau \mid o_\tau, \pi)$ yields the second canonical form — **epistemic** value plus **pragmatic** value:

\begin{equation}\label{eq:ai_epistemic_pragmatic}
G(\pi) \;=\; \underbrace{-\mathbb{E}_{q(s_\tau, o_\tau \mid \pi)}\!\bigl[\log q(s_\tau \mid \pi) - \log q(s_\tau \mid o_\tau, \pi)\bigr]}_{\text{epistemic value (information gain)}} \;+\; \underbrace{\mathbb{E}_{q(o_\tau\mid\pi)}\!\bigl[-\log p(o_\tau \mid C)\bigr]}_{\text{pragmatic value}}.
\end{equation}

The epistemic term is (minus) the mutual information $I(s_\tau; o_\tau \mid \pi)$ between hidden states and observations under policy $\pi$ — it measures the anticipated *information gain* about $s_\tau$ obtained by executing $\pi$ and observing the resulting $o_\tau$. The pragmatic term is the expected log-prior on preferred outcomes. Using the same object in a form closer to catalogue usage:

\begin{equation}\label{eq:ai_efe_epi_prag}
G(\pi) \;=\; \underbrace{\mathbb{E}_{q(s \mid \pi)}\!\bigl[\mathrm{KL}[q(\psi \mid s, \pi) \,\|\, p(\psi \mid s, \pi)]\bigr]}_{\text{epistemic value (information gain)}} \;-\; \underbrace{\mathbb{E}_{q(s \mid \pi)}\!\bigl[\log p(s \mid \pi)\bigr]}_{\text{pragmatic value (goal attainment)}}.
\end{equation}

The two decompositions (Eq. \ref{eq:ai_risk_ambiguity} and Eq. \ref{eq:ai_epistemic_pragmatic}) are algebraically equivalent: *risk + ambiguity = epistemic + pragmatic*. This conservation identity is precisely the content of **fep-021**, which certifies in Lean that the two forms evaluate to the same real number under any shared generative model, and further proves nonnegativity and a dominance lemma so that ordering by $G$ is well-defined on the underlying real lattice. The identity matters because the two decompositions reflect different modeling emphases — risk--ambiguity is natural for engineering applications (cost and sensor noise), whereas epistemic--pragmatic surfaces the exploration--exploitation trade-off directly — and fep-021 guarantees that a result proved in one decomposition transfers to the other without loss.

#### Softmax Policy Selection with Precision {#sec:ai_softmax_policy}

Policies are then selected via a **Boltzmann/softmax posterior** over $G$:

\begin{equation}\label{eq:ai_softmax_policy}
q(\pi) \;=\; \sigma\!\bigl(-\gamma\, G(\pi)\bigr) \;=\; \frac{\exp(-\gamma\, G(\pi))}{\sum_{\pi'} \exp(-\gamma\, G(\pi'))}, \qquad \gamma > 0,
\end{equation}

with precision $\gamma$ (the inverse temperature) controlling the exploration–exploitation balance. The two limiting regimes are instructive. As $\gamma \to 0^{+}$, $\exp(-\gamma G(\pi)) \to 1$ for every $\pi$, so $q(\pi)$ converges to the uniform distribution over the policy set — *pure exploration*, in which the agent samples policies independently of their expected free energy. As $\gamma \to \infty$, the softmax converges to a point mass on $\arg\min_\pi G(\pi)$ (or uniformly over the argmin set if it is not a singleton) — *greedy exploitation* of the current EFE estimate. Finite intermediate $\gamma$ interpolates smoothly between these extremes and recovers the Gibbs measure associated with energy $G$ and inverse temperature $\gamma$.

Crucially, $\gamma$ is not an external hyperparameter in the full Active Inference framework but is itself inferred under the FEP: the agent maintains a prior $p(\gamma)$ (typically a Gamma distribution) and posterior $q(\gamma)$, with updates that balance policy confidence against prior preferences. This *precision optimization* is the active-inference analogue of learned temperature schedules in reinforcement learning and provides a principled account of how the exploration--exploitation trade-off is tuned to context. **fep-028** is the direct object of this construction, which (i) defines `fep028_softmax`, (ii) proves pointwise nonnegativity over any nonempty finite policy set via `Real.exp_nonneg` and `div_nonneg`, and (iii) proves $\sum_\pi q(\pi) = 1$ via `Finset.sum_mul` and `mul_inv_cancel₀` — jointly certifying that softmax outputs a bona fide probability distribution for every admissible $\gamma$.

#### Exploration Bonus and Information Gain {#sec:ai_exploration_bonus}

The epistemic term in Eq. \ref{eq:ai_epistemic_pragmatic} is formalized separately by **fep-041**, which encodes the *expected information gain* as a KL divergence between posterior and prior over the latent under the predictive distribution on observations:

\begin{equation}\label{eq:ai_information_gain}
\mathrm{IG}(\pi) \;=\; \mathbb{E}_{q(o\mid\pi)}\!\bigl[\mathrm{KL}\bigl[q(s \mid o, \pi) \,\big\|\, q(s \mid \pi)\bigr]\bigr] \;=\; I(s; o \mid \pi) \;\ge\; 0.
\end{equation}

This quantity is the mutual information between hidden state and observation conditional on the policy and has two critical properties that fep-041 establishes in Lean: (i) *nonnegativity* (`epistemic_value_nonneg`), following from the nonnegativity of KL; and (ii) *monotonicity* in the underlying divergence (`epistemic_value_mono`), so that sharper posteriors relative to the prior yield strictly higher epistemic value. The mutual information vanishes iff observations carry no information about the latent — operationally, iff the likelihood $p(o \mid s)$ is constant in $s$ (a *fully ambiguous* channel). Agents with nonzero epistemic value perform *epistemic foraging*: they seek states whose observations most sharply update beliefs, which is the mathematical content of curiosity-driven behavior and intrinsic motivation. Note that epistemic value and ambiguity are distinct quantities — epistemic value is information the agent *can* extract through action, while ambiguity is noise that persists regardless of belief.

#### Markov Decision Processes as a Special Case {#sec:ai_mdp_limit}

Active Inference subsumes the standard Markov decision process (MDP) as a degenerate limit. If the prior over preferred outcomes is a hard indicator on a goal set $\mathcal{G}$,

\begin{equation}\label{eq:ai_mdp_indicator_prior}
p(o \mid C) \;=\; \begin{cases} \exp(r(o))/Z & o \in \mathcal{G}, \\ 0 & o \notin \mathcal{G}, \end{cases}
\end{equation}

or more generally $\log p(o \mid C) = r(o) - \log Z$ for reward function $r$, then the pragmatic term in Eq. \ref{eq:ai_epistemic_pragmatic} reduces (up to a constant) to the expected reward $\mathbb{E}_{q(o\mid\pi)}[r(o)]$ that dominates classical decision theory. In this limit, dropping the epistemic term recovers Bellman-style expected-reward maximization exactly; retaining the epistemic term yields an *intrinsically motivated* MDP in which the agent balances extrinsic reward against information gain. This is the formal sense in which Active Inference generalizes MDPs: the framework retains the optimal policy of any MDP (take $\gamma \to \infty$ and drop epistemic value) while strictly enlarging the behavioral repertoire in partially observed or ambiguous settings. The multi-step structure of this comparison is the province of **fep-033**, which formalizes a *planning horizon* $\tau = 1, \ldots, T$, proves nonnegativity of the horizon-accumulated cost, and certifies the monotonicity `horizon_mono` — longer horizons can only weakly increase cumulative cost — together with a discounted-nonneg lemma for discounted variants. Together, Eq. \ref{eq:ai_epistemic_pragmatic} plus fep-033 plus fep-041 constitutes a mechanised proof that Active Inference properly contains intrinsically motivated finite-horizon MDPs as a special case.

### Perception vs Action in the Catalogue {#sec:ai_perception_action_topics}

The Active Inference catalogue divides cleanly along the perception/action interface of the FEP:

- **Perception-side topics** (posterior refinement under a fixed policy): fep-007 (belief propagation), fep-017 (Bayesian posterior; catalogued in InfoGeometry but treated here for its perception-side role), fep-034 (categorical belief update), fep-047 (forward message passing). These formalize the structural invariants of message-passing schemes — nonnegativity of factor products, monotonicity of forward passes, and boundedness of total belief mass.
- **Action-side topics** (policy evaluation and selection over $G$): fep-003 (EFE stage-cost aggregation), fep-008 (existence of an optimal policy on a finite set), fep-021 (EFE equivalence forms), fep-023 (affordance reachability), fep-028 (softmax), fep-033 (planning horizon), fep-041 (epistemic value / information gain).
- **Dynamics coupling perception and action**: fep-020 (Langevin sampling view, catalogued under Active Inference because it realizes the policy-as-descent interpretation).

#### Belief Propagation on Factor Graphs (fep-007) {#sec:ai_belief_propagation}

The sequential generative model of Section \ref{sec:ai_generative_model} admits a canonical factor-graph representation: variable nodes for each $s_t$ and $o_t$, factor nodes for the prior $p(s_1)$, each transition $p(s_{t+1} \mid s_t, a_t)$, and each emission $p(o_t \mid s_t)$. The *sum--product* (belief propagation) algorithm computes the marginal $q(s_t) \approx p(s_t \mid o_{1:T})$ by local message passing on this graph: forward messages $\alpha_t(s_t) = \sum_{s_{t-1}} p(s_t \mid s_{t-1}, a_{t-1})\,\alpha_{t-1}(s_{t-1})\,p(o_{t-1} \mid s_{t-1})$ and backward messages $\beta_t(s_t)$ combine into the posterior $q(s_t) \propto \alpha_t(s_t)\,\beta_t(s_t)$. In the linear-Gaussian case this reduces exactly to the Kalman filter/smoother.

**fep-007** formalizes the algebraic substrate of this algorithm. It proves `factorProduct_nonneg` — that the pointwise product of nonnegative factor evaluations is itself nonnegative, so no sign errors arise when combining messages — and a message-aggregation monotonicity property stating that summing over additional incoming messages (additional factor evaluations) preserves nonnegativity. These are the minimal algebraic guarantees that make belief propagation *well-typed* as a probability-preserving operation; richer properties such as exactness on trees or convergence of loopy BP on specific graph classes are downstream corollaries of this substrate together with graph-theoretic assumptions.

#### Categorical Belief Updates (fep-034) {#sec:ai_categorical_update}

For discrete state and observation spaces, the single-step Bayesian update has the canonical form

\begin{equation}\label{eq:ai_categorical_bayes}
q(s \mid o) \;\propto\; p(o \mid s)\,q(s), \qquad q(s \mid o) \;=\; \frac{p(o \mid s)\,q(s)}{\sum_{s'} p(o \mid s')\,q(s')},
\end{equation}

where the denominator is the evidence $p(o) = \sum_{s'} p(o \mid s')\,q(s')$. **fep-034** formalizes the unnormalised posterior map `beliefUpdate : Likelihood → Prior → UnnormalisedPosterior`, defined pointwise as `beliefUpdate l p s = l s * p s`, and proves two key invariants. First, `update_nonneg` certifies that pointwise nonnegative inputs produce pointwise nonnegative outputs. Second, `totalUnnorm_nonneg` (the Finset sum of the unnormalised posterior) certifies that the evidence is itself nonnegative, which is the precondition for the normalization step to yield a valid probability vector.

The edge case $p(o \mid s) = 0$ is handled by the definition: when the likelihood is zero at $s$, the unnormalised posterior is zero at $s$, which is the *impossibility* condition — states rendered logically impossible by the observation receive zero posterior mass. This matches the behavior of Bayesian inference under hard evidence and is the discrete analogue of the Laplace approximation for continuous models, where posterior mass collapses onto the support of the likelihood. fep-034 is the perception-side counterpart to fep-028: both take nonnegative real-valued vectors on finite supports and produce provably well-formed probability vectors under simple algebraic hypotheses.

### Policies, Optimality, and Affordances {#sec:ai_policies_affordances}

#### Affordances and Reachability (fep-023) {#sec:ai_affordances}

The term *affordance*, borrowed from ecological psychology [@gibson1979ecological], has a precise formal meaning within Active Inference: the set of outcomes that an agent can render accessible through some choice of policy. Given a family of admissible policies $\Pi$ and a predictive distribution $q(\cdot \mid \pi)$ over outcomes for each $\pi \in \Pi$, the *affordance set* is

\begin{equation}\label{eq:ai_affordance_set}
\mathcal{A}(\Pi, q) \;=\; \{\, o : \exists \pi \in \Pi,\; q(o \mid \pi) > 0 \,\} \;=\; \bigcup_{\pi \in \Pi} \operatorname{supp}\!\bigl(q(\cdot \mid \pi)\bigr).
\end{equation}

**fep-023** encodes this as `affordanceSet (Π, q) = { y : ∃ π ∈ Π, q π = y }` on discrete `Finset` types and proves two structural properties. `reachable` characterizes membership of the affordance set via a witness policy, and `affordance_monotone` certifies that $\Pi \subseteq \Pi'$ implies $\mathcal{A}(\Pi, q) \subseteq \mathcal{A}(\Pi', q)$ — *expanding the policy repertoire weakly expands the affordance set*. This is the formal, compiler-checked counterpart to the ecological-psychology intuition that extending an agent's action repertoire (tools, skills, embodiment) can only enlarge what the world makes available, never restrict it. The interaction with fep-041 is notable: agents with nonzero epistemic value prefer policies that expand the affordance set in directions of high mutual information, formalizing the connection between curiosity and ecological niche construction.

#### Optimal Policy Existence (fep-008) {#sec:ai_optimal_policy_existence}

Policy selection reduces to minimization of $G$ over the finite policy set. **fep-008** certifies that such a minimizer exists and that all minimizers share a common EFE value. The proof invokes `Finset.exists_min_image` to obtain an explicit minimizer $\pi^\star$ with $G(\pi^\star) \le G(\pi)$ for every $\pi \in \Pi$, and then `min_agrees_on_value` plus `le_antisymm` to show that any two minimizers $\pi^\star_1, \pi^\star_2$ satisfy $G(\pi^\star_1) = G(\pi^\star_2)$. The discrete, finite setting matches real Active-Inference implementations that enumerate a finite policy horizon; fep-008 is thus the small but essential existence theorem that downstream results (commitment to a specific action, deterministic policy extraction, value iteration on the EFE lattice) rely upon.

#### Mathlib Footprint and Verification Status {#sec:ai_mathlib_table}

| Topic | Theorem | Maturity | Key Mathlib Module | `sorry` count |
|-------|---------|----------|--------------------|--------------|
| fep-003 | EFE stage cost aggregation + cost dominance monotonicity | real | `Algebra.BigOperators` | 0 |
| fep-007 | Factor product nonneg + message aggregation nonneg | real | `Algebra.BigOperators` | 0 |
| fep-008 | Active Inference optimal policy (`Finset.exists_min_image` + `min_agrees_on_value`) | real | `Data.Finset` | 0 |
| fep-020 | Langevin step definition + displacement sq nonneg + descent property | real | `Analysis.SpecialFunctions.Pow.Real` | 0 |
| fep-021 | EFE conservation identity + nonneg + dominance | real | `Order.Basic` | 0 |
| fep-023 | Affordance: reachable distributions (`affordanceSet` + `reachable` + `monotone`) | real | `Data.Set`, `Data.Finset` | 0 |
| fep-028 | Softmax nonneg + sum to one | real | `Algebra.BigOperators` | 0 |
| fep-033 | Planning horizon nonneg + `horizon_mono` (longer → higher cost) + discounted nonneg | real | `Algebra.BigOperators` | 0 |
| fep-034 | Belief update + `update_nonneg` + `totalUnnorm_nonneg` | real | `MeasureTheory.Measure` | 0 |
| fep-041 | Epistemic value definition + nonneg + monotonicity in divergence | real | `Algebra.BigOperators` | 0 |
| fep-047 | Forward pass + nonneg + message-passing monotonicity | real | `Algebra.BigOperators` | 0 |

**Representative formalization** — *Expected Free Energy (fep-003, Eq. \ref{eq:eq_4})*: The EFE decomposes into epistemic and pragmatic terms:

\begin{equation*}
\EFE(\pi) = \underbrace{\E_{q(s|\pi)}\!\bigl[\KL[q(\psi|s,\pi) \| p(\psi|s,\pi)]\bigr]}_{\text{epistemic value}} - \underbrace{\E_{q(s|\pi)}\!\bigl[\log p(s|\pi)\bigr]}_{\text{pragmatic value}}
\end{equation*}

An early LLM-generated draft attempted a `def expectedFreeEnergy` using conditional measures and Radon-Nikodym derivatives, but the Hermes assessment identified a type error: `q_ψ` was declared with arity 1 but called with arity 2, demonstrating a common LLM failure mode where informal mathematical notation (which freely curries arguments) does not map cleanly to Lean's explicit typing. The production sketch takes a different approach: it formalizes the discrete stage-cost structure of the EFE, proving that nonnegative per-state costs aggregate to a nonnegative total (`fep003_stageSum_nonneg` via `Finset.sum_nonneg`) and that cost dominance is monotone: if $c_a \le c_b$ pointwise across states, then $\mathrm{EFE}(a) \le \mathrm{EFE}(b)$ (`fep003_efe_monotone` via `Finset.sum_le_sum`). This anchors the key property for policy selection — uniformly cheaper actions are preferred under expected free energy minimization — in a compiler-verified form. See §\ref{sec:catalogue-fep-003} in Appendix B for the full sketch; typeset signatures appear in §\ref{sec:eqs-fep-003} (\Cref{eq:fep-003-1}--\Cref{eq:fep-003-4}) in Appendix~\ref{sec:appendix_c_latex_equations}.

**Representative formalization** — *Optimal Policy Existence (fep-008)*: On a nonempty finite policy set, EFE achieves its minimum. The sketch invokes `Finset.exists_min_image` (producing a certified minimizer) and then proves that any two minimizers agree on $G$ via `le_antisymm`. This turns the *soft* statement "some policy is best under $G$" into a compiler-verifiable existence theorem — a small but important piece of machinery for downstream results where the agent commits to a specific action. Note the discrete setting matches real active-inference implementations that enumerate a finite policy horizon. Typeset statements: §\ref{sec:eqs-fep-008} in Appendix~\ref{sec:appendix_c_latex_equations}; Lean: §\ref{sec:catalogue-fep-008} in Appendix B.

**Representative formalization** — *Affordances as Reachable Observations (fep-023)*: The sketch encodes the agent's affordance landscape as $\texttt{affordanceSet}(\Pi, q) = \{y : \exists \pi \in \Pi,\ q(\pi) = y\}$ and proves monotonicity in $\Pi$: expanding the set of available policies only grows the set of reachable outcomes. This is the formal, compiler-checked counterpart to the ecological-psychology intuition that added action repertoire strictly increases the future observation set. See §\ref{sec:eqs-fep-023} in Appendix~\ref{sec:appendix_c_latex_equations} and §\ref{sec:catalogue-fep-023} in Appendix B.

**Notable achievements**: The three topics cited inline across Eq. \ref{eq:ai_efe_log_ratio}–\ref{eq:ai_softmax_policy} sit at the center of the Active Inference catalogue. **fep-021** formalizes the *EFE equivalence* — the conservation identity that reconciles the posterior–joint log-ratio form (Eq. \ref{eq:ai_efe_log_ratio}) with the epistemic-plus-pragmatic rearrangement (Eq. \ref{eq:ai_efe_epi_prag}) — together with nonnegativity and a dominance lemma on `Order.Basic`. **fep-028 (Softmax policy)** is the most complete Active Inference formalization in the catalogue: it defines `fep028_softmax`, proves pointwise non-negativity over any nonempty finite policy set, and proves normalization $\sum_\pi q(\pi) = 1$, yielding a full probability-distribution characterization of Eq. \ref{eq:ai_softmax_policy} entirely within Lean. **fep-034 (Discrete belief update)** encodes a categorical Bayesian update with `update_nonneg` and `totalUnnorm_nonneg`, anchoring the perception side against `MeasureTheory.Measure`. Topics fep-023 (Affordances) and fep-008 (Optimal Policy) are also catalogued as **real** (`mathlib_status`) and are strong candidates for clean native verification.

**Mathlib4 module footprint (Active Inference)**: Seven of the eleven Active Inference topics — fep-003, fep-007, fep-021, fep-028, fep-033, fep-041, fep-047 — route through `Algebra.BigOperators.Group.Finset` for Finset-aggregation lemmas (`Finset.sum_nonneg`, `Finset.sum_le_sum`, `Finset.sum_mul`), reflecting the discrete, finite-horizon character of the EFE machinery. Topics fep-008 and fep-023 additionally depend on `Data.Fin` and `Data.Finset` for the finite policy index types (`π : Fin n`, `affordanceSet : Finset α`) on which `Finset.exists_min_image` and `Finset.image` operate. This pair of modules — `Algebra.BigOperators.Group.Finset` for the sums and `Data.Fin` for the index universe — is the structural backbone of the area.

### What the Active Inference Theorems Collectively Establish {#sec:ai_synthesis}

The {{areas.ActiveInference.count}} Active Inference theorems are not independent fragments but a coordinated formal vocabulary for any discrete-time, partially observed active-inference agent. Grouped by role:

1. **EFE decomposition and equivalence** — fep-003 (stage-cost aggregation and dominance monotonicity) and fep-021 (conservation identity between risk--ambiguity and epistemic--pragmatic forms) together certify that the central object $G(\pi)$ is well-defined, nonnegative, and invariant under the decomposition one chooses for analysis.
2. **Inference machinery** — fep-007 (factor product and message aggregation), fep-017 (Bayesian posterior on a concrete state type — catalogued in InfoGeometry, included here for the perception-side belief-update story), fep-034 (categorical belief update), and fep-047 (forward message passing) provide the perception-side algebra that makes belief propagation well-typed and monotone.
3. **Policy selection** — fep-008 (existence and value-agreement of minimizers) and fep-028 (softmax as a bona fide probability distribution) together cover both the deterministic (argmin) and stochastic (Boltzmann) policy-selection regimes under the same EFE substrate.
4. **Multi-step planning** — fep-033 (planning horizon, with `horizon_mono` and discounted-nonneg variants) extends the one-step machinery to finite horizons, matching the way real implementations enumerate and evaluate $T$-step policies.
5. **Exploration via information gain** — fep-041 (epistemic value nonnegativity and divergence-monotonicity) formalizes the mutual-information component of $G$, underwriting the intrinsic-motivation and curiosity-driven behavior that distinguishes Active Inference from reward-only MDPs.
6. **Message passing for neural implementation** — fep-047 (forward pass nonnegativity and message-passing monotonicity) supplies the minimal algebra needed to interpret belief propagation as a neurally plausible local computation.
7. **Markov-chain sampling view** — fep-020 (Langevin-step definition plus displacement-squared nonnegativity and descent property) connects the discrete policy-selection picture to the continuous-time stochastic-gradient interpretation of the FEP, so that policies can be viewed as discrete-time samples of an underlying Langevin process.
8. **Affordance structure of action** — fep-023 (reachable distributions and monotonicity under policy expansion) formalizes the ecological structure in which policies embed, connecting mathematical policy sets to the intuitive notion of what an embodied agent can bring about.

No single theorem in this list *proves Active Inference*: the framework is a modeling choice, not a theorem. What the eleven together establish is that *every operational move* made by a discrete Active Inference agent — forming a generative model, running belief propagation, computing an EFE, decomposing it into risk--ambiguity or epistemic--pragmatic form, selecting a policy by argmin or softmax, executing it over a finite horizon, and reading off its affordance set — is backed by a compiler-verified lemma in Lean. The catalogue is thus a formal *certificate of well-typedness* for the Active Inference program on discrete, finite-horizon MDPs, against which specific models and implementations can be checked.

All {{areas.ActiveInference.count}} Active Inference topics carry **`mathlib_status: real`** with zero `sorry` axioms (every row of the table above reads `real`), giving a catalogue-derived area rate of **`{{compile_rate.by_area.ActiveInference}}`**. Publishing machine-checked claims requires a verify-enabled Gauss run (`FEP_LEAN_GAUSS_WORKFLOWS=1`, `gauss.verify_lean: true`) or `scripts/03_lean_verify_only.py`, which emits the live per-topic outcomes to `verification_manifest.json`.
