# GNN bridge Q3 — continuous-family denotation over the linear-Gaussian carrier

Status: **accepted; the denotation module `gnn_denotation_continuous.lean` is
registered, the exemplar isomorphism-class statement is proved warning-free
with no `sorry` and no new axioms, and the slice is verified end-to-end; see
[REPORT.md](REPORT.md) for the evidence record**. Last updated: 2026-09-04.

This slice opens Direction 2 stage Q3 of the [GNN bridge
program](../../docs/design/gnn-bridge/README.md) under the [bridge
contract](../../docs/design/gnn-bridge/bridge-contract.md) (section 6 stage
S4, section 7 evidence firewall, section 9 no-go registry). Phase definition
and acceptance: [direction-2-gnn-to-lean.md](../../docs/design/gnn-bridge/direction-2-gnn-to-lean.md)
(Q3 row and alignment statement 3).

Q1 — the document AST and decidable well-formedness — is accepted under
[`specs/gnn-bridge-q1-syntax-ast/`](../gnn-bridge-q1-syntax-ast/README.md)
(module `src/fep_lean/formal/gnn_document.lean`, namespace `FEP.GnnDocument`).
Q2 — the discrete-family denotation — is accepted under
[`specs/gnn-bridge-q2-discrete-denotation/`](../gnn-bridge-q2-discrete-denotation/README.md)
(module `src/fep_lean/formal/gnn_denotation.lean`, namespace `FEP.GnnDenotation`).
This slice reuses the Q1 AST, its cross-section extractors (`stateSpaceDecls`,
`parameterizationEntries`, `ontologyBindings`, `WellFormed`), and the Q2
document-lookup helper pattern (`dimNat`, `dimsNat`, `findDecl`, `declDims`,
`parameterizes`, `bindsTerm`) without modifying either accepted module; the
lookups are re-declared in the Q3 namespace rather than importing the Q2
module, so the continuous slice does not couple to the discrete carriers.

## What this slice formalizes

A **denotational semantics** of the continuous linear-Gaussian family: a
well-formed continuous-family GNN document, read under the frozen conventions
below, denotes an instance of the `linear_gaussian_semigroup.lean`
`LinearGaussianParameters`. This realizes [alignment statement
3](../../docs/design/gnn-bridge/direction-2-gnn-to-lean.md):

> A well-formed continuous-family document denotes a `LinearGaussianParameters`
> instance (`F/H/Q/R`, `prior_mean`/`prior_cov`), matching
> `linear_gaussian_semigroup.lean` transition laws.

The six payload variables are bound to the carrier by the frozen prior-gauge
convention, the declared dimensions are checked against the carrier axis, the
`InitialParameterization` entries are checked present, and the
`ActInfOntologyAnnotation` field bindings are checked against the frozen
ontology convention. "Matching the transition laws" is realized by the
denotation landing in the carrier — the denoted instance's `transitionMean`,
`transitionCovariance`, and derived `covariance` ARE the carrier's laws by
construction — and is exhibited by corollaries that drop the denoted exemplar
into existing carrier theorems, mirroring Q2's corollary pattern.

## Frozen Q3 conventions (the document cannot pin these down)

These are the conventions the GNN document's syntax cannot determine; they are
fixed once here and named, not silently resolved. Each is grounded in the
bridge contract's model-kind table (section 3), the P4 boundary record
([`specs/gnn-bridge-p4-continuous-spike/README.md`](../gnn-bridge-p4-continuous-spike/README.md)),
and the exemplar's own parameterization comments.

1. **Axis reading (state variable → carrier axis).** The exemplar's
   hidden-state variable `x` (ontology-bound `ContinuousHiddenState`) is
   declared `x[2,1]`. The frozen reading is the column convention: the first
   declared dimension is the state dimension `n`, the trailing `1` is the
   column-vector convention inherited from the discrete family's state
   blocks. The carrier axis is `Fin n` with payload slot `i` ↔ `Fin i`. This
   is the isomorphism-class caveat of the acceptance statement: a different
   enumeration yields the transported model (for the exemplar, the swapped
   enumeration transports `prior_cov = diag(1/2, 1)` to `diag(1, 1/2)` and
   hence the precision to `diag(1, 2)` — a different carrier instance).
