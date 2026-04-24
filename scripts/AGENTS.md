# fep_lean/scripts/

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Thin orchestrators. Run Python and shell helpers from the **project root** (the directory containing `pyproject.toml`), not from the repository root, unless you wrap them with `uv run --directory <path-to-this-project>`.

Stage 02 discovers every `scripts/*.py` except names starting with `_`; `01_fep_catalogue_and_figures.py` runs first. Maintenance scripts use the `_maint_*.py` prefix so they are **not** run by the pipeline.

## Scripts

| File | Role |
| ---- | ---- |
| `01_fep_catalogue_and_figures.py` | Headless matplotlib, `run_pipeline`, prints artifact paths for the manifest collector |
| `02_run_single_topic.py` | CLI → `orchestrator.run_single_topic`; **positional** `fep-NNN` or **`--topic`** (default `fep-008`); **`--skip-gauss`** sets `FEP_LEAN_GAUSS_WORKFLOWS=0` |
| `03_lean_verify_only.py` | `LeanVerifier` batch over `config/topics.yaml`; preflight `Mathlib.olean`; exits **1** if preflight or any topic fails; **no** Gauss/Hermes |
| `04_generate_reports.py` | `run_pipeline` with Gauss off: validation + manuscript artifacts + figures + `Reporter` (recomputes from YAML; not SQLite replay) |
| `_maint_bootstrap_lean_toolchain.sh` | **Canonical** Mathlib cache + `lake build FepSketches` (run from `projects/fep_lean` or via repo `scripts/00_setup_environment.py`) |
| `00_lean_mathlib_setup.sh` | Wrapper → calls `_maint_bootstrap_lean_toolchain.sh` (compatibility alias for older invocations) |
| `00b_install_opengauss_cli.sh` | Optional: install math-inc OpenGauss `gauss` CLI |
| `catalogue_sketches.py` | **`SKETCHES`**: 50 Lean bodies (`fep-001`…`fep-050`); no leading `import`; verifier prepends `Mathlib`. **`THEOREM_LATEX`**: built by `theorem_latex_signatures.build_theorem_latex_from_sketches(SKETCHES)` (one `amsmath` `aligned` block per `theorem`, with `variable` context + binders + goal). **`LATEX_EQUATIONS`**: topic lists; `assert_latex_complete` keeps counts aligned. |
| `theorem_latex_signatures.py` | Parses each sketch: namespace `variable` + theorem type before `:=`; converts Lean symbols to LaTeX. |
| `topic_latex_equations_data.py` | Re-exports `THEOREM_LATEX` from `catalogue_sketches` (backward compatibility). |
| `_maint_build_topics_catalogue.py` | Regenerate `config/topics.yaml` from `METADATA` + `SKETCHES` + `LATEX_EQUATIONS` (`assert_complete`); manual only |
| `_maint_filter_topics.py` | **Destructive** subset filter; requires **`--ids`**; **`--apply`** to write (default is dry-run print) |
| `_maint_fix_manuscript_counts.py` | Rewrite hard-coded topic totals in markdown (`--total 50`); manual only |
| `_inject_manuscript_vars.py` | One-shot: flatten `manuscript/manuscript_vars.yaml` → replace `{{key}}` placeholders in manuscript/*.md; `--dry-run` to preview without writing |

**uv console script** (see root [`pyproject.toml`](../pyproject.toml)): **`fep-lean-preflight`** → `verification.preflight:main`. Install/sync this project’s venv so the script is on `PATH` when using `uv run fep-lean-preflight`.

Shell helpers are convenience only; the template PDF pipeline does not require them.

## See also

- [../AGENTS.md](../AGENTS.md)
