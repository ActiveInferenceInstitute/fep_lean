# Documentation map

- [Getting started](getting-started.md) — install, catalogue mode, and strict mode.
- [Pipeline](pipeline.md) — stages, modes, and result contract.
- [CLI reference](cli-reference.md) — canonical command surface.
- [Configuration](configuration.md) — settings and environment overrides.
- [Lean 4](lean4.md) — pinned workspace and aggregate generation.
- [Hermes](hermes.md) — HTTP client, cache, retries, and response validation.
- [OpenGauss](opengauss.md) — SQLite state and artifact persistence.
- [Testing](testing.md) — local and CI validation.
- [Cold start](cold-start-and-cleanup.md) — disposable output cleanup.
- [Theorem maturity audit](theorem-maturity-audit.md) — semantic scope review beyond compilation.
- [Quality-gate decision](quality.md) — Ruff baseline, ownership, and staged policy.
- [Test suite review](test-suite-review.md) — structure, coverage, parallelism, and anti-pattern audit.
- [Mahakala adversarial review](mahakala-review.md) — multi-wave red-team, deception detection, and persona-based review.
- [Publication](development.md) — documentation and rendered-artifact gates.

All paths in this directory resolve within this repository. Generated files are
created by `uv run fep-lean catalogue` before manuscript cross-reference checks.