2. **Field surface.** The six continuous-family payload variables are `F`,
   `H`, `Q`, `R`, `prior_mean`, `prior_cov` (bridge contract section 3,
   continuous model kind). Conformance requires each declared with literal
   dimensions (`F`, `H`, `Q`, `R`, `prior_cov` = `[n, n]`; `prior_mean` =
   `[n]`), each parameterized by an `InitialParameterization` entry, and the
   six frozen ontology bindings present: `F=StateTransitionMatrix`,
   `H=ObservationMatrix`, `Q=ProcessNoiseCovariance`,
   `R=ObservationNoiseCovariance`, `prior_mean=PriorMean`,
   `prior_cov=PriorCovariance` (all present in the exemplar document).
3. **Denotation (prior gauge).** The carrier `LinearGaussianParameters` is
   the symmetric-precision stationary parameterization: raw precision
   (positive definite) plus center, with stationary covariance
   `covariance = precision⁻¹`. The document's Equations section declares the
   initial law `x_1 ~ N(prior_mean, prior_cov)`, so the frozen convention is:
   `center := prior_mean` payload, `precision := prior_cov⁻¹` payload — a
   mechanical matrix inversion of the declared prior covariance. Conformance
   carries the payload obligation `priorCov.PosDef`, from which the carrier's
   `precision_posDef` follows by the existing `Matrix.PosDef.inv`.
4. **Role of the `F`/`H`/`Q`/`R` payload values — the P4 boundary, not a
   silent convention.** The document's one-step dynamics/observation surface
   is recorded in the payload and checked at the document surface (literal
   dims, parameterization, bindings), but its numeric values are **not
   consumed** by the denotation. Two grounded reasons, both recorded at the
   family-wide level in the P4 boundary record: (a) the carrier models only
   the state transition semigroup — there is no observation model
   (`H`, `R`) inside `LinearGaussianParameters`; (b) identifying the
   document's one-step decimal `F` with the carrier's `evolution t =
   exp(-t·precision)` is exactly the P4 no-go (transcendental evolution
   entries vs the fixed exact-terminating-decimal policy,
   Lindemann–Weierstrass), and the exemplar's Euler-discretized
   `F = [[1, 1/10], [0, 9/10]]` is not even symmetric, while the carrier's
   precision is symmetric positive definite by construction. A future
   dynamics-gauge slice (recovering precision from one-step data via the
   discrete Lyapunov relation) is the recorded follow-up, not this slice.
5. **Numeric payload domain and the rounding boundary.** The semantic domain
   of the payload entries is `ℝ`. Per the P1 rounding policy (exact Lean
   rationals emitted as shortest exact terminating decimal strings), each
   decimal literal in the exemplar's `InitialParameterization` is read as its
   exact rational value (`1.0 → 1`, `0.9 → 9/10`, `0.1 → 1/10`, `0.2 → 1/5`,
   `0.5 → 1/2`, `0.0 → 0`); non-terminating expansions are a no-go, never
   rounded. The `type=float` declarations mark the GNN runtime's approximate
   numerics; the rounding boundary is explicit and two-sided: the Lean
   denotation is stated over the exact rationals only, and no Lean statement
   here claims that the GNN runtime's `float64` arithmetic equals them
   (direction-2 open problem "float dimensions", honored rather than
   pretended away).
6. **Closed-loop fields are out of scope.** `goal_mean`/`control_gain` (the
   closed-loop continuous kind) land outside the carrier, which has no
   control input. The fixed exemplar is a passive document (no control
   input), so the issue does not arise for it; a closed-loop exemplar would
   need its own convention and is not attempted here.

## Payload-string → typed-table interpretation (the Q1 deferral, carried forward)

