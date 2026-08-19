# fep_lean/src/gauss/ — OpenGauss Integration Layer

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

## Purpose

OpenGauss is the FEP project's persistence + orchestration layer for theorem-proving sessions. This subpackage provides three things:

1. A thin wrapper around the external `gauss` CLI (`check_gauss_cli`, `workflows_enabled`)
2. A SQLite-backed session client (`OpenGaussClient`, `SessionRecord`) that records topics, conversation turns, and verifier logs
3. The orchestrator (`GaussRunner`) that ties the LLM (`llm/hermes.py`) and the Lean checker (`verification/lean_verifier.py`) together so that one topic can be formalised end-to-end

## Files

- `cli.py` — CLI helpers: runs `gauss doctor` and inspects whether heavy Gauss steps are enabled
- `client.py` — `OpenGaussClient` (SQLite database client for topics/turns/logs) and `SessionRecord` (open-session data structure)
- `runner.py` — `GaussRunner` (the orchestrator that runs topics through the LLM then Lean) and `TopicRunResult` (outcome dataclass)
- `__init__.py` — re-exports the public API listed below

## Public API

| Symbol | Kind | Description |
| --- | --- | --- |
| `check_gauss_cli` | function | Runs `gauss doctor` and reports availability |
| `workflows_enabled` | function | Returns whether heavy Gauss workflows are enabled |
| `OpenGaussClient` | class | SQLite client for topics, turns, and logs |
| `SessionRecord` | dataclass | Open session metadata |
| `GaussRunner` | class | Topic-by-topic orchestrator (LLM → Lean) |
| `TopicRunResult` | dataclass | Outcome of one formalisation run |

## Imports

```python
from gauss.client import OpenGaussClient, SessionRecord
from gauss.runner import GaussRunner, TopicRunResult
from gauss.cli import check_gauss_cli, workflows_enabled
```

## See Also

- [`README.md`](README.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../llm/AGENTS.md`](../llm/AGENTS.md) — Hermes explainer used by `GaussRunner`
- [`../verification/AGENTS.md`](../verification/AGENTS.md) — Lean verifier used by `GaussRunner`
