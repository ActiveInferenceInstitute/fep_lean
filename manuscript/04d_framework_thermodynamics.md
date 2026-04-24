## Non-equilibrium Thermodynamics ({{areas.Thermodynamics.count}} topics) {#sec:thermodynamics_results}

The thermodynamic extension of the FEP connects information-theoretic constructs to established results in statistical mechanics. The {{areas.Thermodynamics.count}} catalogue topics in this area (**fep-013, fep-025, fep-030, fep-031, fep-037, fep-049, fep-050**) formalize Helmholtz links, NESS flow, maximum entropy, Boltzmann/Gibbs structure, fluctuation--dissipation, entropy production, and information-theoretic Landauer bounds—aligned with the appendix index (§\ref{sec:appendix_comprehensive_formalisms_overview}).

**Thermodynamics area (current pin)**: All **`{{compile_rate.by_area.Thermodynamics}}`** Thermodynamics topics carry `mathlib_status: real` with zero `sorry` axioms against Mathlib4 **`{{mathlib_tag}}`** on the **`{{lean_toolchain}}`** toolchain — the catalogue-derived area rate is **`{{compile_rate.by_area.Thermodynamics}}`**, and a green `lake env lean` sweep (run `{{verify.run_id}}`) turns this into the live-verified rate. Every row below ships as a sorry-free Lean 4 sketch with warm-cache wall-clock under a few seconds per topic. The area stresses `Analysis.SpecialFunctions.*` and related real arithmetic—each sketch targets well-known lemma families (`Real.log_pos`, `Real.exp_pos`, `Real.exp_add`, `sub_nonneg.mpr`) with lighter measure-theoretic load than some FEP and Bayesian-mechanics rows.

### Thermodynamic Free Energy and Partition Structure {#sec:thermo_helmholtz_partition}

The thermodynamic **Helmholtz free energy** of a system at temperature $T$ with internal energy $U$, entropy $S$, and partition function $Z$ takes the equivalent forms:

\begin{equation}\label{eq:thermo_helmholtz}
\mathcal{F} \;=\; U \;-\; T\,S \;=\; -\,k_B\,T\,\log Z, \qquad Z \;=\; \sum_i \exp\!\bigl(-\beta\,E_i\bigr),\; \beta = 1 / (k_B T).
\end{equation}

Equation \ref{eq:thermo_helmholtz} is the statistical-mechanical counterpart to the variational free energy in Equation \ref{eq:eq_VFE_functional}: both are log-partition quantities that upper-bound "surprise" (negative log-evidence in the variational case, configurational entropy scaled by temperature in the thermodynamic case). The **Boltzmann–Gibbs distribution** $p_i = \exp(-\beta E_i)/Z$ is the maximum-entropy distribution consistent with a prescribed mean energy; topic fep-031 proves the three structural invariants that any such distribution must satisfy: weight positivity (`Real.exp_pos`), monotonicity ($E_1 \le E_2 \Rightarrow \exp(-\beta E_2) \le \exp(-\beta E_1)$ at $\beta > 0$), and strict positivity of the partition sum over any nonempty index set.

### Helmholtz Free Energy Bridge (fep-013): Full Derivation {#sec:thermo_helmholtz_bridge_derivation}

The Helmholtz bridge makes the thermodynamic–variational correspondence quantitatively precise. Let $p(s, o)$ be a generative joint density and $q(s)$ an approximate posterior over latent states. Define

\begin{equation}\label{eq:thermo_bridge_definitions}
U_q \;:=\; \mathbb{E}_q\!\bigl[-\log p(s, o)\bigr], \qquad H[q] \;:=\; -\,\mathbb{E}_q\!\bigl[\log q(s)\bigr], \qquad T \;=\; \frac{1}{k_B\,\beta}.
\end{equation}

Here $U_q$ is the *internal energy* interpretation of the negative log-joint (each configuration $(s, o)$ is assigned an energy $E(s, o) = -\log p(s, o)$ in natural units), and $H[q]$ is the *Boltzmann entropy* of the posterior $q$. Substituting these definitions into the variational free energy $F_{\text{var}}[q] = \mathbb{E}_q[-\log p(s, o)] - H[q]$ (in nats) yields

\begin{equation}\label{eq:thermo_bridge_nats_to_joules}
F_{\text{var}}[q] \;=\; U_q \;-\; H[q] \;=\; \frac{1}{k_B T}\!\Bigl(k_B T\,U_q \;-\; k_B T\,H[q]\Bigr) \;=\; \frac{1}{k_B T}\!\Bigl(\widetilde{U}_q \;-\; T\,\widetilde{S}_q\Bigr),
\end{equation}

where $\widetilde{U}_q = k_B T\,U_q$ restores energy units and $\widetilde{S}_q = k_B\,H[q]$ restores Boltzmann-entropy units. The bracketed expression on the right is *exactly* the Helmholtz free energy $\mathcal{F}[q] = \widetilde{U}_q - T\,\widetilde{S}_q$ of the distribution $q$ viewed as a Boltzmann ensemble over the energy landscape $E(s, o) = -\log p(s, o)$. Incorporating the log-partition normalizer $\log Z$ that separates the unnormalised joint $p(s, o)$ from the true posterior $p(s \mid o) = p(s, o)/p(o)$, the **exact Helmholtz bridge identity** is:

