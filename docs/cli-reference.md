# CLI Reference — fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Complete reference for every command-line entry point in `fep_lean`. Each section lists the exact argparse surface (from the source), every environment variable the command honours, every exit code, and a worked example. All signatures are ground-truthed against `scripts/` and `pyproject.toml`.

---

## Script inventory

The five command-line entry points for `fep_lean`:

| # | Entry point | Location | Pipeline role |
|---|-------------|----------|---------------|
| 1 | `01_fep_catalogue_and_figures.py` | `projects/fep_lean/scripts/` | Primary Stage 4 analysis: catalogue, figures, manuscript vars, optional Gauss batch |
| 2 | `02_run_single_topic.py` | `projects/fep_lean/scripts/` | Single-topic debug entry point (supports `--workflow`) |
| 3 | `03_lean_verify_only.py` | `projects/fep_lean/scripts/` | Lean-only sweep across all (or one) catalogue sketches |
| 4 | `_maint_build_topics_catalogue.py` | `projects/fep_lean/scripts/` | Maintenance: regenerate `config/topics.yaml` from Python authoritative source |
| 5 | `fep-lean-preflight` | installed console script (from `pyproject.toml`) | Toolchain preflight: `gauss doctor`, `lake`, `lean`, Mathlib `.olean` |

All five honour the environment variable contract documented in [`configuration.md`](configuration.md#environment-variables-complete-list).

---

## Template / monorepo (`scripts/02_run_analysis.py`)

**Path** (repository root): [`scripts/02_run_analysis.py`](../../../scripts/02_run_analysis.py). **Not** in this project's `scripts/` directory — it is invoked by the global pipeline after project tests.

**Purpose**: discover every `projects/<name>/scripts/*.py` for the active project, **excluding** filenames starting with `_` (maintenance scripts like `_maint_build_topics_catalogue.py` are run only manually).

**Arguments**:

```text
--project NAME    Project directory under projects/ (e.g. fep_lean)
```

**Environment**:

| Variable | Default | Effect |
| -------- | ------- | ------ |
| `ANALYSIS_SCRIPT_TIMEOUT_SEC` | **7200** | Seconds per analysis subprocess; `0` / `none` / `unlimited` / `inf` = no timeout ([`infrastructure/core/analysis_timeout.py`](../../../infrastructure/core/analysis_timeout.py)) |

**Exit codes**: `0` if every discovered script exits 0; `1` if any script fails or the project has no `scripts/` directory.

**Example**:

```bash
cd /path/to/template
uv run python scripts/02_run_analysis.py --project fep_lean
```

See [configuration.md — Monorepo Stage 02](configuration.md#monorepo-stage-02-repository-root) and [pipeline.md](pipeline.md).

---

## Console scripts (installed via `pyproject.toml`)

### `fep-lean-preflight`

Entry point declared in [`pyproject.toml:24`](../pyproject.toml): `fep-lean-preflight = "verification.preflight:main"`.

```bash
uv run fep-lean-preflight [--require-gauss]
```

**Purpose**: Toolchain readiness check before a full pipeline run. Verifies `gauss doctor` (optional), `lake --version`, `lean --version`, Mathlib `.olean` cache, and writable output directories.

**Flags**:

| Flag | Effect |
|------|--------|
| `--require-gauss` | Treat missing or failing `gauss doctor` as a hard failure (exit 1). Without the flag, gauss absence is logged but non-fatal. |

**Exit codes**:

| Code | Meaning |
|------|---------|
| `0`  | All required checks passed |
| `1`  | At least one required check failed |

**Example**:

```bash
# From the project root (directory containing this project's pyproject.toml)
uv run fep-lean-preflight
# ✓ gauss doctor: ok
# ✓ lake: 4.29.0
# ✓ lean: 4.29.0
# ✓ Mathlib.olean: present
# ✓ output/ writable
# PASS
```

---

## Analysis scripts (`scripts/` at project root)

All main scripts are **thin orchestrators** that delegate to `pipeline.orchestrator`. They are invoked by `scripts/02_run_analysis.py` at Stage 4 of the template pipeline, or directly for ad-hoc runs.

### `01_fep_catalogue_and_figures.py`

Primary analysis entry point. Loads the 50-topic catalogue, validates the environment, optionally runs the full Gauss workflow (Hermes + Lean), writes `manuscript_vars.yaml` and figures, and generates a timestamped report directory.

```bash
# From the project root
uv run python scripts/01_fep_catalogue_and_figures.py
```

**Arguments**: none (configuration via env vars only).

**Environment variables read**:

| Variable | Effect | Default |
|----------|--------|---------|
| `FEP_LEAN_GAUSS_WORKFLOWS` | `1` → enable Gauss stage (Hermes + Lean per topic + SQLite); `0` → thin mode (skip Gauss) | `0` (off by default; export `=1` for live workflows) |
| `FEP_LEAN_LIVE_TESTS` | Fallback: when `FEP_LEAN_GAUSS_WORKFLOWS` is unset, truthy (`1`) enables workflows | unset |
| `OPENROUTER_API_KEY` | Hermes LLM primary key | — |
| `ANTHROPIC_API_KEY` | Hermes LLM fallback key | — |
| `MPLBACKEND` | Forced to `Agg` by the script for headless figure generation | `Agg` |
| `PROJECT_DIR` | Override project root (test fixture use) | (walks up from `src/`) |

**Outputs** (on success, paths printed to stdout):

- `output/figures/area_distribution.png`
- `output/figures/mathlib_coverage.png`
- `output/figures/pipeline_timing.png`
- `manuscript/manuscript_vars.yaml` (regenerated)
- `manuscript/09z_unified_formalism_catalogue.md` (regenerated; gitignored; Lean + typeset LaTeX with `{#sec:…}` anchors and `equation` + `\label{eq:…}`)
- `output/reports/run_YYYYMMDD_HHMMSS/` (full report bundle)

**Exit codes**: `0` on any pipeline outcome (status may be `ok`, `partial`, `warning`, `error` in `PipelineResult` — check `summary.json`). `1` only on unhandled Python exceptions.

**Example**:

```bash
# Thin mode (no LLM, no Lean): fastest way to regenerate figures and reports
FEP_LEAN_GAUSS_WORKFLOWS=0 uv run python scripts/01_fep_catalogue_and_figures.py

# Full mode with live Hermes + Lean (requires API key)
export OPENROUTER_API_KEY=sk-or-v1-...
uv run python scripts/01_fep_catalogue_and_figures.py
```

---

### `02_run_single_topic.py`

Run the pipeline for exactly one catalogue topic. Useful for debugging a single row without waiting for all 50 Lean compilations or Hermes calls.

```bash
uv run python scripts/02_run_single_topic.py [topic_id] [--topic ID] \
    [--workflow {verify,draft,prove,review}] [--skip-gauss]
```

**Arguments**:

| Arg / Flag | Type | Default | Description |
|------------|------|---------|-------------|
| `topic_id` (positional) | `str` | `fep-008` | Topic ID to run (e.g. `fep-001`, `fep-022`) |
| `--topic ID` | `str` | — | Same as positional form; ignored if positional provided |
| `--workflow {verify,draft,prove,review}` | `str` | `verify` | Which Gauss workflow to execute for this topic. `verify` = Lean `lake env lean` only; `draft` = Hermes sketch draft; `prove` = Hermes full proof attempt; `review` = Hermes read-only review of the existing sketch. Honoured when `FEP_LEAN_GAUSS_WORKFLOWS=1`. |
| `--skip-gauss` | flag | `False` | Sets `FEP_LEAN_GAUSS_WORKFLOWS=0` (disables Hermes + GaussRunner + SQLite). Useful for thin-mode single-topic runs. |

**Exit codes**:

| Code | Meaning |
|------|---------|
| `0` | Topic ran successfully |
| `1` | `run_single_topic` returned `status=error` or topic ID unknown |

**Example**:

```bash
# Quick verify: Lean-only, single topic, thin mode
uv run python scripts/02_run_single_topic.py --topic fep-001 --workflow verify --skip-gauss

# Full prove workflow (Hermes + Lean) for fep-022
OPENROUTER_API_KEY=sk-or-v1-... FEP_LEAN_GAUSS_WORKFLOWS=1 \
  uv run python scripts/02_run_single_topic.py fep-022 --workflow prove

# Read-only review workflow
OPENROUTER_API_KEY=sk-or-v1-... FEP_LEAN_GAUSS_WORKFLOWS=1 \
  uv run python scripts/02_run_single_topic.py fep-008 --workflow review

# Default: runs fep-008 with verify workflow under the env's current FEP_LEAN_GAUSS_WORKFLOWS setting
uv run python scripts/02_run_single_topic.py
```

---

### `03_lean_verify_only.py`

Run the Lean compilation step **only**, against every sketch in `config/topics.yaml` (or one specific topic). Does not touch Hermes, does not use `FEP_LEAN_GAUSS_WORKFLOWS`, does not write reports. Use for CI gates, quick sanity checks, or after editing YAML sketches.

```bash
uv run python scripts/03_lean_verify_only.py [--topic ID]
```

**Arguments**:

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--topic ID` | `str` | `None` (verify all 50) | Verify a specific topic by ID; fails with exit 1 if unknown |

**Behaviour**:

1. Loads all topics from `config/topics.yaml`
2. Filters to `--topic` if provided
3. Checks `lake` availability (exits 0 with a warning if missing — not an error)
4. Checks Mathlib `.olean` cache; auto-runs `lake exe cache get` + `lake build` if missing
5. Serially verifies each sketch with `LeanVerifier.verify_sketch` (sequential, `max_workers=1`)
6. Prints per-topic status (`OK` / `OK (sorry)` / `ERROR`) with error/warning counts

**Exit codes**:

| Code | Meaning |
|------|---------|
| `0` | All topics compiled clean (or lake unavailable → skip gracefully) |
| `1` | One or more topics failed to compile, or `--topic` unknown, or Mathlib build failed |

**Timing**: ~262 s for all 50 topics (avg 5.2 s/topic) on a 2024 Mac with a warm Mathlib cache.

**Example**:

```bash
# Verify all 50 topics (from the project root)
uv run python scripts/03_lean_verify_only.py

# Verify only fep-042 after editing YAML
uv run python scripts/03_lean_verify_only.py --topic fep-042
```

---

### `04_generate_reports.py`

Regenerate the Markdown/JSON report bundle (`output/reports/run_*/`) without running Hermes or Lean. Uses `FEP_LEAN_GAUSS_WORKFLOWS=0` by default. Idempotent — each run creates a new timestamped directory and updates the `latest/` symlink.

```bash
uv run python scripts/04_generate_reports.py
```

**Arguments**: none.

**Environment variables**:

| Variable | Effect | Default |
|----------|--------|---------|
| `FEP_LEAN_GAUSS_WORKFLOWS` | Forced to `0` by the script unless already set | `0` |
| `MPLBACKEND` | Forced to `Agg` | `Agg` |

**Outputs**:

- `output/reports/run_YYYYMMDD_HHMMSS/index.md`
- `output/reports/run_YYYYMMDD_HHMMSS/summary.json`
- `output/reports/run_YYYYMMDD_HHMMSS/hermes_report.md` (stub — Hermes skipped)
- `output/reports/run_YYYYMMDD_HHMMSS/lean_report.md` (stub — Lean skipped)
- `output/reports/run_YYYYMMDD_HHMMSS/validation_report.md` (13 checks)
- `output/reports/run_YYYYMMDD_HHMMSS/topics/fep-NNN.md` (×50)
- `output/reports/latest` → symlink to the newest `run_*`

**Exit codes**:

| Code | Meaning |
|------|---------|
| `0` | Report directory written successfully |
| `0` + warning | Pipeline ran but with `status != "ok"` (partial outputs) |

---

## Maintenance scripts (local tooling — not part of the pipeline)

These live in `scripts/` but are **not** invoked by `execute_pipeline.py`. Use them only when explicitly editing the catalogue.

### `_maint_filter_topics.py`

**Destructive**. Rewrites `config/topics.yaml` to a subset of topics by ID.

```bash
uv run python scripts/_maint_filter_topics.py --ids fep-001,fep-014,fep-042 [--apply]
```

| Flag | Effect |
|------|--------|
| `--ids IDS` | Comma-separated topic IDs to keep (required) |
| `--apply` | Actually write the file. Omit for a dry-run (default). |

Use this to temporarily pin the catalogue to a small subset during debugging, then `git checkout config/topics.yaml` to restore.

---

### `_maint_build_topics_catalogue.py`

Regenerates the canonical 50-topic catalogue. `METADATA` (topic IDs, titles, areas, Mathlib modules,
NL statements) is defined inside this script; `lean_sketch` bodies come from
`scripts/catalogue_sketches.py` (`SKETCHES`). Only run this when adding or restructuring catalogue
entries at source. The leading underscore excludes this script from Stage 02 auto-discovery.

```bash
uv run python scripts/_maint_build_topics_catalogue.py
```

Rewrites `config/topics.yaml` from the authoritative Python source.

---

### `_maint_fix_manuscript_counts.py`

Bulk-updates hard-coded topic count strings (e.g. "50 topics") in manuscript markdown files when the catalogue size changes. Idempotent.

```bash
uv run python scripts/_maint_fix_manuscript_counts.py
```

---

## Template-level entry points (from repo root)

The monorepo's `scripts/` directory contains project-agnostic orchestrators. These know about `fep_lean` via `--project fep_lean`.

### `scripts/execute_pipeline.py`

Ten-stage DAG runner (see `../SPEC.md` and `architecture.md`).

```bash
uv run python scripts/execute_pipeline.py --project fep_lean \
    [--skip-infra] [--skip-llm] [--resume] [--core-only] [--stage STAGE]
```

| Flag | Effect |
|------|--------|
| `--project PROJECT` | Required. Must be `fep_lean` for this catalogue |
| `--skip-infra` | Skip Stage 2 (infrastructure tests). Recommended for fep_lean since monorepo infra tests are pre-existing failures outside its scope. |
| `--skip-llm` | Skip LLM review and translation stages (8, 9) |
| `--resume` | Resume from a prior checkpoint in `output/fep_lean/.checkpoints/pipeline_checkpoint.json` |
| `--core-only` | Run only Stages 1–7 (no LLM reviews, no translations) |
| `--stage STAGE` | Run exactly one stage and exit. Valid: `setup`, `infra_tests`, `project_tests`, `analysis`, `render_pdf`, `validate`, `copy`, `llm_reviews`, `llm_translations`, `executive_report` |

**Typical fep_lean invocation**:

```bash
uv run python scripts/execute_pipeline.py --project fep_lean --core-only --skip-infra
```

Produces `output/fep_lean/pdf/fep_lean_combined.pdf` (~1.7 MB) and populates `output/fep_lean/{figures,reports,slides,web,tex,data,simulations,llm,logs}/`. Full run: **~578 s** (core-only, no LLM stages; add **order ~30–60 min** when `FEP_LEAN_GAUSS_WORKFLOWS=1` with the primary `moonshotai/kimi-k2.6` reasoning model — exact duration is provider/queue dependent; see `manuscript_vars.yaml::verify.duration_min` for the latest measured value).

### `scripts/01_run_tests.py`

```bash
uv run python scripts/01_run_tests.py --project fep_lean [--infra-only | --project-only] [--verbose]
```

Runs pytest with the monorepo's standard coverage + timeout configuration. `--project-only` runs just this project's `tests/` tree; `--infra-only` runs `tests/infra_tests/`.

### `scripts/03_render_pdf.py`

```bash
uv run python scripts/03_render_pdf.py --project fep_lean
```

Runs pandoc → xelatex on this project's `manuscript/*.md` to produce `output/fep_lean/pdf/fep_lean_combined.pdf`. Stage 5 of the template pipeline.

### `scripts/04_validate_output.py`

```bash
uv run python scripts/04_validate_output.py --project fep_lean
```

Runs output integrity validation (markdown refs, PDF existence, figure presence).

---

## Environment variables (quick index)

For the complete list with defaults, see [`configuration.md`](configuration.md). Most-used:

| Variable | Where | Quick meaning |
|----------|-------|---------------|
| `ANALYSIS_SCRIPT_TIMEOUT_SEC` | `scripts/02_run_analysis.py` (repo root) | Default **7200** s per analysis script; `unlimited` = no limit |
| `FEP_LEAN_GAUSS_WORKFLOWS` | scripts 01, 02, 04; `FEPPipeline.run` | `1` = full pipeline with Hermes + Lean; falsy = thin mode (`01_fep_*` may set `0`; `run.sh` defaults `1`) |
| `FEP_LEAN_MAX_TOPICS` | `pipeline/core.py` | Cap topics in Gauss batch |
| `HERMES_429_MAX_RETRIES` / `HERMES_NETWORK_MAX_RETRIES` / `HERMES_MAX_MODEL_ATTEMPTS` | `llm/hermes.py` | 429 and transient-transport retries per model; optional model-chain cap |
| `FEP_LEAN_REQUIRE_GAUSS` | preflight, cli.py | `1` = missing gauss is fatal |
| `FEP_LEAN_VERIFY_TIMEOUT` | `LeanVerifier` | per-sketch timeout, seconds (default 300) |
| `FEP_LEAN_LAKE_EXE` / `FEP_LEAN_LEAN_EXE` | `LeanVerifier` | explicit binary paths, bypass PATH |
| `OPENROUTER_API_KEY` / `ANTHROPIC_API_KEY` | Hermes | LLM auth |
| `HERMES_MODEL` | HermesConfig | override primary model |
| `GAUSS_HOME` | gauss/cli, runner, client | session directory root |
| `PROJECT_DIR` | orchestrator | override project root |
| `MPLBACKEND` | matplotlib (scripts force `Agg`) | headless rendering |

---

## Exit-code summary table

| Script | `0` | `1` |
|--------|-----|-----|
| `fep-lean-preflight` | all checks pass | any required check fails |
| `scripts/02_run_analysis.py` (repo root) | all project analysis scripts succeed | any script fails or missing `scripts/` |
| `01_fep_catalogue_and_figures.py` | always (check `summary.json` for status) | unhandled Python exception |
| `02_run_single_topic.py` | topic ran | topic id unknown or `status=error` |
| `03_lean_verify_only.py` | all sketches compile, or lake missing | any sketch fails or Mathlib build fails |
| `04_generate_reports.py` | report written | unhandled Python exception |
| `execute_pipeline.py` | all requested stages succeed | any stage fails |

---

## Navigation

- [← Troubleshooting](troubleshooting.md)
- [Configuration →](configuration.md)
- [API reference →](api.md)
- [← docs/README.md](README.md)
