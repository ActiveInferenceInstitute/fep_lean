# fep_lean formalism and publication handoff

**Date:** 2026-08-23
**Repository:** `ActiveInferenceInstitute/fep_lean`
**Checkout:** `/home/trim/Documents/Git/HumOS/projects/outside_of_hum/fep_lean`
**Release line:** `v1.1.0`

## Mission and evidence boundary

This standalone repository now has an installable `fep_lean` package, a typed
155-topic semantic catalogue in 20 families, a pinned Lean kernel with warning
rejection, an authored formalism relation/capability graph, fail-closed evidence
receipts, and source-to-build manuscript rendering. Keep four claims separate:

1. catalogue generation is deterministic but verifies zero topics;
2. native Lean evidence proves that the exact selected source compiled at the
   pin without warnings or `sorry`;
3. semantic disposition records how closely a row matches its advertised
   scientific topic;
4. bounded Hermes/OpenGauss evidence applies only to the exact source and
   receipt schema it records; publication-grade live evidence requires a
   claim-ready report bound to the final source.

Two bounded one-topic OpenRouter/Hermes smokes were completed on 2026-08-20
against earlier source snapshots: `fep-001` with Kimi K2.6 and `fep-002` with
Gemini 3.7 Flash. Both selected topics passed the then-current pipeline, Gauss
session, and Lean checks. They are historical connectivity and workflow
evidence only: the source and receipt schema subsequently changed, and the
current validator correctly rejects both report directories as non-current.
The retained report directories are
`output/reports/run_20260820_150225_893319` and
`output/reports/run_20260820_150523_744462`.

The later 50-topic report,
`output/reports/run_20260820_183143_709998`, superseded those one-topic smokes
for its own source snapshot. It is now historical too: the schema-2 expansion
changed the roster, body-source manifest, formal resources, and source digests.
It must not be described as current evidence for the 155-topic checkout.

No provider secret is stored in the repository. Versioned publication does not
promote the historical provider runs: only a separately authorized,
source-bound full receipt can make a current Hermes/OpenGauss claim.

## Canonical ownership

| Concept | Maintained owner | Generated projection |
| --- | --- | --- |
| Static topic metadata | `config/catalogue_metadata.yaml` | catalogue YAML/package rows |
| Semantic review | `config/theorem_maturity.yaml` | package API, audit, manuscript |
| Typed relations and capabilities | `config/formalism_relations.yaml` | coverage and atlas projections |
| Lean bodies | `src/fep_lean/catalogue/bodies/*.py`, merged by `registry.py` | YAML and aggregate Lean |
| Theorem equation signatures | `src/fep_lean/catalogue/latex.py` | Catalogue and manuscript equations |
| Expansion novelty and bridges | `config/formalism_novelty.yaml` | Novelty audit and composition checks |
| Formal resource roster | `src/fep_lean/formal/manifest.py` | Lean workspace projection |
| Cross-topic theorems | `src/fep_lean/formal/compositions/*.lean` | Import aggregate and workspace leaves |
| Catalogue join | `src/fep_lean/catalogue/generation.py` | checkout/package YAML |
| Native/full evidence policy | `src/fep_lean/output/evidence.py` | manuscript claim sentences |
| Declaration/axiom audit | `src/fep_lean/verification/formalism_audit.py` | typed audit receipt |
| Formalism atlas renderer | `src/fep_lean/output/formalism_atlas.py` | standalone SVG/HTML |
| Authored manuscript | `manuscript/*.md` | `output/manuscript/` |

Never hand-edit `config/topics.yaml`, `src/fep_lean/data/topics.yaml`,
`lean/FepSketches/fep_all.lean`, any manifested `lean/FepSketches` formal resource,
`docs/formalism-coverage.*`, `docs/formalism-atlas.*`, or generated manuscript
output. Use the owner-provided generators and their `--check` modes.

## Current formal breadth and depth

- Stable schema-2 roster: `fep-001` through `fep-155`, partitioned into 20
  families across five areas.
- The generated coverage report owns all topic/formal-resource declaration,
  import, relation, and capability totals. Do not copy those moving totals into
  this handoff.
- Semantic review contains direct formalizations together with explicit
  conditional and structural proxies. Their assumptions and non-vacuity
  boundaries remain first-class even when the bodies compile.
- Manifested foundations and leaf compositions cover finite and
  measure-theoretic probability, Bayesian inversion, variational duality,
  active inference and controlled planning, temporal inference, causal
  interventions, predictive coding, stochastic thermodynamics, geometric
  optimization, collective inference, learning/model evidence, finite-sample
  risk, policy trees, native blanket transfer, exponential-family duality, and
  exact two-state continuous time.
- `fep-036` now defines a finite binomial sampling law and outcome-indexed
  Laplace prior, proves interiority, monotonicity, exact shrinkage, and
  consistency transfer from a convergent empirical frequency, while the
  statistical-convergence foundation derives the corresponding almost-sure
  Boolean, finite-atom, simultaneous, whole-law `L¹`, and finite-observable
  expectation limits. The `fep-121`--`fep-127` family now adds finite-law
  Laplace squared-risk and Brier-risk transfer plus event containment. It still
  does not claim posterior contraction, minimax optimality, empirical calibration, or a
  marginal-likelihood optimum.
