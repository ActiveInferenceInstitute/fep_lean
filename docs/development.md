# Development Guide — fep_lean

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

## Environment setup

```bash
# From the project root (directory containing pyproject.toml)
uv sync --extra dev
uv run python -c "import sys; sys.path.insert(0, 'src'); from catalogue.topics import FEPTopicCatalogue; print('OK')"
```

For ad-hoc shell sessions (when not going through `uv run`), set `PYTHONPATH`
to cover the project `src/`, the repo root, and the monorepo `infrastructure/`
package so that imports resolve both ways:

```bash
export PYTHONPATH=projects/fep_lean/src:.:infrastructure
```

### Namespace convention for Lean sketches

Every committed sketch is wrapped in a `namespace FEPNNN ... end FEPNNN`
block keyed to the catalogue id (e.g. `namespace FEP014` for fep-014). This
isolation is load-bearing: it prevents cross-topic name collisions when
`lean/FepSketches/fep_all.lean` aggregates the whole catalogue, and it is
enforced by the verifier wrapper and by `tests/test_catalogue_sketches_ssot.py`.
Do not remove the wrappers when editing `SKETCHES` in
`scripts/catalogue_sketches.py`.

### IDE (VS Code / Cursor)

After `uv sync --extra dev`, point your editor at `.venv/bin/python` under the project root. If the **workspace** is the repository root, prefix paths with `projects/fep_lean/` (or the path where this tree lives). If the **workspace** is this project folder, use paths relative to it:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.analysis.extraPaths": [
    "src",
    "."
  ]
}
```

The `extraPaths` entry gives Pylance correct symbol resolution for `catalogue.topics`, `pipeline.core`, etc., without running tests.

---

## Development loop

```bash
# From the project root

# Docs integrity (run from docs/; see docs/AGENTS.md)
cd docs && uv run python check_links.py --strict --include-root && uv run python md_hygiene.py --strict && uv run python pin_audit.py && uv run python xref_audit.py && cd ..

# Tests (raise timeout if Lean cold-start is slow)
uv run pytest tests/ -q --timeout=900 --cov=src --cov-fail-under=89