As in Q2, this slice does **not** implement a payload-string parser. The
transcription step from the document's verbatim brace-block payload strings
(e.g. `prior_cov={( (0.5, 0.0), (0.0, 1.0) )}`-shaped text, here written
multi-line) to the typed `ℝ` tables the denotation consumes is the P1
rounding policy in action: each decimal literal is read as its exact rational
value and placed at its payload position under the axis enumeration above.
For this slice that interpretation is **applied** — the exemplar's typed
payload (`sdPayload`) carries the exact transcribed values — and the
boundary is named here as a finding for the GNN side. A full payload-string
parser remains an explicit follow-up; it is out of scope here and is not
needed to prove the exemplar statement.

## Fixed exemplar

The fixed exemplar is
`GeneralizedNotationNotation/input/gnn_files/continuous/stochastic_dynamics.md`
(read-only; GNN `v1`, passive linear-Gaussian LGSSM document). It is chosen
over the sibling continuous exemplars because it fits the frozen surface with
the least convention debt: it is passive (the closed-loop
`continuous_navigation.md` carries `goal_mean`/`control_gain`, outside the
carrier per convention 6), it parameterizes **all six** field variables (as
does `predictive_coding_agent.md` itself, whose `InitialParameterization`
spans `F`/`H`/`Q`/`R`/`prior_mean`/`prior_cov`; only the Q1 module's
`predictiveCodingExcerpt` — an excerpt transcription of that file — carries
two entries), and its `prior_cov = diag(0.5, 1.0)` makes
the precision recovery genuine (`diag(2, 1)`, not the identity) so the axis
enumeration caveat has numerical content.

The document is transcribed into a `GnnDocument` value `sdDoc` in the module,
exercising the full thirteen-section inventory in canonical order, the nine
state-space declarations (including `type=float` and `type=int` value types),
the six connection edges, the six parameterization entries, the nine ontology
bindings, and the five model parameters. Its exact literals: `F =
[[1, 1/10], [0, 9/10]]`, `H = [[1, 0], [1, 0]]`, `Q = (1/10)·I`,
`R = (1/5)·I`, `prior_mean = (0, 0)`, `prior_cov = diag(1/2, 1)`.

