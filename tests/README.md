# Tests

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

```bash
uv run pytest tests/ -q --cov=src --cov-fail-under=89
```

**347** tests collected (`uv run pytest tests/ --collect-only -q`) across **29** `test_*.py` modules. A small number are **live-only** (Hermes/OpenRouter or httpbin); they auto-run when `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is set and skip otherwise — set `FEP_LEAN_LIVE_TESTS=0` to force-skip in key-present environments. See [AGENTS.md](AGENTS.md).

Policy: prefer real files, real subprocesses, and `monkeypatch` for environment isolation only. See [AGENTS.md](AGENTS.md).
