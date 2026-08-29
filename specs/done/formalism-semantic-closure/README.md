# Formalism semantic closure

Status: closed in the working tree; not committed or published
Closed: 2026-08-20

## Purpose

This feature turns a stable catalogue of Lean files into a connected and
claim-calibrated formal research program. It strengthens exact mathematical
models where the pinned library supports them, narrows titles and prose where
the general scientific theory is not formalized, and makes every retained
boundary visible in the same graph that displays proved composition.

“Closure” here means closure of the local evidence contract, not proof of the
Free Energy Principle as a universal physical theory. A declaration must have
an exact statement, reviewed assumptions, a non-vacuity account, a native
compiler result, and an axiom record before it can support a promoted claim.
Provider-backed or empirical evidence remains a different plane.

## Why this shape

- **Stable scholarly anchors beat roster inflation.** The `fep-001` through
  `fep-050` identifiers remain fixed. Depth is expressed through stronger
  declarations and theorem-bearing relations, not new shallow rows.
- **Claim strength follows the carrier actually formalized.** Finite kernels,
  Bernoulli families, exact quadratics, and finite-state currents are described
  as such. They are not relabeled as general diffusion, statistical-manifold,
  or microscopic thermodynamic theories.
- **Composition is proof-bearing.** A `formal` relation requires a qualified
  theorem that uses declarations from both topic endpoints. Conceptual
  adjacency and missing capability are different edge kinds.
- **Capabilities retain history.** A capability can remain partial even when
  useful component theorems exist. This prevents a posterior algebra result
  from silently becoming an estimator-risk or empirical-consistency theorem.
- **Mathlib is the preferred owner.** Native posterior kernels, KL divergence,
  probability measures, Gaussian laws, calculus, Markov kernels, and fixed
  points are reused at the repository pin. Local definitions fill only the
  bounded models needed to connect them.
- **One join drives prose and pictures.** Coverage, atlas, and manuscript
  variables consume the same validated semantic graph rather than copying
  counts or creating presentation-only dependencies.

## Invariants

1. The family-owned bodies under `src/fep_lean/catalogue/bodies/` own every
   topic Lean body;
   `config/theorem_maturity.yaml` owns its reviewed claim; and
   `config/formalism_relations.yaml` owns capabilities and scientific edges.
   Generated YAML, aggregate Lean, coverage, atlas, and manuscript builds are
   projections only.
2. `fep_lean.formal.manifest` is the single roster of maintained formal
   modules. Projection, declaration inventory, composed-theorem counts,
   digests, and audit imports consume it rather than using independent globs.
3. Every topic primary theorem resolves in its canonical body. Every formal
   edge and resolved capability names qualified evidence declarations in the
   formal closure.
4. Formalized topics cannot retain a blocker; scope and assumption gaps require
   one; calibrated proxy dispositions may retain a blocker for a stronger
   missing facet.
5. Native acceptance requires the exact roster, warning-free compilation, zero
   `sorry`, and a live-source digest match. The declaration receipt separately
   requires complete name resolution, one parsed axiom result per declaration,
   exact resolved-count parity, a zero return code, zero warnings, and zero
   `sorryAx`. Lean's hard-wrapped output is parsed and normalized rather than
   assumed to be line-oriented.
6. The atlas is offline, deterministic, keyboard-operable, complete in its
   fallback tables, and explicit about horizontal panning. Visible edge strokes
   retain scientific line semantics while wider transparent paths provide
   usable pointer targets.
7. Manuscript prose cites exact topic or composed declarations for promoted
   claims and names the finite, conditional, or external boundary of every
   materially stronger interpretation.
8. `fep-036` is formalized only at its finite Bernoulli scope: a binomial PMF,
   outcome-indexed Laplace prior, exact shrinkage identity, consistency transfer
   from a convergent empirical-frequency sequence, and posterior closure. It
   does not promote that conditional convergence theorem into a probabilistic
   LLN, finite-sample risk bound, or marginal-likelihood optimum.

