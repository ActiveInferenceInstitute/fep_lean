# `fep_lean`

The installable Python namespace for the FEP Lean catalogue and verification
pipeline.

- `catalogue/`: family-owned canonical bodies, validated registry, typed
  semantic review, package data, and deterministic coverage projections
- `formal/`: packaged foundations, leaf cross-topic compositions, import
  aggregate, and exact Lake projection
- `verification/`: pinned Lean/Lake checks, native compilation, and
  declaration/axiom auditing
- `llm/`: Hermes provider client
- `gauss/`: SQLite session storage and per-topic runner
- `pipeline/`: catalogue and strict full-mode orchestration
- `output/`: evidence receipts, reports, figures, manuscript variables,
  fail-closed rendering, the offline formalism atlas, and the formal-kernel
  validation dashboard

Use public imports such as:

```python
from fep_lean.catalogue import FEPTopicCatalogue
from fep_lean.output import (
    build_formal_kernel_dashboard,
    build_formalism_atlas,
    validate_native_lean_receipt,
)
from fep_lean.verification import LeanVerifier, run_formalism_audit
```

The wheel intentionally provides no obsolete top-level compatibility modules.
