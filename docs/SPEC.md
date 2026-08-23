# Documentation specification

Documentation is self-contained within this checkout and must describe the
current `fep-lean` CLI and pipeline contract. Every relative link must resolve
from its owning Markdown file. Generated manuscript inputs are materialized by
`uv run fep-lean catalogue` before cross-reference validation.

Required documentation checks:

```bash
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
uv run python docs/theorem_ref_audit.py
uv run python docs/citation_audit.py
uv run python scripts/build_formalism_coverage.py --check
uv run fep-lean atlas --check
uv run fep-lean dashboard --check
uv run python scripts/render_manuscript.py --check
```

Claims about catalogue compilation must be backed by a current validated
native receipt. Claims about maintained-module declarations and axioms must be
backed by the formalism audit. Claims about Hermes/OpenGauss execution must be
backed by an independently validated complete `full` result and its manifest.
Offline catalogue output must be labeled as catalogue data, and numerical
dashboard witnesses must never be described as proof evidence.
