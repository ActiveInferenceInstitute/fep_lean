# fep_lean/src/catalogue/ — FEP Topic Catalogue Data Model

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

## Purpose

Loads the canonical YAML-backed catalogue of FEP theorems (`config/topics.yaml`) into immutable in-memory dataclasses. This is the data-model layer — every other subpackage (`gauss/`, `llm/`, `pipeline/`, `verification/`, `output/`) consumes catalogue entries through these types.

## Files

- `topics.py` — `TopicEntry` (frozen dataclass for a single theorem row) and `FEPTopicCatalogue` (in-memory catalogue loaded from YAML)
- `__init__.py` — re-exports `TopicEntry`, `FEPTopicCatalogue`

## Public API

| Symbol | Kind | Description |
| --- | --- | --- |
| `TopicEntry` | frozen dataclass | One catalogue row: `id`, `title`, `area`, `mathlib`, `mathlib_status`, `nl`, `lean_sketch`, `latex_equations` (optional tuple of display-math strings, one per Lean theorem, maintained next to `SKETCHES` in `scripts/catalogue_sketches.py`); property `lean_chars` |
| `FEPTopicCatalogue` | class | Holds the parsed catalogue; methods: `from_yaml(path)`, `summary()` → counts by area/maturity |

## Imports

```python
from catalogue.topics import FEPTopicCatalogue, TopicEntry

# or via the backward-compat shim at the package root
from fep_lean import FEPTopicCatalogue, TopicEntry
```

## See Also

- [`README.md`](README.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../../config/topics.yaml`](../../config/topics.yaml)
