# Cold start and cleanup — fep_lean

**Version**: v1.0.0 | **Last Updated**: July 2026

Use this when you want the **next** `./run.sh` or `scripts/02_run_analysis.py --project fep_lean` pass to behave like a **fresh** end-to-end run: no stale reports, no old `latest` symlink, no cached test metadata under the project tree.

## What you can always delete (project tree only)

These paths are **regenerated** by the pipeline, tests (with `tmp_path`), or are ephemeral. They are listed in [`.gitignore`](../.gitignore).

| Path | Role | After delete |
|------|------|--------------|
| `output/` | Figures, `reports/run_*`, `latest` symlink, ad-hoc logs, `.cache/` | Recreated on next analysis / Reporter run |
| `manuscript/manuscript_vars.yaml` | Injected metrics from last pipeline | Rewritten in **Manuscript Artifacts**; raw manuscript `{{…}}` shows until regenerated |
| `manuscript/09z_unified_formalism_catalogue.md` | Auto-generated B+C: Lean and typeset LaTeX per topic (`{#sec:…}` + `equation` / `\label{eq:…}`) | Rewritten with `write_unified_formalism_appendix_markdown` |
| `manuscript/09z_appendix_b_lean_catalogue.md` / `09zc_…` | obsolete (older pipeline) | Remove if present; no longer written |
| `.pytest_cache/` | Pytest node id cache | Harmless; recreated on next `pytest` |
| `__pycache__/`, `*.egg-info/` | Python bytecode / install metadata | Recreated by interpreter / `uv sync` |
| `gauss_pf2/`, `gauss_prefetch/`, `gauss_grace/` | Test scratch dirs (belt-and-suspenders ignore) | Safe if present |

**One-shot cleanup from project root** (`projects/fep_lean/`):

```bash
rm -rf output .pytest_cache
rm -f manuscript/manuscript_vars.yaml \
      manuscript/09z_unified_formalism_catalogue.md \
      manuscript/09z_appendix_b_lean_catalogue.md \
      manuscript/09zc_appendix_c_lean_equations.md
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

Do **not** delete `config/topics.yaml`, `scripts/catalogue_sketches.py`, `lean/lakefile.lean`, or `lean/lean-toolchain` — they are source of truth.

**After a wipe**, internal doc links and PDF placeholder resolution expect `manuscript/manuscript_vars.yaml` plus the unified formalism appendix `09z_unified_formalism_catalogue.md` to exist again. Either run the full analysis / Manuscript Artifacts stage, or regenerate **catalogue-only** artifacts without Hermes (from `projects/fep_lean/`):

```bash
PYTHONPATH=src:. uv run python -c "
from pathlib import Path
from catalogue.topics import FEPTopicCatalogue
from output.manuscript import (
    write_manuscript_vars,
    write_unified_formalism_appendix_markdown,
)
root = Path('.').resolve()
c = FEPTopicCatalogue.from_yaml()
write_manuscript_vars(root, c)
write_unified_formalism_appendix_markdown(root, c)
"
```

That repopulates YAML from the checked-in catalogue and default summary fixtures; it does **not** replace a full verifier run’s `verification_manifest.json` metrics — run the pipeline with workflows for live `verify.*` fields.

## Optional: Gauss / Hermes state (outside this directory)

Session and LLM cache live under **`GAUSS_HOME`** (default `~/.gauss`), not under `projects/fep_lean/`.

| Location | When to clear |
|----------|----------------|
| `{GAUSS_HOME}/fep_lean_state.db` | Wipe for a **full** cold Hermes + session history (destructive) |
| Hermes cache table / TTL | Responses keyed by topic + sketch + model; change sketch or model or wait for TTL |

For a **project-only** clean slate you do **not** need to touch `GAUSS_HOME`; clearing `output/` and regenerating manuscript artifacts is enough for reports and figures.

## Optional: Lean / Mathlib build cache (`lean/.lake/`)

| Action | Effect |
|--------|--------|
| Keep `lean/.lake/` | Fast `lake env lean` after first `lake build` / `lake exe cache get` |
| Delete `lean/.lake/` | Next build re-fetches Mathlib and rebuilds (long cold start; use only if cache corruption suspected) |

Also gitignored: `lean/build/`, `lean/FepSketches/` — safe to remove; Lake recreates as needed.

## `run.sh` and full analysis

From the **repository root**, `./run.sh` discovers active projects (including `fep_lean` under `projects/`). For a **full** Hermes + Lean + reports path:

- Export or rely on `run.sh` default: `FEP_LEAN_GAUSS_WORKFLOWS=1` (see root `run.sh`).
- Ensure `OPENROUTER_API_KEY` (or your configured provider) is set if you want live Hermes.

After clearing the rows in **What you can always delete**, run **Run Full Pipeline** (or Stage 2 analysis for `fep_lean`) so stages recreate `output/reports/run_*`, figures, and manuscript artifacts.

## Navigation

- [← Getting started](getting-started.md)
- [Troubleshooting →](troubleshooting.md)
- [Pipeline →](pipeline.md)
- [docs/README.md](README.md)