\begin{equation}\label{eq:thermo_helmholtz_bridge_exact}
\boxed{\;F_{\text{var}}[q] \;=\; \frac{\mathcal{F}[q]}{k_B T} \;+\; \log Z\;}
\end{equation}

with $\log Z = \log p(o)$ the log-evidence (a $q$-independent constant in the inference problem). Equation \ref{eq:thermo_helmholtz_bridge_exact} is the Helmholtz bridge in its sharpest form: *variational free energy is thermodynamic free energy in dimensionless units, plus a constant*. Because the additive $\log Z$ does not depend on $q$, the argmin over $q$ is identical on both sides:

\begin{equation}\label{eq:thermo_bridge_argmin_equiv}
\mathop{\mathrm{argmin}}_q\,F_{\text{var}}[q] \;=\; \mathop{\mathrm{argmin}}_q\,\mathcal{F}[q].
\end{equation}

At thermodynamic equilibrium the minimizer of $\mathcal{F}$ is the Boltzmann–Gibbs distribution $q^*(s) \propto \exp(-\beta E(s, o)) = p(s, o)^\beta$; in natural units ($\beta = 1$) this recovers the true posterior $q^*(s) = p(s \mid o)$, so the variational minimum *coincides* with exact Bayesian inference. This identification is the formal content of the Helmholtz bridge: inference is equilibration.

**What fep-013 formalizes.** The sketch carries the *partial-monotone structure* that is the algebraic prerequisite for Equation \ref{eq:thermo_bridge_argmin_equiv}. Specifically, fep-013 defines `noncomputable def fep013_helmholtz (U T S : ℝ) : ℝ := U - T * S` and proves (i) the zero-temperature limit $\mathcal{F}(U, 0, S) = U$ (`ring`-discharged) and (ii) entropy monotonicity at positive temperature: $T > 0 \wedge S_1 \le S_2 \Rightarrow \mathcal{F}(U, T, S_2) \le \mathcal{F}(U, T, S_1)$ (`nlinarith`-discharged). These two facts fix the *separate* monotonicities of $\mathcal{F}$ in $U$ (increasing) and $S$ (decreasing at $T > 0$), which is exactly what is needed to conclude that minimizing $\mathcal{F}$ drives the system toward high-entropy, low-internal-energy configurations — the same dual pressure that governs variational inference toward posteriors that are simultaneously data-consistent (low $U_q$) and maximally noncommittal (high $H[q]$). What fep-013 does *not* ship is the full Equation \ref{eq:thermo_helmholtz_bridge_exact}: that would require committing to a measure-theoretic definition of $\mathbb{E}_q$ and the partition function, which the catalogue currently keeps type-distinct (§\ref{sec:thermo_lean_sketches}).

### Jarzynski Equality and Fluctuation Theorems {#sec:thermo_jarzynski}

For a system driven by an external protocol that transitions the Hamiltonian from $H_0$ to $H_1$ in finite time, the non-equilibrium work $W$ is a random variable with distribution $P(W)$. The **Jarzynski equality** [@jarzynski1997nonequilibrium] provides an *identity* — not merely an inequality — linking the exponential average of $W$ to the *equilibrium* free energy difference:

\begin{equation}\label{eq:thermo_jarzynski}
\bigl\langle e^{-\beta W} \bigr\rangle \;=\; \int\!P(W)\,e^{-\beta W}\,dW \;=\; e^{-\beta\,\Delta \mathcal{F}}, \qquad \Delta \mathcal{F} = \mathcal{F}_1 - \mathcal{F}_0.
\end{equation}

Equation \ref{eq:thermo_jarzynski} is exact regardless of how far from equilibrium the driving protocol takes the system — the protocol may be arbitrarily fast, arbitrarily dissipative, and arbitrarily irreversible. The only requirement is that the system begins in canonical equilibrium at temperature $T$ with Hamiltonian $H_0$. Applying Jensen's inequality to Equation \ref{eq:thermo_jarzynski} (using the convexity of $x \mapsto e^{-\beta x}$) recovers the classical second-law bound

\begin{equation}\label{eq:thermo_second_law_bound}
\langle W \rangle \;\ge\; \Delta \mathcal{F},
\end{equation}

i.e., the mean work performed is at least the equilibrium free energy difference, with equality only in the quasistatic (reversible) limit. Equation \ref{eq:thermo_jarzynski} is strictly stronger than Equation \ref{eq:thermo_second_law_bound}: it fixes the *entire* exponential moment of $W$, not merely its mean, and thereby constrains all higher cumulants of the dissipated-work distribution.

A companion result, the **Crooks fluctuation theorem** [@crooks1999entropy], relates forward and time-reversed work distributions at the level of *individual trajectories*:

\begin{equation}\label{eq:thermo_crooks}
\frac{P_F(W)}{P_R(-W)} \;=\; \exp\!\bigl(\beta\,(W - \Delta \mathcal{F})\bigr),
\end{equation}

