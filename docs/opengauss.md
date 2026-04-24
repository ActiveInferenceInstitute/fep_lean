# Open Gauss (math-inc) + SQLite Session Store — fep_lean

**Version**: v0.7.1 | **Status**: Active | **Last Updated**: April 2026

---

## Name Disambiguation

| Name | What it is |
| ---- | ---------- |
| **math-inc Open Gauss** | Open-source Lean assistant CLI: [github.com/math-inc/OpenGauss](https://github.com/math-inc/OpenGauss). This is what `fep_lean` refers to for the `gauss` CLI. |
| **`OpenGaussClient`** | [`src/gauss/client.py`](../src/gauss/client.py) — SQLite-backed session store (not the `gauss` binary). |
| **Huawei OpenGauss** | A database product — **not** used here. |

---

## What the Template Does with the `gauss` CLI

1. **`gauss doctor`** — If the `gauss` executable is on `PATH`, [`gauss/cli.py`](../src/gauss/cli.py) runs it (120s timeout). Exit code 0 is required when `FEP_LEAN_REQUIRE_GAUSS=1`.
2. **Strict mode** — `FEP_LEAN_REQUIRE_GAUSS=1` causes missing `gauss` or a failed `doctor` run to fail `run_validation_checks` (check #1 `math_inc_gauss_cli`).
3. **Artifact** — On success, optional `output/reports/gauss_doctor_last.json` records path, return code, and stdout/stderr sizes.
4. **Workflows** — `FEP_LEAN_GAUSS_WORKFLOWS=1` activates the full agentic pipeline: Hermes LLM explanations + `lake env lean` verification + SQLite session persistence.

**Rate limits** — A `[gauss.throttle]` block (if present in local YAML) is **not** read by the current Python pipeline; spacing between topics is not enforced from settings. Hermes HTTP **429** responses are retried with bounded backoff before advancing the model chain; see [`hermes.md`](hermes.md) and [`configuration.md`](configuration.md#gaussthrottle-optional-reserved).

---

## `OpenGaussClient` — SQLite Session Store

When `FEP_LEAN_GAUSS_WORKFLOWS=1`, [`gauss/client.py`](../src/gauss/client.py) (`OpenGaussClient`) is the persistence backend for all formalization sessions. It is **not** the `gauss` binary.

### Complete `OpenGaussClient` method surface

Cross-reference: for the definitive API signature see [`api.md`](api.md#gaussclientpy). The table below exists so this file is self-contained:

| Method | Purpose |
| ------ | ------- |
| `__init__(gauss_home=None)` | Open / create `{gauss_home}/fep_lean_state.db` and sub-dirs. Context-manager-safe. |
| `close()` | Commit and close the SQLite connection. |
| `create_session(topic_id, area, lean_sketch_original='', *, source='fep_lean') -> str` | Insert an `open` session row; return `session_id`. |
| `update_session(session_id, turn_index, role, content, tokens=0)` | Append a row to the `turns` table. |
| `close_session(session_id, status='success', hermes_success=False, lean_compiles=-1)` | Mark the session closed with final status + metrics. |
| `set_refined_sketch(session_id, refined_sketch)` | Write the Hermes-refined Lean sketch back to the session row. |
| `export_session(session_id) -> dict` | Return a `SessionRecord`-shaped dict (raises `KeyError` if unknown). |
| `export_all_sessions(source='fep_lean') -> list[dict]` | Bulk export every session, ordered by `created_at`. |
| `write_artifact(session_id, payload, *, label='result') -> Path` | Write a JSON artifact under `fep_artifacts/session_{id}_{label}.json`. |
| `write_bulk_jsonl(sessions, out_path) -> Path` | Dump many sessions to a single JSONL file. |
| `log_event(event, *, session_id=None, **kwargs)` | Append a structured JSON line to `fep_logs/operations.jsonl`. |
| `get_stats() -> dict` | Aggregate counts: `{total_sessions, lean_compiles, hermes_ok, db_path, …}`. |
| `get_cached_hermes(cache_key) -> dict \| None` | Return stored `HermesResult.as_dict()` for the given SHA-256 key, or `None` on miss. |
| `set_cached_hermes(cache_key, topic_id, stage, model, result_json, lean_sketch_hash)` | Insert or replace a Hermes cache entry; commits immediately. |
| `prune_hermes_cache(ttl_hours=24.0) -> int` | Delete cache entries older than `ttl_hours`; returns row count deleted. |

### Storage Layout

```text
{GAUSS_HOME}/                           # default: ~/.gauss
├── fep_lean_state.db                 # SQLite — sessions, turns, artifacts, logs, hermes_cache (5 tables)
├── fep_artifacts/
│   ├── session_{id}_{label}.json       # Per-topic artifact
│   └── sessions_fep_lean_*.jsonl       # Bulk JSONL export
└── fep_logs/
    └── operations.jsonl                # Structured event log (one JSON per line)
```

### SQLite Schema

**`sessions`** table:

| Column | Type | Description |
|--------|------|-------------|
| `session_id` | TEXT PK | `{topic_id}-{uuid4_hex[:8]}` |
| `topic_id` | TEXT | e.g. `fep-001` |
| `area` | TEXT | e.g. `FEP` |
| `lean_sketch` | TEXT | Original `lean_sketch` from `topics.yaml` |
| `refined_sketch` | TEXT | Hermes-refined sketch (written on success) |
| `status` | TEXT | `open` → `success` / `failed` / `error` / `skipped` |
| `hermes_success` | INTEGER | 0/1 |
| `lean_compiles` | INTEGER | -1: not attempted; 0: compile error; 1: clean |
| `source` | TEXT | Always `fep_lean` |
| `created_at` | REAL | Unix timestamp |
| `closed_at` | REAL | Null until `close_session()` |
| `duration_s` | REAL | Elapsed wall time |

**`turns`** table: `(session_id, turn_index, role, content, tokens, created_at)`.

**`artifacts`** table: `(artifact_id, session_id, file_path, sha256, size_bytes, created_at)`.

**`logs`** table: `(log_id, event, session_id, payload, ts)`.

**`hermes_cache`** table (Hermes result cache; pruned by TTL):

| Column | Type | Description |
|--------|------|-------------|
| `cache_key` | TEXT PK | SHA-256(`topic_id:lean_sketch:model:stage`) |
| `topic_id` | TEXT | e.g. `fep-001` |
| `stage` | TEXT | `verify` / `draft` / `prove` / `review` |
| `model` | TEXT | Model ID used for this result |
| `hermes_result` | TEXT | JSON-serialised `HermesResult.as_dict()` |
| `lean_sketch_hash` | TEXT | SHA-256 of lean sketch at cache time |
| `created_at` | REAL | Unix timestamp (used for TTL pruning) |

Cache entries expire after `HermesConfig.cache_ttl_hours` (default 24 h) and are removed on the next `prune_hermes_cache()` call, which `GaussRunner` invokes at batch start.

### Session Lifecycle (per topic)

> [!IMPORTANT]
> The lifecycle stages strictly execute sequentially (`max_workers=1`). The system prevents LLM asynchronous parallelization to ensure that the downstream validation (`lake env lean` within `LeanVerifier.verify_sketch()`) does not trigger concurrent OS sandbox deadlocks.

```text
create_session(topic_id, area, lean_sketch)
  → session_id = "{topic_id}-{uuid_hex[:8]}"
  → HermesExplainer.explain_topic(topic)    [LLM HTTP call: 2 messages]
_record_hermes_turns:
  update_session(session_id, 0, "system",    system_prompt)
  update_session(session_id, 1, "user",      theorem_block)
  update_session(session_id, 2, "assistant", explanation + refined lean sketch)
  update_session(session_id, 3, "assistant_reasoning", reasoning)  [optional]
  → LeanVerifier.verify_sketch(topic_id, refined_sketch)  [lake env lean]
set_refined_sketch(session_id, refined_sketch)
write_artifact(session_id, payload)         [JSON file]
close_session(session_id, status, hermes_success, lean_compiles)
```

---

## `GaussRunner` API (`src/gauss/runner.py`)

`GaussRunner` orchestrates the per-topic Hermes + `LeanVerifier` + SQLite workflow.

```python
class GaussRunner:
    def __init__(self, lean_verifier: LeanVerifier, hermes: HermesExplainer,
                 client: OpenGaussClient, project_root: Path) -> None: ...

    def run_topic(self, topic: TopicEntry, *, workflow: str = "verify") -> TopicRunResult:
        # Single-topic: Hermes explain → LeanVerifier.verify_sketch → persist session

    def run_topics_batch(self, topics: list[TopicEntry], *,
                         max_topics: int | None = None,
                         workflow: str = "verify") -> list[TopicRunResult]:
        # Batch runner; uses _run_topics_batch_prefetch when FEP_LEAN_PREFETCH=1 and ≥2 topics

    @classmethod
    def create_default(cls, project_root: Path, *,
                       require_cli: bool = False) -> "GaussRunner":
        # Factory: builds HermesExplainer from HermesConfig.from_settings(),
        # LeanVerifier from project lean/ workspace, OpenGaussClient from GAUSS_HOME.
        # When require_cli=True, raises RuntimeError if the gauss CLI is missing.
```

**`TopicRunResult`** is a flat dataclass (no nested `HermesResult` / `VerifyResult`) so it round-trips cleanly through `as_dict()` for JSON persistence. Fields:

| Group | Field | Type | Notes |
|-------|-------|------|-------|
| identity | `topic_id` | `str` | Catalogue id (e.g. `fep-001`) |
| identity | `session_id` | `str` | OpenGauss session row id |
| outcome | `success` | `bool` | True iff Lean verification compiled |
| outcome | `status` | `str` | `success` / `failed` / `hermes_error` / `no_lean_sketch` |
| outcome | `duration_s` | `float` | Wall-clock for the topic |
| outcome | `error` | `str` | First Lean error / Hermes error / skip reason |
| outcome | `workflow` | `str` | `verify` / `draft` / `prove` / `review` |
| outcome | `stage_results` | `list[dict]` | Extra stage outputs (e.g. `review_commentary`) |
| Hermes | `hermes_success` | `bool` | True iff Hermes returned any structured result |
| Hermes | `explanation` | `str` | Plain-text explanation extracted from the LLM reply |
| Hermes | `refined_lean_sketch` | `str` | Post-`restore_lean_structure` Lean body |
| Hermes | `tokens_used` | `int` | Sum of prompt + completion tokens reported by provider |
| Hermes | `hermes_model` | `str` | Model id that produced the reply (`HermesResult.model_used`) |
| Hermes | `cache_hit` | `bool` | True when the reply came from `hermes_cache` rather than the API |
| Lean | `lean_compiles` | `bool` | Final compile result (after baseline fallback) |
| Lean | `lean_has_sorry` | `bool` | True if the verified sketch contained `sorry` |
| Lean | `hermes_lean_compiles` | `bool` | True iff the Hermes-refined sketch itself compiled (before any fallback to the catalogue baseline) |

Full per-topic JSON, including the complete `HermesResult.as_dict()` and `VerifyResult.as_dict()`, is also written to the SQLite `artifacts` table by `_build_artifact_payload`.

**Prefetch mode** (`FEP_LEAN_PREFETCH=1`): `_run_topics_batch_prefetch` overlaps Hermes for topic *N+1* with `lake env lean` verification on topic *N* using a `ThreadPoolExecutor`. Requires ≥ 2 topics and `workflow="verify"`.

---

## `gauss_cli.py` Helpers

```python
def check_gauss_cli(project_root: Path | None, *, require: bool | None = None) -> tuple[bool, str]
    # Runs 'gauss doctor' if on PATH. Returns (ok: bool, message: str).
    # If require=True (or FEP_LEAN_REQUIRE_GAUSS=1) and the CLI is absent/failing,
    # raises GaussCLIError instead of returning False.

def workflows_enabled() -> bool
    # Returns True if FEP_LEAN_GAUSS_WORKFLOWS is truthy
```

`GAUSS_HOME` is probed by `verification.environment.run_validation_checks` for writability (check #3 `open_gauss_config_dir`).

---

## Enabling the Full Agentic Pipeline

First, ensure the OpenGauss CLI is installed natively:

```bash
# Clone math-inc/OpenGauss and install its CLI
bash scripts/00b_install_opengauss_cli.sh
```

Then configure the environment:

```bash
# Set API key and enable workflows
export OPENROUTER_API_KEY=sk-or-...
export FEP_LEAN_GAUSS_WORKFLOWS=1
export GAUSS_HOME=/tmp/my_gauss_home   # Optional override
export FEP_LEAN_REQUIRE_GAUSS=1        # Require the CLI for strict mode

# From the project root:
uv run python scripts/01_fep_catalogue_and_figures.py
```

With no API key, Hermes returns `HermesResult(success=False)` immediately (no network call) and the pipeline continues with `hermes_success=False` for all topics.

---

## See Also

- [AGENTS.md](../AGENTS.md) — project contracts and env vars
- [pipeline.md](pipeline.md) — `FEPPipeline` stages + `run_pipeline` reporting
- [configuration.md](configuration.md) — env vars and YAML
- [api.md](api.md) — `OpenGaussClient` full API
