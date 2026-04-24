# Testing — fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Philosophy: Zero-Mock Policy

All tests in `fep_lean` exercise **concrete components** — **no `MagicMock`, no `mocker.patch`**, no `unittest.mock`, no hand-rolled fakes, no HTTP-substituting adapters. The zero-mock policy is **absolute** for `fep_lean` and it is checked by both `infrastructure/validation/no_mock_enforcer.py` and the template-wide constitutional test gates. This means:

- Tests create SQLite databases (`tmp_path`-scoped `GAUSS_HOME` via `OpenGaussClient` in `gauss/client.py`)
- Tests load `config/topics.yaml` (50 topics)
- Tests call `HermesExplainer.explain_topic()` — returns `HermesResult(success=False)` and **no HTTP call** when `api_key=''`
- Tests use `LeanVerifier` — `pytest.skip` when `lake` is absent or sandbox-restricted
- Tests use `GaussRunner` session creation and SQLite writes where the suite requires `gauss` / `lake` / `lean` on `PATH`

**Validation of the Zero-Mock Strategy**: If `lake env lean` had been mocked for speed, the macOS ELAN proxy deadlock (caused by concurrent `ThreadPoolExecutor` subshell spawning) would never have surfaced until production. By forcing tests to invoke the `lean` binary, the architecture correctly identified that parallelizing formal verifications inherently breaks the sandbox structure, leading to the necessary fix of linear processing (`max_workers=1`).

This strictly keeps test behavior aligned with production.

---

## Test Suite Overview

**347 items collected** (April 2026; refresh with `uv run pytest --collect-only -q` from `projects/fep_lean/`).

### Documentation integrity gates

From `docs/`, the same pass documented in [AGENTS.md](AGENTS.md) applies before large doc edits: `check_links.py --strict --include-root`, `md_hygiene.py --strict`, `pin_audit.py`, and `xref_audit.py`. Failures surface stale anchors, formatting drift, wrong toolchain/model literals in static docs, or broken manuscript equation cross-references.

The full suite runs under a **900-second per-test timeout** (`pytest-timeout` default set in project `pyproject.toml`) — Lean compilation steps honour this ceiling when `lake` is available, and skip cleanly when it is not. Modules under `tests/` include:

| Module | Focus |
|--------|--------|
| `test_fep_topics.py` | Catalogue schema, 50-topic roster, area counts |
| `test_catalogue_sketches_ssot.py` | Enforces SSOT: every `topics.yaml` `lean_sketch` equals `scripts/catalogue_sketches.py::SKETCHES[id]` (fast drift check, no `lake` needed) |
| (per-row) `scripts/03_lean_verify_only.py` | Verifies all 50 YAML sketches via `lake env lean` when `lake` + Mathlib `.olean` cache are present; logs per-topic outcomes to stdout. Full JSON aggregates for manuscripts: `output/reports/run_*/verification_manifest.json` from `Reporter` after a pipeline run with workflows enabled |
| `test_environment_checks.py` | Full `run_validation_checks` |
| `test_environment_sad_paths.py` | Validation edge cases |
| `test_open_gauss_client.py` | SQLite sessions, artifacts, JSONL |
| `test_lean_verifier.py`, `test_lean_verifier_sad_paths.py` | `lake env lean`, skip paths |
| `test_hermes_explainer.py` | Hermes config, no-key fast return, optional live API |
| `test_hermes_error_paths.py` | `preflight()` 200/403 + `fallback_models` chain via `pytest-httpserver` |
| `test_gauss_runner.py`, `test_gauss_runner_branches.py`, `test_gauss_runner_prefetch.py` | Per-topic orchestration; optional Hermes/Lean prefetch |
| `test_gauss_cli.py`, `test_gauss_cli_sad_paths.py` | `gauss doctor` integration |
| `test_pipeline.py`, `test_pipeline_exceptions.py` | `FEPPipeline` stages |
| `test_orchestrator.py`, `test_orchestrator_sad_paths.py`, `test_orchestrator_exceptions.py` | `run_pipeline` / `run_single_topic` |
| `test_reporter.py` | Report bundle files |
| `test_manuscript_artifacts.py`, `test_figure_generation.py` | Vars + figures (parallel + serial figure paths) |
| `test_subpackage_imports.py` | Package layout |

`monkeypatch` appears only for env-var / path wiring (for example `workflows_enabled`, `PROJECT_DIR`), not to stub subprocess or HTTP.

**Monorepo infra:** [`tests/infra_tests/core/test_analysis_timeout.py`](../../../tests/infra_tests/core/test_analysis_timeout.py) covers `parse_analysis_script_timeout_sec` (default **7200** s, `unlimited`, invalid fallbacks).

---

## Running Tests

### Quick reference — run modes