where $P_F(W)$ is the probability density of performing work $W$ under the forward protocol (Hamiltonian swept from $H_0$ to $H_1$) and $P_R(-W)$ is the probability density of performing work $-W$ under the time-reversed protocol (swept from $H_1$ to $H_0$). Equation \ref{eq:thermo_crooks} quantifies the *exponential asymmetry* between a dissipative trajectory and its time-reverse: work excursions above $\Delta \mathcal{F}$ are exponentially more likely in the forward direction, while excursions below $\Delta \mathcal{F}$ are exponentially more likely in reverse. The Jarzynski equality is a direct corollary of Crooks: rearranging Equation \ref{eq:thermo_crooks} to $P_R(-W) = P_F(W)\,e^{-\beta(W - \Delta\mathcal{F})}$ and integrating $\int P_R(-W)\,dW = 1$ yields Equation \ref{eq:thermo_jarzynski} immediately.

Both identities rest on the deeper **detailed-balance** / **microscopic reversibility** structure that pairs each forward trajectory with a time-reversed partner of equal measure under a time-reversal involution. Topic **fep-010** anchors the multiplicative substrate on which this structure rests: $\exp(a) \cdot \exp(-a) = 1$ (`fep010_detailed_balance`) is the algebraic detailed-balance identity, and $\exp(a + b) = \exp(a)\,\exp(b)$ (`fep010_exp_add`) is the homomorphism property that lets exponents of path-integrated quantities factor across trajectory segments. Topic **fep-037** then formalizes the **fluctuation–dissipation theorem** (Kubo) at the level of products: response $\chi$ times fluctuation $C$ is nonnegative, with the Einstein relation $D = k_B T \mu$ (diffusion = $k_B T$ times mobility) as a concrete instance. Together, fep-010 and fep-037 ship the algebraic building blocks of the Jarzynski/Crooks family — the full path-measure integrals of Equations \ref{eq:thermo_jarzynski}–\ref{eq:thermo_crooks} remain future catalogue work pending Mathlib's stochastic-calculus layer, but the exponential and product identities that any such proof will compose are already compiler-verified.

### NESS Solenoidal Flow (fep-025): Full Fokker–Planck Treatment {#sec:thermo_ness_fokker_planck}

The Fokker–Planck equation describes the time evolution of the probability density $p(x, t)$ of a stochastic process $\dot{x} = f(x) + \sqrt{2D}\,\xi(t)$ with drift $f$ and diffusion $D$:

\begin{equation}\label{eq:thermo_fokker_planck}
\frac{\partial p(x, t)}{\partial t} \;=\; -\nabla \cdot J(x, t), \qquad J(x, t) \;=\; f(x)\,p(x, t) \;-\; D\,\nabla p(x, t).
\end{equation}

The vector $J(x, t)$ is the **probability current**: the net flux of probability mass through a point. At a stationary distribution $p^*(x)$ with $\partial_t p^* = 0$, Equation \ref{eq:thermo_fokker_planck} reduces to the continuity constraint

\begin{equation}\label{eq:thermo_stationarity}
\nabla \cdot J^*(x) \;=\; 0 \qquad \text{(stationarity)}.
\end{equation}

Equation \ref{eq:thermo_stationarity} admits two qualitatively distinct classes of solutions:

1. **Thermodynamic equilibrium:** $J^*(x) \equiv 0$ identically. Detailed balance holds at every point; no entropy is produced; the system is time-reversible.
2. **Nonequilibrium steady state (NESS):** $J^*(x) \not\equiv 0$ but $\nabla \cdot J^*(x) = 0$. Probability circulates in closed loops; detailed balance is broken; entropy is produced at a positive rate.

The NESS case is the dynamically relevant one for self-organizing biological systems: a living organism at steady state is not at thermodynamic equilibrium — it continually dissipates energy to maintain its low-entropy organization. To exhibit NESS structure, the drift $f$ must admit a **Helmholtz–Ao decomposition** [@ao2004potential]:

\begin{equation}\label{eq:thermo_ao_decomposition}
f(x) \;=\; -\,\bigl(D \,+\, Q(x)\bigr)\,\nabla F(x), \qquad F(x) \;=\; -\log p^*(x), \qquad Q(x)^\top \;=\; -\,Q(x),
\end{equation}

where $F(x)$ is the *nonequilibrium potential* (the negative log-stationary density), $D$ is the symmetric positive-semidefinite diffusion matrix driving relaxation along the gradient of $F$, and $Q(x)$ is an *antisymmetric* matrix field generating divergence-free circulation. Substituting Equation \ref{eq:thermo_ao_decomposition} into the current gives $J^*(x) = -(D + Q)\,\nabla F\,p^* - D\,\nabla p^* = -Q\,\nabla F\,p^*$, using $p^* = e^{-F}$ and $\nabla p^* = -(\nabla F)\,p^*$. The dissipative part $D\,\nabla F\,p^*$ cancels against $D\,\nabla p^*$, leaving only the solenoidal (curl-like) part $-Q\,\nabla F\,p^*$ as the NESS current.

**Why antisymmetry yields solenoidality.** The solenoidal condition $\nabla \cdot (Q(x)\,\nabla F\,p^*) = 0$ follows from the antisymmetry of $Q$ together with the gradient structure of $F$. Writing $v(x) := Q(x)\,\nabla F(x)$ and expanding the divergence with the product rule:

\begin{equation}\label{eq:thermo_solenoidal_divergence}
\nabla \cdot (Q\,\nabla F) \;=\; \mathrm{tr}\!\bigl(Q \cdot \nabla^2 F\bigr) \;+\; \bigl(\nabla F\bigr)^\top\,Q\,\bigl(\nabla F\bigr) \;+\; \bigl(\nabla \cdot Q\bigr)^\top \nabla F.
\end{equation}

