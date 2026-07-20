# Testing

Run from the project root:

```bash
uv run pytest tests/ -q --cov=src --cov-fail-under=89
```

The suite uses real temporary files, SQLite databases, subprocesses, and local
HTTP servers. Environment variables isolate secrets and expensive external
integration tests; they do not manufacture successful execution results.

Required release gates are:

```bash
uv run python scripts/_maint_build_fep_all_lean.py
uv run pytest tests/ -q --cov=src --cov-fail-under=89
uv run python docs/check_links.py --strict --include-root
uv run python docs/md_hygiene.py --strict
uv run python docs/pin_audit.py
uv run python docs/xref_audit.py
```

Full Lean and Hermes validation additionally requires the pinned toolchain,
Mathlib build, OpenGauss, and credentials; `fep-lean preflight` reports each
missing capability without modifying the workspace.