## Code and test pointers

- Topic models and semantics: `fep_lean.catalogue.bodies`,
  `fep_lean.catalogue.semantics`, and `config/theorem_maturity.yaml`.
- Formal ownership and composition: `fep_lean.formal.manifest`,
  `fep_lean.formal.declarations`, `fep_lean.formal.projection`, and
  `src/fep_lean/formal/composed.lean`.
- Capability graph and coverage: `fep_lean.catalogue.relations`,
  `fep_lean.catalogue.coverage`, and `config/formalism_relations.yaml`.
- Native and axiom evidence: `fep_lean.verification.lean_verifier`,
  `fep_lean.verification.formalism_audit`, and
  `fep_lean.output.evidence`.
- Publication and visualization: `fep_lean.output.manuscript`,
  `fep_lean.output.rendering`, `fep_lean.output.formalism_atlas`,
  `manuscript/04f_semantic_closure_and_validation.md`, and
  `docs/formalism-atlas.html`.
- Behavioral gates: `tests/test_formalism_depth_upgrades.py`,
  `tests/test_formal_composition.py`, `tests/test_formalism_relations.py`,
  `tests/test_formalism_audit.py`, `tests/test_formalism_coverage.py`,
  `tests/test_formalism_atlas.py`, and
  `tests/test_manuscript_rendering.py`.

## Dead ends and consequential divergences

- A large new shared probability foundation was not introduced. Direct use of
  pinned Mathlib plus small topic-local carriers produced clearer assumption
  boundaries; the composed module owns only genuine cross-topic witnesses.
- Aggregate compilation initially hid missing per-topic imports. The final
  contract therefore includes an exact native roster sweep in addition to the
  aggregate build.
- The declaration probe initially imported a stale composed `.olean`. The
  durable rule is to build the manifested composed target before an import-based
  axiom audit; source compilation alone does not refresh the import artifact.
- General Gibbs minimization, continuous Langevin convergence, multidimensional
  information geometry, cross-coupled Onsager response, and microscopic
  erasure protocols were not inferred from narrower exact theorems. Titles,
  assumptions, and limitations carry those boundaries instead.
- Empirical-prior estimation initially remained partial because a bounded
  smoothed count and posterior update alone did not define a sampling law or
  estimator limit. The final closure adds the finite binomial PMF, its
  outcome-indexed estimator, exact shrinkage, and consistency transfer while
  retaining risk, probabilistic-LLN, and marginal-likelihood limits in prose.
- The first responsive atlas put its inspector after a tall scroll plane and
  made edge paths too thin to select. Independent screenshot critique led to a
  pre-graph evidence drawer, bounded pan viewport, external metric summary,
  larger render scale, pan guidance, and wide invisible interaction strokes.

## Visual provenance

No external artwork or screenshot served as a style target. The visual standard
was internal and evidence-led: a dark research-instrument surface, readable
theorem cards, line styles that remain meaningful without color, complete
canonical totals outside the scroll plane, and immediate access to exact
evidence.

- [Desktop acceptance capture](assets/formalism-atlas-1440x900.png) records the
  exact 1440x900 review viewport and drove the full-width inspector, metric
  summary, larger graph scale, and pan cue.
- [Mobile acceptance capture](assets/formalism-atlas-390x844.png) records the
  exact 390x844 review viewport and drove the bounded scroll plane, visible
  evidence feedback, two-column metric summary, and touch-target correction.
- `docs/formalism-atlas.svg` and `docs/formalism-atlas.html` remain the
  deterministic publication outputs; the captures are review provenance, not
  generation owners.

An unprimed reviewer inspected both exact captures after the fixes and found no
remaining high-confidence visual defect. The expected mobile tradeoff is that
filters, inspector, metrics, and pan guidance precede the map by one short page
scroll.

## External boundary

Local closure does not authorize credentials or provider calls. A complete
Hermes/OpenGauss run and its independently validated full-report receipt remain
external acceptance work until the user supplies permitted credentials through
the existing mechanism.