- The formalism audit is designed to resolve every primary, relation,
  capability, and manifested formal-resource declaration, reject warnings and
  `sorryAx`, and require one parsed axiom result per declaration before
  recording the standard dependencies reported by Lean.

Compilation is not a proof of the FEP as a physical theory. Read
`docs/formalism-coverage.md` and `docs/theorem-maturity-audit.md` before
summarizing scientific completeness.

## Current 155-topic source and retained evidence

- Maintained metadata, maturity, novelty, relation, family-body, and formal
  manifest owners span the 155-topic source. Their catalogue, aggregate Lean,
  formal-resource, coverage, atlas, dashboard, manuscript, wheel, and receipt
  projections are regenerated and pass their deterministic drift checks.
- `output/formalism-audit.json` is current schema-4 evidence for the 155-topic
  source: 823/823 declarations resolved, 699 evidence declarations, Lean
  4.33.1 with the locked Mathlib revision, zero warnings, no `sorryAx`, and no
  untrusted axiom. `output/native-verification.json` independently validates
  the ordered 155-topic roster under the same toolchain with zero failures,
  warnings, or `sorry`.
- The schema-3 Python acceptance receipt binds the complete canonical
  collected-node roster, records zero failures or errors, and enforces the
  maintained 89% line-coverage floor.
  The schema-4 browser receipt replays six source-bound screenshots in Chrome
  151 and verifies all twenty families, 155 topics, 133 relations, and fifteen
  typed numerical witnesses without external requests or viewport overflow.
- The 2026-08-20 full Hermes/OpenGauss report remains historical for its exact
  50-topic source digest. Current provider claims still require a new,
  independently validated source-bound full report. Keep provider, native,
  declaration, numerical, and manuscript evidence planes separate.

## Reproduction commands

Run from the repository root:

```bash
uv sync --locked --extra dev
uv lock --check
uv pip check
uv run python scripts/_maint_build_topics_catalogue.py --check
uv run python scripts/_maint_build_fep_all_lean.py --check
uv run python scripts/_maint_build_formal_modules.py --check
uv run python scripts/theorem_maturity_audit.py --check
uv run python scripts/build_formalism_coverage.py --check
uv run python scripts/build_formalism_atlas.py --check
uv run fep-lean dashboard --check
uv run python docs/pin_audit.py --check-latest
uv run mypy src
uv run ruff check src tests scripts docs
uv run ruff format --check src tests scripts docs
(cd lean && lake build FepSketches)
uv run fep-lean verify --fail-on-warnings \
  --receipt output/native-verification.json
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
uv run fep-lean catalogue
uv run python scripts/render_manuscript.py --check
uv run python docs/theorem_ref_audit.py
uv run python docs/citation_audit.py
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/xref_audit.py
uv run python scripts/capture_browser_acceptance.py
uv run python scripts/build_release_bundle.py --run-python-acceptance
uv run fep-lean preflight
git diff --check

release_a_dir="$(mktemp -d)"
release_b_dir="$(mktemp -d)"
archive_a="$release_a_dir/fep-lean-1.1.0-155.tar.gz"
archive_b="$release_b_dir/fep-lean-1.1.0-155.tar.gz"
SOURCE_DATE_EPOCH=0 uv run python scripts/build_release_bundle.py \
  --output "$archive_a"
SOURCE_DATE_EPOCH=0 uv run python scripts/build_release_bundle.py \
  --output "$archive_b"
cmp "$archive_a" "$archive_b"
sha256sum "$archive_a" "$archive_b"
SOURCE_DATE_EPOCH=0 uv run python scripts/build_release_bundle.py \
  --check --output "$archive_a"
SOURCE_DATE_EPOCH=0 uv run python scripts/build_release_bundle.py \
  --check --output "$archive_b"
```

The canonical Python-acceptance command runs the exact collected suite and
atomically writes `output/pytest.xml`, `output/coverage.xml`, and
`output/python-acceptance.json`; a raw `pytest` run is a useful development
gate but is not a release receipt. Catalogue/manuscript generation precedes
that receipt because `manuscript/manuscript_vars.yaml` owns the canonical test
count. Browser capture follows the final renderer sources and atlas/dashboard
bytes. The two archive builds must remain byte-identical and independently
validate against the live checkout before publication.

Independently validate the native receipt against the live source tree before
using its prose projection. The CI workflow contains the exact validation
snippet.

## Historical external stage

`FEP-FULL-002` and `FEP-PROV-003` were closed for the earlier 50-topic snapshot
by its full report and artifact validation. That dated task closure is not a
current 155-topic acceptance receipt. The two earlier one-topic smokes remain
historical as well.

Never print, persist, or infer credentials from a successful run. A retained
receipt supports only the exact source digest and roster it records; it does not
authorize publication or establish the FEP as a physical theory.

## Next-review protocol

1. Read the nearest `AGENTS.md`, inspect `git status --short --branch`, and
   preserve unrelated or concurrent changes.
2. Edit maintained owners only; regenerate and inspect every projection.
3. Treat semantic-disposition changes as mathematical review, not as an
   automatic consequence of compilation.
4. Run impact analysis if GitNexus becomes available. It was unavailable for
   this nested checkout, so this pass used direct import/declaration searches,
   consumer tests, and native builds with reduced graph confidence.
5. Before any separately authorized publication, inspect the exact diff, run
   all applicable gates, commit intentionally, push, and verify remote parity.
