# fep_lean — canonical backlog

Only open work belongs here. Completed work is represented by passing evidence
in the repository history or an eventual changelog; do not add struck-through
rows or a completed-work archive to this table.

| ID | Outcome | Acceptance probe | Dependencies | Priority | Evidence source |
| --- | --- | --- | --- | --- | --- |
| FEP-FULL-002 | Exercise a real Hermes plus OpenGauss plus Lean full-mode smoke run and then the complete selected catalogue. | With credentials supplied out of band, `uv run fep-lean preflight` is `status: ok`; `uv run fep-lean run --topic fep-001` and `uv run fep-lean run` return `complete: true`, with matching report and verification manifest counts. | A permitted provider key, healthy `gauss doctor`, and writable `GAUSS_HOME`. | P0 | `ISA.md` ISA-05/06; `src/pipeline/core.py`; `src/gauss/runner.py` |
| FEP-PROV-003 | Confirm the report receipt independently on a real complete full-mode run. | After FEP-FULL-002, recompute every `summary.json.artifact_hashes` entry, verify relative paths stay inside the run directory, and confirm the verification/run manifests agree with `complete`, mode, selected count, and topic rows. | FEP-FULL-002 and the checked-in report schema. | P1 | `src/output/reporter.py`; `tests/test_reporter.py`; `ISA.md` ISA-07 |

| T1 | Make the configured mypy gate runnable: flat `src/` imports need `mypy_path = ["src"]` and `types-PyYAML`; otherwise remove the aspirational config. | `uv run mypy src/` exits 0 (or no `[tool.mypy]` section remains). | — | P2 | `pyproject.toml` `[tool.mypy]`; observed 30+ import-not-found errors 2026-08-18 |
| T2 | Run the opt-in full-catalogue Lean compile gate (`FEP_LEAN_CATALOGUE_COMPILE_TEST=1`) on a documented CI/maintainer cadence. | Gate executes and fails the build on any non-clean compile; locally verified 2026-08-18: 50/50 clean in 104 s. | Warm Lake workspace. | P2 | `tests/test_catalogue_sketches_compile.py` |
| T3 | Add a credential-gated end-to-end live test of `run_single_topic("fep-001", mode="full")`. | With `FEP_LEAN_LIVE_TESTS=1` and credentials, the test asserts a structured PipelineResult. | Provider key, healthy gauss. | P2 | `src/pipeline/orchestrator.py` |
| T4 | Pin the ruff rule set in `pyproject.toml` (`[tool.ruff.lint]` select: I001, UP037, UP035, F401, F811, E402, E741, SIM105, SIM201) so future ruff versions cannot reintroduce failures. | `uv run ruff check src/` passes on a fresh ruff install. | — | P3 | 2026-08-18 pass fixed 57 findings to 0 |
| T5 | Resolve the `hermes.fallback_count` manuscript token mismatch (code emits `hermes.model_fallback_count`). | `_inject_manuscript_vars.py --dry-run` leaves zero unmatched placeholders in shipped chapters. | — | P3 | `manuscript` chapters; `src/output/manuscript.py` |
| T6 | Update the monorepo-scoped `PYTHONPATH` snippet in `docs/development.md` for the standalone repo. | The documented export works from this checkout root. | — | P3 | `docs/development.md` |

## Closure rule

An item leaves this table only when its acceptance probe passes in the current
checkout, the evidence is retained in a test/report/documentation change where
appropriate, and the result is recorded in the repository's changelog or
release notes. Until then, the row remains open even if a partial local probe
looks promising.
