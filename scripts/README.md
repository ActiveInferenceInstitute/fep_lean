# Scripts

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Entry points for automation. Primary: `01_fep_catalogue_and_figures.py` (template analysis stage).

## Recommended (from project root)

```bash
cd projects/fep_lean
uv sync --extra dev
uv run fep-lean-preflight   # optional: gauss / lean / lake / Mathlib
uv run python scripts/01_fep_catalogue_and_figures.py
uv run python scripts/02_run_single_topic.py fep-001
# or: uv run python scripts/02_run_single_topic.py --topic fep-001
uv run python scripts/03_lean_verify_only.py
uv run python scripts/04_generate_reports.py
```

`uv run` uses this package’s `pyproject.toml` (`pythonpath = src`). Scripts that import `infrastructure.*` are normally run through the **template** `02_run_analysis.py --project fep_lean`, which extends `PYTHONPATH`.

## From repository root (template)

```bash
uv run python scripts/02_run_analysis.py --project fep_lean
```

## Manual `PYTHONPATH` (advanced)

From the monorepo root, if you must invoke a script directly:

```bash
PYTHONPATH=.:infrastructure:projects/fep_lean/src \
  python3 projects/fep_lean/scripts/02_run_single_topic.py fep-003
```

## Maintenance scripts

These scripts are excluded from the automated pipeline (underscore prefix) and must be run manually.

| Script | Usage |
|--------|-------|
| `_inject_manuscript_vars.py` | Injects all `manuscript_vars.yaml` values into `{{variable}}` placeholders across manuscript/*.md. Run with `--dry-run` first to preview. Skips: `09z_unified_formalism_catalogue.md`, `AGENTS.md`, `README.md`, `preamble.md`. |
| `_maint_build_topics_catalogue.py` | Regenerate `config/topics.yaml` from `METADATA` + `SKETCHES`; requires `--apply`. |
| `_maint_filter_topics.py` | Destructive subset filter; dry-run by default, requires `--ids` and `--apply`. |
| `_maint_fix_manuscript_counts.py` | Rewrite hard-coded topic totals in markdown (`--total 50`). |

```bash
# Example: inject with preview
uv run python scripts/_inject_manuscript_vars.py --dry-run

# Example: apply injection
uv run python scripts/_inject_manuscript_vars.py
```

See [AGENTS.md](AGENTS.md).
