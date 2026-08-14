# fep_lean/src/pipeline/ — Formalisation DAG Orchestrator

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

## Purpose

Coordinates the 4-stage FEP formalisation pipeline that connects [`catalogue/`](../catalogue/AGENTS.md) → [`verification/`](../verification/AGENTS.md) → [`gauss/`](../gauss/AGENTS.md) (which internally delegates to [`llm/`](../llm/AGENTS.md) and [`verification/lean_verifier.py`](../verification/lean_verifier.py)) → [`output/`](../../output/), executing topological dependencies in order. Run reporting (`Reporter.generate`) runs in the enclosing `orchestrator.run_pipeline` after `FEPPipeline.run()` returns. Two entry points are exposed for scripts: `run_pipeline()` (everything) and `run_single_topic()` (verify one target).

## Files

- `core.py` — `FEPPipeline` (the DAG executor), `PipelineResult` (final state), `StepResult` (per-stage outcome)
- `orchestrator.py` — programmatic entry points (`run_pipeline`, `run_single_topic`) and `project_root` helper
- `__init__.py` — re-exports the public API

## Public API

| Symbol | Kind | Description |
| --- | --- | --- |
| `FEPPipeline` | class | Core DAG executor; takes a catalogue and runs the four recorded stages in dependency order |
| `PipelineResult` | dataclass | Final state output of a DAG run |
| `StepResult` | dataclass | Individual stage outcome |
| `run_pipeline` | function | Programmatic entry point — runs everything for the full catalogue |
| `run_single_topic` | function | Programmatic entry point — verifies one target topic |
| `project_root` | function | Returns the absolute `Path` to `projects/fep_lean/` |

## DAG stages (four recorded in `PipelineResult.stages`)

1. **Load Catalogue** — `FEPTopicCatalogue.from_yaml(config/topics.yaml)` with optional topic/area filters (`catalogue/`)
2. **Environment Validation** — `run_validation_checks(project_root)` runs 13 checks (`verification/environment.py`)
3. **Gauss Sessions** — `GaussRunner.run_topics_batch` per topic: Hermes refine → `LeanVerifier.verify_sketch` (`lake env lean`) → SQLite session (`gauss/runner.py`, `llm/hermes.py`, `verification/lean_verifier.py`, `gauss/client.py`). Skipped when `FEP_LEAN_GAUSS_WORKFLOWS` is unset.
4. **Manuscript Artifacts** — `write_manuscript_vars` + `write_unified_formalism_appendix_markdown` + `write_all_catalogue_figures` (`output/`)

Run reporting (`Reporter.generate`) runs in the enclosing `orchestrator.run_pipeline` after `FEPPipeline.run()` returns; it is **not** a fifth `StepResult` in `PipelineResult.stages`.

## Imports

```python
from pipeline.core import FEPPipeline, PipelineResult, StepResult
from pipeline.orchestrator import run_pipeline, run_single_topic, project_root
```

## See Also

- [`README.md`](README.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../../scripts/AGENTS.md`](../../scripts/AGENTS.md) — thin script wrappers that call `run_pipeline()`
