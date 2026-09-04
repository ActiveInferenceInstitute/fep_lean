# GNN bridge Q4 — renderer and execution statements

Status: **verified end-to-end; the statement module
`gnn_render_statements.lean` is registered, the matrix-fragment and
execution-semantics statements are proved warning-free with no `sorry` and
no new axioms, and all slice gates are green — see [REPORT.md](REPORT.md)
for the evidence record**. Last updated: 2026-09-04.

This slice opens Direction 2 stage Q4 of the [GNN bridge
program](../../docs/design/gnn-bridge/README.md) under the [bridge
contract](../../docs/design/gnn-bridge/bridge-contract.md) (section 6 stage
S6, section 7 evidence firewall, section 9 no-go registry). Phase definition
and acceptance:
[direction-2-gnn-to-lean.md](../../docs/design/gnn-bridge/direction-2-gnn-to-lean.md)
(Q4 row and alignment statement 5):

> **Renderer preservation.** For each render target, the rendered program's
> denotation equals the document's denotation (statement per target; proofs
> follow only where a target has a formal semantics to state against).

Q1 — the document AST and decidable well-formedness — is accepted under
[`specs/gnn-bridge-q1-syntax-ast/`](../gnn-bridge-q1-syntax-ast/README.md)
(module `src/fep_lean/formal/gnn_document.lean`, namespace `FEP.GnnDocument`).
Q2 — the discrete-family denotation — is accepted under
[`specs/gnn-bridge-q2-discrete-denotation/`](../gnn-bridge-q2-discrete-denotation/README.md)
(module `src/fep_lean/formal/gnn_denotation.lean`, namespace
`FEP.GnnDenotation`). This slice reuses both modules **without modifying
them**, plus the kernel machinery of `src/fep_lean/formal/finite_probability.lean`
(`FiniteKernel.comp`, `FiniteKernel.predictive` and their laws) and
`src/fep_lean/formal/finite_markov_dynamics.lean` (`kernelPower`,
`kernelPower_add` — the discrete Chapman–Kolmogorov law, the discrete
counterpart of the `FiniteMarkovSemigroup.transition_add` semigroup law of
`src/fep_lean/formal/continuous_time_markov.lean:89`).

## What this slice formalizes

Two things, per the Q4 row:

1. **Alignment statement 5 per render target.** For each of the nine render
   targets of `GeneralizedNotationNotation/src/render/`, either a Lean
   `Prop`-valued statement of the preservation fragment that fep_lean can
   state today, or a documented no-go row — never a fake statement.
2. **Execution semantics composed from the kernel machinery.** The
   policy-conditioned rollout of a denoted discrete-family model, proved
   equal to the `kernelPower` composition of its transition kernel — the
   semantic target that any discrete-family execute target must realize.

The Q4 acceptance bar is *statements accepted in a slice; proofs scheduled
or explicitly deferred*. Statements that reduce mechanically to existing
carrier theorems are proved in this slice; everything else is scheduled in
the proof-schedule table below or carries a no-go row.

## Frozen Q4 conventions (the syntax cannot pin these down)

1. **Target layout contract, discrete family.** The four matrix-emitting
   discrete-family render targets (pymdp, activeinference_jl, jax,
   jax_pomdp) consume the five tables under one frozen layout:
   `A[observation, hidden_state]`, `B[next_state, previous_state, action]`,
   `C[observation]`, `D[hidden_state]`, `E[action]`. Evidence in the GNN
   sources: `GeneralizedNotationNotation/src/render/pymdp/pymdp_renderer.py`
   (comment "pymdp 1.0.0 B[s',s,a]"),
   `GeneralizedNotationNotation/src/render/jax/jax_renderer.py`
   (`self.models.B[:, :, action]` composed with `self.models.A[observation, :]`),
   and `GeneralizedNotationNotation/src/render/activeinference_jl/activeinference_renderer.py`
   (shape assertions `(NUM_OBSERVATIONS, NUM_STATES)` and
   `(NUM_STATES, NUM_STATES, NUM_ACTIONS)`; next-state read `B[:, current_state, action]`).
   This is exactly the Q2 payload order (`aLikelihood outcome state`,
   `bTransition next previous policy`), so the target layout map is the
   identity on the Q2 payload tables — the fact the slice's matrix-fragment
   statements make precise.
