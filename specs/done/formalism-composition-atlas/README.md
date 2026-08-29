# Formalism composition, validation, and atlas

Status: closed in the working tree; not committed or published
Closed: 2026-08-19

## Purpose

This feature turns a set of independently compiling topic sketches into an
auditable formal-research surface without pretending that compilation proves
the Free Energy Principle as a physical theory. It preserves the stable
50-topic roster while adding native mathematical depth, theorem-witnessed
cross-topic composition, retained capability state, declaration and axiom
auditing, and a deterministic visual account of what is proved, related, or
still blocked.

The central design choice is separation of evidence planes. Canonical theorem
intent, semantic review, authored scientific relations, native Lean receipts,
and credentialed full execution answer different questions. Combining them
would make a green compiler result look like scientific completeness.

## Why this shape

- **Depth precedes roster growth.** Stable IDs are useful scholarly anchors.
  Adding more shallow rows would increase apparent breadth while weakening the
  meaning of the catalogue.
- **Mathlib owns the mathematics it already provides.** Native conditional
  independence, kernel invariance, binary entropy, strict concavity, and
  contraction APIs avoid local near-duplicate abstractions and inherit the
  pinned library's theorem ecosystem.
- **A relation is formal only when a theorem witnesses it.** Shared imports are
  implementation co-occurrence, not a scientific implication. The typed graph
  therefore requires a qualified declaration on every formal edge and forbids
  witnesses on conceptual and blocker edges.
- **Resolution state remains visible.** The canonical graph retains satisfied
  capability nodes beside open and partial nodes and requires declaration
  evidence on the resolved states.
- **One canonical join drives every view.** Coverage JSON, Markdown, SVG, HTML,
  and manuscript variables rebuild through `build_formalism_coverage`. Drift
  gates compare each generated projection with that owner.
- **Proof evidence is the default interactive layer.** The HTML atlas opens on
  formal edges and retains every conceptual and blocker relation in filters
  and accessible tables. The static SVG deliberately shows the complete graph.

## Invariants

1. This feature preserves the exact `fep-001` through `fep-050` roster; roster
   growth is outside its contract.
2. The family-owned bodies under `src/fep_lean/catalogue/bodies/` own topic
   Lean bodies, while
   `src/fep_lean/formal/composed.lean` owns maintained cross-topic theorems and
   `fep_lean.formal.manifest` owns the formal-module roster. Workspace Lean,
   topic YAML, coverage, and atlas files are generated projections whose
   freshness gates reject divergence from those owners.
3. A formal graph edge names a qualified declaration that resolves in the
   canonical source and compiles at the pinned Lean/Mathlib toolchain.
4. Semantic dispositions and capability states remain explicitly authored in
   their configuration owners; generators never derive them from compilation.
5. `β = 0` is described as zero inverse temperature, equivalently an
   infinite-temperature limit, never as zero physical temperature.
6. Native claim readiness rejects warnings and `sorry`; acceptance invokes the
   verifier with `--fail-on-warnings`. Declaration audit rejects unresolved
   names, stale projections, warnings, and `sorryAx`.
7. The atlas is deterministic, offline, keyboard-operable, safe from injected
   HTML, complete in its fallback tables, and color-independent in its status
   and edge semantics.
8. Missing provider credentials remain an explicit external boundary. Local
   proof acceptance never substitutes for a claim-ready full Hermes/OpenGauss
   report.

## Code and test pointers

- Native topic bodies and metadata join:
  `fep_lean.catalogue.bodies`, `fep_lean.catalogue.generation`, and
  `config/theorem_maturity.yaml`.
- Cross-topic ownership and projection:
  `fep_lean.formal.manifest`, `fep_lean.formal.declarations`,
  `fep_lean.formal.projection`,
  `src/fep_lean/formal/composed.lean`, and
  `scripts/_maint_build_formal_modules.py`.
- Typed relations and coverage:
  `fep_lean.catalogue.relations`, `fep_lean.catalogue.coverage`, and
  `config/formalism_relations.yaml`.
- Declaration/axiom validation:
  `fep_lean.verification.formalism_audit` and
  `scripts/audit_formalisms.py`.
- Visualization:
  `fep_lean.output.formalism_atlas`, `scripts/build_formalism_atlas.py`,
  `docs/formalism-atlas.svg`, and `docs/formalism-atlas.html`.
- Behavioral gates:
  `tests/test_formalism_depth_upgrades.py`,
  `tests/test_formal_composition.py`, `tests/test_formalism_relations.py`,
  `tests/test_formalism_audit.py`, `tests/test_formalism_coverage.py`, and
  `tests/test_formalism_atlas.py`.

## Rejected paths and consequential divergences

- The initial atlas deliberately rendered unresolved capabilities instead of
  hiding them. Later semantic-closure work discharged most of those bounded
  obligations without changing the graph model; this is why capability state
  is retained data rather than a one-time backlog view.
- Continuous diffusion, multidimensional information geometry, cross-coupled
  thermodynamic response, general alpha divergence, and microscopic erasure
  remain outside the finite or one-parameter theorems now displayed. The atlas
  carries exact assumption and limitation text rather than inferring those
  stronger theories from visual proximity.
- A default all-relations interactive view is rejected in favor of a
  formal-edge default. Boundary-anchored F-label routes and explicit source and
  target labels make proof direction visible; filters and tables retain every
  authored relation without a copied count.
- Topic cards carry compact status; capability cards add evidence or
  blocked-topic counts. Exact declaration identifiers belong in the inspector
  and complete tables, where they remain untruncated and copyable.
- The first responsive layout put the evidence inspector after the full-height
  graph and exposed only the thin visible edge stroke to pointer input. The
  accepted design uses a pre-graph evidence drawer, a bounded pan viewport, and
  wide transparent hit strokes while preserving the visible edge notation.

## Visual provenance

The in-tree visual standard is a restrained research-instrument map: dark navy
working surface, high-contrast theorem cards, explicit provenance labels, and
line styles that remain meaningful without color. The generated render is
`docs/formalism-atlas.svg`; `docs/formalism-atlas.html` is its interactive
counterpart. `tests/test_formalism_atlas.py` pins deterministic geometry,
complete node/edge conservation, offline assets, keyboard interaction, and
accessible fallback tables. The exact desktop and mobile review captures, and
the decisions they drove, are retained by the later
[`formalism-semantic-closure`](../formalism-semantic-closure/README.md) record.
