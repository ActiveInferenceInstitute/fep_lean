# Formalism catalogue 120 — closed rationale

Status: closed
Opened: 2026-08-20
Accepted: 2026-08-21
Working-tree policy: shared, dirty, uncommitted, and unpublished

## Purpose

The catalogue contains 120 ordered Free Energy Principle, Active Inference,
Bayesian Mechanics, Information Geometry, and Thermodynamics topics. The
expansion exists to make breadth inspectable without allowing topic count,
compilation, a numerical chart, or provider output to masquerade as scientific
completeness.

Each topic therefore belongs to an exact roster and family, owns a canonical
Lean body, names its primary and supporting declarations, records assumptions
and non-vacuity, and carries a reviewed semantic disposition. The reusable
formal kernel, cross-topic relations, numerical witnesses, generated
manuscript, and native receipts are separate evidence planes over that same
catalogue.

The number 120 is a bounded interface, not a claim that the relevant
literature is exhausted. It was large enough to force the original monolithic
source and fixed-size visual assumptions to fail, while remaining small enough
for exact joins, per-topic native compilation, declaration-level axiom audits,
and human review.

## Why the system has this shape

### One roster and one body registry

The old body monolith made every extension a collision-prone edit and allowed
fixed ranges to become shadow catalogue owners. The accepted design derives
the ordered roster from the schema-2 seal in
[`config/catalogue_metadata.yaml`](../../../config/catalogue_metadata.yaml), then
joins it to family-owned `BODIES` maps through
[`catalogue/registry.py`](../../../src/fep_lean/catalogue/registry.py). There is no
compatibility alias or second numeric range.

Five broad areas remain stable lenses, but 15 families own the finer research
structure. Area and family are separate metadata fields, although every
current family belongs to exactly one area. Scientific relations may cross
those area boundaries without creating a second family hierarchy.

### Foundations and leaf compositions

Reusable mathematics belongs to manifested foundations. Cross-topic claims
belong to six leaf composition modules, while `FepSketches.composed` is only an
import aggregate. This keeps implementation imports distinct from scientific
relations and makes a relation witness reviewable without opening a growing
proof monolith.

The formal resource roster is owned by
[`formal/manifest.py`](../../../src/fep_lean/formal/manifest.py). Topic bodies may
use the aggregate topic namespace; foundations may not. A theorem-backed
relation must resolve in a manifested composition leaf and consume both
endpoint namespaces. A `formal_pairing` conclusion exposes both endpoint laws
as a conjunction and is classified as non-derivational; the validator does not
reinterpret the pairing as an implication between them.

### Honest breadth instead of uniform promotion

Native compilation is necessary but not sufficient. The accepted semantic
census is 101 `formalized`, 13 `conditional_proxy`, and 6
`structural_proxy` topics. The 19 scoped proxies are retained because their
finite carriers, supplied certificates, or structural analogues do not prove
the unrestricted scientific title one might otherwise infer.

This distinction is owned by
[`config/theorem_maturity.yaml`](../../../config/theorem_maturity.yaml) and tested
as an exact reviewed set. Narrowing a theorem is preferable to adding `sorry`,
a custom axiom, or promotional prose.

### Lexical checks are evidence boundaries

Several early validators scanned raw Lean text. That made comments and strings
capable of fabricating declarations, imports, namespace use, or relation
endpoints. The shared lexer in
[`lean_source.py`](../../../src/fep_lean/lean_source.py) now blanks nested comments
and strings while preserving offsets, and the catalogue, novelty, coverage,
reference, LaTeX, generation, and formal-inventory consumers use that neutral
surface.

Source parsing still does not replace Lean elaboration. It establishes exact
ownership and closure before native compilation; the declaration receipt then
queries the kernel for resolution and axiom dependencies.

### Numerical results explain but never certify

Ten deterministic witnesses make assumptions and boundary behavior visible.
Nine exactly instantiate named theorem surfaces; the sub-Gaussian envelope is
explicitly a `structural_analogue`. The stronger label is opt-in rather than a
default so a new diagnostic cannot silently promote itself.

[`numerical_witnesses.py`](../../../src/fep_lean/verification/numerical_witnesses.py)
owns evaluation, finite values, residuals, tolerances, boundary observations,
plot schemas, exact family closure, and checkout-bound theorem references.
[`formalism_presentation.py`](../../../src/fep_lean/output/formalism_presentation.py)
freezes the single join consumed by both renderers. Plots never own a second
scientific roster or recalculate the invariant.

### Evidence planes remain separate

The repository distinguishes:

