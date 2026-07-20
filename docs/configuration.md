# Configuration

The runtime source is [`config/settings.yaml`](../config/settings.yaml).
Environment variables override secrets and operational limits.

| Setting | Purpose |
| --- | --- |
| `gauss.home` / `GAUSS_HOME` | SQLite state, exported artifacts, and logs |
| `gauss.default_model` | Hermes primary model when `hermes.model` is absent |
| `gauss.verify_lean` | Require the Lean verification stage |
| `output.root` | Generated figures and reports root |
| `hermes.model` | Primary Hermes model |
| `hermes.fallback_models` | Ordered configured model chain |
| `hermes.timeout_s` | Request deadline |
| `hermes.cache_ttl_hours` | SQLite response-cache lifetime |

Important environment variables include `OPENROUTER_API_KEY`,
`ANTHROPIC_API_KEY`, `HERMES_API_BASE`, `HERMES_MODEL`,
`FEP_LEAN_LAKE_EXE`, `FEP_LEAN_LEAN_EXE`, `FEP_LEAN_VERIFY_TIMEOUT`,
`FEP_LEAN_MAX_TOPICS`, and `FEP_LEAN_OUTPUT_ROOT`.

`fep-lean preflight` performs no download, build, database write, or report
write. Use `fep-lean setup` when dependency acquisition is required.
