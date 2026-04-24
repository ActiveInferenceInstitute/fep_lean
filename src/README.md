# fep_lean/src/

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

This directory contains the six Python subpackages that drive the FEP Lean
pipeline. The layer runs end-to-end per-topic formalisation sessions (LLM
explanation + Lean 4 compilation + SQLite session capture), and emits the
artifacts consumed by the manuscript stage (`manuscript_vars.yaml`, figures,
per-topic markdown reports).

## Subpackages

| Subpackage | Role | Key public API |
| ---------- | ---- | -------------- |
| [`catalogue/`](catalogue/) | Load the 50-topic YAML catalogue into frozen `TopicEntry` rows. | `FEPTopicCatalogue`, `TopicEntry`, `FEPTopicCatalogue.from_yaml()` |
| [`verification/`](verification/) | Lean 4 toolchain and workspace checks. | `LeanVerifier`, `VerifyResult`, `run_validation_checks` (13 checks), `fep-lean-preflight` |
| [`llm/`](llm/) | Hermes LLM explainer (OpenRouter / Anthropic) with a 6-model fallback chain. | `HermesConfig`, `HermesExplainer`, `HermesResult`, `HermesAPIError` |
| [`gauss/`](gauss/) | SQLite-backed session store and per-topic orchestrator. | `OpenGaussClient`, `SessionRecord`, `GaussRunner`, `TopicRunResult` |
| [`output/`](output/) | Pure side-effect artifact generators: figures, manuscript vars, reports. | `write_manuscript_vars`, `write_all_catalogue_figures`, `Reporter`, `ReportPaths` |
| [`pipeline/`](pipeline/) | 4-stage FEP pipeline DAG + entry-point wrappers. | `FEPPipeline`, `PipelineResult`, `StepResult`, `run_pipeline`, `run_single_topic` |

## Package boundaries

- `catalogue/` has **no sibling dependencies** — it is the source-of-truth data layer.
- `verification/` depends only on `gauss.cli` (for `check_gauss_cli`) and the
  stdlib; it does not import the LLM or pipeline layer.
- `llm/` imports `catalogue.topics.TopicEntry` under `TYPE_CHECKING` only; at
  runtime it depends only on `urllib` and `yaml`.
- `gauss/` wires `llm/` + `verification/` + `catalogue/` into a per-topic
  orchestration loop; this is the only module that owns the SQLite file.
- `output/` reads `catalogue/` and the `PipelineResult` / `TopicRunResult`
  dataclasses produced upstream; it never runs LLM or Lean jobs itself.
- `pipeline/` is the top-level DAG: it composes all five sibling packages and
  exposes `run_pipeline()` / `run_single_topic()` for the Stage-02 analysis
  scripts and interactive CLIs.

## Import convention

Internal modules prefer qualified subpackage paths, e.g.

```python
from catalogue.topics import FEPTopicCatalogue
from verification.lean_verifier import LeanVerifier
from gauss.runner import GaussRunner
```

The package root (`src/__init__.py`) re-exports every public symbol for
backward compatibility, but new code should import from the subpackage path.

See [`AGENTS.md`](AGENTS.md) for the full export list, contract notes, and
run-time wiring. The 4 recorded pipeline stages are documented in
[`pipeline/README.md`](pipeline/README.md): Load Catalogue → Environment
Validation → Gauss Sessions → Manuscript Artifacts.
