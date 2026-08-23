# fep_lean

`fep_lean` is a standalone catalogue of 155 Free Energy Principle, Active
Inference, Bayesian Mechanics, Information Geometry, and Thermodynamics topics.
Each row contains a reviewed invariant, explicit assumptions, a Lean 4 theorem
body, and typeset signatures. The pinned Lean workspace is the compilation
authority; the semantic review separately records how far each theorem reaches
toward its topic label. The schema-2 roster spans 20 reviewed families in five
areas and is a versioned interface, not an exhaustive census of the FEP
literature. The twenty families include five second-expansion families for
finite-sample risk, closed-loop policy trees, native blanket transfer, finite
exponential-family dual geometry, and exact two-state continuous time.

## Contract

`full` execution is strict. It requires the pinned Lean/Lake/Mathlib workspace,
the `gauss` executable, configured Hermes credentials, and writable SQLite
state. Every selected row must compile without `sorry` or Lean warnings, and a
requested review workflow must complete its post-compile review turn.
**Missing capability or incomplete stage → `complete: false`, no report
directory.**

`catalogue` execution is deterministic and offline. It validates the complete
YAML source and writes figures, manuscript variables, the unified appendix, and
a report explicitly marked `catalogue`; it does not count topics as verified.

`verify` execution is Lean-only. It runs the sealed-roster native compile sweep
without Hermes or OpenGauss. Add `--receipt output/native-verification.json
--fail-on-warnings` to persist independently revalidatable native evidence.

`atlas` execution is deterministic and offline. It projects the canonical
coverage join into a standalone SVG and an interactive, keyboard-accessible
HTML graph; `--check` fails on missing or stale bytes. The graph distinguishes
derivational formal edges from checked formal pairings that place two endpoint
laws side by side without asserting implication. Both name qualified Lean
witnesses; conceptual and blocker edges remain visibly non-proof evidence.

`dashboard` execution is also deterministic and offline. It renders static
and interactive numerical witnesses for all fifteen expansion families. The
first ten cover Bayesian inversion, variational duality, control, temporal
inference, causal intervention, predictive coding, path thermodynamics,
categorical Fisher geometry, consensus, and finite concentration; the latest
five cover Laplace/Brier risk transfer, policy-tree feedback, native blanket
conditional independence, exponential-family duality, and a two-state master
equation. These witnesses expose computational behavior and boundary cases but
never replace native Lean or axiom-audit evidence.

## Formal depth

The live formalism is organized into theorem-connected strands rather than a
headline theorem count: normalized finite probability and information
algebras, including support-free separation for the explicitly totalized finite
KL; posterior-form variational free energy and a uniquely attained evidence
lower bound; both expected-free-energy decompositions; a transition-consistent
infer--select--act joint and prior-sensitive Boolean policy witness;
stage-dependent cumulative finite-horizon EFE; finite Bayesian inversion,
variational duality, controlled and temporal inference, causal interventions,
and generalized predictive coding; path-space fluctuation identities and
reversible KL dissipation; categorical Fisher geometry, Cramér--Rao,
natural-gradient, mirror-descent, and replicator laws; collective inference;
finite concentration and model-evidence results; finite Laplace/Brier risk
transfer; observation-contingent policy-tree recursion and dominance; native
`CondIndepFun` blanket transfer; scalar exponential-family KL/Bregman duality;
and an exact two-state continuous-time semigroup, master equation, detailed
balance, relaxation, and Lyapunov law. The generated
[coverage report](docs/formalism-coverage.md) owns all current counts, and the
[atlas](docs/formalism-atlas.html) shows exactly which relations have Lean
witnesses. The semantic firewall requires every non-formalized row to expose
an explicit scope or assumption boundary. The reusable kernel is an explicit
manifest of foundations and leaf composition modules; `composed.lean` is only
their import aggregate. The maturity audit, rather than compilation alone,
records which rows are direct formalizations and which remain conditional or
structural proxies.

**Current evidence boundary.** The maintained source now spans 155 topics. The
current exact-roster native receipt independently validates 155/155 topics
under Lean 4.33.1 and Mathlib `v4.33.1`, with zero failures, warnings, or
`sorry`. The schema-4 declaration/axiom receipt independently validates all
823 required formal-resource declarations, including 699 evidence
declarations, with no warnings, `sorryAx`, or untrusted axioms. The schema-3
Python receipt binds the complete canonical collected-node roster, zero
failures or errors, and line coverage at or above the maintained 89% floor to
the same frozen source and test roster. The schema-4
browser receipt replays all six accepted screenshots in Chrome 151 against 155
topics, 20 families, and 15 typed numerical witnesses. The full report
[`run_20260820_183143_709998`](output/reports/run_20260820_183143_709998/)
remains historical evidence for the earlier 50-topic source snapshot and does
not bind the 155-topic source; the earlier Kimi and Gemini one-topic runs are
historical smoke evidence as well. No provider secret is stored in the
repository, and no execution receipt authorizes publication or proves the FEP
as a physical theory.

## Quick start

Run operator commands from a source checkout. Installed wheels support the
packaged `FEPTopicCatalogue.default()` API and `fep-lean --help`; substantive
commands deliberately require the checkout-owned configuration, Lean
workspace, and manuscript assets. From another directory, pass
`--project-root /path/to/fep_lean` before the subcommand.

```bash
uv sync --extra dev
uv run python docs/pin_audit.py --check-latest
uv run fep-lean catalogue
uv run fep-lean atlas
uv run fep-lean dashboard
uv run fep-lean setup
uv run fep-lean verify --fail-on-warnings \
  --receipt output/native-verification.json
uv run fep-lean preflight
uv run fep-lean run
```

