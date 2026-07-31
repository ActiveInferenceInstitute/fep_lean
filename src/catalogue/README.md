# fep_lean/src/catalogue/

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

Data-model layer for the FEP theorem catalogue. Loads
[`config/topics.yaml`](../../config/topics.yaml) into frozen `TopicEntry` rows
held by an in-memory `FEPTopicCatalogue`. This subpackage has **no sibling
dependencies**: every other module in `src/` reads from it, but nothing here
reads from them.

## Public API

### `TopicEntry` (frozen dataclass)

One catalogue row. Fields:

| Field | Type | Purpose |
| ----- | ---- | ------- |
| `id` | `str` | Topic identifier, e.g. `fep-001`. |
| `title` | `str` | Human-readable theorem title. |
| `area` | `str` | One of the five canonical areas (FEP, ActiveInference, BayesianMechanics, InfoGeometry, Thermodynamics). |
| `mathlib` | `str` | Primary Mathlib4 import hint (e.g. `MeasureTheory.Measure.MeasureSpace`). |
| `mathlib_status` | `str` | One of `real` \| `partial` \| `aspirational`. All 50 rows are currently `real`. |
| `nl` | `str` | Natural-language anchor used by the Hermes prompt and per-topic reports. |
| `lean_sketch` | `str` | Canonical Lean 4 sketch body (wrapped in a `namespace FEPNNN ... end FEPNNN`). |

The `lean_chars` computed property returns `len(lean_sketch)` and is used by
the catalogue figure generator (`output/figures.py`) for the Lean-size
distribution plots.

### `FEPTopicCatalogue`

In-memory view of `config/topics.yaml`.

```python
from catalogue.topics import FEPTopicCatalogue

cat = FEPTopicCatalogue.from_yaml()  # uses project-root / config / topics.yaml
assert len(cat.topics) == 50
summary = (
    cat.summary()
)  # {'total_topics': 50, 'areas': {...}, 'maturity': {...}, 'area_maturity': {...}}
```

`from_yaml(path=None)` resolves `path` explicitly when given, else walks two
parents from this file to `<project>/config/topics.yaml`.

`summary()` returns a dict with total topic count, per-area counts sorted by
area name, global maturity tallies (over `real` / `partial` / `aspirational`),
and per-area maturity tallies. Rows with unknown maturity are normalised to
`partial` to keep the tallies self-consistent.

## Catalogue facts

- **50 topics** across **5 areas**: FEP = 14, ActiveInference = 11,
  BayesianMechanics = 10, InfoGeometry = 8, Thermodynamics = 7.
- All 50 rows are `mathlib_status: real` and compile clean under Lean **4.29.0**
  + Mathlib **v4.29.0** (zero `sorry`, zero errors).
- Source-of-truth for the Lean bodies is
  [`scripts/catalogue_sketches.py`](../../scripts/catalogue_sketches.py) (the
  `SKETCHES` dict). `tests/test_catalogue_sketches_ssot.py` enforces that
  `config/topics.yaml` mirrors it.

See [`AGENTS.md`](AGENTS.md) for the import-contract notes and the
catalogue-extension workflow (add a topic in three places, regenerate YAML,
run the SSOT test, then the compile test).
