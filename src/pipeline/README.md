# fep_lean/src/pipeline/

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

Top-level 4-stage FEP formalisation DAG orchestrator. Composes
[`catalogue/`](../catalogue/), [`verification/`](../verification/),
[`gauss/`](../gauss/), and [`output/`](../output/) into a single
`FEPPipeline.run()` call that produces a `PipelineResult`.

## Public API

| Symbol | Role |
| ------ | ---- |
| `FEPPipeline` | The 4-stage DAG (`core.py`). Construct with `FEPPipeline(project_root)`, run with `.run(topic_filter=..., area_filter=...)`. |
| `PipelineResult` | Dataclass returned by `.run()`. Holds `status`, `total_duration`, `run_dir`, `stages: list[StepResult]`, `lean_stats`, `topic_results: list[TopicRunResult]`. `.steps` is an alias for `.stages`. |
| `StepResult` | One stage record: `name`, `status ∈ {ok, warning, error, skipped}`, `message`, `duration_s`, `payload`, `error`. |
| `run_pipeline` | Thin wrapper (`orchestrator.py`) used by Stage-02 scripts. Runs `FEPPipeline.run()`, then `Reporter.generate(result)`. |
| `run_single_topic` | Same wrapper, restricted to one topic id. |

## The four recorded stages

`FEPPipeline.run()` appends exactly four `StepResult` rows to
`PipelineResult.stages`:

1. **Load Catalogue** — calls `FEPTopicCatalogue.from_yaml()`, applies
   `area_filter` / `topic_filter`, and caps at `FEP_LEAN_MAX_TOPICS` when
   set. Emits `status: "error"` if the YAML is missing or empty.
2. **Environment Validation** — runs `verification.environment.run_validation_checks`
   (13 checks). Emits `status: "warning"` if any check fails soft, `status:
   "error"` if a hard dependency is missing.
3. **Gauss Sessions** — per-topic `GaussRunner.run_topic()` loop. Emits
   `status: "skipped"` when `FEP_LEAN_GAUSS_WORKFLOWS` is unset / `0`, and
   otherwise one `TopicRunResult` per topic is appended to
   `PipelineResult.topic_results`.
4. **Manuscript Artifacts** — writes `manuscript_vars.yaml`, the unified
   formalism appendix (`09z_unified_formalism_catalogue.md`: Lean + LaTeX per topic; `{#sec:…}` + `equation` / `\label{eq:…}`),
   and the nine catalogue figures via `output/`. Stage 4 may overlap
   manuscript-vars + that appendix with
   figure rendering via `ThreadPoolExecutor(max_workers=2)`; inside figure
   rendering, `write_all_catalogue_figures` fans out to
   `ProcessPoolExecutor` (spawn).

Run reporting (`output.reporter.Reporter.generate`) runs in
`orchestrator.run_pipeline` **after** `FEPPipeline.run()` returns — it is
*not* a fifth entry in `PipelineResult.stages`.

## Entry points

```python
from pipeline.orchestrator import run_pipeline, run_single_topic

# Full catalogue (or a subset)
result = run_pipeline(area_filter="ActiveInference")

# One topic
result = run_single_topic("fep-008")
```

Both entry points respect `FEP_LEAN_GAUSS_WORKFLOWS`; when unset, stage 3
is skipped and `topic_results` stays empty.

See [`AGENTS.md`](AGENTS.md) for the full stage contract and the env-var
surface (`FEP_LEAN_MAX_TOPICS`, `FEP_LEAN_FIGURES_MP`,
`FEP_LEAN_PREFETCH`).