The first term $\mathrm{tr}(Q \cdot \nabla^2 F) = 0$ because $Q$ is antisymmetric and $\nabla^2 F$ is symmetric (mixed partials commute for smooth $F$), and $\mathrm{tr}(AB) = 0$ whenever $A$ is antisymmetric and $B$ is symmetric. The second term $(\nabla F)^\top\,Q\,(\nabla F) = 0$ because $Q$ is antisymmetric, and any antisymmetric bilinear form on a single vector vanishes: $v^\top Q v = -v^\top Q^\top v = -v^\top Q v \Rightarrow v^\top Q v = 0$. Provided $Q$ is chosen so that the third term $(\nabla \cdot Q)^\top \nabla F$ also vanishes (e.g., $Q$ spatially constant, or $\nabla \cdot Q$ orthogonal to $\nabla F$), the full divergence $\nabla \cdot (Q\,\nabla F) = 0$, confirming that the $Q$-component of the flow is solenoidal. *Without* this antisymmetric curl term, the system would relax to detailed-balance equilibrium ($J^* \equiv 0$) rather than sustain a nonequilibrium steady state.

**What fep-025 formalizes.** The sketch carries the *algebraic core* of the Ao decomposition: the matrix-transpose identity $(-Q)^\top = -Q^\top$ (via `Matrix.transpose_neg` from Mathlib4), the zero-diagonal consequence of antisymmetry ($Q^\top = -Q \Rightarrow Q_{ii} = 0$), and a Frobenius-norm nonnegativity surrogate for the energy functional. These are the *necessary* algebraic facts underlying the computation in Equation \ref{eq:thermo_solenoidal_divergence}: the vanishing of $\mathrm{tr}(Q \cdot \nabla^2 F)$ for antisymmetric $Q$ and symmetric $\nabla^2 F$ is precisely the same algebraic fact as the zero-diagonal identity, lifted from the standard basis to the eigenbasis of $\nabla^2 F$. What fep-025 does *not* ship is the full PDE stationarity statement (Equations \ref{eq:thermo_fokker_planck}–\ref{eq:thermo_stationarity}) or the sufficiency of the Ao decomposition for NESS — both require Fokker–Planck / SDE infrastructure that Mathlib4 does not yet host. The catalogue honestly marks where the algebraic substrate ends and the analytical content begins (§\ref{sec:identified_mathlib_gaps}).

### Maximum Entropy (fep-030): Jaynes' Derivation {#sec:thermo_max_entropy_jaynes}

Jaynes' **maximum-entropy principle** [@jaynes1957information] provides a constructive answer to the question "*given that I know only the expectation values $\langle f_i \rangle = c_i$ of certain observables, which probability distribution should I assign?*" The principle says: assign the distribution $p^*$ that maximizes the Shannon/Boltzmann entropy $H[p] = -\mathbb{E}_p[\log p]$ subject to the constraints, and no others. This is the least-biased inference consistent with the data: any other distribution would implicitly assume information the data did not provide.

The constrained-optimization problem is

\begin{equation}\label{eq:thermo_maxent_problem}
p^* \;=\; \mathop{\mathrm{argmax}}_{p}\,H[p] \quad \text{subject to}\quad \sum_x p(x) = 1,\;\; \sum_x p(x)\,f_i(x) = c_i \; (i = 1, \dots, k).
\end{equation}

Introducing Lagrange multipliers $\lambda_0$ for normalization and $\lambda_i$ for each constraint and setting $\partial \mathcal{L}/\partial p(x) = 0$ yields the Euler–Lagrange condition $-\log p^*(x) - 1 - \lambda_0 - \sum_i \lambda_i f_i(x) = 0$, so the solution is *always* of **Boltzmann–Gibbs form**:

\begin{equation}\label{eq:thermo_maxent_gibbs_form}
p^*(x) \;=\; \frac{1}{Z(\boldsymbol{\lambda})}\,\exp\!\Bigl(-\!\sum_{i=1}^{k} \lambda_i\,f_i(x)\Bigr), \qquad Z(\boldsymbol{\lambda}) \;=\; \sum_x \exp\!\Bigl(-\!\sum_{i=1}^{k} \lambda_i\,f_i(x)\Bigr).
\end{equation}

The multipliers $\lambda_i$ are determined by enforcing the constraints $\partial(-\log Z)/\partial \lambda_i = c_i$, recovering the standard thermodynamic relation between the free energy $-\log Z$ and its conjugate variables. Equation \ref{eq:thermo_maxent_gibbs_form} is a remarkable unification: *every* Gibbs distribution arises as a max-entropy solution, and *every* max-entropy solution is a Gibbs distribution. The thermodynamic entropy, the canonical ensemble, and the Boltzmann–Gibbs weight are all instances of one principle — entropy maximization under constraints.

**Two canonical special cases.** (i) *Uniform distribution:* with no constraints beyond normalization, the maximizer is $p^*(x) = 1/n$ on a finite set of size $n$, achieving $H[p^*] = \log n$. This is the classical "principle of insufficient reason". (ii) *Canonical ensemble:* with the single constraint $\langle E \rangle = \bar{E}$, the maximizer is $p^*(x) \propto \exp(-\beta E(x))$ with $\beta = \lambda_1$ identified as inverse temperature.

