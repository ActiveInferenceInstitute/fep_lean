# fep_lean — canonical backlog

Only open work belongs here. Completed work is represented by passing evidence
in the repository history or an eventual changelog; do not add struck-through
rows or a completed-work archive to this table.

| ID | Outcome | Acceptance probe | Dependencies | Priority | Evidence source |
| --- | --- | --- | --- | --- | --- |
| FEP-FULL-002 | Exercise a real Hermes plus OpenGauss plus Lean full-mode smoke run and then the complete selected catalogue. | With credentials supplied out of band, `uv run fep-lean preflight` is `status: ok`; `uv run fep-lean run --topic fep-001` and `uv run fep-lean run` return `complete: true`, with matching report and verification manifest counts. | A permitted provider key, healthy `gauss doctor`, and writable `GAUSS_HOME`. | P0 | `ISA.md` ISA-05/06; `src/pipeline/core.py`; `src/gauss/runner.py` |
| FEP-PROV-003 | Confirm the report receipt independently on a real complete full-mode run. | After FEP-FULL-002, recompute every `summary.json.artifact_hashes` entry, verify relative paths stay inside the run directory, and confirm the verification/run manifests agree with `complete`, mode, selected count, and topic rows. | FEP-FULL-002 and the checked-in report schema. | P1 | `src/output/reporter.py`; `tests/test_reporter.py`; `ISA.md` ISA-07 |

| T1 | CLOSED 2026-08-18: `mypy_path = ["src"]` + `explicit_package_bases` + `types-PyYAML` configured; `uv run mypy src` exits 0 (23 files, strict). | `uv run mypy src` → "Success: no issues found in 23 source files". | — | P2 | `pyproject.toml`; CI `python` job runs it per push |
| T2 | CLOSED 2026-08-18: `FEP_LEAN_CATALOGUE_COMPILE_TEST=1` promoted into the CI `lean` job after `lake build FepSketches`. | CI `lean` job executes the 50-topic gate and fails on any non-clean compile; locally verified 50/50 clean in 104 s. | Warm Lake workspace (CI builds it). | P2 | `.github/workflows/ci.yml`; `tests/test_catalogue_sketches_compile.py` |
| T3 | CLOSED 2026-08-18: `tests/test_live_end_to_end.py` added — opt-in `FEP_LEAN_LIVE_TESTS=1` + API key + built workspace; runs `run_single_topic("fep-001", mode="full")` and asserts a structured PipelineResult. | Test runs (not skips) under the gate; asserts stage trail, session_id, hermes_model, lean_compiles, duration. | Provider key, healthy gauss, built workspace. | P2 | `tests/test_live_end_to_end.py` |
| T4 | CLOSED 2026-08-18: `[tool.ruff.lint] extend-select` pinned to F, I, UP, SIM (every rule fixed in the 2026-08-18 pass is enforced); `uv run ruff check src tests scripts docs` passes clean. | `uv run ruff check src tests scripts docs` → "All checks passed!" under the pinned set. | — | P3 | `pyproject.toml`; CI runs it per push |
| T5 | CLOSED 2026-08-18: `fallback_count` emitted as an alias of `model_fallback_count` in `_hermes_block_from_summary` (both default and computed paths). | `build_manuscript_vars(...)["hermes"]["fallback_count"]` resolves; injector substitutes `{{hermes.fallback_count}}`. | — | P3 | `src/output/manuscript.py` |
| T6 | CLOSED 2026-08-18: `docs/development.md` PYTHONPATH snippet now shows the standalone form (`export PYTHONPATH=src`) with the monorepo variant kept as a scoped note. | The documented export works from this checkout root. | — | P3 | `docs/development.md` |

## Closure rule

An item leaves this table only when its acceptance probe passes in the current
checkout, the evidence is retained in a test/report/documentation change where
appropriate, and the result is recorded in the repository's changelog or
release notes. Until then, the row remains open even if a partial local probe
looks promising.
