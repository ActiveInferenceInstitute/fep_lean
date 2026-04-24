# fep_lean/tests/

Pytest suite for `src/`. Tests call the `gauss`, `lake` and `lean` binaries (no mocks).

## Test census

**Canonical scale**: `uv run pytest tests/ --collect-only -q` → **347** tests in **29** modules (`test_*.py`). Per-file counts match `pytest --collect-only` per module (regenerate with `pytest ... --collect-only` if drift appears).

| File | Tests | Description |
|------|------:|-------------|
| `test_catalogue_sketches_compile.py` | 1 | Opt-in full-catalogue `verify_batch` (`FEP_LEAN_CATALOGUE_COMPILE_TEST=1`) |
| `test_catalogue_sketches_ssot.py` | 2 | `topics.yaml` `lean_sketch` matches `catalogue_sketches.SKETCHES` |
| `test_edge_cases.py` | 19 | Input validation, wrap-code, empty catalogues |
| `test_environment_checks.py` | 1 | 13-check validation against the project tree |
| `test_environment_sad_paths.py` | 22 | Sad path coverage for `verification.environment` |
| `test_fep_all_lean_ssot.py` | 3 | `fep_all.lean` namespaces vs `topics.yaml`; no stray `sorry` |
| `test_fep_topics.py` | 6 | Catalogue load/summary invariants |
| `test_figure_generation.py` | 10 | Figure generation (process pool + serial `FEP_LEAN_FIGURES_MP=0`) |
| `test_gauss_cli.py` | 4 | `gauss doctor` happy path |
| `test_gauss_cli_sad_paths.py` | 7 | Missing/broken `gauss` binary, fallback path |
| `test_gauss_runner.py` | 11 | Per-topic session orchestration (1 API-key test) |
| `test_gauss_runner_branches.py` | 9 | FixedHermes / BoomClient / review-workflow controlled branches |
| `test_gauss_runner_prefetch.py` | 5 | `FEP_LEAN_PREFETCH` batch path vs serial; no API key |
| `test_hermes_comprehensive.py` | 41 | Dotenv, key affinity, `_call_api` (loopback servers), `_parse_response` (1 API-key test) |
| `test_hermes_error_paths.py` | 9 | `preflight()` 200/403 + `fallback_models` chain via `pytest-httpserver` (no mocks) |
| `test_hermes_explainer.py` | 41 | Config, cache TTL, cache_hit field, preamble, extract, system prompt, restore_lean_structure, _strip_extra_theorems (1 API-key test) |
| `test_lean_verifier.py` | 24 | VerifyResult, wrap-code, verify_sketch, verify_batch |
| `test_lean_verifier_sad_paths.py` | 15 | OSError, timeout, missing lake/lean paths |
| `test_maint_fep_all_generator.py` | 7 | `scripts/_maint_build_fep_all_lean.py` generator invariants (SSOT for materialized `fep_all.lean`) |
| `test_manuscript_artifacts.py` | 21 | `manuscript_vars.yaml` + full topic catalogue markdown |
| `test_open_gauss_client.py` | 15 | SQLite session store CRUD, hermes_cache round-trip, prune, export, stats |
| `test_orchestrator.py` | 6 | End-to-end pipeline on the project tree (1 API-key test) |
| `test_orchestrator_exceptions.py` | 1 | PermissionError from Reporter |
| `test_orchestrator_sad_paths.py` | 5 | Unknown topics, corrupt YAML, broken env |
| `test_pipeline.py` | 26 | FEPPipeline four recorded stages + orchestrator + workflow kwarg (1 API-key test) |
| `test_pipeline_exceptions.py` | 3 | Missing catalogue, validation warnings |
| `test_preflight.py` | 8 | `run_preflight` with present/missing binaries, cli, sad paths |
| `test_reporter.py` | 18 | Markdown + JSON report generation + `verification_manifest.json` |
| `test_subpackage_imports.py` | 7 | All subpackages importable standalone |