- deterministic catalogue and projection freshness;
- semantic maturity and relation classification;
- per-topic native Lean compilation;
- declaration resolution and trusted-axiom evidence;
- deterministic numerical diagnostics;
- browser and visual acceptance;
- optional Hermes/OpenGauss execution; and
- manuscript publication bytes.

A clean result in one plane cannot close another. In particular, current
native and declaration receipts do not make the retained 50-topic provider
report current, and none of these artifacts proves the Free Energy Principle
as a physical theory or authorizes publication.

## Invariants that must survive

1. The sealed roster, metadata rows, maturity rows, family body keys, generated
   YAML rows, aggregate Lean namespaces, and full native receipt rows are the
   same ordered tuple from `fep-001` through `fep-120`.
2. The original 50 canonical body strings retain the SHA-256 values recorded
   in the [extraction baseline](assets/slice-01-original-body-sha256.json).
3. Every topic belongs to exactly one declared family, and body-module family
   ownership agrees with catalogue metadata.
4. No maintained source constructs a competing fixed topic range or exposes a
   second body-registry alias.
5. Every primary, supporting, boundary, capability, novelty-bridge, and
   theorem-backed relation declaration resolves in the canonical closure.
6. Foundations do not import topic namespaces. Cross-topic bridge ownership is
   confined to manifested composition leaves.
7. Formal relation endpoint use is checked on comment-free Lean code;
   `formal_pairing` exposes a conjunction in the theorem conclusion.
8. Native claim readiness requires the complete live roster, complete owner
   manifest, current projections, matching Lean and Mathlib identities, zero
   warnings, and zero `sorry`.
9. Declaration-audit readiness requires one unambiguous axiom result per
   declaration and rejects every axiom outside the versioned allowlist.
10. Numerical witnesses cover the exact ten expansion families, contain only
    finite plotted values, expose boundary behavior, and identify theorem
    instances separately from structural analogues.
11. Atlas and dashboard bytes derive only from the immutable presentation
    join, remain offline, conserve all counts, expose accessible tables, and
    pass their drift checks.
12. Rendering is fail-closed and transactional: malformed or unresolved
    placeholders, missing required assets, and stale chapters cannot leave a
    partial publication tree. Unavailable optional external evidence renders
    an explicit false claim-ready state instead of aborting publication.
13. Historical receipts remain readable historical evidence but cannot become
    current through an adapter or stale digest.

## Scientific scope

The kernel provides explicit finite, finite-dimensional, and selected
measure-theoretic results across Bayesian inversion, variational duality,
active inference, controlled and temporal inference, causal intervention,
predictive coding, stochastic thermodynamics, information geometry,
collective inference, and learning/model evidence.

The maturity ledger is authoritative about limitations. Examples include
finite reachable belief indices rather than arbitrary POMDP belief spaces,
finite-jet correction rather than an unrestricted generalized-coordinate
flow, explicit support conditions for logarithmic thermodynamic identities,
square invertible charts for the natural-gradient result, conditional
log-moment premises for PAC-Bayes, and totalized real-valued finite KL rather
than unqualified extended-real KL at zero reference support.

The generated [coverage report](../../../docs/formalism-coverage.md) and
[maturity audit](../../../docs/theorem-maturity-audit.md) are the current
machine-derived maps. This record intentionally does not duplicate their full
tables.

## Pointers to the mechanics

| Concern | Owner | Behavioral contract |
| --- | --- | --- |
| Roster and families | `config/catalogue_metadata.yaml`, `catalogue/schema.py` | `tests/test_catalogue_registry_ssot.py`, `tests/test_semantics.py` |
| Canonical bodies | `catalogue/bodies/*.py`, `catalogue/registry.py` | `tests/test_catalogue_registry.py`, `tests/test_fep_all_lean_ssot.py` |
| Novelty and bridges | `config/formalism_novelty.yaml`, `catalogue/novelty.py` | `tests/test_formalism_novelty.py`, `tests/test_expansion_compositions.py` |
| Relations and capabilities | `config/formalism_relations.yaml`, `catalogue/coverage.py` | `tests/test_formalism_relations.py`, `tests/test_formalism_coverage.py` |
| Formal kernel | `formal/manifest.py`, `formal/*.lean`, `formal/compositions/*.lean` | `tests/test_formal_foundations.py`, family formalism tests |
| Lean lexical ownership | `lean_source.py`, `formal/declarations.py` | comment/string mutation tests in catalogue, semantics, coverage, and foundations suites |
| Native receipt | `verification/lean_verifier.py`, `output/evidence.py` | `tests/test_native_evidence.py`, `tests/test_cli.py` |
| Declaration audit | `verification/formalism_audit.py` | `tests/test_formalism_audit.py` |
| Numerical evidence | `verification/numerical_witnesses.py` | `tests/test_numerical_witnesses.py` |
| Presentation | `output/formalism_presentation.py`, atlas/dashboard renderers | presentation, atlas, dashboard, distribution, and CLI tests |
| Publication | `output/manuscript.py`, `output/rendering.py`, `output/reporter.py` | manuscript, reporter, pipeline, and orchestrator tests |