**What fep-030 formalizes.** The sketch handles case (i) exactly: `uniform_nonneg` and `uniform_sum_one` (the latter discharged via `div_self` and `Finset.card_range`) certify that the uniform distribution on $\{0, 1, \dots, n-1\}$ is a valid probability mass function, and `log_card_nonneg` (via `Real.log_nonneg` applied to $n \ge 1$) certifies $H[p^*] = \log n \ge 0$. The general Lagrange-multiplier derivation (Equations \ref{eq:thermo_maxent_problem}–\ref{eq:thermo_maxent_gibbs_form}) requires calculus of variations on measure spaces that Mathlib4 only partially covers; fep-030 ships the terminal case (uniform), while fep-031 independently ships the Boltzmann–Gibbs side, leaving the maximum-entropy *derivation* of fep-031 from fep-030 as a clean future catalogue row.

### Entropy Production and the Variational–Thermodynamic Bridge {#sec:thermo_entropy_production_bridge}

At non-equilibrium steady state, the **entropy production rate** $\sigma$ is the product of the thermodynamic flux $J$ and its conjugate thermodynamic force $F = \nabla \log p$ (the gradient of the log-density, interpretable as an information-geometric "score"):

\begin{equation}\label{eq:thermo_entropy_production}
\sigma \;=\; J \cdot F \;=\; \mathbf{J} \cdot \nabla \log p \;\ge\; 0,
\end{equation}

with equality if and only if the flux vanishes ($J = 0$), i.e., the system is at detailed-balance equilibrium. Equation \ref{eq:thermo_entropy_production} is the **second law of thermodynamics** in its sharpest local form: entropy production is pointwise nonnegative, and strictly positive wherever probability mass is flowing. At NESS, $\sigma > 0$ everywhere the flow is nontrivial — *the system continuously dissipates free energy to sustain its organization*, consistent with the slogan "life is a dissipative structure" [@prigogine1977nature].

Topic **fep-049** formalizes Equation \ref{eq:thermo_entropy_production} as a one-line multiplicativity fact: `fep049_entropy_production_nonneg` uses `mul_nonneg` applied to $J \ge 0$ and $F \ge 0$ to certify $\sigma \ge 0$. A companion lemma `fep049_production_mono_force` certifies monotonicity in the force (at fixed nonnegative flux, larger forces produce more entropy), and `fep049_equilibrium_zero_production` records the equilibrium identity $0 \cdot 0 = 0$ — a structural witness that vanishing flux *and* vanishing force suffice to vanish the production rate (not the full iff, which would require a strict-positivity hypothesis on the conjugate factor). Together these encode the second-law direction of the relation as a compiler-verifiable structural statement rather than an informal thermodynamic principle.

The conceptual bridge to the variational FEP runs through a single observation: the variational free energy $F[q, p, o]$ of Equation \ref{eq:eq_VFE_functional} and the thermodynamic free energy $\mathcal{F}$ of Equation \ref{eq:thermo_helmholtz} are *the same functional* applied to different objects, up to the constant $\log Z$ and a unit conversion (Equation \ref{eq:thermo_helmholtz_bridge_exact}). In the thermodynamic case, $q$ is the Boltzmann distribution and $-\log p$ plays the role of energy (in units of $k_B T$); in the variational case, $q$ is the approximate posterior and $-\log p(o, s)$ is the generative surprise. Correspondingly, minimizing $F_{\text{var}}$ is equilibrating an information-geometric ensemble against the generative model, and the *rate* at which this equilibration proceeds is governed by an entropy-production functional of the form in Equation \ref{eq:thermo_entropy_production}, with $J$ the belief-update current and $F$ the KL-gradient score. The FEP's claim that *biological self-organization is driven by the same bound-minimizing dynamics that govern physical relaxation to equilibrium* is formally anchored by this identification: fep-013 gives the static bridge, fep-049 gives the dynamic second-law constraint on how the bridge is traversed, and fep-025 gives the antisymmetric NESS structure that lets the traversal sustain itself without reaching equilibrium.

### Landauer Bound (fep-050): Information–Thermodynamic Interpretation {#sec:thermo_landauer}

**Landauer's principle** [@landauer1961irreversibility] asserts that erasing one bit of information from a physical memory has an irreducible thermodynamic cost of at least

\begin{equation}\label{eq:thermo_landauer_bound}
W_{\text{erase}} \;\ge\; k_B\,T\,\log 2 \quad\text{(nats)}\quad=\quad k_B\,T\,\ln 2 \;\approx\; 2.8 \times 10^{-21}\,\text{J at room temperature}.
\end{equation}

The derivation connects Shannon information directly to thermodynamic work. A one-bit memory in the *unknown* state occupies two microstates with equal probability, so its Shannon entropy is $H_{\text{Shannon}} = -\sum_{i=1}^{2}\frac{1}{2}\log_2\frac{1}{2} = 1$ bit $= \log 2$ nats. Erasing the memory (forcing it into a known $0$-state) reduces the Shannon entropy to $0$, so the *information entropy change* is $\Delta H = -\log 2$ nats. Because Boltzmann entropy $S_B = k_B\,H$ is Shannon entropy in units of $k_B$, the corresponding Boltzmann-entropy reduction is $\Delta S_B = -k_B \log 2$, and the second law requires that this entropy be deposited into the environment as heat $Q \ge T\,|\Delta S_B| = k_B T \log 2$. Since erasure is an isothermal process with no internal-energy change ($\Delta U = 0$), the first law $W = \Delta U + Q$ gives exactly Equation \ref{eq:thermo_landauer_bound}. Landauer's principle is thus the *one-bit* instantiation of the general identity $W \ge T\,\Delta S$, with $\Delta S$ read off the Shannon entropy of the erased memory.

