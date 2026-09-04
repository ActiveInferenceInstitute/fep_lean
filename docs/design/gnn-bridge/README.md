# GNN bridge program

Status: **implementation slices accepted — Direction 1 P1+P2
([P1 report](../../../specs/gnn-bridge-p1-finite-spike/REPORT.md)) and P3
([P3 report](../../../specs/gnn-bridge-p3-certificates/REPORT.md)); P4
closed at its documented extraction boundary
([P4 report](../../../specs/gnn-bridge-p4-continuous-spike/REPORT.md));
Direction 2 Q1 accepted
([Q1 report](../../../specs/gnn-bridge-q1-syntax-ast/REPORT.md)); Q2
([Q2 report](../../../specs/gnn-bridge-q2-discrete-denotation/REPORT.md)),
Q3 ([Q3 report](../../../specs/gnn-bridge-q3-continuous-denotation/REPORT.md)),
and Q4
([Q4 report](../../../specs/gnn-bridge-q4-renderer-execution-statements/REPORT.md))
accepted**. This document is the design goal;
implementation status lives in the spec slices per the
[design lifecycle](../README.md). The active catalogue program lives in
[FEP research horizons](../fep-research-program/README.md); this program is an
independent articulation with the sibling repository
`GeneralizedNotationNotation` (GNN). No topics, formalism relations, atlas
edges, or `fep-NNN` identifiers are claimed or reserved; the registered
implementation artifacts are the Q1–Q4 foundation modules owned by their
spec slices.

## Why this program exists

GNN is a text-based notation for Active Inference generative models with a
25-step processing pipeline that validates, renders, and executes model
documents. fep_lean states and proves invariants about the same objects in
Lean 4. The released manuscript already names the gap:

> Executable Active-Inference tools and notations such as pymdp or GNN
> occupy a different layer. They specify and run model instances; Lean
> states and proves invariants. A useful bridge would translate a typed
> model representation into a common Lean probability/kernel structure,
> generate proof obligations for normalization and conditional independence,
> and retain a provenance link back to executable parameters.

(citation markers removed; `manuscript/05d_comparative_analysis.md:37`.) The
same chapter adds that a numerical implementation can be tested on data while
a theorem is checked for deductive correctness, and that "neither subsumes
the other" (`manuscript/05d_comparative_analysis.md:39`). This program keeps
both layers and makes their agreement checkable instead of asserted.

## Parties and authority

| Party | Role in the bridge |
| --- | --- |
| fep_lean | Lean 4 semantic authority: laws, kernels, blankets, free-energy and decision quantities, and their proofs; the pinned workspace is the compilation authority |
| GNN | Notation and tooling authority: GNN document syntax, the pipeline step registry, render targets, and execution semantics |
| Interchange artifact | GNN document files carrying mandatory provenance back to the Lean source |

## North star

```text
named Lean generative-model definition
  -> deterministic projection (variables, index types, dependencies, parameters)
  -> GNN document with provenance
  -> GNN validate / ontology / render / execute (steps 3, 5, 10, 11, 12)
  -> execution artifacts (render and execution summaries)
  -> certificate: execution-derived quantities vs Lean-witnessed properties
```

and the reverse direction:

```text
GNN syntax and step inventory (doc/gnn/gnn_syntax.md; src/pipeline/step_registry.py)
  -> Lean AST and decidable well-formedness
  -> static and dynamic semantics
  -> denotations reusing fep_lean carriers (FiniteLaw, FiniteKernel, FiniteHMM, LinearGaussianParameters)
  -> FEP instantiation and renderer-preservation statements
```

Every arrow must be deterministic and name its evidence plane. An arrow that
requires judgment calls is a finding to resolve, not a pipeline stage.

## The two directions

- [Direction 1 — render and execute Lean-expressed generative models](direction-1-lean-to-gnn.md):
  from a Lean expression of a generative model to a GNN document the GNN
  toolchain renders and executes, with certificates back to Lean.
- [Direction 2 — formalize GNN steps and methods](direction-2-gnn-to-lean.md):
  from the frozen GNN syntax surface and step registry to Lean ASTs, decidable
  well-formedness, dynamic semantics, and alignment theorems on fep_lean
  carriers.
