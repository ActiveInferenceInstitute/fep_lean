# fep_lean — deferred backlog

Created 2026-08-18 by the comprehensive review + hardening pass. Items here are
validated findings that were deliberately **not** implemented in that pass;
each carries an acceptance criterion so a future session can pick them up
without re-deriving the analysis.

## Toolchain

- **T1 — mypy gate is not runnable in-repo.** `[tool.mypy] strict = true` is
  configured in `pyproject.toml` but the `src/` tree uses flat,
  `pythonpath=["src"]`-style imports (`from catalogue.topics import ...`) that
  mypy cannot resolve without `mypy_path` configuration, and PyYAML ships no
  inline stubs (`import-untyped`). Observed: 30+ `import-not-found` errors on a
  stock `uv run mypy src/`.
  Acceptance: add `mypy_path = ["src"]` (or package the modules properly) and
  `types-PyYAML` to the dev extras; `uv run mypy src/` exits 0, or the config
  is removed if the gate is intentionally aspirational.

## Testing

- **T2 — serial_lean full-catalogue gate runs only opt-in.**
  `tests/test_catalogue_sketches_compile.py` skips unless
  `FEP_LEAN_CATALOGUE_COMPILE_TEST=1`; CI should run it after a warm Lake
  workspace so the 50-topic sorry-free claim is machine-enforced per commit.
  Acceptance: CI job (or documented maintainer cadence) executes the gate and
  fails the build on any non-clean compile. Verified locally 2026-08-18: all
  50 sketches compile clean in 104 s.
- **T3 — fep-lean run end-to-end live test is not automated.** The full-mode
  path (Hermes -> Lean -> SQLite -> report) is exercised only through unit-level
  seams; a credential-gated integration test would catch chain-advance and
  caching regressions against the live API.
  Acceptance: an opt-in (`FEP_LEAN_LIVE_TESTS=1`) test runs
  `run_single_topic("fep-001", mode="full")` and asserts a structured result.

## Packaging / config

- **T4 — pyproject.toml has no [tool.ruff] section.** `docs/development.md`
  tells developers to run `uv run ruff check src/`, which now passes clean
  under ruff's default rules (2026-08-18), but nothing pins the rule set, so
  future ruff versions can reintroduce failures. Acceptance: add a minimal
  `[tool.ruff.lint]` select list covering the rules fixed in this pass
  (I001, UP037, UP035, F401, F811, E402, E741, SIM105, SIM201) and document it
  in `docs/development.md`.
- **T5 — no `hermes.fallback_count` token.** Manuscript prose references
  `{{hermes.fallback_count}}` while the code produces
  `hermes.model_fallback_count`. The injector leaves the unmatched token
  literal. Acceptance: either add `fallback_count` as an alias in
  `_hermes_block_from_summary` or normalise the manuscript prose to the
  existing key; `_inject_manuscript_vars.py --dry-run` should report zero
  unmatched `{{...}}` placeholders in shipped chapters.

## Docs

- **T6 — docs/development.md PYTHONPATH note references monorepo layout.**
  It suggests `export PYTHONPATH=projects/fep_lean/src:.:infrastructure`,
  which applies only to the old monorepo checkout, not this standalone repo.
  Acceptance: update the snippet to the standalone form (`src` on
  `PYTHONPATH` or `uv run`) or scope the note explicitly to monorepo users.
