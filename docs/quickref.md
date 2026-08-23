# Quick reference

```bash
uv sync --extra dev
uv run fep-lean catalogue
uv run fep-lean setup
uv run fep-lean verify
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
uv run fep-lean atlas --check
uv run fep-lean dashboard --check
uv run fep-lean preflight
uv run fep-lean run --topic fep-001
```

The full test and documentation gates are listed in
[`testing.md`](testing.md). Generated output lives under `output/`; manuscript
variables and the unified appendix live under `manuscript/`.
