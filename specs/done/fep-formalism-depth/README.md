# Package and evidence foundation

Status: closed in the working tree; not committed or published
Closed: 2026-08-20

## Purpose

This feature gives the research artifact one collision-resistant Python
package and one fail-closed route from maintained mathematical sources to
generated catalogues, evidence receipts, and manuscript output. Its purpose is
not to make every repository file installable. It makes the public runtime
surface usable outside the checkout while keeping authoring, proof, and
publication evidence distinguishable.

“Usable outside the checkout” applies to the installed Python namespace,
packaged catalogue/composed resources, and CLI discovery. Substantive operator
commands remain explicitly checkout-bound because duplicating the Lean,
configuration, and manuscript owners into a wheel would create a second
authoring environment.

The design responds to two failure modes that are especially dangerous in a
formal research package: generic top-level imports can silently resolve to the
wrong distribution, and a successful offline catalogue run can be mistaken for
proof or provider-backed execution. The package and evidence seams prevent both
classes of false confidence.

## Reasons for the architecture

- **One public namespace.** `fep_lean` is the sole installed root. Retaining
  loose roots such as `catalogue`, `pipeline`, or `output` would preserve import
  collisions and make an isolated-wheel smoke meaningless.
- **Generated data, maintained owners.** The wheel carries the generated topic
  catalogue and composed Lean source it needs at runtime. Static metadata,
  semantic review, and authored proof bodies remain separately reviewable
  owners in the canonical source checkout.
- **Evidence planes do not coerce into one another.** Catalogue completion,
  native Lean compilation, semantic disposition, and a credentialed full run
  answer different questions. Each has a separate predicate and receipt path.
- **Rendering never mutates scholarship.** Authored manuscript files are inputs.
  Placeholder resolution and declared assets are validated before an isolated
  build tree is written.
- **Warnings are evidence.** Project-owned Lean warnings, `sorry`, stale source
  digests, and unresolved variables fail the relevant gate instead of being
  normalized away in reporting prose. Warning lists survive the topic, pipeline,
  summary, run-manifest, verification-manifest, and receipt-validator seams.

## Invariants

1. Distribution metadata exports exactly the `fep_lean` root and the
   `fep-lean = fep_lean.cli:main` console entry point. No compatibility shims
   restore the removed generic roots. CLI help works from installed bytes;
   substantive commands reject missing checkout owners and accept an explicit
   `--project-root`.
2. `fep_lean.catalogue.generation` is the catalogue join. Its checkout YAML and
   `fep_lean.data` package resource are byte-identical projections.
3. `config/catalogue_metadata.yaml`, `config/theorem_maturity.yaml`, and
   `fep_lean.catalogue.sketches` own different facts. A generator may join them
   but may not infer one from another.
4. `fep_lean.output.evidence` owns native/full evidence selection. A catalogue
   result with zero verified topics can never populate a native or full-run
   success claim.
5. Native receipts are bound to the selected roster and live canonical source.
   Full reports remain separately subject to independent artifact-hash and
   manifest reconciliation, including per-topic warnings and zero-warning
   aggregate parity. The repository receipt adapter always supplies a live
   source root.
6. `fep_lean.output.rendering` writes only a destination tree after all
   placeholders and manuscript assets validate. Authored Markdown remains
   byte-stable.
7. Missing provider credentials are an external-state boundary. They do not
   authorize credential discovery, weaken local gates, or turn catalogue mode
   into simulated full execution.

## Code and test pointers

- Package surface: `src/fep_lean/__init__.py`, `src/fep_lean/cli.py`, and
  `pyproject.toml`.
- Installed resources: `src/fep_lean/data/topics.yaml` and
  `src/fep_lean/formal/composed.lean`.
- Catalogue ownership: `fep_lean.catalogue.schema`,
  `fep_lean.catalogue.semantics`, `fep_lean.catalogue.sketches`, and
  `fep_lean.catalogue.generation`.
- Evidence and rendering: `fep_lean.output.evidence`,
  `fep_lean.output.manuscript`, and `fep_lean.output.rendering`.
- Distribution and failure contracts: `tests/test_distribution.py`,
  `tests/test_native_evidence.py`, `tests/test_manuscript_rendering.py`,
  `tests/test_catalogue_sketches_ssot.py`, and `tests/test_pipeline.py`.

## Dead ends and consequential divergences

- A facade over the old loose modules was rejected. It would have made both
  public surfaces appear supported while leaving import ambiguity intact.
- Loading authoring YAML directly from the checkout was rejected for the
  default catalogue API. Installed bytes must work without a repository root.
- Treating the installed console's `site-packages` ancestor as a project root
  was rejected. Operator commands now state their checkout dependency and fail
  before reading arbitrary ambient paths.
- In-place template substitution was removed rather than made reversible.
  Source mutation and partial output after a late placeholder failure are both
  incompatible with publication evidence.
- One universal `complete` flag was rejected. The implementation retains
  evidence-specific readiness predicates even though that requires more
  explicit reporting code.
- The package build intentionally consumes generated runtime resources rather
  than making the wheel a second authoring environment. Canonical metadata and
  proof projections remain source-workflow concerns.

## Visual provenance

This foundation had no external visual baseline or image-matching requirement.
Its user-visible visualization was designed and accepted in the later
[`formalism-semantic-closure`](../formalism-semantic-closure/README.md) record,
which preserves the exact desktop and mobile review captures.