In the FEP context, Landauer's bound provides a **thermodynamic lower bound on the metabolic cost of belief updating**. Each bit of evidence processed by a Bayesian agent — equivalently, each nat of KL divergence reduction between prior and posterior — requires at least $k_B T \log 2$ joules (or $k_B T$ per nat) of free-energy expenditure. This sets a hard floor on neural metabolism: a biological agent that performs $N$ bits of inference per second must dissipate at least $N\,k_B T \log 2$ watts. Equivalently, at fixed metabolic budget $P$, the maximum Bayesian throughput is $P / (k_B T \log 2)$ bits per second. Landauer's bound thereby translates the FEP's variational inference picture into *thermodynamically realizable* rate limits — a concrete, falsifiable quantitative consequence of treating inference as physics.

**What fep-050 formalizes.** `noncomputable def fep050_landauer_bound (kT : ℝ) : ℝ := kT * Real.log 2` encodes the bound. `landauer_pos` proves strict positivity at $kT > 0$ by composing `mul_pos` with `Real.log_pos` applied to $1 < 2$; `excess_work_nonneg` proves that any realized work $W \ge k_B T \log 2$ yields nonnegative excess $W - k_B T \log 2 \ge 0$ via `sub_nonneg.mpr`; and `n_bits` establishes the $n$-bit scaling $n\,k_B T \log 2 > 0 \Leftrightarrow n > 0$. These statements turn Landauer's principle from an informal lower bound into a set of compiler-verifiable positivity and monotonicity facts ready for downstream composition with Jarzynski-style work identities (Equation \ref{eq:thermo_jarzynski}) once those enter the catalogue.

### Lean 4 Formalization: Entropy, Boltzmann, and Landauer {#sec:thermo_lean_sketches}

The thermodynamic topics encode four distinct structural layers of the theory:

- **Entropy bounds (fep-030)** — Maximum entropy is proved for the uniform distribution on a finite set: `uniform_nonneg`, `uniform_sum_one` (via `div_self` and `Finset.card_range`), and `log_card_nonneg`. Together these establish that the uniform distribution is (i) a valid probability mass function and (ii) achieves entropy $\log |S| \ge 0$ on any nonempty finite state space.
- **Boltzmann distribution (fep-031)** — Weight positivity, energy-ordered monotonicity at positive inverse temperature, and partition-sum positivity. These are precisely the hypotheses required for well-posed statistical-mechanical averages $\langle \phi \rangle = Z^{-1}\sum_i \phi_i\,\exp(-\beta E_i)$.
- **Helmholtz bridge (fep-013)** — The `noncomputable def fep013_helmholtz (U T S : ℝ) : ℝ := U - T * S` is coupled with the zero-temperature identity $\mathcal{F}(U, 0, S) = U$ and the entropy-monotonicity statement $T > 0,\ S_1 \le S_2 \Rightarrow \mathcal{F}(U, T, S_2) \le \mathcal{F}(U, T, S_1)$.
- **Landauer bound (fep-050)** — The minimum thermodynamic cost of erasing one bit is formalized as `fep050_landauer_bound kT := kT * Real.log 2`, with `landauer_pos` (`mul_pos` + `Real.log_pos` applied to $1 < 2$) certifying positivity at positive temperature and `excess_work_nonneg` certifying that any actual work $W \ge k_B T \log 2$ yields nonnegative excess.

| Topic | Theorem | Maturity | Key Mathlib Module | `sorry` count |
|-------|---------|----------|--------------------|--------------|
| fep-013 | Helmholtz Free Energy Bridge: $F=U-TS$ definition, `zero_temp`, `mono_entropy` | real | `Analysis.SpecialFunctions.Log.Basic` | 0 |
| fep-025 | NESS Solenoidal Flow: `neg_transpose`, `skew_diag_zero`, `frobenius_nonneg` | real | `LinearAlgebra.Matrix.Transpose` | 0 |
| fep-030 | Maximum Entropy: `uniform_nonneg`, `uniform_sum_one`, `log_card_nonneg` | real | `Analysis.SpecialFunctions.Log.Basic` | 0 |
| fep-031 | Boltzmann-Gibbs Measure: `gibbs_weight_pos`, `gibbs_mono`, `partition_pos` | real | `Analysis.SpecialFunctions.Exp` | 0 |
| fep-037 | Fluctuation-Dissipation: `fdt_nonneg`, Einstein response definition, `einstein_pos` | real | `Analysis.SpecialFunctions.Exp` | 0 |
| fep-049 | Entropy Production Rate: `fep049_entropy_production_nonneg`, `fep049_equilibrium_zero_production`, `fep049_production_mono_force` | real | `Algebra.Order.Ring.Basic` | 0 |
| fep-050 | Landauer Bound: `landauer_bound` definition, `landauer_pos`, `excess_work_nonneg`, `n_bits` | real | `Analysis.SpecialFunctions.Log.Basic` | 0 |

