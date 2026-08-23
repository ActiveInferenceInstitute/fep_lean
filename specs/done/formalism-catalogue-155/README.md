# Formalism catalogue 155

## Purpose

This expansion closes five deliberately finite mathematical seams in the
catalogue while keeping proof, numerical, browser, publication, and optional
provider evidence separate. The stable interface is 155 ordered topics in 20
families across the five established areas. That number records a reviewed
scope; it is not a claim of scientific completeness.

The canonical roster and its mathematical meaning live in
[`config/catalogue_metadata.yaml`](../../../config/catalogue_metadata.yaml),
[`config/theorem_maturity.yaml`](../../../config/theorem_maturity.yaml), and the
family-owned [`BODIES`](../../../src/fep_lean/catalogue/bodies/) registry. The
formal module graph is owned by
[`formal/manifest.py`](../../../src/fep_lean/formal/manifest.py). This record
explains why those owners have their present boundaries rather than duplicating
their declarations.

## Why the catalogue stops at 155

Planning passes proposed cuts of 145, 155, and 180 topics. All identified the
same five manuscript limitations: finite-sample calibration, observation-
contingent policy trees, transfer from finite blanket laws to Mathlib's native
conditional independence, differentiable exponential-family geometry, and an
exact continuous-time thermodynamic example.

The 155 cut retains the established seven-topic family granularity. It leaves
room for assumptions, boundary cases, and non-vacuity witnesses instead of
padding each area to a round number. The larger proposal correctly exposed the
need for carrier-transfer theorems, but its attempt to promote every checked
pairing into an implication was not mathematically justified. The smaller
proposal supplied proof-ready theorem shapes and became the basis of the five
families.

The five additions remain intentionally narrow:

- finite Laplace smoothing, Brier excess risk, and event transfer;
- finite-horizon policy trees with nonempty finite action spaces;
- finite-law embeddings into genuine Mathlib `CondIndepFun` statements;
- a scalar finite exponential family with explicit support and derivative
  hypotheses; and
- an exact positive-rate, two-state continuous-time Markov model.

## Invariants

- The schema-2 catalogue metadata is the sole ordered roster owner. Its
  `first_id`/`last_id` seal derives the expected contiguous ID interval, and
  registry/body projections must match that interval exactly; no consumer owns
  a second authoritative topic list.
- Every family owns one ordered `BODIES` map. The registry is the only merger;
  there is no `TOPIC_BODIES` compatibility surface.
- Reusable mathematics belongs to manifested foundation modules. Topic bodies
  are theorem-facing projections, and foundations do not import topic
  namespaces.
- Cross-topic results live in manifested composition leaves. The aggregate
  composition module imports those leaves and owns no duplicate theorem body.
- Relation kind is authored and checked from theorem shape and endpoint use; it
  is never inferred from names or imports.
- Maturity, novelty, relations, capabilities, theorem references, and numerical
  mirrors resolve against the canonical declaration closure and fail closed.
- Both renderers consume one immutable presentation join. They own no second
  topic, family, relation, capability, or witness roster.
- Catalogue, native Lean, declaration/axiom, numerical, browser, Python,
  provider, and publication evidence remain distinct classes. Passing one does
  not promote another.
- Generated YAML, Lean workspace projections, coverage, maturity, atlas,
  dashboard, manuscript variables, rendered publication, and release archive
  are projections. They are regenerated and drift-checked, never hand-edited.
- The supported compiler policy is the newest matching stable Lean/Mathlib
  pair. RCs, nightlies, floating branches, and mismatched stable tags fail the
  pin audit. The accepted cut uses Lean 4.33.1 and Mathlib 4.33.1.

These boundaries are pinned by the catalogue, semantic, composition, formal,
visual, browser, manuscript, and release tests under [`tests/`](../../../tests/).

## Evidence boundaries

Current evidence is validated at its own parser or browser boundary rather
than inferred from filenames. The durable entry points are:

- native Lean receipt: [`output/native-verification.json`](../../../output/native-verification.json);
- declaration/axiom receipt: [`output/formalism-audit.json`](../../../output/formalism-audit.json);
- browser receipt and images: [`assets/`](assets/);
- Python JUnit, coverage, and acceptance receipts: [`output/`](../../../output/);
- rendered manuscript and renderer provenance: [`output/manuscript/`](../../../output/manuscript/);
- deterministic release owner:
  [`output/release_bundle.py`](../../../src/fep_lean/output/release_bundle.py).

External Hermes/OpenGauss execution is optional and requires a separate
credential and spend decision. Historical provider reports do not become
current merely because the local formal source advances.

## Visual provenance

The retained 120-topic atlas and dashboard captures in
[`formalism-catalogue-120/assets`](../formalism-catalogue-120/assets/) were the
comparison standard for information density, topic/family legibility,
relation visibility, witness discoverability, and mobile reading order. They
were not pixel baselines.

The six accepted 155-topic captures and their schema-4 interaction receipt are
in [`assets/`](assets/). [The visual review](visual-review.md) records their
hashes, Chrome identity, rejection/remediation history, and the final unprimed
verdict. The images are presentation evidence, not Lean proof receipts.

## Divergences and rejected paths

- The planned single `test_formalism_155_spikes.py` did not ship. The retained
  `#print axioms` probes became family-owned fixtures under [`spikes/`](spikes/)
  and are exercised by the risk/policy, native-blanket, and
  geometry/continuous-time suites.
- The native-blanket family did not substitute finite mutual information for
  conditional independence. Its stop/go theorem reaches Mathlib's native
  `CondIndepFun` predicate.
- Continuous time was not generalized to SDE, Langevin, Fokker--Planck, NESS,
  or continuous-path semantics. The exact two-state semigroup is the claimed
  boundary.
- Exponential-family geometry was not promoted to an unrestricted smooth
  manifold or global dual-flatness claim.
- Finite-horizon policy-tree optimality was not described as arbitrary or
  infinite-horizon POMDP optimality.
- Deterministic numerical witnesses and compilation were not described as
  empirical or physical validation of the Free Energy Principle.
- Mobile dashboard plots were not omitted to shorten the page. They remain
  complete in five indexed disclosure groups, with exact tables retained.
- Coincident numerical series were not separated by a fabricated value offset;
  they share one exact rail and use distinct centered marker identities.

These exclusions are scientific scope firewalls. Widening one requires new
theorems and evidence, not a documentation edit.
