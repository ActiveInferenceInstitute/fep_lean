# Authorship Guide — Adding Topics to the fep_lean Catalogue

**Version**: v1.0.0 | **Last Updated**: July 2026

This guide walks through adding a new formalization topic to the 50-topic FEP
catalogue, from writing the natural language statement through verifying the
Lean 4 sketch and passing the test suite.

**See also:**
- [`development.md`](development.md) — dev environment and dependency setup
- [`hermes.md`](hermes.md) — Hermes LLM architecture and fallback chain
- [`opengauss.md`](opengauss.md) — SQLite session schema and storage layout
- [`testing.md`](testing.md) — coverage requirements and test patterns
- [`troubleshooting.md`](troubleshooting.md) — error recovery

---

## 1. Prerequisites

```bash
# Install project dependencies
cd projects/fep_lean
uv sync --extra dev

# Verify Lean 4 toolchain (requires elan)
lean --version     # e.g. Lean (version 4.29.0, ...) — match `lean/lean-toolchain`
lake --version

# Optional: verify gauss CLI for Hermes workflows
gauss doctor
```

Lean 4 and lake must be installed via [elan](https://github.com/leanprover/elan).
`gauss` is optional — local Lean verification works without it.  The Mathlib
`.olean` cache (`lean/.lake/`) must be built or already present; see
`troubleshooting.md` for cache warm-up steps.

---

## 2. The Topic Data Model

Each catalogue entry is a `TopicEntry` dataclass defined in
`src/catalogue/topics.py`.  The YAML representation maps directly to its fields:

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique identifier, **must** match `fep-NNN` pattern (zero-padded) |
| `title` | `str` | Short human-readable name (≤ 80 chars) |
| `area` | `str` | One of the five recognised areas (see below) |
| `mathlib` | `str` | Primary Mathlib4 import path (e.g. `MeasureTheory.Measure.rnDeriv`) |
| `mathlib_status` | `str` | `real` / `partial` / `aspirational` (see §4) |
| `nl` | `str` | Natural language statement of the theorem (2–4 sentences) |
| `lean_sketch` | `str` | Lean 4 theorem skeleton or proof |

**The five areas:**

| Area | Description |
|---|---|
| `FEP` | Free Energy Principle and variational inference |
| `ActiveInference` | Active Inference and policy selection |
| `BayesianMechanics` | Bayesian Mechanics and Markov blankets |
| `InfoGeometry` | Information Geometry and statistical manifolds |
| `Thermodynamics` | Non-equilibrium Thermodynamics and entropy |

**ID assignment:** New topics follow `fep-NNN` where NNN is the next integer
after the current maximum.  As of v1.0.0 the catalogue contains `fep-001` through
`fep-050`; the next topic should be `fep-051`.

---

## 3. Step-by-Step: Authoring a New Topic

### Step 1 — Write the natural language statement

The `nl` field should be 2–4 sentences that:
- State the theorem precisely (what is being proved)
- Name the key mathematical objects (measures, distributions, manifolds)
- Reference the relevant Mathlib import

**Example (`fep-001`):**
```
For any two probability measures on a measurable space, the measure of a set
under their sum is bounded above by the sum of the individual measures. This
follows from the σ-subadditivity property of measures. Formalises the measure
subadditivity lemma used in variational free energy bounds.
```

### Step 2 — Identify the Mathlib4 import

Search Mathlib4 for the relevant module:

```bash
# Search by keyword in Mathlib
cd projects/fep_lean/lean
lake env lean --stdin <<'EOF'
import Mathlib
#check MeasureTheory.measure_union_le
EOF
```

Use the canonical import path (e.g. `MeasureTheory.Measure.MeasurableSpace`) as
the `mathlib` field.

Add a matching row to `METADATA` in [`scripts/_maint_build_topics_catalogue.py`](../scripts/_maint_build_topics_catalogue.py) (same id, title, area, mathlib hint, and `mathlib_status`) before you regenerate `config/topics.yaml` in Step 5.

### Step 3 — Write the Lean 4 sketch

Add a `SKETCHES["fep-051"]` string in [`scripts/catalogue_sketches.py`](../scripts/catalogue_sketches.py). That dict is the authoring source of truth; [`LeanVerifier`](../src/verification/lean_verifier.py) prepends `import Mathlib` and `open` lines — **do not** put a leading `import` in the stored body.

**Shape (matches existing topics):**
```lean
variable {α : Type*} [MeasurableSpace α]

/-- One-line docstring; theorem names use the fep051_* prefix. -/
theorem fep051_measure_sum_bound
    (μ ν : Measure α) (s : Set α) :
    (μ + ν) s ≤ μ s + ν s := by
  exact measure_union_le s s
```

For local experiments you can use `lake env lean --stdin` with `import Mathlib` at the top; **committed** bodies must follow the no-import `SKETCHES` format so the verifier and [`tests/test_catalogue_sketches_ssot.py`](../tests/test_catalogue_sketches_ssot.py) stay aligned.

**Rules:**
- Use only Mathlib4 declarations (no custom axioms)
- Name hypotheses explicitly (e.g. `hac : q ≪ p`)
- Shipped catalogue policy is **sorry-free** `real` (see §4); avoid `sorry` in what you intend to merge unless you are explicitly staging a non-`real` path and not asserting all-real rollups in tests

**Cursor lean4:** See [Catalogue source of truth](lean4.md#catalogue-source-of-truth) and [Cursor lean4 commands](lean4.md#cursor-lean4-commands) in [lean4.md](lean4.md) for `SKETCHES` vs `topics.yaml` vs `lean/FepSketches/*.lean`, the learn/refactor/doctor/formalize/golf map, and verification gates.

### Step 4 — Set `mathlib_status`

See §4 below. For topics you plan to merge into this repository’s catalogue under current CI, target **`real`** (no `sorry`). The test suite expects every row to contribute to the all-`real` rollups in [`tests/test_fep_topics.py`](../tests/test_fep_topics.py).

### Step 5 — Regenerate `config/topics.yaml`

After `METADATA` and `SKETCHES` are updated, regenerate the YAML (do **not** hand-paste a new `lean_sketch` as the primary workflow):

```bash
cd projects/fep_lean
uv run python scripts/_maint_build_topics_catalogue.py
```

That script writes each row’s `lean_sketch` from `SKETCHES[id]`. If you edit `topics.yaml` only, CI fails unless `SKETCHES` contains the same strings.

> **YAML:** The maint script emits valid multiline `lean_sketch` fields; if you inspect the file, use `|` blocks for `nl`/`lean_sketch` when editing manually (still discouraged vs regenerating).

### Step 6 — Verify locally (required before submitting)

```bash
cd projects/fep_lean

# Drift check: YAML lean_sketch matches SKETCHES (no lake required)
uv run pytest tests/test_catalogue_sketches_ssot.py -v

# Verify only your new sketch (fast, no LLM)
uv run python scripts/03_lean_verify_only.py --topic fep-051

# Verify the full catalogue on disk
uv run python scripts/03_lean_verify_only.py
```

Interpret the output:
- `compiles=True, has_sorry=False` — clean proof, matches shipped `real` policy
- `compiles=True, has_sorry=True` — gaps; do not merge into `SKETCHES` / aggregates until resolved unless you are intentionally changing maturity policy (§4)
- `compiles=False` — sketch has errors; fix before submitting

---

## 4. Mathlib Maturity Levels

| Status | Meaning | CI sorry gate |
|---|---|---|
| `real` | Compiles with no `sorry`; all imports exist in Mathlib4 | Passes |
| `partial` | Compiles but ≤50% of sub-goals use `sorry` | Passes (sorry permitted in topic body) |
| `aspirational` | Core theorem statement is sketched; key lemmas are `sorry`'d | Passes |

**Shipped catalogue (current repo):** All **50** topics have `mathlib_status: real`, `SKETCHES` bodies are **sorry-free**, and [`tests/test_fep_topics.py`](../tests/test_fep_topics.py) asserts the maturity rollups are all-`real`. The `partial` / `aspirational` rows above describe **staging or hypothetical** workflows; they are not the state of the committed catalogue.

**Aggregates:** There is no `sorry` in `lean/FepSketches/fep_all.lean` or `Basic.lean`. CI rejects non-comment `sorry` in those files.

The `topics.yaml` `mathlib_status` field is metadata for the manuscript and
Hermes prompts — it does not affect compilation.  The CI gate operates on the
Lean source files under `lean/FepSketches/`.

---

## 5. Running Lean Verification Locally

```bash
# All catalogue topics
uv run python scripts/03_lean_verify_only.py

# Single topic
uv run python scripts/03_lean_verify_only.py --topic fep-001

# With verbose Lean output
FEP_LEAN_VERIFY_VERBOSE=1 uv run python scripts/03_lean_verify_only.py --topic fep-001
```

**Interpreting `VerifyResult`:**

| Field | Type | Meaning |
|---|---|---|
| `compiles` | `bool` | True if `lake env lean` exits 0 |
| `has_sorry` | `bool` | True if any `sorry` appears in compiled output |
| `errors` | `list[str]` | Lean error messages |
| `warnings` | `list[str]` | Lean warnings |
| `stdout` | `str` | Raw compiler stdout (truncated) |
| `duration_s` | `float` | Wall-clock seconds for this topic |
| `lean_version` | `str` | Lean version string |
| `topic_id` | `str` | Topic ID passed to verifier |

---

## 6. Testing Before Submitting

```bash
# Validate catalogue invariants (topic count, area distribution, maturity)
uv run pytest tests/test_fep_topics.py -v

# Full suite
uv run pytest tests/ -q --timeout=900
```

**After adding a topic**, update the count assertion in `tests/test_fep_topics.py`:

```python
# Line ~23: update expected count
def test_catalogue_loads_50_topics() -> None:
    # Change 50 → 51
    assert len(c.topics) == 51
    assert ids == [f"fep-{i:03d}" for i in range(1, 52)]
```

Also update `_EXPECTED_AREAS` if you added a topic in a new or underrepresented area:

```python
_EXPECTED_AREAS = {
    "FEP": 15,            # was 14 — added one FEP topic
    "ActiveInference": 11,
    ...
}
```

---

## 7. Common Mistakes and Debugging

### "unknown identifier" or "unknown tactic"

The import is wrong or incomplete.  Check the Lean 4 / Mathlib4 module path:

```bash
cd projects/fep_lean/lean
lake env lean --stdin <<'EOF'
import Mathlib
#check MeasureTheory.measure_union_le
EOF
```

If `#check` fails with "unknown identifier", the lemma does not exist in the
pinned Mathlib version (`v4.29.0`). Find the correct name or restate the sketch; **merging** a new topic as `aspirational` while the suite still expects all-`real` requires coordinated test updates (see §4).

### "type mismatch" or universe errors

Universe polymorphism issues are common with `Type*` vs `Type u`.  Use
`{α : Type*}` unless the theorem requires a specific universe level.  Add
`variable {α : Type*}` at the top of the sketch block.

### sorry in CI

The CI gate runs `grep -n 'sorry' fep_all.lean Basic.lean` and fails if any
non-comment `sorry` is found. **Committed `SKETCHES` must stay sorry-free** to match current policy and [`tests/test_fep_topics.py`](../tests/test_fep_topics.py). If you are experimenting with `sorry` in a branch, do not merge `fep_all.lean` / `Basic.lean` / `SKETCHES` changes that introduce `sorry` until you either remove placeholders or relax the maturity tests and aggregates in a deliberate change. Local `LeanVerifier` runs can still report `has_sorry=True` for scratch files.

### FEP_LEAN_GAUSS_WORKFLOWS not set (Hermes skipped)

This is expected in local dev.  Hermes requires an API key and
`FEP_LEAN_GAUSS_WORKFLOWS=1`.  For local Lean-only iteration:

```bash
uv run python scripts/03_lean_verify_only.py --topic fep-NNN
```

### Sandbox deadlock (macOS)

If `lake env lean` hangs indefinitely on macOS, the elan sandbox may be locked.
See `troubleshooting.md → ELAN sandbox deadlock` for recovery steps.

### `test_catalogue_loads_50_topics` fails after adding a topic

Update the count assertion as described in §6.  This test is intentionally
strict — it documents the expected state of the catalogue.

---

## 8. Interpreting HermesResult and VerifyResult

After running a full pipeline step with Hermes enabled:

**`HermesResult` fields:**

| Field | Type | Meaning |
|---|---|---|
| `success` | `bool` | True if Hermes returned a non-empty response |
| `model_used` | `str` | OpenRouter model ID that produced the response |
| `explanation` | `str` | 2–4 sentence proof strategy explanation |
| `refined_lean_sketch` | `str` | The ````lean` block from the response |
| `reasoning` | `str` | Extended thinking text (DeepSeek-R1, o1, o3 only) |
| `tokens_used` | `int` | Total tokens (prompt + completion) |
| `duration_s` | `float` | API call wall-clock time |
| `cache_hit` | `bool` | True if the result was served from the SQLite cache |
| `error` | `str` | Error message if `success=False` |
| `topic_id` | `str` | The topic ID passed to the explainer |

**`VerifyResult` fields:**

| Field | Type | Meaning |
|---|---|---|
| `compiles` | `bool` | True if `lake env lean` exits 0 |
| `has_sorry` | `bool` | True if any `sorry` appears in the output |
| `errors` | `list[str]` | Parsed Lean error messages |
| `warnings` | `list[str]` | Parsed Lean warnings |
| `stdout` | `str` | Raw `lake env lean` stdout |
| `duration_s` | `float` | Compiler wall-clock time |
| `lean_version` | `str` | Lean version string |
| `topic_id` | `str` | Topic ID |

---

## 9. Optional: Running Hermes Commentary

To get LLM-generated proof strategy commentary for your new topic:

```bash
# Set API key (OpenRouter recommended)
export OPENROUTER_API_KEY=sk-or-...

# Enable Gauss workflows
export FEP_LEAN_GAUSS_WORKFLOWS=1

# Run single topic with Hermes
uv run python scripts/02_run_single_topic.py fep-051
```

The output is saved to `$GAUSS_HOME/fep_artifacts/` as a JSON artifact and to the
SQLite DB at `$GAUSS_HOME/fep_lean_state.db` (default `~/.gauss/`).  Results are cached: rerunning the
same topic (same `lean_sketch`, same `model`) returns from cache without a new
API call (24-hour TTL by default).

**Workflow stages** (requires `FEP_LEAN_GAUSS_WORKFLOWS=1`):

| Stage | Hermes directive | Use when |
|---|---|---|
| `verify` (default) | Refine existing sketch | Normal pipeline |
| `draft` | Draft new skeleton | Starting a new topic from NL only |
| `prove` | Fill sorry holes | Upgrading `partial` → `real` |
| `review` | Post-compile commentary | Final quality review before merge |

---

## 10. Adding Tests for New Topics

The test suite enforces strict invariants about the catalogue.  After adding a
topic, update these files:

### `tests/test_fep_topics.py`

Update the count and area expectations:

```python
# test_catalogue_loads_50_topics → change 50 to 51
assert len(c.topics) == 51
assert ids == [f"fep-{i:03d}" for i in range(1, 52)]

# _EXPECTED_AREAS → add 1 to the relevant area count
_EXPECTED_AREAS = {
    "FEP": 15,   # example: added one FEP topic
    ...
}
```

### Per-row compilation (no pytest target)

Per-row compilation is driven by `scripts/03_lean_verify_only.py` (logs to
stdout) and, when **`FEP_LEAN_GAUSS_WORKFLOWS=1`**, the **Gauss Sessions** stage
(**`GaussRunner`** + **`LeanVerifier`**). Both invoke `lake env lean` for every
row in `config/topics.yaml`. Aggregated counts for manuscripts land in
**`output/reports/run_*/verification_manifest.json`** (written by **`Reporter`**
after a full pipeline run). Adding a topic requires no test edit; the sweep picks
it up from YAML automatically.

### Coverage

The 89% coverage gate (`--cov-fail-under=89`) covers `src/` only, not `config/`
or `tests/`.  Adding a YAML entry or test file does not affect coverage.  Adding
new Python code in `src/` requires corresponding tests to maintain the gate.

---

## Documentation gates

If your change touches markdown under `docs/` or manuscript cross-links, run the four audits in [AGENTS.md](AGENTS.md) from the `docs/` directory: `check_links.py --strict --include-root`, `md_hygiene.py --strict`, `pin_audit.py`, and `xref_audit.py`. See [troubleshooting.md](troubleshooting.md) if `pin_audit` or `xref_audit` fails.

## Navigation

- [← docs/README.md](README.md)
- [Testing →](testing.md)
- [Topics reference →](topics-reference.md)
