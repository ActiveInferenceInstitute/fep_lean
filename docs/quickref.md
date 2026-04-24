# Quick Reference — fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Run from **the project root** (the directory containing `pyproject.toml`) unless noted.

## Setup (one-time)

```bash
# From repository root, sync this project's venv
uv sync --directory projects/fep_lean --extra dev

# Export PYTHONPATH so direct python / pytest invocations resolve imports
# (project src FIRST so src/llm, src/catalogue, etc. win over any shadowing packages)
export PYTHONPATH=projects/fep_lean/src:.:infrastructure

# Lean toolchain + Mathlib cache (~3 GB, ~5 min)
bash scripts/_maint_bootstrap_lean_toolchain.sh
./scripts/00b_install_opengauss_cli.sh

# Optional: OpenRouter key for Hermes (core-only mode does not need it)
export OPENROUTER_API_KEY=sk-or-v1-...
```

## Key env vars (most-used)

| Variable | Purpose | Default |
| -------- | ------- | ------- |
| `PYTHONPATH` | `projects/fep_lean/src:.:infrastructure` for direct script / pytest invocations (project src first) | unset |
| `FEP_LEAN_GAUSS_WORKFLOWS` | `1` enables full Gauss + Hermes + Lean batch; `0` = core-only (default) | `0` |
| `OPENROUTER_API_KEY` | Primary Hermes auth; required only when workflows are enabled | — |

## Run commands

```bash
# Catalogue, validation, manuscript vars, figures (default: core-only mode)
uv run python scripts/01_fep_catalogue_and_figures.py

# Quick verification — single topic, fastest smoke test
uv run python scripts/02_run_single_topic.py --topic fep-001

# Single topic with full Gauss workflow (requires API key)
FEP_LEAN_GAUSS_WORKFLOWS=1 OPENROUTER_API_KEY=sk-or-... \
  uv run python scripts/02_run_single_topic.py fep-008 --workflow prove

# Full batch with Hermes + Lean (all 50 topics)
FEP_LEAN_GAUSS_WORKFLOWS=1 OPENROUTER_API_KEY=sk-or-... \
  uv run python scripts/01_fep_catalogue_and_figures.py

# Lean verification only (no LLM)
uv run python scripts/03_lean_verify_only.py

# Regenerate reports (when wired to existing pipeline output)
uv run python scripts/04_generate_reports.py

# Rebuild baseline 50-topic YAML (maintenance; not run by template Stage 02)
uv run python scripts/_maint_build_topics_catalogue.py
```

## Reference timings (representative hardware)

Full-batch run on a recent Mac with warm Mathlib cache, `FEP_LEAN_GAUSS_WORKFLOWS=1`, OpenRouter primary reachable:

| Metric | Value |
| ------ | ----- |
| Total wall-clock | **order ~30–60 min** (50 topics, primary `moonshotai/kimi-k2.6` reasoning model + Lean + SQLite; provider/queue dependent — see `manuscript_vars.yaml::verify.duration_min` for the latest measured value) |
| Hermes explanations | **50 / 50** succeed (with fallback chain) |
| Lean `lake env lean` proofs | **50 / 50** on shipped catalogue when verify sweep is green |
| Core-only mode (no workflows) | ~2–3 min (catalogue + figures + vars) |
| Lean-only sweep (`03_lean_verify_only.py`) | ~262 s (avg 5.2 s/topic) |
| Full template pipeline (`execute_pipeline.py --core-only --skip-infra`) | ~578 s |

## Test commands

Run from **the project root** so `pytest-cov` maps to `src/` and the **89 %** combined line+branch gate matches [`pyproject.toml`](../pyproject.toml). The in-file timeout is already **900 s**; setting it again on the CLI is equivalent:

```bash
uv run pytest tests/ --timeout=900 --cov=src --cov-fail-under=89
```

Expected outcome: **347** tests collected (346 pass, 1 API-key-gated skip) from `projects/fep_lean/`; confirm with `uv run pytest --collect-only -q`. Coverage at or above the gate (see monorepo [`docs/_generated/canonical_facts.md`](../../../docs/_generated/canonical_facts.md) for current figures).

Running pytest from the monorepo root with a path like `pytest path/to/fep_lean/tests/` and `--cov=path/to/fep_lean/src` can report a lower total under some branch-coverage settings than the project-local command above. Prefer running from the project root with `--cov=src` for authoritative coverage.

## Toolchain preflight

Before a long `lake build` or when debugging missing tools:

```bash
# from project root
uv run fep-lean-preflight
# stricter: fail if gauss doctor fails
uv run fep-lean-preflight --require-gauss
```

