# fep_lean/src/

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

Data model, validation, verification, and pipeline execution for the FEP Lean project.

## Directory Structure
To support isolation, reusability, and testing, the source is divided into six domain-aligned subpackages. For backward compatibility, the top-level `src/__init__.py` re-exports all major public entrypoints.

| Subpackage | Responsibility | Key Exports |
|---|---|---|
| `catalogue/` | Data model layer | `FEPTopicCatalogue`, `TopicEntry` |
| `verification/` | Lean 4 / Lake verification | `LeanVerifier`, `run_validation_checks` |
| `gauss/` | OpenGauss SQLite & Runner | `OpenGaussClient`, `GaussRunner` |
| `llm/` | LLM API interface (Hermes) | `HermesExplainer`, `HermesConfig` |
| `output/` | Artifact generation | `Reporter`, `build_manuscript_vars`, `write_all_catalogue_figures` |
| `pipeline/` | Orchestration (4-stage DAG) | `FEPPipeline`, `run_pipeline`, `run_single_topic` |

## Imports

Internal modules use qualified subpackage imports for modularity:

```python
from catalogue.topics import FEPTopicCatalogue
from verification.lean_verifier import LeanVerifier
```

With `src/` on `PYTHONPATH` (default for this project’s `uv run` and tests). Packaged installs may use the `fep_lean.*` namespace instead.

## See also

- [../AGENTS.md](../AGENTS.md)