Use `uv run fep-lean --help` for filters, workflow selection, and the explicit
checkout root. The equivalent maintained scripts are thin command wrappers in
[`scripts/`](scripts/).

## Source of truth

- [`config/catalogue_metadata.yaml`](config/catalogue_metadata.yaml) maintains
  the stable roster's descriptive and Mathlib metadata.
- [`config/theorem_maturity.yaml`](config/theorem_maturity.yaml) maintains the
  semantic review independently of syntactic compilation maturity.
- [`config/formalism_novelty.yaml`](config/formalism_novelty.yaml) records every
  post-baseline topic's nearest predecessors, invariant, carrier delta, and
  required composition theorem.
- [`config/formalism_relations.yaml`](config/formalism_relations.yaml) maintains
  reviewed formal, conceptual, and blocker relations plus retained open,
  partial, and satisfied capability history. Shared imports never create
  scientific-dependency edges.
- [`src/fep_lean/catalogue/bodies/`](src/fep_lean/catalogue/bodies/) contains
  the family-owned Lean bodies;
  [`registry.py`](src/fep_lean/catalogue/registry.py) validates their canonical
  order and [`latex.py`](src/fep_lean/catalogue/latex.py) derives theorem
  signatures.
- [`config/topics.yaml`](config/topics.yaml) and
  [`src/fep_lean/data/topics.yaml`](src/fep_lean/data/topics.yaml) are generated,
  byte-identical catalogue projections; regenerate them with
  [`scripts/_maint_build_topics_catalogue.py`](scripts/_maint_build_topics_catalogue.py).
- [`lean/FepSketches/fep_all.lean`](lean/FepSketches/fep_all.lean) is the tracked
  aggregate generated by
  [`scripts/_maint_build_fep_all_lean.py`](scripts/_maint_build_fep_all_lean.py).
- [`src/fep_lean/formal/manifest.py`](src/fep_lean/formal/manifest.py) owns the
  formal-resource roster. Canonical cross-topic proofs live in
  [`formal/compositions/`](src/fep_lean/formal/compositions/), while
  [`composed.lean`](src/fep_lean/formal/composed.lean) is the import-only
  aggregate; all tracked Lake projections are generated by
  [`scripts/_maint_build_formal_modules.py`](scripts/_maint_build_formal_modules.py).
- [`docs/formalism-coverage.md`](docs/formalism-coverage.md),
  [`docs/formalism-atlas.svg`](docs/formalism-atlas.svg), and
  [`docs/formalism-atlas.html`](docs/formalism-atlas.html) are generated views
  of the same canonical semantic graph.

## Review contracts

- [`ISA.md`](ISA.md) defines the ideal state, anti-criteria, and evidence gates.
- [`TODO.md`](TODO.md) is the canonical open-only backlog with behavior-based
  acceptance probes.
- [`CHANGELOG.md`](CHANGELOG.md) records the local audit evidence and remaining
  release boundary.
- [`manuscript/04i_formalism_catalogue_155.md`](manuscript/04i_formalism_catalogue_155.md)
  states the five new families, theorem assumptions, non-vacuity witnesses,
  and evidence boundaries in one authored chapter.
- [`HANDOFF.md`](HANDOFF.md) gives the next reviewer the operating protocol,
  evidence receipt, and remaining extension scope.

## Development checks

```bash
uv run python scripts/_maint_build_topics_catalogue.py --check
uv run python scripts/_maint_build_fep_all_lean.py --check
uv run python scripts/_maint_build_formal_modules.py --check
uv run python scripts/theorem_maturity_audit.py --check
uv run python scripts/build_formalism_coverage.py --check
uv run fep-lean atlas --check
uv run fep-lean dashboard --check
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
uv run python docs/theorem_ref_audit.py
uv run python docs/citation_audit.py
uv run python scripts/render_manuscript.py --check
uv run pytest tests/ -q --cov=src --cov-fail-under=89
uv run mypy src
uv run ruff check src tests scripts docs
uv run ruff format --check src tests scripts docs
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
```

The reproducible build and publication gates are documented in
[`docs/getting-started.md`](docs/getting-started.md),
[`docs/pipeline.md`](docs/pipeline.md), and
[`docs/cold-start-and-cleanup.md`](docs/cold-start-and-cleanup.md).

## Layout

| Path | Purpose |
| --- | --- |
| `src/fep_lean/catalogue` | typed semantic model, family-owned canonical bodies, generation, and coverage projections |
| `src/fep_lean/formal` | packaged foundations, leaf compositions, import aggregate, and workspace projection |
| `src/fep_lean/verification` | read-only capability checks, Lean compiler bridge, and declaration/axiom audit |
| `src/fep_lean/llm` | configured Hermes HTTP client |
| `src/fep_lean/gauss` | SQLite sessions and per-topic orchestration |
| `src/fep_lean/output` | evidence receipts, fail-closed rendering, figures, reports, the offline formalism atlas, and the typed numerical dashboard |
| `src/fep_lean/pipeline` | strict `full` and explicit offline `catalogue` modes |
| `lean` | pinned Lake workspace and tracked aggregate |
| `manuscript` | source chapters and generated publication inputs |

## Notation

Lean identifiers are deliberately topic-prefixed (`fepNNN_*`) and should be
read together with the corresponding invariant and `assumption_review` in
`config/theorem_maturity.yaml`. The generated appendix renders exact theorem
signatures; prose notation is never an alternative source for the Lean API.