**lean4-skills:** `/lean4:doctor` (plugin: elan, `LEAN4_SCRIPTS`, MCP) is separate from the above; map plugin issues to [troubleshooting.md](troubleshooting.md#lean4-skills-lean4doctor-vs-this-repo) and [lean4.md](lean4.md#cursor-lean4-commands).

## Area names (50-topic distribution)

| Area | Count |
| ---- | ----- |
| FEP | 14 |
| ActiveInference | 11 |
| BayesianMechanics | 10 |
| InfoGeometry | 8 |
| Thermodynamics | 7 |

## Topic IDs

`fep-001` … `fep-050` (see `config/topics.yaml`). Under current policy every row is **`mathlib_status: real`** (committed maturity tag) with a compiling sketch (YAML is the source of truth; regenerate via maint scripts as needed).

## Key paths

| Path | Description |
| ---- | ----------- |
| `config/settings.yaml` | Runtime configuration |
| `config/topics.yaml` | 50 topic definitions |
| `manuscript/config.yaml` | Paper metadata (v0.7.1 `paper.version`, 15 keywords, zh/de/fr translations) |
| `manuscript/manuscript_vars.yaml` | Injected placeholders for PDF (`{{…}}`) |
| `manuscript/09z_unified_formalism_catalogue.md` | Generated B+C: Lean + equation catalogue (`{#sec:…}` anchors; `equation` + `\label{eq:…}`) |
| `output/reports/run_*/` | Run output directories |
| `~/.gauss/` | Default GAUSS_HOME (SQLite + artifacts) |

## Environment variables (most-used)

For the complete grepped-from-source list, see [`configuration.md`](configuration.md#environment-variables-complete-list). **Monorepo Stage 02** (repo-root `scripts/02_run_analysis.py`): default **`ANALYSIS_SCRIPT_TIMEOUT_SEC=7200`** (2 h per analysis script); see [`configuration.md` § Monorepo](configuration.md#monorepo-stage-02-repository-root).

| Variable | Purpose |
| -------- | ------- |
| `PYTHONPATH` | `projects/fep_lean/src:.:infrastructure` for direct imports (project `src` first to defeat shadowing) |
| `ANALYSIS_SCRIPT_TIMEOUT_SEC` | Per-script timeout for Stage 02 (default **7200**; `0`/`unlimited` = none) |
| `OPENROUTER_API_KEY` | Primary Hermes auth (OpenRouter endpoint) |
| `ANTHROPIC_API_KEY` | Fallback Hermes auth (Anthropic endpoint) |
| `HERMES_MODEL` | Override Hermes primary model ID |
| `HERMES_429_MAX_RETRIES` | Retries after HTTP 429 on the **current** model before next in chain (default 2) |
| `HERMES_NETWORK_MAX_RETRIES` | Retries after transient transport errors (`IncompleteRead`, dropped connections, …) on the **current** model (default 2) |
| `HERMES_MAX_MODEL_ATTEMPTS` | Cap models tried per topic from fallback chain (optional) |
| `FEP_LEAN_GAUSS_WORKFLOWS` | `1` enables full Gauss + Hermes + Lean; omit/`0` for thin mode (`01_fep_*` sets `0` unless `FEP_LEAN_LIVE_TESTS`; **`run.sh`** defaults to `1` when unset) |
| `FEP_LEAN_LIVE_TESTS` | When workflows unset, truthy value enables Gauss from `01_fep_*` |
| `FEP_LEAN_MAX_TOPICS` | Cap catalogue batch size for Gauss Sessions (smoke runs) |
| `FEP_LEAN_REQUIRE_GAUSS` | `1` makes missing `gauss doctor` a hard failure |
| `FEP_LEAN_VERIFY_TIMEOUT` | Per-sketch Lean compile timeout (default 300 s) |
| `FEP_LEAN_LAKE_EXE` / `FEP_LEAN_LEAN_EXE` | Explicit binary paths (bypass PATH + elan proxy) |
| `FEP_LEAN_PREFETCH` | `1` overlaps Hermes topic N+1 with Lean verify for topic N (verify workflow, ≥2 topics) |
| `FEP_LEAN_FIGURES_MP` | `0` renders catalogue PNGs serially in-process (skip `ProcessPoolExecutor`) |
| `GAUSS_HOME` | Override default `~/.gauss` session directory |
| `PROJECT_DIR` | Override project root (tests / template injection) |

## Navigation

- [Getting Started →](getting-started.md)
- [Troubleshooting →](troubleshooting.md)
- [CLI Reference →](cli-reference.md)
- [Configuration →](configuration.md)
- [← docs/README.md](README.md)
