# Hermes

`HermesExplainer` is a configured HTTP client. It requires credentials in full
mode and never returns a successful result without a usable Lean block.

Settings are read from `config/settings.yaml` and environment overrides. The
primary model is followed by the configured ordered chain. Transport and rate
limit retries are bounded; every model change is recorded in the topic result.

Responses are cached in the SQLite store by topic, source hash, model, and
workflow. Cache entries expire according to `hermes.cache_ttl_hours`.

`review` performs a second real Hermes request after the refined sketch has
compiled. `draft` and `prove` remain explicit workflow choices and are never
silently converted to another workflow.
