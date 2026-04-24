# AGENTS.md — fep_lean

## Purpose

Template-integrated project for a **catalogue of 50** FEP / Active Inference / Bayesian Mechanics / Information Geometry / Thermodynamics topics ([`config/topics.yaml`](config/topics.yaml)), each with natural-language statements and Lean 4 sketches. Regenerate the canonical YAML with [`scripts/_maint_build_topics_catalogue.py`](scripts/_maint_build_topics_catalogue.py) (maintenance only; underscore prefix excludes it from Stage 02 auto-discovery).

Export **`FEP_LEAN_GAUSS_WORKFLOWS=1`** (or **`FEP_LEAN_LIVE_TESTS=1`** when the workflows var is unset) before analysis when you want live Hermes + Lean; the analysis entry script defaults workflows **off** so the core pipeline finishes without API calls.

When workflows are enabled, `FEPPipeline` ([`pipeline/core.py`](src/pipeline/core.py)) records four stages: **Load Catalogue**, **Environment Validation**, **Gauss Sessions** (Hermes + per-topic `lake env lean` + SQLite via [`gauss/runner.py`](src/gauss/runner.py)), **Manuscript Artifacts**. Reporting ([`output/reporter.py`](src/output/reporter.py)) runs after `run()` in the orchestrator, not as a fifth pipeline stage.

Inside **Gauss Sessions**: OpenRouter Hermes ([`llm/hermes.py`](src/llm/hermes.py)), `lake env lean` ([`verification/lean_verifier.py`](src/verification/lean_verifier.py)), and [`OpenGaussClient`](src/gauss/client.py) persistence.