2. **Statement shape, and why it is not fake.** The statable statement per
   target is *conditional*: if the target's consumed tables are faithful to
   the document's payload under the frozen target layout, then they coincide
   with the carrier masses of the denoted model (`denoteDiscrete`). The
   antecedent is the renderer's own layout contract (a checkable, pointwise
   property), the consequent is a carrier-level equality — no quantification
   over arbitrary "semantics" is introduced. The full program-denotation
   equality of alignment statement 5 (the rendered *program's* behavior) is
   not statable where no formal semantics of the target language exists in
   fep_lean; those targets get no-go rows, not placeholder Props.
3. **Execution semantics, discrete family.** Under a fixed policy, the
   executed rollout of a denoted model is the iterated predictive of its
   transition kernel; the slice proves it equals the `kernelPower` of the
   kernel applied to the initial law, plus the time-additivity corollary
   (`policyRollout m policy (k + n)` through `kernelPower_add` — the discrete
   Chapman–Kolmogorov composition, sibling of
   `FiniteMarkovSemigroup.transition_add`). Per-step *observation updates*
   (belief filtering) are alignment statement 4's territory and stay outside
   this slice.
   The fixed-policy rollout coincides with the carrier's existing open-loop
   machinery: `active_inference.lean` already ships `rolloutKernel` /
   `plannedState` / `rolloutKernel_append` (open-loop policy lists), and the
   module proves `rolloutKernel m (List.replicate n policy) =
   kernelPower n (m.transition policy)` and
   `policyRollout m policy n = plannedState m (List.replicate n policy)` —
   the Q4 execution semantics is the fixed-policy special case of the
   carrier's plan machinery, not a second rollout registry.
4. **Continuous family.** The continuous denotation is Q3's deliverable
   (`specs/gnn-bridge-q3-continuous-denotation/`, module
   `gnn_denotation_continuous.lean`, namespace `FEP.GnnContinuous`, landed
   concurrently by the Q3 worker). Its own header records that the carrier
   consumes only the prior gauge (`prior_mean`/`prior_cov`): the
   `F`/`H`/`Q`/`R` payload values are recorded but not consumed, and
   identifying one-step decimal dynamics with the carrier's
   `exp(-t·precision)` law is the P4 no-go (transcendental entries). The jax
   continuous render fragment is therefore **not stated** in this slice:
   there is no carrier-side field for an emitted `F`/`H`/`Q`/`R` table to
   coincide with, and the one-step dynamics identification is no-go on the
   Q3 side. The OU semigroup laws of
   `src/fep_lean/formal/linear_gaussian_semigroup.lean` remain the intended
   kernel machinery for a future continuous execution statement.

## Target inventory and disposition

Render targets (step 11), enumerated from
`GeneralizedNotationNotation/src/render/render.py` (`RENDER_CLI_TARGETS`)
and cross-checked against the canonical `FRAMEWORK_REGISTRY` of
`GeneralizedNotationNotation/src/render/framework_registry.py`
(`RENDER_CLI_TARGETS` is the canonical nine-target render surface;
`FRAMEWORK_REGISTRY` of the same file holds nine framework entries —
the CLI's six base frameworks plus `pytorch`/`numpyro`/`stan`, which the
CLI does not expose — and the CLI's `rxinfer_toml`, `discopy_combined`,
and `jax_pomdp` are target aliases of the `rxinfer`, `discopy`, and `jax`
renderer families):

| # | Target | Disposition | Lean statement | Proof status |
| --- | --- | --- | --- | --- |
| 1 | `pymdp` | statable (matrix fragment) | `Statement5Pymdp` | proved (`statement5DiscreteMatrices_holds`) |
| 2 | `rxinfer` | **no-go** — the rendered artifact is a Julia `@model` factor graph whose meaning is message passing; fep_lean carries no message-passing semantics to state preservation against | — | — |
| 3 | `rxinfer_toml` | **no-go** — a TOML configuration artifact for the RxInfer path; no operational semantics exists to preserve | — | — |
| 4 | `activeinference_jl` | statable (matrix fragment) | `Statement5ActiveInferenceJl` | proved (`statement5DiscreteMatrices_holds`) |
| 5 | `discopy` | **no-go** — the rendered artifact is a string diagram whose semantics is functorial (DisCoPy-side); fep_lean carries no denotation for these diagrams | — | — |
| 6 | `discopy_combined` | **no-go** — same artifact class as `discopy` | — | — |
| 7 | `bnlearn` | **no-go** for program semantics (a generated `pgmpy`/`bnlearn` network script); the CPT-layout fragment is **deferred**, not stated: pgmpy's `TabularCPD` parent-instantiation enumeration order is a convention the GNN side has not frozen, and freezing it unilaterally here would violate the contract's convention-freezing rule | — | — |
| 8 | `jax` | statable (discrete matrix fragment); continuous fragment **not stated** — the Q3 carrier consumes only the prior gauge, so no `F`/`H`/`Q`/`R` counterpart field exists (convention 4) | `Statement5Jax` | discrete fragment proved; continuous fragment not statable today |
| 9 | `jax_pomdp` | statable (matrix fragment) | `Statement5JaxPomdp` | proved (`statement5DiscreteMatrices_holds`) |

Execution targets (step 12), enumerated from
`GeneralizedNotationNotation/src/execute/README.md`, the executor dispatch in
`GeneralizedNotationNotation/src/execute/executor.py` (in-process handlers
`_execute_pymdp_script`, `_execute_rxinfer_config`, `_execute_discopy_diagram`,
`_execute_jax_script`, plus `_execute_framework_spec` for the configured
frameworks), and the per-target runners under
`GeneralizedNotationNotation/src/execute/`. Per the Direction 2
table, the Lean target for this row is the *family denotations* (Q2/Q3), not
per-target programs; Q4 contributes the execution semantics every discrete
rollout must realize (`policyRollout`, proved against `kernelPower`):

| # | Target | Disposition |
| --- | --- | --- |
| 1 | `pymdp` | discrete rollout semantics applies (`policyRollout`); program semantics no-go (Python runtime) |
| 2 | `rxinfer` | **no-go** — variational message passing has no formal counterpart in fep_lean |
| 3 | `activeinference_jl` | discrete rollout semantics applies (`policyRollout`); program semantics no-go (Julia runtime) |
| 4 | `jax` | discrete rollout semantics applies; continuous fragment not statable today (convention 4) |
| 5 | `discopy` | **no-go** — diagram execution has no formal counterpart |
| 6 | `pytorch` | discrete rollout semantics applies conditionally (same fragment shape as pymdp); program semantics no-go (torch runtime) |
| 7 | `numpyro` | **no-go** — NUTS/SVI sampling semantics has no formal counterpart in fep_lean |
| 8 | `stan` | **no-go** — HMC sampling semantics has no formal counterpart in fep_lean |

Free-text sections (`ModelAnnotation`, `Footer`, `Signature`) carry no
semantics and are not rendered targets; they stay outside the formal object
language, as fixed in the Direction 2 doc.

## Statement module

`src/fep_lean/formal/gnn_render_statements.lean`, namespace
`FEP.GnnRenderStatements`, importing `FepSketches.gnn_document`,
`FepSketches.gnn_denotation`, `FepSketches.active_inference`,
`FepSketches.finite_probability`, and `FepSketches.finite_markov_dynamics`.
Every statement is a `Prop`-valued definition or a theorem signature that
compiles proof-free; proofs are supplied only where mechanical (reduction to
`denoteDiscrete`'s field construction and the `kernelPower` /
`FiniteKernel.predictive` laws). No `sorry`, no new axioms.

Proof-schedule table (statements not proved in this slice):

| Statement | Why deferred | Reopen condition |
| --- | --- | --- |
| Full program-denotation equality per statable target (statement 5, whole artifact) | requires a formal semantics of the target-language program surface (pymdp/jax/Julia script ASTs + execution), which does not exist in fep_lean | future slice; prerequisite is a formalized program-surface fragment per target, to be opened on the fep_lean side |
| jax continuous matrix fragment | the Q3 denotation consumes only the prior gauge (`prior_mean`/`prior_cov`); emitted `F`/`H`/`Q`/`R` tables have no carrier counterpart, and one-step dynamics identification is the P4 no-go | reopens only if a continuous carrier with consumed dynamics fields lands (convention 4) |
| bnlearn CPT-layout fragment | requires freezing pgmpy's parent-instantiation enumeration — a GNN-side convention question | statement opens after the GNN side freezes the enumeration convention |
| Observation-update (filtering) fragment | alignment statement 4 territory | Q5+ per the Direction 2 phasing |

## Acceptance

- [x] Bounded spec slice opened before any Lean code landed.
- [x] Formal module `src/fep_lean/formal/gnn_render_statements.lean`
  (namespace `FEP.GnnRenderStatements`) states alignment statement 5 for
  every statable render target and documents no-gos for the rest; registered
  in `src/fep_lean/formal/manifest.py` as a FOUNDATION row immediately after
  the Q3 worker's `gnn_denotation_continuous` row (coordination contract:
  Q3 is first mover on the manifest; Q4 appends after it).
