# Architecture — fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Overview

`fep_lean` implements a **formalization pipeline** (`FEPPipeline` + `pipeline/orchestrator.py`) composed of layered packages under `src/`. Each layer has a single responsibility; calls flow downward only.

Note — **stage counts**: `FEPPipeline.run()` appends **four** `StepResult` rows to `PipelineResult.stages` (Load Catalogue, Environment Validation, Gauss Sessions, Manuscript Artifacts). `Reporter.generate` is **not** a fifth stage in that list; `orchestrator.run_pipeline` calls it after `run()` returns. The manuscript's six-node DAG figure groups manuscript artifacts and run reports for readability — it does not change the four named pipeline stages in code.

## `src/` layout — six packages

The project's Python source is split into six packages under `projects/fep_lean/src/`. Each is a
regular top-level import (e.g. `from gauss.runner import GaussRunner`) because the project
prepends `src/` to `sys.path` rather than wrapping everything in a single distribution package.

| Package | Purpose | Key public modules |
|---------|---------|-------------------|
| `catalogue` | YAML-backed topic catalogue (50 rows) | `catalogue.topics` (`FEPTopicCatalogue`, `TopicEntry`) |
| `gauss` | OpenGauss CLI glue + SQLite session store + per-topic runner | `gauss.cli`, `gauss.client` (`OpenGaussClient`), `gauss.runner` (`GaussRunner`, `TopicRunResult`) |
| `llm` | Hermes LLM explainer (OpenRouter HTTP) | `llm.hermes` (`HermesConfig`, `HermesExplainer`, `HermesResult`) |
| `output` | Manuscript / figures / reporter writers | `output.manuscript`, `output.figures`, `output.reporter` (`Reporter`) |
| `pipeline` | Pipeline core + thin orchestrator | `pipeline.core` (`FEPPipeline`, `PipelineResult`, `StepResult`), `pipeline.orchestrator` |
| `verification` | Environment checks + `lake env lean` subprocess wrapper | `verification.environment`, `verification.lean_verifier` (`LeanVerifier`, `VerifyResult`) |

Plus one **module** at the package root — `src/_paths.py` — that every subpackage imports for
directory resolution (see below).

> [!WARNING]
> **PYTHONPATH ordering matters.** `projects/fep_lean/src/` **must** come before the
> repository-level `infrastructure/` directory on `PYTHONPATH` / `sys.path`. Reason:
> `infrastructure/llm/` (Ollama integration used by the *template*) would otherwise **shadow**
> `projects/fep_lean/src/llm/` (Hermes / OpenRouter), and imports like `from llm.hermes import …`
> would resolve to the wrong package. The project's own scripts insert `src/` at position 0 before
> any infra paths; if you wire the project into a fresh environment (IDE, container, CI), export:
>
> ```bash
> export PYTHONPATH="projects/fep_lean/src:infrastructure:."
> ```
>
> Verify with `uv run python -c "import llm.hermes; print(llm.hermes.__file__)"` — the path must
> end in `projects/fep_lean/src/llm/hermes.py`, not `infrastructure/llm/…`.

## `src/_paths.py` — shared path resolution

A single helper, `project_root()`, lets every subpackage locate the project directory without
depending on the pipeline layer:

```python
from _paths import project_root

root = project_root()
# → Path("…/projects/fep_lean") by default
# → Path(os.environ["PROJECT_DIR"]) when that env var is set (for tmp_path test fixtures)
```

**Resolution rules** (from `src/_paths.py`):

1. If the `PROJECT_DIR` environment variable is set, return `Path(os.environ["PROJECT_DIR"])`
   verbatim. This is used by the test suite to inject `tmp_path` roots without monkeypatching.
2. Otherwise return the directory containing `src/` (`Path(__file__).resolve().parent.parent`).

No code below the orchestrator layer calls `Path(__file__)` directly for project navigation —
everything routes through `project_root()` so that tests can redirect the tree at will.

## Monorepo boundary (template Stage 02)

