# Agent interface

The repository exposes one canonical command:

```bash
uv run fep-lean catalogue
uv run fep-lean preflight
uv run fep-lean run
```

The catalogue is the validated source in `config/topics.yaml`. The tracked Lean
aggregate is generated from `scripts/catalogue_sketches.py`. Agents must run
`fep-lean catalogue` for offline artifact work and `fep-lean preflight` before
full execution. A full result is publishable only when its JSON has
`mode: full`, `complete: true`, and `verified_topics` equal to the selected
topic count.