- [x] The execution-semantics statements are proved against the kernel
  machinery (`kernelPower`, `kernelPower_add`, `FiniteKernel.predictive_comp`)
  with no `sorry` and no new axioms, including the exemplar corollary on the
  P1 symmetric Boolean model.
- [x] Matrix-fragment statements are proved (they reduce mechanically to
  `denoteDiscrete` and `FiniteKernel.mass`).
- [x] `cd lean && lake build FepSketches` — zero errors, zero warnings.
- [x] Axiom probe over the slice's statements shows no new axioms.
- [x] `uv run python scripts/_maint_build_formal_modules.py --check`,
  `uv run python scripts/_maint_build_fep_all_lean.py --check`,
  `uv run python scripts/build_formalism_coverage.py --check`, and
  `uv run python scripts/_maint_build_lean_landscape.py --check` green after
  registration.
- [x] Gate parity: `uv run python docs/check_links.py --strict --include-root`
  and `uv run python docs/md_hygiene.py --strict`.
- [x] `uv run pytest tests/test_formal_composition.py
  tests/test_native_evidence.py -q` green.

## Mathlib dependency

The statement module imports the finite carriers and kernel machinery
(`FepSketches.finite_probability`, `FepSketches.finite_markov_dynamics`) and,
transitively, `Mathlib` (ℝ, `Fintype`, `Finset` sums). No new Mathlib import
surface beyond what Q2's module already requires; no `Init`-only attempt is
made because the carrier theorems used are Mathlib-based.

