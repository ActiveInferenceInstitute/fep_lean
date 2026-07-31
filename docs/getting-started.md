# Getting started

```bash
uv sync --extra dev
uv run fep-lean catalogue
uv run pytest tests/ -q
```

For strict verification, install the pinned Lean workspace and OpenGauss,
configure `OPENROUTER_API_KEY` or an Anthropic-compatible Hermes endpoint, then
run:

```bash
uv run fep-lean setup
uv run fep-lean verify
uv run fep-lean preflight
uv run fep-lean run
```

`verify` compiles the catalogue with Lean only and needs no Hermes credentials.
`preflight` is read-only. `setup` is the only command that downloads or builds
Lean dependencies. A failed full run returns a non-zero exit status and does
not create a successful report.
