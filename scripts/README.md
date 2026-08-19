# Scripts

The public command is `uv run fep-lean`. The numbered files remain thin local
wrappers for environments that discover Python scripts automatically:

- `01_fep_catalogue_and_figures.py` → `fep-lean catalogue`
- `02_run_single_topic.py` → `fep-lean topic ID`
- `03_lean_verify_only.py` → `fep-lean verify` (Lean only; no Hermes/Gauss)
- `04_generate_reports.py` → `fep-lean report`

Maintenance sources are prefixed with `_maint_`. Regenerate YAML and the tracked
Lean aggregate after editing catalogue source:

```bash
uv run python scripts/_maint_build_topics_catalogue.py
uv run python scripts/_maint_build_fep_all_lean.py
```

Do not invoke repository-root modules or set a monorepo-specific `PYTHONPATH`;
each wrapper resolves this checkout's `src/` directory directly.
