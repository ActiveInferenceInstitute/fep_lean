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
```

Claims about Lean compilation, Hermes calls, or published artifacts must be
backed by a complete `full` result and its manifest. Offline catalogue output
must be labelled as catalogue data.
