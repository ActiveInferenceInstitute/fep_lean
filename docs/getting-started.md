# Getting Started with fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Paths below assume **the project root**: the directory that contains `pyproject.toml`, `src/`, and `scripts/`. In the monorepo it is usually `projects/fep_lean/` when listed in [`docs/_generated/active_projects.md`](../../../docs/_generated/active_projects.md); template CLI uses `--project fep_lean`.

## Prerequisites

| Requirement | Minimum Version | Notes |
| ------------- | --------------- | ----- |
| Python | 3.10+ | CI uses 3.12 |
| [uv](https://docs.astral.sh/uv/) | 0.5+ | Dependency and test runner (required) |
| [elan](https://github.com/leanprover/elan) + Lake | — | Required for Lean 4 verification tests and `lake build` in `lean/` |
| `OPENROUTER_API_KEY` | — | **Optional**; Hermes returns a fast failure without one, core-only mode runs fine |
| [math-inc/OpenGauss](https://github.com/math-inc/OpenGauss) `gauss` CLI | — | Optional; `gauss doctor` checks, full test suite expects it on `PATH` when tools are present |

Note: `FEP_LEAN_GAUSS_WORKFLOWS` defaults to `0` (**core-only mode**, no API key needed). Set it to `1` and provide `OPENROUTER_API_KEY` for the full Hermes + Lean batch run.

## Installation

**fep_lean** has its own [`pyproject.toml`](../pyproject.toml) and lockfile. Install its venv explicitly (recommended):

```bash
# from repository root (replace the path with your checkout location)
uv sync --directory path/to/fep_lean --extra dev
```

Or from the project directory:

```bash
cd path/to/fep_lean   # directory containing pyproject.toml
uv sync --extra dev
```

From the **repository root**, the template monorepo also uses:

```bash
uv sync
```

for root-level tools; that does not replace the `fep_lean` sync above when working on this project.

### PYTHONPATH (required for direct script execution)

When running project scripts or tests directly (not via `uv run --directory`), export:

```bash
export PYTHONPATH=projects/fep_lean/src:.:infrastructure
```

This puts (1) the project's own `src/` packages (`pipeline`, `catalogue`, `llm`, `verification`, `output`, `gauss`) first so project-local imports win over any shadowing modules, (2) the repository root for `infrastructure.*` imports, and (3) the `infrastructure/` directory so flat imports work. Without this export, direct `python scripts/...` invocations will hit `ModuleNotFoundError: llm.hermes` or `No module named 'catalogue'`. See [troubleshooting.md](troubleshooting.md) for the PYTHONPATH shadowing entry.

Optional API key (session or `~/.gauss/.env`):

```bash
export OPENROUTER_API_KEY=sk-or-...
```

## First commands

Catalogue load, validation, manuscript vars, and figures (no Gauss workflows unless you set the env flag):

```bash
# from project root
uv run python scripts/01_fep_catalogue_and_figures.py
```

### Quick verification

The fastest way to confirm your install is working end-to-end is a single-topic run:

```bash
# from project root (core-only; no API key needed)
uv run python scripts/02_run_single_topic.py --topic fep-001
```

Expected: the script loads `fep-001` from `config/topics.yaml`, runs validation + Lean verification, and exits 0. Takes ~5–10 s with a warm Mathlib cache. Use this whenever a fresh checkout, PYTHONPATH change, or Lean toolchain update should be smoke-tested before attempting a full batch.

### Full topic batch

Run **all 50 topics** through the orchestrator with Hermes + Lean verification. Set `FEP_LEAN_GAUSS_WORKFLOWS=1` to enable the full Gauss workflow inside `GaussRunner`:

```bash
# from project root (requires OPENROUTER_API_KEY for Hermes)
FEP_LEAN_GAUSS_WORKFLOWS=1 OPENROUTER_API_KEY=sk-or-... \
  uv run python scripts/01_fep_catalogue_and_figures.py
```

**Timing**: End-to-end with `FEP_LEAN_GAUSS_WORKFLOWS=1` is dominated by Hermes latency (environment-dependent). Native compilation for all rows is **`50/50`** on a green sweep against Mathlib **v4.29.0**. Without workflows (core-only mode, default), catalogue + figures are typically a few minutes.

Via the **template** analysis stage (from repo root):

```bash
uv run python scripts/02_run_analysis.py --project fep_lean
```

Stage 02 runs each project script in a subprocess with a default timeout of **7200 s** (2 h) per script (`ANALYSIS_SCRIPT_TIMEOUT_SEC`; see [configuration.md](configuration.md#monorepo-stage-02-repository-root)). For a **full** Hermes + Lean batch, set `FEP_LEAN_GAUSS_WORKFLOWS=1` (and `OPENROUTER_API_KEY`); the repo [`run.sh`](../../../run.sh) exports workflows on by default for interactive shells — bare `uv run` does not.

## Lean workspace

One-time Mathlib / Lake setup:

```bash
# from projects/fep_lean (or repo root with path adjusted)
bash scripts/_maint_bootstrap_lean_toolchain.sh
# or: cd lean && lake exe cache get && lake build
```

Toolchain preflight (`gauss doctor` when required, `lean`/`lake` versions, Mathlib `.olean` check):

```bash
# from project root
uv run fep-lean-preflight
```

Optional Lean-only sweep (all catalogue sketches):

```bash
# from project root
uv run python scripts/03_lean_verify_only.py
```

From **repository root** (same effect, if you know the path to the project):

```bash
uv run --directory path/to/fep_lean fep-lean-preflight
uv run --directory path/to/fep_lean python scripts/03_lean_verify_only.py
```

## Troubleshooting

The full guide is in [`troubleshooting.md`](troubleshooting.md) (15+ common failure modes with exact fix commands). The three issues first-run users hit most:

- **`ModuleNotFoundError: llm.hermes`** — PYTHONPATH shadowing; the top-level monorepo `llm/` package is overriding the project's `src/llm/`. Fix: `export PYTHONPATH=projects/fep_lean/src:.:infrastructure` (project src comes **first**). See [troubleshooting.md PYTHONPATH entry](troubleshooting.md#pythonpath-shadowing).
- **`ModuleNotFoundError: No module named 'catalogue'`** — your shell isn't in the project dir or is missing `PYTHONPATH`. Either `cd` to the project root or prefix commands with `uv run --directory <path-to-project>`. See [troubleshooting.md #1–#3](troubleshooting.md#1-modulenotfounderror-no-module-named-infrastructure).
- **`error: unknown identifier 'xxxx'` from Lean** — usually sandbox contention on macOS when parallel Lean processes fight the elan proxy. `LeanVerifier.verify_batch` runs with `max_workers=1` (see `src/verification/lean_verifier.py`) to prevent this. See [troubleshooting.md #11](troubleshooting.md#11-lake-env-lean-segfaults-hangs-on-macos).

---

## Cold start (wipe build outputs)

To rerun full analysis from a clean slate under this repo (no stale `output/reports/latest`, regenerated manuscript vars), follow [cold-start-and-cleanup.md](cold-start-and-cleanup.md). Typical one-liner: `rm -rf output .pytest_cache` plus removing `manuscript/manuscript_vars.yaml` and `manuscript/09z_unified_formalism_catalogue.md` if present.

---

## Outputs

- Figures: `output/figures/`
- Reports: `output/reports/run_*/`
- Manuscript variables: `manuscript/manuscript_vars.yaml`
- Unified formalism appendix (generated): `manuscript/09z_unified_formalism_catalogue.md` (often gitignored; Lean + typeset LaTeX per topic, pandoc section anchors `{#sec:catalogue-…}` / `{#sec:eqs-…}`, and displayed equations with `\label{eq:fep-NNN-k}` for `\Cref{…}` / `\eqref{…}` — see `docs/xref_audit.py`)
- SQLite (when sessions run): `{GAUSS_HOME}/fep_lean_state.db`

## Tests

```bash
# from project root
uv run pytest tests/ -q --timeout=900 --cov=src --cov-fail-under=89
```

Expected result: tests pass with coverage at or above the **89%** combined line+branch gate (`fail_under = 89` in [`pyproject.toml`](../pyproject.toml)); see [`docs/_generated/canonical_facts.md`](../../../docs/_generated/canonical_facts.md) in the monorepo for the latest collected-test count. Live API tests run automatically when `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is present; set `FEP_LEAN_LIVE_TESTS=0` to suppress them in key-present CI environments.

For the math-inc `gauss` CLI vs this project's `OpenGaussClient`, see [`opengauss.md`](opengauss.md#name-disambiguation).

Run pytest from **the project root** so `--cov=src` matches the layout in [`pyproject.toml`](../pyproject.toml). Invoking `pytest` on `tests/` via a long path from the repository root with a mismatched `--cov=` can report lower totals than the project-local run. Details: [testing.md](testing.md), [quickref.md](quickref.md).

### Documentation gates (from `docs/`)

After editing markdown under `docs/` or project-root `README.md` / `AGENTS.md`, run the four fast audits in [AGENTS.md](AGENTS.md): `check_links.py --strict --include-root`, `md_hygiene.py --strict`, `pin_audit.py`, and `xref_audit.py`. They catch broken anchors, list/header formatting drift, stale Lean or model pins in static prose, and broken manuscript `\ref` targets.

## Navigation

- [← docs/README.md](README.md)
- [Architecture →](architecture.md)
- [Configuration →](configuration.md)
- [Open Gauss notes →](opengauss.md)
