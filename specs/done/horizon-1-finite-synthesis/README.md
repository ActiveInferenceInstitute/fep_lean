# Horizon 1 finite synthesis

Status: **accepted and complete**.

Horizon 1 exists to replace a catalogue of individually meaningful finite
results with one inspectable vertical certificate, while making the remaining
scientific gaps executable rather than rhetorical. The mathematical scope is
owned by the [Horizon 1 design](../../../docs/design/fep-research-program/horizon-1-finite-synthesis.md),
and the cross-horizon evidence rules live in the
[research contract](../../../docs/design/fep-research-program/research-contract.md).
This archived spec records why the implementation has its final shape, the
invariants future work must preserve, and the alternatives that failed.

## What Horizon 1 establishes

The terminal theorem is
`FEPComposed.FiniteReferenceAgent.finiteReferenceAgent_terminal` in
`src/fep_lean/formal/compositions/finite_reference_agent.lean`. It composes
maintained owners rather than restating their results:

- the fixed Boolean learner starts from a fair prior and reaches masses
  (1/10) and (9/10) after two true observations;
- one further true observation is lifted to the shared 16-state Boolean
  ((I,S,A,E)) carrier through exact posterior and marginal bridges;
- posterior-form variational free energy has the exact posterior as its unique
  optimum;
- an explicit asymmetric posterior report loss gives an attained one-step
  observation-dependent decision, and the emitted `true` action is the action
  interface's positive-time refresh kernel;
- the same carrier has a full-support stationary law that factorizes as
  (P(S,A)P(I\mid S,A)P(E\mid S,A)), hence
  (I\perp E\mid(S,A)), and is invariant under that selected kernel; and
- the same lifted updated posterior yields strict decrease of both the
  repository-real and Mathlib-native divergences (D(P\|\pi)).

This is one finite, synthetic, model-specific certificate. It does not prove
transition-aware planning, expected-free-energy-optimal control, physical
thermodynamic dissipation, causal identification, empirical adequacy, or a
universal Free Energy Principle.

## Why the result has this shape

### One carrier, not coincidental Boolean types

The first terminal attempt exposed two genuine incompatibilities: the learned
posterior was non-Dirac while the policy model interpreted a Boolean belief as
a point mass, and the policy state had cardinality two while the blanket state
had cardinality sixteen. The record `FiniteReferenceCoherence` and the theorems
immediately following it retain that failed merge as a proved boundary.

The accepted repair did not coerce those carriers. H1.4 introduced a bounded
belief index whose interpretation contains the exact learned law. H1.7 then
owned the lift from an internal law to the 16-state blanket carrier, the lifted
likelihood/posterior commutation laws, and the action-indexed hold/refresh
semigroup. The terminal leaf only composes those maintained seams.

### A genuine sensory--active blanket

A singleton conditioner can make a factorization syntactically easy while
evading the scientific claim. The final theorem instead uses the existing
`FEP.MarkovBlanket.Blanket Bool Bool` owner, which is the nontrivial
sensory--active product, proves positive support on distinct blanket states,
and reconstructs the same stationary joint pointwise from its blanket law and
conditional internal--external law.

### Decision first, broader control later

The maintained policy-tree model has no transition field. Horizon 1 therefore
proves the strongest honest connection available: the exact posterior drives
an asymmetric one-step decision, and the emitted action is passed unchanged to
the transition-bearing action interface. It does not claim that tree values
optimize downstream transition consequences or expected free energy. Those
are later carrier and objective seams, not omitted proof steps.

### Native and repository KL stay distinct

The project finite KL is real-valued and totalized; Mathlib's measure KL is
extended nonnegative real and preserves singular infinity. The bridge keeps
full reference support explicit and fixes the orientation as (D(P\|\pi)).
H1.2's native mutual-information data processing is likewise not renamed as
the project's real-valued finite epistemic value because no maintained bridge
identifies those carriers.

## Invariants

Future work must preserve all of the following:

- Lean `v4.33.1`, Mathlib tag `v4.33.1`, and revision
  `0df444a360eaa60ab8c11dca51a86af692955474` remain one exact pin set.
- `src/fep_lean/formal/manifest.py` is the only formal-resource roster;
  projections, package data, aggregate imports, declaration ownership, and
  release provenance derive from it.
- foundations and new composition leaves have unique declaration namespaces;
  only the sealed released compatibility roster may use flat `FEPComposed`.
- the first H1.8 non-coherence result remains public evidence. A positive
  terminal theorem must not erase a failed carrier translation.
- posterior learning, the VFE optimum, decision state, emitted action,
  transition kernel, blanket factorization, invariant law, and strict KL claim
  must be connected by named equalities on the same concrete carrier.
- blanket factorization and transition invariance are separate facts. Horizon
  1 does not infer rowwise blanket dynamics, causal identification, or
  free-energy descent from either one.
- strict KL belongs only to the positive-time refresh branch and a nonuniform
  input law. The hold branch is identity and may only support equality or
  nonincrease.
- public theorem receipts must remain warning-free and free of `sorry`,
  `admit`, opaque proof shortcuts, or custom axioms.
- broader publication receipts are regenerated after source freeze; archived
  H1 acceptance is not a substitute for a current release bundle.

## Canonical pointers

- Formal ownership and projections:
  `src/fep_lean/formal/manifest.py`, `src/fep_lean/formal/declarations.py`, and
  `scripts/_maint_build_formal_modules.py`.
- Scientific implication boundaries:
  `src/fep_lean/formal/compositions/finite_scientific_implications.lean`.
- Native KL and decision risk: `src/fep_lean/formal/decision_risk.lean`.
- Repeated posterior learning:
  `src/fep_lean/formal/finite_posterior_learning.lean`.
- Posterior-indexed decision and emitted action:
  `src/fep_lean/formal/compositions/finite_policy_action.lean`.
- Blanket/action semigroup and strict contraction:
  `src/fep_lean/formal/continuous_time_markov.lean`.
- Terminal composition and retained no-go:
  `src/fep_lean/formal/compositions/finite_reference_agent.lean`.
- Decision history and rejected alternatives: [`choices.md`](choices.md).
- Exact H1.0 pin/API probe:
  [`spikes/h1_0_mathlib_readiness.lean`](spikes/h1_0_mathlib_readiness.lean).

The corresponding `tests/test_horizon1_*.py` files pin public declarations,
source ownership, scientific boundaries, projection parity, and native compile
behavior. Exact theorem rosters remain discoverable from the formal manifest
and declaration parser rather than duplicated here.

## Accepted evidence

The final serialized native barrier built `FepSketches.fep_all` and
`FepSketches.composed` successfully across 8,745 jobs. The focused H1/formal
matrix passed 117 tests with 16 opt-in cases skipped. Formal projections were
byte-current, and the five terminal public theorems compiled warning-free with
axiom probes reporting only `propext`, `Classical.choice`, and `Quot.sound`.

Independent Lean, domain, and skeptical reviews accepted the repaired theorem
and the narrow wording above. GitNexus could not index this nested checkout, so
impact analysis used source/import tracing plus focused consumer tests; graph
completeness therefore has reduced confidence, while the tested formal
contracts do not.

No visual baseline or inspiration asset governed this formal slice. The
graphical abstract belongs to the manuscript publication contract, not this
spec.

## Next boundary

Horizon 2 may open at H2.0. Horizon 3 remains closed until the H2.7 exit and
the H3.G0 stop/go decision. Any later finite fallback must reuse the accepted
terminal carrier or introduce an explicit reviewed bridge; it must not call the
proved first H1.8 carrier mismatch a successful composition.