# Single topic with workflows
export FEP_LEAN_GAUSS_WORKFLOWS=1
export OPENROUTER_API_KEY=sk-or-...
uv run python scripts/02_run_single_topic.py fep-001
```

**Full 50-topic Hermes + Lean catalogue run** (from repo root; allow long wall-clock time):

```bash
export FEP_LEAN_GAUSS_WORKFLOWS=1
export OPENROUTER_API_KEY=sk-or-...
# Optional smoke: export FEP_LEAN_MAX_TOPICS=5
# Optional: export ANALYSIS_SCRIPT_TIMEOUT_SEC=unlimited
uv run python scripts/02_run_analysis.py --project fep_lean
```

From the project root:

```bash
uv run ruff check src/
```

---

## Project layout

```text
<project-root>/
├── config/           topics.yaml, settings.yaml
├── docs/
├── lean/             Lake workspace
├── manuscript/
├── output/           generated (often gitignored)
├── scripts/          thin orchestrators + _maint_* tools
├── src/
│   ├── catalogue/
│   ├── gauss/
│   ├── llm/
│   ├── pipeline/
│   ├── verification/
│   └── output/
├── tests/
├── AGENTS.md, PAI.md, SPEC.md, README.md
└── pyproject.toml
```

---

## Adding a topic

Authoring path is **SSOT-first** (see [lean4.md](lean4.md) and [authorship-guide.md](authorship-guide.md)):

1. Add a row to `METADATA` in [`scripts/_maint_build_topics_catalogue.py`](../scripts/_maint_build_topics_catalogue.py) (id, title, area, mathlib hint, `mathlib_status`).
2. Add the Lean body to `SKETCHES` in [`scripts/catalogue_sketches.py`](../scripts/catalogue_sketches.py) — no leading `import` (verifier wraps with Mathlib + opens).
3. Regenerate YAML: from the project root, `uv run python scripts/_maint_build_topics_catalogue.py`.
4. Update Lake aggregates if required ([`lean/FepSketches/fep_all.lean`](../lean/FepSketches/fep_all.lean), etc.) and bump tests that fix topic counts / area rollups ([`tests/test_fep_topics.py`](../tests/test_fep_topics.py)).
5. Run the **SSOT check first**: `uv run pytest tests/test_catalogue_sketches_ssot.py -v`. This test is the canonical single-source-of-truth gate — it walks every row in `config/topics.yaml` and asserts that its `lean_sketch` equals the corresponding `SKETCHES[...]` entry in `scripts/catalogue_sketches.py` (including the `namespace FEPNNN ... end FEPNNN` wrapper). If it fails, regenerate the YAML and re-run rather than hand-editing.
6. Then run `tests/test_fep_topics.py` and the full suite. With Lake available, drive the full per-row sweep with `uv run python scripts/03_lean_verify_only.py` (stdout only), or enable **`FEP_LEAN_GAUSS_WORKFLOWS=1`** and use the **Gauss Sessions** stage (`GaussRunner` + `LeanVerifier`) so **`Reporter`** writes **`output/reports/run_*/verification_manifest.json`** and related run bundle files.

Hand-editing `config/topics.yaml` without updating `SKETCHES` will fail [`tests/test_catalogue_sketches_ssot.py`](../tests/test_catalogue_sketches_ssot.py) unless you mirror the same strings in both places (error-prone — prefer editing Python sources and regenerating).

---

## Modifying core modules

| Area | Path | Notes |
| ---- | ---- | ----- |
| Gauss orchestration | `gauss/runner.py` | Preserve per-topic `TopicRunResult` error capture; update `test_gauss_runner.py` |
| Hermes | `llm/hermes.py` | Prompt changes → exercise `test_hermes_explainer.py` |
| Pipeline | `pipeline/core.py` | Stage list is authoritative; update `test_pipeline.py` |
| Reports | `output/reporter.py` | Update `test_reporter.py` against `tmp_path` outputs |
| Orchestrator | `pipeline/orchestrator.py` | Template entrypoints; see `test_orchestrator*.py` |

---

## Standards

- Type hints on public APIs; prefer dataclasses for structured results.
- Tests exercise local HTTP, subprocess, and temporary-file boundaries directly.
- Use `logging.getLogger(__name__)` for library code.

---

## Script CLI notes

- **`02_run_single_topic.py`**: topic as **positional** `fep-NNN` or **`--topic`** (default `fep-008`). **`--skip-gauss`** disables Gauss workflows.
- **`03_lean_verify_only.py`**: calls **`LeanVerifier`** only; no Gauss/Hermes.
- **`_maint_filter_topics.py`**: **`--ids`** is required; dry-run is the default (omit **`--apply`**). Underscore-prefixed so the pipeline auto-discovery skips it.

---

## Troubleshooting

Quick list. See [`troubleshooting.md`](troubleshooting.md) for 15 failure modes with exact fix commands.

- **`ModuleNotFoundError: No module named 'catalogue'`** — run commands from the project root, or use `uv run --directory <project-root>`, or set `PYTHONPATH` to include `./src` relative to that root.
- **`error: unknown identifier 'xxxx'` during batch processing** — macOS ELAN sandbox deadlock from parallel `lake env lean`. `LeanVerifier.verify_batch` runs with `max_workers=1` (see `src/verification/lean_verifier.py`); do not lower this.
- **`lake build` fails on `_verify_fep-NNN_<hash>`** — stale `.olean` from a leaked verifier temp file. From the project root: `find lean/.lake/build/lib/FepSketches -name "_verify_*" -delete`.

---

## CI pattern

The GitHub Actions job **fep_lean** installs elan, runs `lake build` under the project’s `lean/` directory, installs the math-inc `gauss` CLI, then:

`uv run pytest tests/ --timeout=900 --cov=src --cov-fail-under=89`

(workdir: project root.)

## Coverage from the monorepo root

Prefer running pytest from the project root with `--cov=src`. Invoking pytest via a path like `pytest <path-to-project>/tests/` with `--cov=<path-to-project>/src` from the repository root can under-report versus the project-local run (see [testing.md](testing.md)).

---

## Navigation

- [← Testing](testing.md)
- [API reference →](api.md)
- [← docs/README.md](README.md)
