# Documentation contract

All documentation is local to this checkout. Keep links relative to the file
that owns them, keep toolchain/model claims synchronized with the canonical
configuration, and mark generated values as generated data.

Run the documentation and generated-visual gates from the project root:

```bash
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
uv run python docs/theorem_ref_audit.py
uv run python docs/citation_audit.py
uv run python scripts/build_formalism_coverage.py --check
uv run python scripts/_maint_build_lean_landscape.py --check
uv run fep-lean atlas --check
uv run fep-lean dashboard --check
```

Use `uv run fep-lean catalogue` to materialize manuscript variables and the
unified appendix before checking manuscript cross-references.

`formalism-coverage.*`, `formalism-atlas.*`, and
`formal-kernel-dashboard.*` are generated projections. Edit their canonical
catalogue, relation, formal-module, or renderer owners, never the generated
bytes. The dashboard is explanatory numerical evidence and never substitutes
for Lean compilation or the declaration/axiom audit.
