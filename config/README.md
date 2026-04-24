# fep_lean/config — Configuration Reference

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

## Files

| File | Purpose |
| ---- | ------- |
| `settings.yaml` | Hermes block + project metadata (read by `HermesConfig.from_settings`); `gauss.*` / `orchestration.*` are mostly defaults or notes—see [`../docs/configuration.md`](../docs/configuration.md) |
| `topics.yaml` | **50** FEP topic definitions (`fep-001` … `fep-050`); regenerate via `scripts/_maint_build_topics_catalogue.py` if rebuilding the baseline |

## settings.yaml

Authoritative fields live in the checked-in file. Highlights:

- `project.version` should match `pyproject.toml` and `manuscript/config.yaml`.
- `hermes.*` is loaded by `HermesConfig.from_settings()` in `llm/hermes.py` (env overrides apply).
- `GAUSS_HOME` and API keys come from the environment or `~/.gauss/.env`; SQLite paths use `gauss/client.py` (defaults described in [`../docs/opengauss.md`](../docs/opengauss.md)).

## Config override examples

```bash
# From the project root

GAUSS_HOME=/tmp/test-gauss uv run python scripts/01_fep_catalogue_and_figures.py

OPENROUTER_API_KEY="" uv run python scripts/01_fep_catalogue_and_figures.py

GAUSS_LOG_LEVEL=DEBUG uv run python scripts/02_run_single_topic.py fep-001
```

## topics.yaml — Topic format

Every topic must include:

```yaml
- id: fep-NNN           # unique 001..050
  title: ...
  area: FEP             # FEP | ActiveInference | BayesianMechanics | InfoGeometry | Thermodynamics
  mathlib: ...
  mathlib_status: ...   # real | partial | aspirational
  nl: ...
  lean_sketch: |
    ...
```

## Navigation

- **AGENTS.md**: [AGENTS.md](AGENTS.md)
- **Parent project**: [../README.md](../README.md)
- **Source layout**: [../src/README.md](../src/README.md)