## Decisions that changed during implementation

- Collective inference remained a seven-topic family, but a separate
  `finite_markov_dynamics` foundation was added so consensus and path results
  reuse explicit kernel-power, invariance, reversibility, contraction, and
  mass-conservation laws rather than standing on generic averaging alone.
- The proposed “equal-weight logarithmic pool” was mathematically a
  unit-weight product of experts. The topic, declarations, bridge, manuscript,
  and numerical language were renamed rather than preserving the false label.
- The PAC-Bayes topic was narrowed to a deterministic conditional loss-gap
  theorem with positive inverse temperature, full-support prior, Gibbs
  certificate, and explicit log-MGF budget. It does not manufacture its own
  high-probability data event.
- Soft Bellman evidence gained a nonempty-action premise, positive partition,
  exact recursion, and an actionwise soft-value upper bound after review found
  the earlier statement too weak.
- The categorical Fisher carrier gained a genuine `Fin 2` tangent-spanning and
  energy-four witness, while the duplicated-score null direction remains the
  explicit rank-deficient boundary.
- The source-preservation contract for provider output became exact
  non-comment token equality for this proof-complete corpus. A permissive
  theorem-name intersection admitted weakened `: True` declarations and even
  an indented custom-axiom escape, so it was rejected.
- Renderer-specific topic arrays and fixed card geometry were removed. The
  five areas stay stable, but family/topic placement, relation kinds, witness
  cards, and mobile heights are data-driven.
- Native verification reached current 120-topic evidence. Provider execution
  did not run against the expanded source; the prior full receipt remains
  historical and the external stage stays explicit in [`TODO.md`](../../../TODO.md).

## Acceptance evidence

The machine-readable [acceptance receipt](assets/acceptance.json) records the
settled counts, test result, native and declaration receipt hashes, visual
hashes, and external-provider boundary.

At acceptance:

- the catalogue contains 120 topics in 15 families and five areas;
- the semantic census is 101 formalized, 13 conditional proxies, and 6
  structural proxies;
- the source exposes 422 topic and 463 formal-resource theorem/lemma
  declarations, for 885 total, plus 318 definitions;
- the graph contains 20 derivational formal relations, 70 formal pairings, 8
  conceptual relations, and 43/43 satisfied capabilities;
- the retained [JUnit suite](assets/pytest.xml) reports 737 passed and 22
  skipped, while the separately retained [coverage report](assets/coverage.xml)
  records 5,964 of 6,575 statements covered, or 90.71%;
- the native receipt verifies 120/120 topics with zero warnings and zero
  `sorry`; and
- the declaration receipt resolves 647/647 audited declarations, including
  558 evidence declarations, with no `sorryAx` or untrusted axiom.

## Visual provenance

No external screenshot, mood board, or third-party interface served as a
baseline. The visual standard was the canonical data itself plus repeated
fresh, unprimed review: every area/family and every numerical witness had to be
inspectable without clipping, false visual precision, or loss of evidence
boundaries.

The retained [visual review](visual-review.md) explains that standard and the
Chrome interaction probe. Its final accepted evidence is:

- [atlas standalone](assets/atlas-120-standalone.png),
  [desktop](assets/atlas-120-desktop.png), and
  [mobile](assets/atlas-120-mobile.png);
- [dashboard standalone](assets/dashboard-120-standalone.png),
  [desktop](assets/dashboard-120-desktop.png), and
  [mobile](assets/dashboard-120-mobile.png); and
- the [browser interaction receipt](assets/browser-interaction-receipt.json).

Superseded summary crops used during iteration were removed rather than being
retained as ambiguous evidence. The six accepted captures establish
presentation acceptance only; they are neither theorem receipts nor empirical
evidence for the Free Energy Principle.

## Open external boundary

Current native and declaration evidence is cryptographically bound to the
expanded source; manuscript, numerical, and visual evidence is current under
its deterministic drift checks and retained artifact hashes. Current
Hermes/OpenGauss full-mode evidence does not bind the expansion. A new external
run requires a separately confirmed credential and spend boundary and must
pass the live-source report validator. Until then, the 2026-08-20 50-topic
report and earlier one-topic smokes remain historical artifacts.

No commit, push, pull request, upload, or publication occurred while closing
this record.
