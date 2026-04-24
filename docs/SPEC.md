# docs/ Specification — what this folder promises

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

> **Not the functional spec.** For the system behaviour of `fep_lean` (pipeline stages,
> catalogue maturity, testing policy, CI gates) see [`../SPEC.md`](../SPEC.md). This file
> is scoped to what `projects/fep_lean/docs/` commits to as a documentation artifact.

## Purpose

This folder is the **reference layer** for `fep_lean`: the hand-maintained narrative,
API, and operational material that a developer or automated agent needs in order to
read, use, extend, or review the project without having to reverse-engineer the source.

The primary audiences, in priority order:

1. **Agents acting on behalf of users** (this project is agent-heavy and needs
   machine-parseable, unambiguous, ground-truthed docs).
2. **Developers** newly assigned to the project who want to ship within the first day.
3. **Paper readers** looking up a topic, a Lean sketch, or a configuration variable
   that is referenced from the manuscript.
4. **Reviewers / auditors** verifying claims made in the manuscript or in CI logs.

## Scope

**In scope** for `docs/`:

- How to install, run, debug, and extend `fep_lean`.
- The public API surface of every `src/` subpackage.
- Every environment variable the code reads, with defaults and provenance.
- Every CLI flag of every entry-point script.
- The file layout of `output/reports/run_*/` and the generated manuscript slices.
- The theoretical background sufficient to understand the 50-topic catalogue at
  the level of definitions, statements, and references.
- A glossary of FEP / Bayesian-mechanics terminology.
- Troubleshooting recipes for every reproducible failure mode.

**Out of scope** for `docs/`:

- The system-level functional spec (in [`../SPEC.md`](../SPEC.md)).
- The agent behaviour contract (in [`../AGENTS.md`](../AGENTS.md)).
- The paper itself (in [`../manuscript/`](../manuscript/)).
- Code implementation — docs point to `src/` for that, never replicate it.

## Operating Contracts

These are the hard invariants the docs must satisfy; CI should enforce them
via `check_links.py`, `md_hygiene.py`, `pin_audit.py`, and `xref_audit.py`;
manual review still covers narrative accuracy beyond what those gates encode.

### A. Accuracy (ground-truthed against code)

- **A1. Topic count.** Any narrative that names a number of topics must say **50**
  unless the immediate context is a subset filter. Authoritative source:
  [`../config/topics.yaml`](../config/topics.yaml).
- **A2. Area distribution.** The canonical per-area counts are:
  FEP = 14, ActiveInference = 11, BayesianMechanics = 10, InfoGeometry = 8,
  Thermodynamics = 7.
- **A3. Pipeline stages.** `FEPPipeline.run()` records **four** named stages in
  `PipelineResult.stages` (Load Catalogue, Environment Validation, Gauss Sessions,
  Manuscript Artifacts). Run reporting (`Reporter.generate` → `output/reports/run_*/`)
  runs inside `pipeline.orchestrator.run_pipeline` *after* `FEPPipeline.run()` returns,
  so it is **not** a fifth stage in `stages`. When `FEP_LEAN_GAUSS_WORKFLOWS` is
  unset or `0`, Gauss Sessions is skipped (recorded as `status: "skipped"`).
- **A4. Environment validation.** `run_validation_checks` (in
  `../src/verification/environment.py:328-343`) issues **13** checks. Any doc that
  names a number of checks must say 13 and the list must match the names in the
  source.
- **A5. Test scale.** Pytest collects **347** items (`uv run pytest --collect-only -q`
  from `projects/fep_lean/`). The last known green run reports
  **346 pass / 1 skip** and **~90 %** combined line+branch coverage against the **89 %** gate in
  `pyproject.toml::fail_under = 89`.
- **A6. Lean sketches.** All 50 topics are `mathlib_status: real` and compile clean
  (zero `sorry`, zero errors) on Lean v4.29.0 + Mathlib v4.29.0. Illustrative code
  fences in `topics-reference.md` may simplify; canonical bodies are authored in
  `../scripts/catalogue_sketches.py` (`SKETCHES`), and `../config/topics.yaml` must
  match (`tests/test_catalogue_sketches_ssot.py`). Every committed sketch is wrapped
  in a `namespace FEPNNN ... end FEPNNN` block keyed to the catalogue id (for
  instance `namespace FEP014 ... end FEP014` for fep-014); this isolation is
  load-bearing for the `lean/FepSketches/fep_all.lean` aggregate and is enforced by
  the SSOT test and the verifier wrapper.
- **A7. Lean version pin.** Any claim about Mathlib / Lean version must match
  `../lean/lakefile.lean` (`require mathlib @ "v4.29.0"`) and
  `../lean/lean-toolchain` (`leanprover/lean4:v4.29.0`).
- **A8. Stage 02 analysis timeout.** The template Stage 02 runner
  (`../../../scripts/02_run_analysis.py`) uses `ANALYSIS_SCRIPT_TIMEOUT_SEC` with
  default **7200** seconds per project script unless overridden; parsing lives in
  [`../../../infrastructure/core/analysis_timeout.py`](../../../infrastructure/core/analysis_timeout.py).
