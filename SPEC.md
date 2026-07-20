# fep_lean functional specification

**Version:** 1.0.0

## Scope

The project validates a 50-topic YAML catalogue against a pinned Lean 4.29.0
and Mathlib 4.29.0 workspace. It can also call the configured Hermes service,
persist each session in SQLite, and generate deterministic manuscript and report
artifacts.

## Execution modes

### `catalogue`

This mode performs strict YAML/schema/source-parity validation and generates
offline figures, manuscript variables, the unified appendix, and a report. It
records `verified_topics: 0` and `capabilities.verification: false`.

### `full`

This is the default for the programmatic API and requires every configured
capability: `gauss doctor`, the exact Lean/Lake pins, a complete Mathlib build,
writable GAUSS_HOME, and Hermes credentials. It executes one Hermes + Lean +
SQLite session per selected topic. A topic succeeds only when the Hermes-derived
sketch compiles without proof holes. Any failed capability or topic makes the
pipeline incomplete and prevents a successful report.

## Public API

```python
from pipeline.core import FEPPipeline
from pipeline.orchestrator import run_pipeline, run_single_topic

result = run_pipeline(mode="catalogue")
result = run_pipeline(mode="full", topic_filter=["fep-001"])
result = run_single_topic("fep-001", mode="full")
```

`PipelineResult` exposes `mode`, `complete`, `catalogue_topics`,
`verified_topics`, `capabilities`, `failure_reason`, `stages`, and
`topic_results`. `TopicRunResult` records both the refined sketch and its
`verification_source`; no result is silently substituted or relabeled.

## Validation

`run_validation_checks(project_root, mode=...)` is read-only. It never downloads
Mathlib, invokes a build, creates a database, or writes a report. The explicit
`fep-lean setup` command performs dependency acquisition and `lake build` with a
bounded timeout.

The catalogue loader rejects missing fields, wrong row counts, duplicate or
out-of-order IDs, unsupported areas/statuses, empty theorem bodies, mismatched
equation counts, and divergence from `scripts/catalogue_sketches.py`.

## Artifacts

Successful runs write a timestamped report containing Markdown, JSON, a
verification manifest, and SHA-256 hashes. Manuscript generation writes
`manuscript/manuscript_vars.yaml` and
`manuscript/09z_unified_formalism_catalogue.md`. These generated files are
validated before publication and are not evidence of verification unless the
run mode is `full` and `complete` is true.