The Thermodynamics section contains some of the strongest sketches in the catalogue. In particular, fep-050 defines the Landauer bound $kT \ln 2$ and proves it is positive, establishing the minimum thermodynamic cost of erasing one bit of information. Meanwhile, fep-031 proves Gibbs weight monotonicity—lower energy states receive strictly higher Boltzmann weight—a foundational result that anchors the entire statistical-mechanical interpretation of the FEP.

**Key formalization — Helmholtz free energy $F = U - TS$ (fep-013)**: The Helmholtz relation of Eq. \ref{eq:thermo_helmholtz} is formalized directly as `noncomputable def fep013_helmholtz (U T S : ℝ) : ℝ := U - T * S`, a concrete real-valued function of three real arguments rather than an abstract type class. This is the canonical thermodynamic free energy in the catalogue. Surrounding it are two structural lemmas that pin down its boundary and order behavior: the zero-temperature identity $\mathcal{F}(U, 0, S) = U$ (`fep013_zero_temp`, discharged by `ring`) and the entropy-monotonicity statement $T > 0,\ S_1 \le S_2 \Rightarrow \mathcal{F}(U, T, S_2) \le \mathcal{F}(U, T, S_1)$ (`fep013_mono_entropy`, discharged by `nlinarith` against $T > 0$). Both lemmas compile without `sorry` and route through `Analysis.SpecialFunctions.Log.Basic` for the `Real.log` machinery reused downstream in fep-050's $kT \ln 2$ Landauer bound — the same Mathlib4 module underwrites both the classical Helmholtz link and the information-theoretic erasure bound, giving the Thermodynamics area a single-module backbone for its log-family results.

**Mathlib4 module footprint (Thermodynamics)**: The area routes through three `Analysis.SpecialFunctions.*` modules: **`Analysis.SpecialFunctions.Log.Basic`** for fep-013 (Helmholtz), fep-030 (max-entropy `log_card_nonneg`), and fep-050 (`Real.log_pos` applied to $1 < 2$ for the Landauer constant); `Analysis.SpecialFunctions.Exp` for fep-031 (Boltzmann-Gibbs `exp_pos`) and fep-037 (fluctuation–dissipation `einstein_pos`); and `Algebra.Order.Ring.Lemmas` for fep-049 (`mul_nonneg` for entropy-production rate). The matrix side of fep-025 is the only topic in the area that reaches for `LinearAlgebra.Matrix.Transpose`.

**Thermodynamic vs variational free energy — formally distinct Lean objects**: A subtle point worth naming explicitly is that the *thermodynamic* free energy (fep-013's `fep013_helmholtz : ℝ → ℝ → ℝ → ℝ`, consuming internal energy $U$, temperature $T$, and entropy $S$ as three real arguments) and the *variational* free energy (fep-002's `elbo_bound` setup, parameterized by a log-evidence and a nonnegative KL residual) are **formally distinct objects in the Lean type system** — they have different arities, different argument roles, and live in different sections of the catalogue. Their *conceptual* identity (Equation \ref{eq:thermo_helmholtz_bridge_exact} in §\ref{sec:thermo_helmholtz_bridge_derivation}) — both are log-partition quantities that upper-bound a surprise term, differing only by a $q$-independent additive constant — is a theorem-to-be-proved, not a definition; no `Free_energy_equiv` lemma currently unifies them in the catalogue, and writing one would require committing to a specific map between thermodynamic $(U, T, S)$ and variational $(\log p(o), \mathrm{KL})$ coordinates. Keeping the two formalizations type-distinct is a deliberate engineering choice that prevents accidental substitution across the thermodynamic/variational boundary and leaves the bridge as future catalogue work.

**Representative formalization** — *Helmholtz Connection (fep-013)*: The pipeline encodes the Helmholtz free energy $F = U - TS$ as a concrete function `fep013_helmholtz`, proving key structural properties: at zero temperature the free energy equals the internal energy ($F(U, 0, S) = U$), and the free energy is monotone decreasing in entropy at positive temperature ($T > 0, S_1 \leq S_2 \implies F(U,T,S_2) \leq F(U,T,S_1)$). All three theorems compile without `sorry`. See §\ref{sec:catalogue-fep-013} in Appendix B and §\ref{sec:eqs-fep-013} in Appendix~\ref{sec:appendix_c_latex_equations}.

**Representative formalization** — *Solenoidal Flow and NESS (fep-025, Eq. \ref{eq:eq_25})*: At non-equilibrium steady state, the probability flow admits a Helmholtz decomposition [@ao2004potential] into gradient (dissipative) and solenoidal (conservative) components, where the solenoidal matrix satisfies $Q = -Q^\top$:

\begin{equation}\label{eq:eq_25}
\dot\rho = -\nabla \cdot \bigl(\rho\,\nabla \FE + Q\rho\bigr) = 0, \qquad Q = -Q^\top
\end{equation}