**API-key tests**: 4 tests skip when no API key is present; they run automatically when
`OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is set. Set `FEP_LEAN_LIVE_TESTS=0` to
suppress them even when keys exist (e.g. cost-controlled CI or core-only pipeline runs —
the pipeline scripts set this automatically when `--core-only`/`--no-llm` is active).
Collected total matches **`pytest --collect-only`** (currently **347**).

Coverage for `output/figures.py` uses worker processes: `[tool.coverage.run] concurrency = ["multiprocessing"]` in `pyproject.toml` so `ProcessPoolExecutor` chart workers are included in the line report.

## Parallel test runs (`pytest-xdist`)

`pytest-xdist` is an optional **dev** dependency. **Default / CI:** run without `-n` so the shared `lean/.lake` build tree is not stressed by concurrent `lake env lean` from different workers. Files that touch the real Lean workspace heavily are marked `@pytest.mark.serial_lean` (`test_lean_verifier.py`, `test_lean_verifier_sad_paths.py`, `test_catalogue_sketches_compile.py`) for documentation; **safe** parallel invocation still requires excluding or isolating those tests (e.g. run them in a separate job, or use `-n 0`).

### Full-catalogue compile gate (opt-in pytest)

- **`test_catalogue_sketches_compile.py`**: Skipped unless **`FEP_LEAN_CATALOGUE_COMPILE_TEST=1`**. Runs `LeanVerifier.verify_batch` on all 50 `topics.yaml` rows after `check_mathlib_built()` passes (partial Mathlib caches fail with a clear skip/fail — leaf module probes were tightened so root-only `Mathlib.olean` is insufficient).
- **CLI parity**: **`uv run python scripts/03_lean_verify_only.py`** is the default full sweep for CI and local runs; exit **1** if any topic fails.

Per-topic results also appear when **`FEP_LEAN_GAUSS_WORKFLOWS=1`** (`GaussRunner` + `LeanVerifier`). **`Reporter`** writes **`verification_manifest.json`** under `output/reports/run_*/` for manuscript **`{{compile_rate_*}}`** injection. `test_lean_verifier.py` exercises representative sketches with real `lake env lean` calls.

Example (faster feedback on pure-Python tests only — adjust ignores as needed):

```bash
uv run pytest tests/ -q --timeout=900 --cov=src --cov-fail-under=89
# Optional, not default:
# uv run pytest tests/ -n auto --dist loadfile -q  # may still race .lake if lean tests run on multiple workers
```

## API-Key Tests (4 tests, `@pytest.mark.skipif`)

These tests skip when no API key is detected. They run automatically on machines with
`OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` set, unless `FEP_LEAN_LIVE_TESTS=0`
explicitly suppresses them:

1. `test_run_topic_with_real_hermes` — end-to-end GaussRunner: OpenRouter call → SQLite → LeanVerifier
2. `test_hermes_explain_topic_real_api_call` — HTTP round-trip through `_call_api` → `_parse_response` → `HermesResult` (wall-clock budget: **720 s** — covers reasoning-model timeout 300 s + 2 retry/fallback cycles)
3. `test_run_single_topic_ok` — full orchestrator with live Hermes + Reporter output files
4. `test_pipeline_full_hermes_single_topic` — FEPPipeline with live Gauss Sessions stage

Note: `test_call_api_http_error` and `test_call_api_url_error` are **not** API-key tests —
they use loopback `HTTPServer` (404 response) and a refused-port socket; both always run.

### Coverage note

The 4 live API tests contribute ~3% line coverage in `src/llm/hermes.py` and related modules. Skipping them (no key, or `FEP_LEAN_LIVE_TESTS=0`) drops total coverage to ~88%, below the 90% gate. The pipeline therefore requires an API key to be present so these tests run and coverage is met.

## Requirements

Install:

- **Lean**: [elan](https://github.com/leanprover/elan), then pin `lean/lean-toolchain` (relative to the project root) and run `lake build` in `lean/` once.
- **Open Gauss**: clone [math-inc/OpenGauss](https://github.com/math-inc/OpenGauss) and run `./scripts/install.sh --plain --noninteractive` (see upstream docs).

`conftest.py` sets `FEP_LEAN_REQUIRE_GAUSS=1` when `gauss`, `lake`, and `lean` all resolve; otherwise it sets `FEP_LEAN_TOOLS_MISSING` and tests that need tools skip or degrade gracefully.

`FEP_LEAN_GAUSS_WORKFLOWS=0` by default so most tests avoid unsolicited LLM traffic; workflow integration tests enable the flag where needed.

`monkeypatch` (and `setattr`) is used for env-var parsing (`workflows_enabled`), `_call_api` overrides, `time.sleep`, `sys.argv`, `preflight.project_root`, and PATH isolation (e.g. hiding `gauss`) — never for stubbing core subprocess or CLI behavior.

## Test isolation: `FEP_LEAN_OUTPUT_ROOT`

Tests that drive the orchestrator (`run_pipeline`, `run_single_topic`) write Reporter run-dirs and the `output/.cache/` test-count cache.  To keep these out of the canonical `output/reports/run_*/` tree on the developer's checkout, those test modules must redirect the output root.  Two equivalent idioms are supported:

- **Env var (preferred for autouse fixtures)** — set `FEP_LEAN_OUTPUT_ROOT` to a per-test `tmp_path`.  `FEPPipeline`, `Reporter`, and `run_pipeline()` honour it automatically.  See `tests/test_orchestrator.py` and `tests/test_orchestrator_sad_paths.py` for the autouse fixtures.
- **Keyword argument** — pass `output_root=tmp_path` to `FEPPipeline(...)`, `Reporter(...)`, or `run_pipeline(..., output_root=tmp_path)`.

Without this redirection a test run leaves a trail of small `run_YYYYMMDD_HHMMSS` directories in `output/reports/` and clobbers the `latest` symlink, hiding the most recent real run.  The autouse fixtures already guarantee isolation for the orchestrator tests; new tests that exercise the Reporter must follow the same convention.

## Running

From the project root:

```bash
uv run pytest tests/ --timeout=900 --cov=src --cov-report=term-missing --cov-fail-under=89
```

To suppress API-key tests (e.g. cost-controlled CI with keys present):

```bash
FEP_LEAN_LIVE_TESTS=0 uv run pytest tests/ --timeout=900 --cov=src --cov-fail-under=89
```

## Coverage

Target: 89% line coverage (`pyproject.toml: fail_under = 89`). Current exceeds target.
Gap: paths requiring live Lean toolchain or network (Hermes API) are covered when `FEP_LEAN_GAUSS_WORKFLOWS=1` and API keys present.