From the **repository root** (outside this project's checkout directory), the template runs [`scripts/02_run_analysis.py`](../../../scripts/02_run_analysis.py) as **Project Analysis**. It executes each discovered `projects/<project>/scripts/*.py` (except `_*.py`) in a subprocess whose wall-clock limit defaults via **`ANALYSIS_SCRIPT_TIMEOUT_SEC=7200`** (2 hours per script), implemented in [`infrastructure/core/analysis_timeout.py`](../../../infrastructure/core/analysis_timeout.py). This is independent of `FEPPipeline`'s internal timeouts (e.g. `FEP_LEAN_VERIFY_TIMEOUT` for `lake env lean`).

See [configuration.md — Monorepo Stage 02](configuration.md#monorepo-stage-02-repository-root) and [pipeline.md](pipeline.md).

```text
┌──────────────────────────────────────────────────────────────┐
│  Entry Layer                                                 │
│  scripts/01_fep_catalogue_and_figures.py, 02_run_single_*.py │
│  pipeline/orchestrator.py — run_pipeline, run_single_topic    │
├──────────────────────────────────────────────────────────────┤
│  Application Layer                                           │
│  pipeline/core.py — FEPPipeline (catalogue → validate →      │
│    Gauss → manuscript artifacts) + PipelineResult            │
├──────────────────┬──────────────────┬────────────────────────┤
│  Agentic Layer   │                  │                        │
│  gauss/runner.py │ llm/hermes.py     │ verification/        │
│  (orchestrate)   │ (OpenRouter HTTP) │ lean_verifier.py     │
├──────────────────┴──────────────────┴────────────────────────┤
│  Catalogue / manuscript / figures                              │
│  catalogue/topics.py; src/output/manuscript.py → vars + unified 09z appendix │
│  manuscript/; output/figures/                                  │
├──────────────────────────────────────────────────────────────┤
│  Persistence                                                   │
│  gauss/client.py — SQLite + artifacts + JSONL + logs         │
│  output/reporter.py — Markdown + JSON reports                 │
├──────────────────────────────────────────────────────────────┤
│  Config                                                        │
│  config/settings.yaml  +  config/topics.yaml (50 topics)     │
└──────────────────────────────────────────────────────────────┘
```

---

## Textbook alignment (Lean sketches)

**Published PDF** catalogue material for all rows is **`config/topics.yaml`** plus the generated **`manuscript/09z_unified_formalism_catalogue.md`**: fenced Lean and, per topic, pandoc section anchors `{#sec:catalogue-…}` / `{#sec:eqs-…}` with displayed `equation` blocks carrying `\label{eq:fep-NNN-k}` for `\Cref{…}` / `\eqref{…}` (see `docs/xref_audit.py`). LaTeX rows come from `LATEX_EQUATIONS` at render time when importable, else from each row’s `latex_equations` in YAML.

Catalogue bodies are **`sorry`-free** and tiered by strength (not by YAML tag):

| Tier | Meaning | Example topics |
|------|---------|----------------|
| T0 | Structural anchors (nonnegativity, monotonicity) | Many measure-mass lemmas |
| T1 | Standard identities / finite combinatorics | fep-028 softmax sum; fep-008 `exists_min_image` |
| T2 | Measure-theoretic steps toward divergence / integration | fep-014 union/monotonicity; future KL when Mathlib pin allows |

The **`mathlib`** string in each YAML row is a **navigation hint**; the **pinned** `mathlib4` tag in `lean/lakefile.lean` may lag `master` (e.g. native KL API).

---

## Layer Descriptions

### Entry Layer

| Path | Role |
|------|------|
| `scripts/01_fep_catalogue_and_figures.py` | Template `02_run_analysis.py` hook; calls `run_pipeline` |
| `scripts/02_run_single_topic.py` | Thin CLI for `run_single_topic` |
| `pipeline/orchestrator.py` | `run_pipeline()`, `run_single_topic()` — reporting and env wiring |

`run_pipeline` always constructs `FEPPipeline`; with `FEP_LEAN_GAUSS_WORKFLOWS=1`, **Gauss Sessions** runs inside it (otherwise that stage is skipped).

### Application Layer — `FEPPipeline`

`pipeline/core.py` runs these **stages** (names match `StepResult.name`):

| # | Stage | Description |
|---|-------|-------------|
| 1 | Load Catalogue | `catalogue.topics.FEPTopicCatalogue.from_yaml` — 50 topics (after optional filters) |
| 2 | Environment Validation | `verification.environment.run_validation_checks` — 13 checks |
| 3 | Gauss Sessions | `gauss.runner.GaussRunner.run_topics_batch` — Hermes, `LeanVerifier`, SQLite per topic; **skipped** unless `FEP_LEAN_GAUSS_WORKFLOWS` is truthy (`gauss/cli.workflows_enabled`) |
| 4 | Manuscript Artifacts | `write_manuscript_vars`, `write_unified_formalism_appendix_markdown`, `write_all_catalogue_figures` |

`Reporter.generate` and timestamped `output/reports/run_*/` bundles are invoked from **`run_pipeline`** in `orchestrator.py` after `FEPPipeline.run()` returns.

### Agentic Layer

| Module | Key class | Responsibility |
|--------|-----------|----------------|
| `gauss/runner.py` | `GaussRunner`, `TopicRunResult` | Per-topic orchestration |
| `llm/hermes.py` | `HermesExplainer`, `HermesConfig`, `HermesResult` | OpenRouter HTTP |
| `verification/lean_verifier.py` | `LeanVerifier`, `VerifyResult` | `lake env lean`, sorry detection |

### Catalogue and figures

| Module | Role |
|--------|------|
| `catalogue/topics.py` | `FEPTopicCatalogue`, `TopicEntry` |
| `output/figures/` | Figure writers for catalogue charts |

### Persistence and reporting

| Module | Role |
|--------|------|
| `gauss/client.py` | SQLite session DB, turns, artifacts, JSONL, ops log |
| `output/reporter.py` | Markdown + JSON under `output/reports/run_*/` |

### Config Layer

| File | Purpose |
|------|---------|
| `config/settings.yaml` | Runtime config: GAUSS_HOME, Hermes model, orchestration |
| `config/topics.yaml` | 50 topic definitions: id, title, area, mathlib, nl, lean_sketch |

**Config override priority**: env vars → `config/settings.yaml` → code defaults.

---

## Data Flow

```text
config/topics.yaml
    │
    ▼
FEPTopicCatalogue.from_yaml()   [50 TopicEntry objects]
    │
    ▼
FEPPipeline.run()                    ← pipeline/core.py
    │
    ├─► Load Catalogue / Environment Validation
    │
    ├─► GaussRunner.run_topics_batch(topics)     for each topic (skipped if workflows off):
    │       ├─► OpenGaussClient.create_session(topic_id, area, lean_sketch)
    │       ├─► HermesExplainer.explain_topic(topic)
    │       │       └─► POST openrouter.ai (2-message: system + user)
    │       ├─► _record_hermes_turns:
    │       │       ├─► update_session(0, "system", system_prompt)
    │       │       ├─► update_session(1, "user",   theorem_block)
    │       │       └─► update_session(2, "assistant", explanation + lean sketch)
    │       ├─► set_refined_sketch(session_id, refined_lean_sketch)
    │       ├─► LeanVerifier.verify_sketch(...)
    │       │       └─► lake env lean <temp_file>       → VerifyResult
    │       ├─► write_artifact(session_id, payload)    → .json under GAUSS_HOME
    │       └─► close_session(session_id, hermes_success, lean_compiles=...)
    │
    └─► Manuscript Artifacts: write_manuscript_vars + write_unified_formalism_appendix_markdown
        + write_all_catalogue_figures → manuscript/ + output/figures/
    │
    ▼
orchestrator.run_pipeline()          ← after FEPPipeline.run() returns
    │
    └─► Reporter.generate(catalogue, pipeline_result)
            ├─► output/reports/run_YYYYMMDD_HHMMSS/index.md
            ├─► output/reports/run_.../summary.json
            ├─► output/reports/run_.../hermes_report.md
            ├─► output/reports/run_.../lean_report.md
            ├─► output/reports/run_.../validation_report.md
            └─► output/reports/run_.../topics/fep-NNN.md
```

---

## Design Decisions

### 1. SQLite-First Persistence

All sessions are stored in `{GAUSS_HOME}/fep_lean_state.db` (SQLite via `OpenGaussClient`):

- Queryable by topic_id, area, source
- Replay without re-running Hermes
- Bulk JSONL export for downstream analysis

### 2. LLM Model Fallback Chain

Hermes tries an **8-model chain** (primary + 7 fallbacks; all free-tier OpenRouter by default, see [`hermes.md`](hermes.md#model-fallback-chain-openrouter-free-tier)) so the pipeline completes when the primary model is overloaded or flaky. On each model, **HTTP 429** and **transient** transport errors (`IncompleteRead`, `URLError`, etc.) are retried with backoff (`HERMES_429_MAX_RETRIES`, `HERMES_NETWORK_MAX_RETRIES`) before advancing to the next model. **5xx** and non-retryable fetch failures typically advance the chain; hard **4xx** from a completed HTTP response (invalid key, bad model ID) can stop the chain and (on 401/403) globally disable Hermes for the remainder of the run. See [`hermes.md`](hermes.md#error-handling).

### 3. Graceful Lean Skip

`LeanVerifier.verify_sketch` never raises: when `lake` is absent or sandboxed, it returns `VerifyResult(skip_reason='...')`. The pipeline records `lean_compiles=-1` (not attempted) and continues.

### 4. Stage Independence

`FEPPipeline` stages can fail or be skipped (notably **Gauss Sessions** when workflows are off) without always aborting the rest. `PipelineResult.status` reflects aggregate outcome (`ok`, `warning`, `partial`, `error`).

### 5. Zero-Mock Testing

The pytest suite (**347** collected items from `projects/fep_lean/`; exact: `uv run pytest --collect-only -q`) uses SQLite (`tmp_path`), the checked-in YAML catalogue, `gauss` / `lake` / `lean` where required by `conftest.py`, and HTTP where an API key is present. No `unittest.mock` for subprocess or CLI.

### 6. Serial Verification for Determinism

A core agentic architecture lesson extracted during the orchestration development: `LeanVerifier` expressly refuses concurrent parallel processing (`ThreadPoolExecutor` was purged). Spawning multiple `lake env lean` subshells inherently causes MacOS ELAN proxy sandbox deadlocks, blocking child processes from accessing `.olean` imports and manufacturing fake math compiler issues (e.g., `unknown identifier`). Deterministic pipeline guarantees override execution speed, thus all checks occur linearly.

---

## Module Dependency Graph

```text
scripts/01_fep_catalogue_and_figures.py
    └─► pipeline/orchestrator.py
            ├─► pipeline/core.py (FEPPipeline)
            │       ├─► _paths.py (project_root)
            │       ├─► catalogue/topics.py
            │       │       └─► config/topics.yaml
            │       ├─► verification/environment.py
            │       │       └─► gauss/cli.py
            │       ├─► gauss/runner.py
            │       │       ├─► llm/hermes.py
            │       │       │       └─► urllib.request → OpenRouter API
            │       │       ├─► verification/lean_verifier.py
            │       │       │       └─► subprocess → lake env lean
            │       │       └─► gauss/client.py
            │       │               └─► sqlite3
            │       ├─► output/manuscript.py
            │       └─► output/figures/
            └─► output/reporter.py   ← called after FEPPipeline.run() returns
```

No circular dependencies. Each module depends only on modules in lower layers.

---

## Documentation integrity

Markdown under `docs/` and project-root `README.md` / `AGENTS.md` are guarded by `check_links.py`, `md_hygiene.py`, `pin_audit.py`, and `xref_audit.py` (see [docs/AGENTS.md](AGENTS.md) and [docs/SPEC.md](SPEC.md) invariants **B3–B6**). Run them after structural edits so toolchain pins, internal links, and manuscript `\ref` targets stay consistent with the code.

---

## Navigation

- [← docs/README.md](README.md)
- [Pipeline →](pipeline.md)
- [API reference →](api.md)
- [Troubleshooting →](troubleshooting.md)
- [CLI Reference →](cli-reference.md)
- [Configuration →](configuration.md)