- [Bridge contract](bridge-contract.md): the shared, mirrored agreement both
  sides edit and honor.

## Model-kind alignment

The bridge aligns the two supported model kinds on each side:

| GNN model kind | fep_lean counterpart |
| --- | --- |
| Discrete POMDP family: `A` likelihood, `B` transition ordered `(next_state, previous_state, action)`, `C` preferences, `D` initial prior, optional `E` habit, `F[1]` variational-free-energy readout | finite carrier family: `lean/FepSketches/active_inference.lean` (`GenerativeModel`), `lean/FepSketches/finite_probability.lean` (`FiniteLaw`, `FiniteKernel`), `lean/FepSketches/temporal_inference.lean` (`FiniteHMM`) |
| Continuous linear-Gaussian family: `F/H/Q/R` with `prior_mean`/`prior_cov`, `x_t = F x_{t-1} + u_{t-1} + N(0,Q)`, `y_t = H x_t + N(0,R)` | smooth/stochastic carrier family: `lean/FepSketches/linear_gaussian_semigroup.lean`, `lean/FepSketches/scalar_gaussian_semigroup.lean`, `lean/FepSketches/continuous_time_markov.lean` |

Blanket structure and the ontology bindings `s=HiddenState`, `o=Observation`,
`π=PolicyVector`, `u=Action` correspond to
`lean/FepSketches/markov_blanket.lean` and `lean/FepSketches/native_blanket.lean`.

## Decisions fixed by this design

1. **One interchange artifact.** GNN document files only. Any typed
   intermediate projection stays private to the emitter.
2. **Provenance is mandatory.** Every emitted document records source
   repository, commit digest, Lean module and definition, and generator
   identity in a provenance section.
3. **Deterministic projection or nothing.** No heuristic or model-based
   extraction sits inside the emitter; judgment belongs to the mapping
   review, not the pipeline.
4. **Evidence planes stay distinct.** Lean native compilation, semantic
   review, numerical witnesses, and GNN pipeline execution remain separate
   evidence classes. A GNN run never promotes a Lean claim, and a Lean claim
   never substitutes for an executed artifact.
5. **Two model kinds only.** Discrete/categorical and continuous
   linear-Gaussian. Anything else is out of scope until the contract is
   reopened.
6. **Misfit is reported, not repaired.** Where a projected model exceeds a
   backend, the GNN `unsupported` render status applies; the bridge never
   distorts a model to force a fit.
7. **No catalogue or relation claims.** This program adds no topics, no
   formalism relations, no atlas edges, and reserves no `fep-NNN`
   identifiers. Future rows arrive only through the existing novelty and
   semantic-review gates.
8. **Inline-code cross-references only.** Cross-repo paths are written as
   code, never as markdown links, because each repository validates links
   independently and relative links across repositories would break on
   either side's hosting.
9. **Mirrored contract.** The canonical contract lives in this directory;
   the mirror lives at
   `GeneralizedNotationNotation/doc/other/fep_lean/bridge-contract.md`.
   Contract edits land in both checkouts in the same working session.
10. **Spec-first lifecycle.** A bounded spec under `specs/` precedes any
    code: no projection module, emitter, or Lean AST lands without an opened
    slice, and the slice's acceptance record owns implementation status.

## Current stage and checklist

- [x] P0 — inventory and bridge contract (this directory).
- [x] P1 — single-model spike: the finite
      `symmetricBoolModel trueBiasedPolicyPrior` instance projected to
      `FepLeanSymmetricBool.md`; strict validation exit 0; 9/9 render
      targets; step 12 executed 9 scripts — 7 rc=0, rxinfer rc=1 (finding
      F1), bnlearn skipped (rendered, not executed)
      ([report](../../../specs/gnn-bridge-p1-finite-spike/REPORT.md)).
- [x] P2 — deterministic projection with a `--check` freshness gate;
      byte-identical regeneration; ruff+mypy clean
      ([report](../../../specs/gnn-bridge-p1-finite-spike/REPORT.md)).
