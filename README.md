# FEP_Lean — Lean 4 Formalization of the Free Energy Principle

> **Release v1.0.0** (2026-04-24) · DOI [10.5281/zenodo.19699234](https://doi.org/10.5281/zenodo.19699234) · License [CC BY 4.0](LICENSE)
>
> **Cite as:** Friedman, D. A. (2026). *Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics.* Active Inference Journal. Zenodo. <https://doi.org/10.5281/zenodo.19699234>
>
> **Upstream template:** this project is produced and continuously re-verified via the [`docxology/template`](https://github.com/docxology/template) monorepo, which injects validated package- and manuscript-level metadata at render time.
>
> **Release PDF:** [`fep_lean_v1_04-24-2026.pdf`](fep_lean_v1_04-24-2026.pdf) — 168 pages, 1.82 MB, 50/50 `sorry`-free against pinned Lean 4.29.0 / Mathlib 4.29.0.

---

**Version**: v1.0.0 | **Last Updated**: 2026-04-24 — from the project root, `uv run pytest tests/ --collect-only -q` → **347** tests collected; full `uv run pytest tests/` targets **≥89%** combined line+branch coverage on `src/` (see [`tests/AGENTS.md`](tests/AGENTS.md) for the test census)

**Headline (native verify)**: **`50/50`** catalogue sketches compile sorry-free under `lake env lean` with Mathlib **v4.29.0** / Lean **v4.29.0** (see `lean/lean-toolchain`). Hermes timings vary with `FEP_LEAN_GAUSS_WORKFLOWS` and API keys. First checkout: `bash projects/fep_lean/scripts/_maint_bootstrap_lean_toolchain.sh` or `uv run python scripts/00_setup_environment.py --project fep_lean`.

## What it is

A research project with **50** curated topics in [`config/topics.yaml`](config/topics.yaml) (FEP, Active Inference, Bayesian mechanics, information geometry, thermodynamics). Topic Lean sketches are defined in [`scripts/catalogue_sketches.py`](scripts/catalogue_sketches.py) (SSOT); `config/topics.yaml` is regenerated from it via [`scripts/_maint_build_topics_catalogue.py`](scripts/_maint_build_topics_catalogue.py). Each topic has 4–5 Lean 4 theorems (214 total) wrapped in namespaces. Python tooling syncs the catalogue into manuscript variables, figures, and optional report bundles. The manuscript (`manuscript/`) produces a full academic paper (PDF, HTML, slides) via pandoc + XeLaTeX.

**Open Gauss** here is the **[math-inc/OpenGauss](https://github.com/math-inc/OpenGauss)** command-line tool (`gauss`). Tests and CI run `gauss doctor` and `lake build` — no shell shims.

## Prerequisites

On `PATH`: **`gauss`**, **`lake`**, **`lean`** (install via Open Gauss installer + [elan](https://github.com/leanprover/elan)). Pin the toolchain with `lean/lean-toolchain` and run `lake build` in `lean/` at least once.

## Quick start

```bash
# From the fep_lean project root:
uv sync --extra dev   # pytest / pytest-timeout when using project-local env
uv run pytest tests/ --cov=src --cov-fail-under=89
```

From monorepo root (after root `uv sync`), run tests **from the project directory** so coverage resolves against `src/` as intended:

```bash
cd <path-to-fep_lean> && uv run pytest tests/ --cov=src --cov-fail-under=89
```

Toolchain smoke check before long runs: `uv run fep-lean-preflight` (see `pyproject.toml` console script).

Template pipeline (from repo root):

```bash
uv run python scripts/02_run_analysis.py --project fep_lean
```

`scripts/01_fep_catalogue_and_figures.py` sets `FEP_LEAN_GAUSS_WORKFLOWS=0` unless `FEP_LEAN_LIVE_TESTS=1` (thin catalogue + figures + vars by default).

## Environment

| Variable | Meaning |
| -------- | ------- |
| `FEP_LEAN_REQUIRE_GAUSS` | When set, validation fails if `gauss` / `gauss doctor` is missing or fails |
| `FEP_LEAN_GAUSS_WORKFLOWS` | When truthy, `FEPPipeline` runs **Gauss Sessions** (Hermes + per-topic `lake env lean` + SQLite), not a standalone whole-tree `lake build` |
| `FEP_LEAN_PREFETCH` | When truthy, `GaussRunner` may overlap Hermes for the next topic with Lean verify on the current topic (`verify` workflow, ≥2 topics); see [AGENTS.md](AGENTS.md) |
| `FEP_LEAN_FIGURES_MP` | Set `0` to force serial matplotlib figure generation (default: process pool with spawn in `output/figures.py`) |
| `HERMES_429_MAX_RETRIES` | Hermes: retries after HTTP 429 on the current model (default **2**); see [docs/hermes.md](docs/hermes.md) |
| `HERMES_NETWORK_MAX_RETRIES` | Hermes: retries after transient OpenRouter/stream drops (`IncompleteRead`, etc.) on the current model (default **2**) |
| `PROJECT_DIR` | Optional override for project root (tests / template injection) |

Full Hermes / Gauss env list: [docs/configuration.md](docs/configuration.md#environment-variables-complete-list).

## Layout

- `src/` — catalogue, validation (`environment`, `lean_verifier`, `preflight`), figures, orchestrator, Gauss + Hermes
- `lean/` — minimal Lake package (`lake build` in normal analysis/tests)
- `manuscript/` — paper source and `config.yaml`
- `output/` — generated figures, reports (disposable)
- `docs/` — deeper technical notes

## Cold start (clear intermediates)

To force the **next** `./run.sh` / full analysis to recreate reports, figures, and manuscript injection from scratch, remove disposable paths documented in **[docs/cold-start-and-cleanup.md](docs/cold-start-and-cleanup.md)** (`output/`, optional `manuscript_vars.yaml`, `09z_unified_formalism_catalogue.md`, pytest cache; remove legacy `09z_appendix_b_lean_catalogue.md` / `09zc_appendix_c_lean_equations.md` if present). Optional: wipe `GAUSS_HOME` SQLite for a Hermes/session cold slate, or `lean/.lake/` only if you need a Mathlib rebuild.

See [AGENTS.md](AGENTS.md) for contracts and check names.

## Cursor / agents (Gauss + Lean)

For the in-repo OpenGauss client and Hermes assistant layer, see [`src/gauss/`](src/gauss/) and [`src/llm/hermes.py`](src/llm/hermes.py). The legacy monorepo Cursor "gauss" skill at `.cursor/skills/gauss/SKILL.md` was removed; current ground truth lives in this project's [docs/hermes.md](docs/hermes.md) and [docs/pipeline.md](docs/pipeline.md).

## Contributing and tests

- **Setup, first runs, troubleshooting**: [docs/getting-started.md](docs/getting-started.md)
- **Test policy, coverage gate (`--cov=src`), live-only tests**: [docs/testing.md](docs/testing.md)
- **Developer loop, CI, lint**: [docs/development.md](docs/development.md)
- **Manuscript conventions** (placeholders, Appendix B, no duplicate Lean fences): [manuscript/AGENTS.md](manuscript/AGENTS.md)

Run the suite from the project root so coverage matches `pyproject.toml` (see [quickref](docs/quickref.md)).

## Project Location

Authoritative discovery list: [`docs/_generated/active_projects.md`](../../docs/_generated/active_projects.md). When `fep_lean` is under `projects/`, `./run.sh` and `scripts/01_run_tests.py --project fep_lean` apply. A copy may live under `projects_in_progress/` until promoted; internal paths stay the same relative to the project root.