| Mode | Command | Live API? | Coverage |
|------|---------|-----------|----------|
| **Full pipeline** (recommended) | `./run.sh --pipeline` | **Yes**, if key set | ≥90% ✓ |
| All tests, key present | `uv run pytest tests/ -v` | **Yes** | ≥90% ✓ |
| All tests, suppress live | `FEP_LEAN_LIVE_TESTS=0 uv run pytest tests/ -v` | No | ~88% ✗ |
| All tests, force live | `FEP_LEAN_LIVE_TESTS=1 uv run pytest tests/ -v` | Yes (errors without key) | ≥90% ✓ |
| Single live API test | `FEP_LEAN_LIVE_TESTS=1 uv run pytest tests/test_hermes_explainer.py::test_hermes_explain_topic_real_api_call -v -s` | Yes | — |

### Standard test run

```bash
# from project root (projects/fep_lean/)
uv run pytest tests/ -q --timeout=900 --cov=src --cov-report=term-missing --cov-fail-under=89
```

From the monorepo root, either `cd` to the project directory first or use `uv run --directory <path-to-project> pytest ...` with the same flags.

Single file:

```bash
uv run pytest tests/test_open_gauss_client.py -v
```

With an OpenRouter key (live Hermes tests enabled automatically):

```bash
OPENROUTER_API_KEY=sk-or-... uv run pytest tests/ -v
```

Suppress live API tests even when a key is present (cost-controlled local run):

```bash
FEP_LEAN_LIVE_TESTS=0 uv run pytest tests/ -v
```

### Coverage dependency on live tests

The 4 API-key tests contribute ~3% line coverage in `src/llm/hermes.py` and related
modules. Skipping them (no key or `FEP_LEAN_LIVE_TESTS=0`) drops total coverage to
~88%, below the 90% pipeline gate. The pipeline therefore requires `OPENROUTER_API_KEY`
or `ANTHROPIC_API_KEY` to be set so these tests run and coverage is met.

### Timing budget for live API tests

The 4 API-key tests use a **720-second (12-minute)** per-test wall-clock budget. This is
conservative by design: a reasoning model (DeepSeek-R1, o1) hitting its 300 s timeout
followed by two fallback models with exponential-backoff retries can take up to ~600 s.
The 720 s ceiling leaves headroom while still catching genuine hangs. The per-test
`pytest-timeout` ceiling in `pyproject.toml` is 900 s (separate mechanism).

---

## `tests/conftest.py`

- Inserts the project `src/` directory on `sys.path` and sets `MPLBACKEND=Agg`.
- Records missing `gauss` / `lake` / `lean` in `FEP_LEAN_TOOLS_MISSING` when absent (warn-only; does not abort collection).
- Sets `FEP_LEAN_REQUIRE_GAUSS=1` when all three tools resolve.
- Defaults `FEP_LEAN_GAUSS_WORKFLOWS=0` so most tests stay in catalogue-first mode unless a test enables workflows.

---

## Coverage

Combined line+branch gate for `src/`: **≥ 89% line coverage against the `--cov-fail-under=89` gate** (see project `pyproject.toml` and CI job **fep_lean**). The April 2026 suite reports ≥89% on every CI matrix leg.

Measure coverage with the working directory set to **the project root** and **`--cov=src`**. Invoking pytest from the repository root via a long path to `tests/` with a mismatched `--cov=` prefix can under-report versus the project-local run, depending on `pytest-cov` and branch tracking.

**Multiprocessing:** `output/figures.py` uses `ProcessPoolExecutor` (spawn) for chart workers. `pyproject.toml` sets `[tool.coverage.run] concurrency = ["multiprocessing"]` so those subprocesses count toward the line report.

**Optional `pytest-xdist`:** listed under `[project.optional-dependencies] dev`; default CI and local runs stay single-process because the shared `lean/.lake` tree must not be stressed by concurrent `lake env lean`. See [`tests/AGENTS.md`](../tests/AGENTS.md).

---

## What Is NOT Automatically Tested

- Live Hermes calls without `OPENROUTER_API_KEY`
- Full 50-topic Gauss batches in every PR (CI uses real `gauss` + `lake` but runtime is bounded by job timeout)
- Out-of-order pipeline stages (the four recorded stages stay sequential; internal overlap is limited to manuscript vs figures and optional Hermes prefetch — see [`pipeline.md`](pipeline.md))

## Lean-only catalogue check

`scripts/03_lean_verify_only.py` runs `lake env lean` on every sketch **after** preflight checks for `Mathlib.olean`. It exits **0 with a warning** if Mathlib is not yet built (graceful degradation so the pipeline continues), and exits **1** only if a topic that was compiled actually fails. To enable full verification locally: `cd lean && lake exe cache get && lake build`.

---

## Navigation

- [← docs/README.md](README.md)
- [Development →](development.md)
- [Architecture →](architecture.md)