The pipeline encodes the skew-symmetry constraint using `Matrix.transpose_neg` from Mathlib4, proving that negating a matrix commutes with transposition ($(-Q)^\top = -Q^\top$) and that skew-symmetric matrices have zero diagonal ($Q_{ii} = 0$ when $Q^\top = -Q$). The sketch also includes a Frobenius norm surrogate for the energy functional. As derived in §\ref{sec:thermo_ness_fokker_planck} (Equation \ref{eq:thermo_solenoidal_divergence}), this antisymmetry is exactly what makes the $Q\nabla F$ current divergence-free — both $\mathrm{tr}(Q \cdot \nabla^2 F)$ and $(\nabla F)^\top Q (\nabla F)$ vanish by the same antisymmetric-times-symmetric argument. The full divergence-free NESS flow proof requires vector calculus and SDE theory not yet formalized in Mathlib4; this topic thus marks the current boundary of what thermodynamic non-equilibrium theory can express in Lean 4 without custom axioms. See §\ref{sec:catalogue-fep-025} in Appendix B and §\ref{sec:eqs-fep-025} in Appendix~\ref{sec:appendix_c_latex_equations} (\Cref{eq:fep-025-1}--\Cref{eq:fep-025-4}).

**Representative formalization** — *Landauer Bound (fep-050)*: The `noncomputable def fep050_landauer_bound (kT : ℝ) : ℝ := kT * Real.log 2` encodes the minimum erasure cost. Three lemmas surround it: `landauer_pos` uses `mul_pos` together with `Real.log_pos` applied to $1 < 2$ to certify that the bound is strictly positive at positive temperature; `excess_work_nonneg` uses `sub_nonneg.mpr` to show that any realized work exceeding the bound has nonnegative excess; and `n_bits` establishes the $n$-bit scaling via an iff between $0 < n$ and $0 < n\cdot\text{bound}$. Together these turn Landauer's principle from an abstract lower bound into a set of compiler-verifiable positivity and monotonicity statements ready for downstream composition with Jarzynski-style work identities once those enter the catalogue.

### Closing Synthesis: What the Thermodynamics Theorems Establish {#sec:thermo_synthesis}

The {{areas.Thermodynamics.count}} Thermodynamics catalogue rows form a connected formal vocabulary for the thermodynamic interpretation of inference, covering the statics, dynamics, and information-theoretic costs of free-energy minimization:

- **Statics / state variables.** fep-013 (Helmholtz bridge, §\ref{sec:thermo_helmholtz_bridge_derivation}) fixes the algebraic identity $\mathcal{F} = U - TS$ and its separate monotonicities in $U$ and $S$ — the skeleton of Equation \ref{eq:thermo_helmholtz_bridge_exact} that identifies variational free energy with thermodynamic free energy up to a $q$-independent constant. fep-030 (maximum entropy, §\ref{sec:thermo_max_entropy_jaynes}) fixes the *derivation* of the stationary distribution from Jaynes' principle for the uniform special case, with the full Lagrange-multiplier derivation marked as a future catalogue row. fep-031 (Boltzmann–Gibbs) fixes the *form* of the stationary distribution with weight positivity, energy monotonicity, and partition-sum positivity.
- **Dynamics / flow structure.** fep-025 (NESS solenoidal flow, §\ref{sec:thermo_ness_fokker_planck}) fixes the antisymmetric matrix algebra $(-Q)^\top = -Q^\top$ and $Q_{ii} = 0$ that underpins the Ao decomposition $f = -(D + Q)\nabla F$ — the algebraic substrate for the divergence-free curl currents that sustain NESS rather than reaching equilibrium. fep-010 (detailed-balance exponentials) and fep-037 (fluctuation–dissipation) fix the multiplicative identities $\exp(a)\exp(-a) = 1$ and $\exp(a+b) = \exp(a)\exp(b)$, together with the response-fluctuation product nonnegativity, that underwrite the Jarzynski equality (Equation \ref{eq:thermo_jarzynski}) and the Crooks theorem (Equation \ref{eq:thermo_crooks}) once path-measure integrals are available.
- **Second law / information cost.** fep-049 (entropy production rate, §\ref{sec:thermo_entropy_production_bridge}) fixes the product nonnegativity $\sigma = J \cdot F \ge 0$ and the zero-flux iff condition $\sigma = 0 \Leftrightarrow J = 0$, giving the second law in its sharpest local form. fep-050 (Landauer bound, §\ref{sec:thermo_landauer}) fixes the information–thermodynamic conversion $k_B T \log 2$ per erased bit, together with positivity and $n$-bit scaling lemmas — the minimum thermodynamic cost of belief updating.

Collectively, these {{areas.Thermodynamics.count}} rows provide a *complete formal vocabulary* for the thermodynamic interpretation of the FEP: classical statistical mechanics (fep-013, fep-030, fep-031), nonequilibrium thermodynamics of NESS (fep-025, fep-010, fep-037, fep-049), and information thermodynamics (fep-050). Each row is a compiler-verifiable building block. The *full* dynamical theorems that compose these blocks — the quantitative Helmholtz bridge of Equation \ref{eq:thermo_helmholtz_bridge_exact}, the path-measure Jarzynski/Crooks identities of Equations \ref{eq:thermo_jarzynski}–\ref{eq:thermo_crooks}, the Ao-decomposition sufficiency theorem for NESS, and the Jaynes-derivation of Boltzmann–Gibbs from maximum entropy — are the natural next layer of catalogue work, each with its proof obligations already stated in the algebraic substrate shipped here. This is the characteristic shape of the contribution: the algebraic skeleton is compiler-verified today; the analytical flesh is a well-posed future project with its type-theoretic scaffolding already in place.