## No-go and risk register

| Trigger | Disposition in this slice |
| --- | --- |
| A render target with no statable semantics | Documented no-go rows (rxinfer, rxinfer_toml, discopy, discopy_combined, bnlearn) — no Lean statement is minted for them |
| Pressure to state a "semantics" as an unconstrained abstract parameter | Rejected by convention 2: statements are conditional on the frozen layout contract, not quantified over arbitrary interpretations |
| Continuous-family render fragment without a consumed dynamics carrier | Not stated (convention 4): the Q3 carrier consumes only the prior gauge; recorded in the proof-schedule table with its reopen condition |
| pgmpy CPT enumeration order | Deferred with the reason recorded; convention question filed to the mirror folder |
| Manifest coordination (Q3 first mover) | Q4 waited for the `gnn_denotation_continuous` manifest row before appending its own FOUNDATION row and running the projection scripts; module drafting proceeded independently |
| Evidence firewall (bridge contract section 7) | Compilation establishes only that the stated fragments hold as Lean Props; it establishes nothing about GNN pipeline behavior, and no execution statistic is promoted to a proved property |

## Boundaries

- The formal module is additive: one new foundation resource, no edits to
  the accepted Q1 AST module or the Q2 denotation module, no edits to any
  existing Lean carrier, no catalogue topics, no relation or atlas claims,
  no `fep-NNN` identifier.
- `composed.lean` stays the import-only aggregate over composition leaves; a
  foundation module is not imported there, and `fep_all.lean` is
  catalogue-body-driven and does not list this module.
- The manifest edit is limited to appending one FOUNDATION row after the Q3
  worker's row; the projection scripts are run only after that row exists.
- Cross-repo references are inline code paths, never markdown links (bridge
  contract decision).
- No edits outside this slice's spec directory, the statement module, the
  manifest row, and script-owned projections.

## Mirror-folder finding for the GNN side

The pgmpy `TabularCPD` parent-instantiation enumeration order (the column
order of CPT tables in bnlearn-emitted scripts) is a convention the bridge
cannot state preservation against until the GNN side freezes it. The GNN-side
mirror folder (`GeneralizedNotationNotation/doc/other/fep_lean/`) is the
right place to record that question. Until the convention is frozen, bnlearn
keeps its no-go row and no statement is minted for its CPT-layout fragment.
