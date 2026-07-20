# Documentation contract

All documentation is local to this checkout. Keep links relative to the file
that owns them, keep toolchain/model claims synchronized with the canonical
configuration, and mark generated values as generated data.

Run the four documentation gates from the project root:

```bash
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
```

Use `uv run fep-lean catalogue` to materialize manuscript variables and the
unified appendix before checking manuscript cross-references.
