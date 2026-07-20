# Pipeline

The pipeline has four recorded stages:

1. **Load Catalogue** — strict YAML validation and optional filters.
2. **Environment Validation** — bounded, read-only capability checks.
3. **Gauss Sessions** — full mode only: Hermes, Lean, and SQLite per topic.
4. **Manuscript Artifacts** — deterministic figures, variables, and appendix.

`Reporter.generate` runs only after a complete pipeline result. Full mode never
turns an unavailable service into a successful-looking partial run. Catalogue
mode records the Gauss stage as `not_run`, writes a report marked
`catalogue`, and reports zero verified topics.

## Programmatic use

```python
from pipeline.orchestrator import run_pipeline, run_single_topic

offline = run_pipeline(mode="catalogue")
strict = run_pipeline(mode="full", topic_filter=["fep-001"])
single = run_single_topic("fep-001", mode="full")
```

The report contains `summary.json`, stage Markdown, a verification manifest,
and SHA-256 artifact hashes. The in-memory result remains the source for the
report, so serialized topic fields must stay aligned with `TopicRunResult`.