**Open Gauss** here means the **[math-inc/OpenGauss](https://github.com/math-inc/OpenGauss)** `gauss` CLI (Lean tooling), **not** Huawei OpenGauss DBMS.

---

## Disposable artifacts (cold start)

For a clean **next** `./run.sh` / full analysis: delete **`output/`**, **`manuscript/manuscript_vars.yaml`**, **`manuscript/09z_unified_formalism_catalogue.md`**, **`.pytest_cache/`** (all in `.gitignore`). Remove stale `09z_appendix_b_lean_catalogue.md` / `09zc_appendix_c_lean_equations.md` if left from an older run. Optional: **`{GAUSS_HOME}/fep_lean_state.db`** (Hermes + sessions), **`lean/.lake/`** (long Mathlib refetch — only if cache is corrupt). Do **not** delete **`config/topics.yaml`**, **`scripts/catalogue_sketches.py`**, **`scripts/topic_latex_equations_data.py`**, or **`lean/lean-toolchain`**. Full table and commands: [docs/cold-start-and-cleanup.md](docs/cold-start-and-cleanup.md).

---

## Layout

| Path | Role |
| ---- | ---- |
| [`config/topics.yaml`](config/topics.yaml) | 50-topic catalogue (`TopicEntry` schema) |
| [`config/settings.yaml`](config/settings.yaml) | Project metadata, GAUSS_HOME, Hermes/OpenRouter settings |
| [`catalogue/topics.py`](src/catalogue/topics.py) | `TopicEntry`, `FEPTopicCatalogue` |
| [`verification/environment.py`](src/verification/environment.py) | `run_validation_checks(project_root)` — 13 checks |
| [`gauss/cli.py`](src/gauss/cli.py) | `check_gauss_cli`, `workflows_enabled` |
| [`gauss/client.py`](src/gauss/client.py) | `OpenGaussClient` — SQLite session store + artifact export |
| [`verification/lean_verifier.py`](src/verification/lean_verifier.py) | `LeanVerifier` — `lake env lean` compilation checker |
| [`verification/preflight.py`](src/verification/preflight.py) | `run_preflight`, CLI `fep-lean-preflight` — gauss / lean / lake / Mathlib probe |
| [`llm/hermes.py`](src/llm/hermes.py) | `HermesExplainer` — OpenRouter HTTP client + FEP system prompt. `HermesConfig.fallback_models` is a first-class user-supplied chain (overrides `_FREE_MODEL_CHAIN`); `HermesExplainer.preflight()` probes the endpoint with `max_tokens=1` before Stage 4 to fail fast on 4xx credential errors |
| [`gauss/runner.py`](src/gauss/runner.py) | `GaussRunner` — per-topic orchestration (Hermes + Lean + SQLite) |
| [`pipeline/core.py`](src/pipeline/core.py) | `FEPPipeline` — staged DAG |
| [`output/reporter.py`](src/output/reporter.py) | `Reporter` — Markdown + JSON report from `PipelineResult` |
| [`output/figures.py`](src/output/figures.py) | Catalogue figures → `output/figures/` |
| [`output/manuscript.py`](src/output/manuscript.py) | `manuscript_vars.yaml` from catalogue |
| [`pipeline/orchestrator.py`](src/pipeline/orchestrator.py) | `run_pipeline`, `run_single_topic` |
| [`lean/`](lean/) | Minimal Lake workspace (`lake build` when workflows enabled); committed sketches under `lean/FepSketches/` are **`Basic.lean`**, **`fep_all.lean`**, and ephemeral **`_verify_*`** verifier files — not a parallel catalogue of 50 long-lived topic `.lean` files (those live in YAML/`catalogue_sketches.py` SSOT above) |
| [`scripts/01_fep_catalogue_and_figures.py`](scripts/01_fep_catalogue_and_figures.py) | Analysis-stage entry point |
| [`tests/`](tests/) | **347** pytest items in **29** `test_*.py` modules — see [`tests/AGENTS.md`](tests/AGENTS.md) |

---

## Validation checks (`run_validation_checks`) — 13 checks

1. `math_inc_gauss_cli` — `gauss doctor`; fails validation when `FEP_LEAN_REQUIRE_GAUSS=1`
2. `lean_cli` — `lean --version` if `lean` on PATH
3. `open_gauss_config_dir` — `GAUSS_HOME` or `~/.gauss` writable
4. `lean_workspace` — `lean/lakefile.lean` (or `.toml`) and `lean/FepSketches/`
5. `mathlib_built` — Mathlib `.olean` build probe for the pinned workspace
6. `topics_yaml`
7. `project_layout` — `manuscript/`, `config/`, `src/`, `lean/`
8. `python_scientific_stack`
9. `output_writable`
10. `manuscript_config`
11. `scripts_tests_layout`
12. `catalogue_loader`
13. `references_bib` (optional)

---

## Environment Variables

| Variable | Default | Effect |
| -------- | ------- | ------ |
| `FEP_LEAN_REQUIRE_GAUSS` | unset | If truthy, missing or failing `gauss doctor` fails validation |
| `FEP_LEAN_GAUSS_WORKFLOWS` | unset | If truthy, pipeline runs Hermes + `GaussRunner` + Lean verify |
| `FEP_LEAN_LIVE_TESTS` | auto | **Test-suite gate** — controls whether live API tests run during `pytest`. Auto-enabled when `OPENROUTER_API_KEY`/`ANTHROPIC_API_KEY` is present; set `=0` to suppress even with a key (cost control). The pipeline scripts (`execute_pipeline.py`, `execute_multi_project.py`) automatically set `=0` when `--core-only`/`--no-llm` is in effect. Set `=1` to force-enable regardless of key presence. |
| `FEP_LEAN_MAX_TOPICS` | unset | Optional positive int: cap catalogue batch size after filters |
| `ANALYSIS_SCRIPT_TIMEOUT_SEC` | 7200 | Repo Stage 02 per-script timeout (`0`/`unlimited` = none) |
| `HERMES_429_MAX_RETRIES` | 2 | Retries after HTTP **429** on the **current** model (exponential backoff), before advancing to the next model in the chain |
| `HERMES_NETWORK_MAX_RETRIES` | 2 | Retries after **transient** transport errors (`IncompleteRead`, `URLError`, …) on the **current** model |
| `HERMES_MAX_MODEL_ATTEMPTS` | unset | Max models to try per topic from the OpenRouter fallback chain |
| `GAUSS_HOME` | `~/.gauss` | Root for SQLite DB, artifacts, logs |
| `OPENROUTER_API_KEY` | unset | Required for live Hermes LLM explanations via OpenRouter |
| `ANTHROPIC_API_KEY` | unset | First-class alternate: use with `HERMES_API_BASE=https://api.anthropic.com/v1` to bypass OpenRouter entirely (see [`docs/troubleshooting.md § Hermes HTTP 403`](docs/troubleshooting.md#hermes-http-403)) |
| `HERMES_MODEL` | from settings | Override Hermes primary model |
| `HERMES_API_BASE` | OpenRouter | Override API base URL; set to `https://api.anthropic.com/v1` for Anthropic-direct |
| `FEP_LEAN_VERIFY_TIMEOUT` | 300 | `lake env lean` timeout in seconds |
| `FEP_LEAN_LAKE_EXE` | auto | Absolute path to `lake` binary; bypasses elan proxy resolution entirely |
| `FEP_LEAN_LEAN_EXE` | auto | Absolute path to `lean` binary; bypasses elan proxy resolution entirely |
| `FEP_LEAN_PREFETCH` | unset | If `1`/`true`/`yes`/`on`, `GaussRunner.run_topics_batch` overlaps Hermes for topic *N+1* with Lean verify on topic *N* (`verify` workflow, ≥2 topics). SQLite and Lean stay single-threaded. |
| `FEP_LEAN_SKIP_FALLBACKS` | unset | If truthy, `check_gauss_cli` skips all alternative binary discovery paths (for sandboxed / CI environments) |
| `FEP_LEAN_FIGURES_MP` | parallel | If `0`/`false`/`no`/`off`, `write_all_catalogue_figures` skips `ProcessPoolExecutor` and renders PNGs serially in-process |
| `PROJECT_DIR` | auto | Set by `scripts/02_run_analysis.py` to project root |

### Run modes at a glance

| Mode | Command | Live API calls? | `FEP_LEAN_LIVE_TESTS` |
|------|---------|-----------------|----------------------|
| **Full pipeline** | `./run.sh --pipeline` | **Yes**, if key set | auto (key controls it) |
| **Direct pytest, key present** | `uv run pytest tests/ -v` | **Yes** | auto (key controls it) |
| **Direct pytest, suppress live** | `FEP_LEAN_LIVE_TESTS=0 uv run pytest tests/ -v` | No | forced off |
| **Direct pytest, force live** | `FEP_LEAN_LIVE_TESTS=1 uv run pytest tests/ -v` | Yes | forced on |
| **Single live test** | `FEP_LEAN_LIVE_TESTS=1 uv run pytest tests/test_hermes_explainer.py::test_hermes_explain_topic_real_api_call -v -s` | Yes | forced on |

> **Note on coverage**: The 4 live API tests contribute ~3% of line coverage in `src/llm/hermes.py` and related modules. Coverage falls to ~88% when live tests are skipped, below the 90% gate. Always run with a key present (or ensure `FEP_LEAN_LIVE_TESTS` is unset) for accurate coverage measurement.

---

## Pipeline stages (`FEPPipeline.run`)

`FEPPipeline.run()` appends **four** `StepResult` rows to `PipelineResult.stages`:

| # | Stage name | Role |
|---|------------|------|
| 1 | Load Catalogue | `FEPTopicCatalogue.from_yaml`, optional topic/area filter |
| 2 | Environment Validation | `run_validation_checks` (13 checks) |
| 3 | Gauss Sessions | One `HermesExplainer.preflight()` probe (fails fast on 4xx), then `GaussRunner.run_topics_batch` per topic — Hermes (`llm/hermes.py`) + `LeanVerifier.verify_sketch` (`lake env lean`) + SQLite (`gauss/client.py`). Recorded as `skipped` when `FEP_LEAN_GAUSS_WORKFLOWS` is falsy. |
| 4 | Manuscript Artifacts | `write_manuscript_vars` + `write_unified_formalism_appendix_markdown` + `write_all_catalogue_figures` (figures: optional `ProcessPoolExecutor`, see `FEP_LEAN_FIGURES_MP`) |

Run reporting (`Reporter.generate` → `output/reports/run_YYYYMMDD_HHMMSS/`) is invoked from [`pipeline/orchestrator.run_pipeline`](src/pipeline/orchestrator.py) **after** `FEPPipeline.run()` returns and is **not** a fifth entry in `PipelineResult.stages`.

Hermes and per-topic Gauss **markdown** under those report dirs is built from the in-memory pipeline payload (`TopicRunResult.as_dict()` on each row of `PipelineResult.topic_results`), not by re-querying SQLite. When extending the runner or serializer, keep that dict aligned with what [`output/reporter.py`](src/output/reporter.py) reads — notably Hermes-facing keys such as `tokens_used`, `explanation`, `refined_lean_sketch`, `hermes_model`, `cache_hit`, and `hermes_lean_compiles` — or aggregate and per-topic sections will look empty.

---

## Topic catalogue

- **50 topics** in `config/topics.yaml` (`fep-001`…`fep-050`)
- **5 areas**: FEP (14), ActiveInference (11), BayesianMechanics (10), InfoGeometry (8), Thermodynamics (7)
- **50 `mathlib_status: real`** rows (compiling Lean sketches from `scripts/catalogue_sketches.py`); eight deep-dive manuscript appendices highlight representative ids
- Each topic: `id`, `title`, `area`, `mathlib`, `mathlib_status`, `nl`, `lean_sketch`
- **Lean SSOT + Cursor lean4 commands:** [docs/lean4.md](docs/lean4.md) (`#catalogue-source-of-truth`, `#cursor-lean4-commands`); CI enforces `topics.yaml` `lean_sketch` == `scripts/catalogue_sketches.SKETCHES` via [`tests/test_catalogue_sketches_ssot.py`](tests/test_catalogue_sketches_ssot.py)

---

## GaussRunner workflow stages

`GaussRunner.run_topic(topic, workflow=...)` and `run_topics_batch(..., workflow=...)` support four workflow stages:

| Stage | Hermes directive | When to use |
|-------|-----------------|-------------|
| `"verify"` (default) | Refine the existing sketch; report compile status | Standard pipeline pass |
| `"draft"` | Produce a new typed skeleton using `sorry` freely | Starting a topic from NL only |
| `"prove"` | Attempt a full proof; minimise `sorry` usage | Upgrading `partial` → `real` |
| `"review"` | Verify then request post-compile quality commentary | Final review before merge |

Stages other than `"verify"` require `FEP_LEAN_GAUSS_WORKFLOWS=1`; otherwise they silently degrade to `"verify"`.

The `review` stage runs two Hermes calls: the standard verify call followed by a second call with a review preamble + compile context.  Both results are cached (see below).

Each `TopicRunResult` carries `workflow: str` (effective stage) and `stage_results: list[dict]` (supplementary stage data, e.g. review commentary).

---

## Hermes result caching

Hermes API responses are cached in `{GAUSS_HOME}/fep_lean_state.db` table `hermes_cache` keyed by `SHA-256(topic_id:lean_sketch:model:stage)`.

- **Cache TTL**: 24 hours by default; configurable via `settings.yaml` `hermes.cache_ttl_hours` or `HermesConfig.cache_ttl_hours`
- **Cache hit**: `HermesResult.cache_hit = True`; response returned immediately without API call
- **Cache pruning**: Entries older than TTL are removed on each `GaussRunner` instantiation
- **Cache invalidation**: Changing the `lean_sketch`, primary model, or workflow stage produces a new cache key

---

## Sorry gate (CI)

The `fep-lean` CI job includes a step that rejects any non-comment `sorry` introduced into `lean/FepSketches/fep_all.lean` or `lean/FepSketches/Basic.lean`:

```bash
SORRY_LINES=$(grep -n 'sorry' fep_all.lean Basic.lean | grep -Ev ':[[:space:]]*--' || true)
[ -z "$SORRY_LINES" ] || exit 1
```

The gate runs before the 25-minute Gauss CLI install so failures are fast.  All 50 current catalogue entries compile cleanly with zero `sorry`.

---

## SQLite persistence (`OpenGaussClient`)

All session state is persisted in `{GAUSS_HOME}/fep_lean_state.db`:

Five SQL tables:

- **sessions**: `session_id`, `topic_id`, `area`, `lean_sketch`, `refined_sketch`, `status`, `hermes_success`, `lean_compiles`, `source`, `created_at`, `closed_at`, `duration_s`
- **turns**: per-session conversation turns (role, content, tokens)
- **artifacts**: JSON artifact manifests (path + sha256)
- **logs**: structured operation log events
- **hermes_cache**: LLM response cache keyed by topic + sketch hash, TTL-pruned (see above)

Filesystem exports:

- **Artifacts**: `{GAUSS_HOME}/fep_artifacts/session_*.json`
- **Bulk JSONL**: `{GAUSS_HOME}/fep_artifacts/sessions_fep_lean_*.jsonl`
- **Operations log**: `{GAUSS_HOME}/fep_logs/operations.jsonl`

---

## Test suite

```bash
# From the fep_lean project root:
uv run pytest tests/ -q --timeout=900 --cov=src --cov-fail-under=89
```

For the **89% coverage gate**, run from the project root with `--cov=src`. Invoking pytest from the monorepo root with a different `--cov` source path may report a lower total under some `pytest-cov` / branch settings.

Coverage gate is **89%**; see [`pyproject.toml`](pyproject.toml) `tool.coverage.report`.

---

## Navigation

- [README.md](README.md) — quick start
- In-repo Gauss client + Hermes layer: [`src/gauss/`](src/gauss/), [`src/llm/hermes.py`](src/llm/hermes.py); see [docs/hermes.md](docs/hermes.md) and [docs/pipeline.md](docs/pipeline.md). Cursor skill stub: [`.cursor/skills/gauss/SKILL.md`](../../.cursor/skills/gauss/SKILL.md) (points here; full detail in this file).
- [SPEC.md](SPEC.md) — functional spec
- [PAI.md](PAI.md) — AI agent interface
- [docs/](docs/) — extended reference
- Parent: [`../README.md`](../README.md) (path from repo root is usually `projects/fep_lean/`)