The acceptance statement is `denoteContinuous sdDoc sdPayload sdConforms =
stochasticDynamicsParameters`, where `stochasticDynamicsParameters` is the
hand-stated reference carrier instance (precision `diag(2, 1)`, zero center —
stationary covariance `diag(1/2, 1)`, exactly the document's declared prior).
The statement's content: the frozen prior-gauge convention, applied to the
document's exact literals, mechanically recovers the hand-derived precision
and center as a `LinearGaussianParameters` value.

## Acceptance

- [x] Bounded spec slice opened before any Lean code landed (this file).
- [x] Formal module `src/fep_lean/formal/gnn_denotation_continuous.lean`
  (namespace `FEP.GnnContinuous`) defines the continuous-family denotation
  over the existing carrier (`LinearGaussianParameters` from
  `linear_gaussian_semigroup.lean`); registered in
  `src/fep_lean/formal/manifest.py` immediately after the `gnn_denotation`
  row.
- [x] The exemplar document is transcribed (`sdDoc`) and its well-formedness
  is proved (`WellFormed sdDoc`, by `decide`).
- [x] The exemplar denotation isomorphism-class statement is proved:
  `denoteContinuous sdDoc sdPayload sdConforms = stochasticDynamicsParameters`,
  warning-free, no `sorry`, no new axioms.
- [x] Corollaries connect the denoted parameters to the carrier's derived
  quantities: the stationary covariance equals the document's declared prior
  covariance, and the zero-time transition laws (Dirac boundary) hold via the
  existing `transitionMean_zero` / `transitionCovariance_zero`.
- [x] `cd lean && lake build FepSketches` — zero errors, zero warnings.
- [x] `uv run python scripts/_maint_build_formal_modules.py --check` and
  `uv run python scripts/_maint_build_fep_all_lean.py --check` green after
  registration.
- [x] Gate parity: `build_formalism_coverage.py --check`,
  `_maint_build_lean_landscape.py --check`,
  `docs/check_links.py --strict --include-root`, `docs/md_hygiene.py --strict`,
  and `uv run pytest tests/test_formal_composition.py
  tests/test_native_evidence.py -q`.

## Mathlib dependency

The denotation module imports the carrier (`FepSketches.linear_gaussian_semigroup`)
and, transitively, `Mathlib.LinearAlgebra.Matrix.PosDef` (via
`Mathlib.Analysis.Matrix.PosDef`). `Init`-only is impossible here: the carrier
itself is Mathlib-based (`linear_gaussian_semigroup.lean` opens with Mathlib
imports). This is the genuine, recorded Mathlib requirement; the Q1 AST module
stays `Init`-only because it carries no semantics. The Q2 module's two Mathlib
imports (`Fintype.Basic`, `BigOperators`) are mirrored for the `Fintype.card`
reductions, plus `Mathlib.LinearAlgebra.Matrix.Notation` for the payload matrix
literals.

## No-go and risk register

| Trigger | Disposition in this slice |
| --- | --- |
| Exemplar conventions require semantic interpretation beyond syntax | The six conventions above are named and frozen in this README, not resolved silently; the payload-string → typed-table step is applied (not parsed) and recorded as a finding for the GNN side. |
| `InitialParameterization` brace-block shape and full decimal parser | Deferred (Q1/Q2 deferral carried forward); out of scope for the exemplar statement. |
| Identifying the document's one-step `F`/`Q` decimals with the carrier's `exp(-t·precision)` law | No-go per the P4 boundary record (transcendental evolution entries; asymmetric Euler `F`); the `F`/`H`/`Q`/`R` values are recorded but not consumed; a dynamics-gauge slice is the recorded follow-up. |
| Observation model (`H`, `R`) inside the carrier | No-go: `LinearGaussianParameters` has no observation fields; recorded, not fabricated. |
| Closed-loop `goal_mean`/`control_gain` fields | Out of scope (convention 6); the fixed exemplar is passive. |
| Non-terminating-decimal payloads | No-go per the P1 rounding policy; the exemplar's payloads are all exact terminating decimals. |
| `type=float` exactness pretense | No-go: the denotation is stated over exact rationals; no claim connects it to runtime float behavior (convention 5). |
| A different axis enumeration than slot `i` ↔ `Fin i` | Would yield the transported model; recorded as the isomorphism-class caveat (convention 1). |
| Mathlib/API blocker | None anticipated; `Matrix.posDef_diagonal_iff` / `Matrix.PosDef.inv` / `Matrix.diagonal_mul_diagonal` cover the diagonal-payload proofs. |

## Boundaries

- The formal module is additive: one new foundation resource, no edits to the
  accepted Q1 AST module, the accepted Q2 denotation module, or any existing
  Lean carrier; no catalogue topics, no relation or atlas claims, no `fep-NNN`
  identifier.
- `composed.lean` stays the import-only aggregate over composition leaves; a
  foundation module is not imported there, and `fep_all.lean` is
  catalogue-body-driven and does not list this module.
- Cross-repo references are inline code paths, never markdown links (bridge
  contract decision 8).

## Mirror-folder findings for the GNN side

1. The continuous-family brace-block payload shape (`((…), (…))` rows for a
   matrix, `(…)` for a vector) is the convention the bridge relies on, same
   as the discrete family — a future payload-string parser needs this frozen
   target in `GeneralizedNotationNotation/doc/other/fep_lean/`.
2. The exemplar's `F` bakes in an Euler discretization at `dt = 0.1`
   (`ModelParameters`), so "one-step `F`" is not identifiable with a
   continuous-time carrier law without a declared step-time semantics. A
   future dynamics-gauge slice needs either a `StepTime`-style declared
   semantic field or a drift-matrix section on the GNN side.