- **A9. Parallelism contracts.** Stage 4 may overlap manuscript vars + appendix markdown
  with `write_all_catalogue_figures` via `ThreadPoolExecutor` in `pipeline/core.py`.
  `write_all_catalogue_figures` (`output/figures.py`) dispatches the nine PNGs through
  `ProcessPoolExecutor` with ``spawn`` (fallback: serial). Set `FEP_LEAN_FIGURES_MP=0` to
  force serial rendering. Optional `FEP_LEAN_PREFETCH=1` enables Hermes prefetch for the
  next topic while Lean verifies the current topic (`gauss/runner.py`; `verify` workflow,
  batch size ≥ 2). `verify_batch` remains sequential (`max_workers=1`). CI and default
  developer runs use single-process pytest; `pytest-xdist` is optional and documented as
  unsafe for concurrent Lean workspace access unless tests are partitioned manually.
  Coverage uses `concurrency = ["multiprocessing"]` in `pyproject.toml` so figure worker
  processes are traced.

### B. Cross-linking

- **B1.** All internal links are relative paths (never absolute `/Users/...` paths).
- **B2.** Every doc has a `## Navigation` section linking back to at least
  `README.md` plus one "forward" and one "back" link.
- **B3.** `check_links.py` (basic mode) exits 0 against `docs/`.
- **B4.** `check_links.py --strict` exits 0 — all `#anchor` targets exist in their
  target files.
- **B5.** `pin_audit.py` exits 0 — every Lean toolchain, Mathlib tag, and Hermes
  **primary** model literal in project `*.md` files outside `manuscript/` (which
  uses `{{…}}` placeholders) matches the canonical pins read from
  `../lean/lean-toolchain`, `../lean/lakefile.lean`, and
  `../config/settings.yaml` (`hermes.model`, cross-checked against
  `gauss.default_model`).
- **B6.** `xref_audit.py` exits 0 — every `\ref{...}` / `\eqref{...}` /
  `\Cref{...}` / `\cref{...}` in `../manuscript/*.md` resolves to a pandoc
  `{#id}` anchor or a LaTeX `\label{id}` definition.

### C. Style and hygiene

- **C1.** Every file ends in a newline.
- **C2.** Headings use `#` with a trailing space. Exactly one `# H1` per file.
- **C3.** List markers (`-`, `*`, `+`) have a trailing space.
- **C4.** `md_hygiene.py` exits 0 (basic mode) and `md_hygiene.py --strict`
  is clean of orphan brackets, trailing whitespace, and tabs outside code blocks.
- **C5.** Code fences specify a language when the block is non-trivial
  (```bash`, ```python`, ```lean`, ```yaml`).

### D. Show, don't tell

- **D1.** Every public API section in `api.md` has a runnable example or a
  concrete schema.
- **D2.** Every environment variable in `configuration.md` has a default,
  an example value, and a named code site that reads it (`file.py:line`).
- **D3.** Every troubleshooting entry in `troubleshooting.md` cites:
  (a) the exact error the user sees, (b) the root cause, (c) the *exact* fix
  commands.

### E. Version alignment

- **E1.** The `**Version**:` line on every file in this folder matches the
  documentation hygiene release (currently **`v0.7.1`**, aligned with
  `../manuscript/config.yaml::paper.version`). Bump both together when cutting a
  docs/manuscript-only release; bump `../pyproject.toml` `project.version` and
  `../config/settings.yaml::project.version` when releasing the Python package
  to the same number (they may temporarily diverge by patch until aligned).
- **E2.** "Last Updated" month can be set on any edit but must not be in the future.

## How to extend

When you add a topic, rename a module, change a flag, or bump a version, the docs
update sweep must touch:

1. Any file listed above that hard-codes the changed number / name.
2. `README.md` (the index — if you add a new doc, it must be linked here).
3. `SPEC.md` and `AGENTS.md` inside this folder (both mention invariants).
4. `cli-reference.md` if CLI surface changed.
5. `configuration.md` if env vars changed.
6. `api.md` if public symbols changed.
7. Run `check_links.py --strict --include-root`, `md_hygiene.py --strict
   --include-root`, `pin_audit.py`, and `xref_audit.py`; all must exit 0.

## Validation loop

```bash
cd projects/fep_lean/docs

# Fast: pass/fail
uv run python check_links.py
uv run python md_hygiene.py

# Thorough: anchors, orphan brackets, trailing whitespace, duplicate H1, max line
uv run python check_links.py --strict --include-root -v
uv run python md_hygiene.py --strict --include-root --max-line 200 -v

# Toolchain / model literal drift vs SSOT; manuscript \\ref integrity
uv run python pin_audit.py --verbose
uv run python xref_audit.py --verbose
```

Exit code `0` ⇒ docs pass. Exit code `1` ⇒ at least one issue; the line(s)
listed in stdout identify the file and line.

## Navigation

- [← Project SPEC](../SPEC.md)
- [docs/AGENTS.md](AGENTS.md) — editing conventions for this folder
- [docs/README.md](README.md) — document index
