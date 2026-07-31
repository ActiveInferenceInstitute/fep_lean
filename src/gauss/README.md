# fep_lean/src/gauss/

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

OpenGauss integration layer: CLI wrapper, SQLite session client, and the
per-topic orchestrator that drives one theorem through the LLM and the Lean
verifier. This is the only subpackage that owns the SQLite file
(`{GAUSS_HOME}/fep_lean_state.db`, default `~/.gauss/fep_lean_state.db`).

## Public API

### `OpenGaussClient` (`client.py`)

SQLite-backed session store. Exposes:

- `create_session(topic_id, area, lean_sketch_original) → session_id`
- `update_session(session_id, turn_index, role, content, tokens)`
- `close_session(session_id, status, hermes_success, lean_compiles)`
- `export_session(session_id)` / `export_all_sessions(source)`
- `write_artifact(session_id, payload)` / `write_bulk_jsonl(sessions, out_path)`
- `log_event(event, **kwargs)` / `get_stats()`

### Database schema (5 tables, all `CREATE TABLE IF NOT EXISTS`)

| Table | Purpose |
| ----- | ------- |
| `sessions` | One row per formalisation session (topic × run), with `status ∈ {open, success, failed, skipped}` and a tri-state `lean_compiles` column. |
| `turns` | Conversation turns (`role ∈ {system, user, assistant}`, content, token count). |
| `artifacts` | JSON artifact manifests (path + sha256 + size_bytes). |
| `logs` | Structured operation log events. |
| `hermes_cache` | LLM response cache keyed by topic + sketch + model + stage (SHA-256). |

`PRAGMA journal_mode = WAL` and `PRAGMA foreign_keys = ON` are applied at
open time. `SessionRecord` is the dataclass view returned from
`export_session` / `export_all_sessions`.

### `GaussRunner` (`runner.py`)

Per-topic orchestrator. The main entry points are:

- `run_topic(topic)` — one topic through Hermes + Lean + SQLite commit.
- `run_topics_batch(topics)` — a list of topics, honouring the prefetch flag.
- `GaussRunner.create_default(project_root)` — factory that constructs a
  runner with default `HermesConfig`, `LeanVerifier`, and `OpenGaussClient`.

### `TopicRunResult` (dataclass)

Core fields: `topic_id`, `session_id`, `success`, `status`, `hermes_success`,
`lean_compiles`, `lean_has_sorry`, `duration_s`, `error`, `workflow`
(default `verify`; `draft` / `prove` / `review` when set via
`FEP_LEAN_GAUSS_WORKFLOWS`), `stage_results` (list of per-workflow-stage
dicts for multi-stage runs).

Hermes-derived fields surfaced for downstream reporters
(`Reporter._gen_topic_md`, `output.manuscript.build_manuscript_vars`):
`explanation`, `refined_lean_sketch`, `tokens_used`, `hermes_model`,
`cache_hit`, and `hermes_lean_compiles` (True only if the **Hermes-refined**
sketch compiled directly; False covers both Hermes failure and the
baseline-fallback path where the original YAML sketch was used).
`as_dict()` returns a JSON-safe view of every field.

### `check_gauss_cli` / `workflows_enabled`

Module-level helpers in `cli.py`:

- `check_gauss_cli()` — checks the `gauss` CLI on PATH and returns a
  `(found, version)` tuple, used by stage 2 (environment validation).
- `workflows_enabled()` — returns True only when `FEP_LEAN_GAUSS_WORKFLOWS`
  is set to `1` / `true` / `yes` / `on`. Stage 3 (Gauss Sessions) is
  recorded as `status: "skipped"` when this is False.

## Prefetch mode

Set `FEP_LEAN_PREFETCH=1` to overlap Hermes on topic *n+1* with the
Lean compile of topic *n*, via a 1-thread `ThreadPoolExecutor` inside the
batch loop. Disabled by default because Hermes latency variance can occlude
Lean logs on interactive runs.

See [`AGENTS.md`](AGENTS.md) for the full wiring (Hermes + LeanVerifier +
SQLite) and the per-stage workflow preambles (`verify`, `draft`, `prove`,
`review`) used to condition the Hermes prompt.

**See also:** monorepo Cursor skill [`../../../.cursor/skills/gauss/SKILL.md`](../../../.cursor/skills/gauss/SKILL.md) (math-inc CLI vs this package vs Huawei DB).