- [x] P3 — certificate protocol run on the P1 instance: C1
      (policy posterior, |Δtrue| = 5.96e-08) and C2 (VFE vs `log 2`,
- [x] P4 — closed at the extraction boundary: `F = e^{-1}`,
      `Q = 1 − e^{-2}` are transcendental and the contract's fixed
      rounding policy admits terminating decimals only; documented no-go
      with a recorded unblock path (owner-level rounding extension)
      ([report](../../../specs/gnn-bridge-p4-continuous-spike/REPORT.md)).
      **Superseded by P4b** — contract v0.2 (float64 rounding extension
      for non-terminating exact reals) reopened the phase; the scalar-OU
      instance emitted, strict-validated, rendered on all five
      continuous-capable backends, and executed on four (pytorch
      skipped: torch absent), with the four discrete-only backends
      honestly reporting `unsupported`
      ([P4b report](../../../specs/gnn-bridge-p4b-continuous-emission/REPORT.md)).
- [x] Q1 — GNN document AST and decidable well-formedness:
      `src/fep_lean/formal/gnn_document.lean` (`FEP.GnnDocument`),
      warning-free, no `sorry`, Init-only, manifest-registered; both
      regeneration gates green
      ([report](../../../specs/gnn-bridge-q1-syntax-ast/REPORT.md)).
- [x] Q2 — discrete-family denotation over `FiniteLaw`/`FiniteKernel`/
      `FiniteHMM`: module `src/fep_lean/formal/gnn_denotation.lean`
      (`FEP.GnnDenotation`), exemplar isomorphism-class statement proved
      warning-free, no `sorry`, no new axioms
      ([report](../../../specs/gnn-bridge-q2-discrete-denotation/REPORT.md)).
- [x] Q3 — continuous-family denotation over `LinearGaussianParameters`:
      module `src/fep_lean/formal/gnn_denotation_continuous.lean`
      (`FEP.GnnContinuous`), prior-gauge convention frozen, exemplar
      statement proved warning-free
      ([report](../../../specs/gnn-bridge-q3-continuous-denotation/REPORT.md)).
- [x] Q4 — renderer and execution statements: module
      `src/fep_lean/formal/gnn_render_statements.lean`
      (`FEP.GnnRenderStatements`), matrix-fragment statements proved per
      statable target, execution semantics proved against `kernelPower`,
      documented no-go rows for the rest
      ([report](../../../specs/gnn-bridge-q4-renderer-execution-statements/REPORT.md)).

Opening any unchecked row requires a bounded spec slice per the
[design lifecycle](../README.md).

## Reading order

1. This README.
2. [Bridge contract](bridge-contract.md) — the shared rules both sides honor.
3. [Direction 1](direction-1-lean-to-gnn.md) and
   [Direction 2](direction-2-gnn-to-lean.md).
4. Background: [FEP background](../../fep-background.md) and
   [formal-kernel methods](../../formal-kernel-methods.md); on the GNN side,
   the mirror folder `GeneralizedNotationNotation/doc/other/fep_lean/`.

## Operating the bridge

The five commands of record (run from the fep_lean repo root; both repos
must be on their recorded commits — the emitter and status command
regenerate provenance from `git rev-parse HEAD`):

| Command | Purpose |
| --- | --- |
| `uv run python specs/gnn-bridge-p1-finite-spike/projection.py` | Emit the P1 document (`FepLeanSymmetricBool.md`) at the current heads |
| `uv run python specs/gnn-bridge-p1-finite-spike/projection.py --check` | Freshness gate: regenerated bytes vs on-disk artifact (exit 0 = fresh) |
| `uv run python specs/gnn-bridge-p3-certificates/certify.py` | Certificate protocol: C1/C2 execution-derived quantities vs Lean witnesses |
| `uv run python specs/gnn-bridge-w1-bridge-operations/bridge_status.py` | One-shot bridge health: the four W1 checks in one command |
| `uv run python specs/gnn-bridge-w1-bridge-operations/bridge_status.py --refresh-digests` | Custody-drift healing: rewrite the P1 document at current heads (digest lines only; never content) |

When to use `--refresh-digests`: only after
`bridge_status.py` reports `STALE-CUSTODY (digest-only)` — the on-disk
document differs from regeneration solely on `source_commit` /
`pipeline_commit` lines. That is expected after either repo's HEAD moves
and is healed by re-running the emitter at the new heads. A
`CONTENT-DRIFT` classification must never be healed by
`--refresh-digests`; review the divergence and re-emit deliberately
through the P1 slice.
