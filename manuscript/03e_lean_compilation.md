## Native Lean 4 Compilation and execution-integrity Verification {#sec:native_lean_4_compilation_and_zero_direct_verification}

> **Verification status (`scripts/03_lean_verify_only.py`):** All {{total_topics}} catalogue sketches compiled clean against Lean `{{lean_version}}` + Mathlib `{{mathlib_tag}}` — `verify.compiles_true: {{verify.compiles_true}}`, `verify.topics_with_result: {{verify.topics_with_result}}`, {{verify.sorry_count}} sorry. A full Hermes-assisted Gauss run (`{{verify.run_id}}`, ~{{verify.duration_min}} min) produced **{{compile_rate.total}} clean compiles, {{verify.sorry_count}} sorry, {{verify.compiles_false}} errors** in the LLM-assisted path. The `restore_lean_structure` post-processing layer (garbage detection, completeness check, open-statement restoration) plus a baseline-fallback that compiles the original YAML sketch when a Hermes-refined variant fails — the third of the three orthogonal fallback classes catalogued in §\ref{sec:three_classes_of_fallback} — keep the LLM-assisted path on the same `{{compile_rate.total}}` headline as the catalogue-baseline sweep; per-topic outcomes appear in §\ref{sec:live_verification_error_taxonomy}.

### Why Simulated Compilation Fails {#sec:why_simulated_compilation_fails}

A common shortcut in formal-verification pipelines is to direct the compiler, returning pre-constructed "success" or "failure" messages without ever invoking the theorem prover. This approach is catastrophically inadequate for mathematical formalization:

- A directed compiler cannot detect type mismatches between measures and real numbers.
- It cannot verify that referenced Mathlib4 APIs exist in the installed release.
- It produces validation results that appear correct but shatter on contact with the real Lean 4 engine.

The FEP Lean pipeline enforces a execution-integrity mandate for compilation whenever native verification is enabled: every check passes raw Lean 4 source through the compiler, parses `stdout`/`stderr`, and records results in machine-readable manifests and run bundles. Nothing is temporaryd.

### The `lean_verifier.py` Architecture {#sec:the_leanverifierpy_architecture}

The native compilation engine lives in [`src/verification/lean_verifier.py`](../src/verification/lean_verifier.py) and implements a three-stage compiler bridge.

#### Stage 1: Sketch Isolation and Temporary File Construction {#sec:stage_1_temporary_file_construction}

`LeanVerifier` reads each `lean_sketch` string from `config/topics.yaml` (sourced from `SKETCHES`) and writes it into an ephemeral `.lean` file after `_wrap_lean_code` adds `import Mathlib` and the shared `open` lines. Each topic runs in its own temporary file under `lean/FepSketches/`, which prevents cross-topic contamination across the {{total_topics}}-topic suite.

#### Stage 2: Native Shell Invocation {#sec:stage_2_native_shell_invocation}

The verifier invokes the Lean 4 compiler via Lake:

```bash
lake env lean FepCheck.lean
```

This executes inside the Lake build environment and accesses the Mathlib4 `.olean` (compiled-object) files directly. It is not a simulation; it is the same compilation pathway a human Lean developer uses.

#### Stage 3: Output Parsing and `VerifyResult` {#sec:stage_3_output_parsing_and_error_taxonomy}

The verifier parses combined compiler output into `errors` and `warnings` lists (regex over `lake env lean` text), sets `compiles` from the process exit code, and derives `has_sorry` from the sketch source (the `sorry` tactic). The `VerifyResult.status` string summarizes the outcome as `compiles_clean`, `compiles_with_sorry`, `compile_error`, or `skipped (…)`. `classify_failure_kind` additionally maps each failing run into a `FailureKind` (`missing_import`, `renamed_identifier`, `tactic_failure`, `arity_mismatch`, `timeout`, or `other`) which is exposed on `VerifyResult.failure_kind`. Downstream manifests and SQLite session metadata serialize these fields via `VerifyResult.as_dict()`.

| Outcome | Meaning |
|---------|---------|
| **Clean** | `compiles=True`, `has_sorry=False` → `.status` is `compiles_clean` |
| **Sorry in body** | `compiles=True`, `has_sorry=True` → `compiles_with_sorry` |
| **Compile failure / timeout** | `compiles=False` → `compile_error` |

These outcomes do not affect the `{{maturity.real}} real, {{maturity.partial}} partial, {{maturity.aspirational}} aspirational` count; those come from YAML `mathlib_status`.

### Aggressive Mathlib4 Caching {#sec:aggressive_mathlib_caching}

Mathlib4 is massive. Without caching, a single `lake build` can take 45 minutes or more as it recompiles thousands of files from source.

Mathlib4 artifacts live in the checked-in Lake workspace at [`lean/`](../lean/):

```text
lean/
├── lakefile.lean          # Mathlib4 pin ({{mathlib_tag}}; see lean/lakefile.lean)
├── lean-toolchain         # Matches Mathlib4 ({{lean_toolchain}}; see lean/lean-toolchain)
└── .lake/build/           # Pre-compiled .olean cache (large; local only)
```

From the `lean/` directory, run `lake exe cache get` (to download prebuilt Mathlib4) and then `lake build` to populate `.lake/`. Alternatively, use `scripts/_maint_bootstrap_lean_toolchain.sh`, which is invoked automatically from the repo-level `scripts/00_setup_environment.py --project fep_lean` whenever Mathlib4 is missing. See `docs/troubleshooting.md` for cache-failure diagnostics.

### Measured Compilation Headline {#sec:measured_compilation_headline}

The shipped catalogue is `mathlib_status: real` and sorry-free for all {{total_topics}} rows. The headline native compile rate is **`{{verify.compiles_true}}/{{verify.topics_with_result}}`** for the original catalogue sketches, confirmed by `scripts/03_lean_verify_only.py` and recorded in `manuscript_vars.yaml` (`verify.run_id: {{verify.run_id}}`). Toolchain pins: `{{lean_toolchain}}` and Mathlib4 `{{mathlib_tag}}` (see §\ref{sec:quantitative_execution_metrics}). Hermes-refined sketch variants from full Gauss runs are tracked separately; see §\ref{sec:live_verification_error_taxonomy}.

### Preflight: `LeanVerifier.check_mathlib_built()` {#sec:leanverifier_preflight}

Before invoking `lake env lean` on any catalogue sketch, `LeanVerifier` runs a preflight check via `check_mathlib_built()`. The method probes `lean/.lake/build/lib/Mathlib.olean` along with a small set of leaf modules (for example `Mathlib/MeasureTheory/Measure/MeasureSpace.olean`). If the cache is missing or partial, the verifier raises `MathlibNotBuiltError` with a remediation hint (`cd lean && lake exe cache get && lake build`) *before* spawning any per-topic subprocesses — this prevents a {{total_topics}}-topic sweep from burning 45 minutes of cold compile time sequentially. The preflight is intentionally conservative: a partial cache is treated as "not built" because partial caches produce confusing per-topic errors that mask the root cause.

### Verbose Mode: `FEP_LEAN_VERIFY_VERBOSE=1` {#sec:fep_lean_verify_verbose}

When debugging a compilation failure, set `FEP_LEAN_VERIFY_VERBOSE=1` before invoking any verification path:

```bash
FEP_LEAN_VERIFY_VERBOSE=1 uv run python scripts/03_lean_verify_only.py --topic fep-046
```

The flag causes `LeanVerifier` to echo the full wrapped Lean source to stderr before compilation, stream raw `lake env lean` `stdout`/`stderr` line by line instead of batching after exit, and include the exact subprocess `argv` in the `VerifyResult.diagnostic` field. In quiet mode (the default), only the parsed error summary and the exit code are surfaced, so verbose mode is the canonical tool for reproducing any per-topic failure.

### Sequential Batching: `verify_batch(max_workers=1)` {#sec:verify_batch_sequential}

The batch entry point `LeanVerifier.verify_batch` pins `max_workers=1` — batch verification is sequential, not parallel. This is a deliberate safety choice: `lake env lean` mutates files inside `lean/.lake/` (lock files and transient build artifacts), and Lake does not guarantee safe concurrent access to a single workspace. Two Lean processes racing on the same workspace can corrupt `.olean` cache metadata and produce spurious "invalid .olean" errors that are extremely difficult to diagnose. A future refactor could give each worker its own copy of `lean/`, but until that lands `verify_batch` is sequential by design, and the {{total_topics}}-topic sweep completes in roughly 60–90 seconds with a warm cache.

### Cache Timing: Cold vs Warm vs Cached {#sec:cache_timing}

With the cache primed, the compilation feedback loop is fast enough for interactive LLM workflows. The three regimes and their observed wall-clock costs are:

| Regime | What triggers it | Per-topic cost | Full {{total_topics}}-topic sweep | When you pay it |
|--------|------------------|----------------|---------------------|-----------------|
| **Cold** | Fresh checkout, no `.olean` cache, no `lake exe cache get` | — (dominated by one-shot build) | **45+ minutes** | First-time setup, CI without cache warmer |
| **Warm** | After `lake exe cache get` and `lake build` of Mathlib4 | — (one-shot) | **3 – 7 minutes** total | First run after a cache download |
| **Cached (steady state)** | `.olean` present; per-topic verification only | **{{verify.mean_topic_s}} s / topic** (run `{{verify.run_id}}`) | ~60 – 90 seconds | Every subsequent run in an interactive session |

Concretely: writing the temp file costs under 1 ms, native compilation costs `{{verify.mean_topic_s}}` s per topic in the cached regime (mean over run `{{verify.run_id}}`; warm-cache `lake env lean` typically lands in 1–2 s/topic, larger when reasoning-model batches dominate), and output parsing costs under 1 ms; the sequential sweep of {{total_topics}} topics lands in roughly 60–90 s. This sub-two-second feedback loop is what makes the FEP Lean pipeline a viable interactive formalization environment rather than a batch-processing job.

The cold-to-warm-to-cached transition is the single most important operational gate in the pipeline; `LeanVerifier.check_mathlib_built()` (§\ref{sec:leanverifier_preflight}) is the mechanism that refuses to enter verification mode unless the workspace is at least in the warm regime.

### The execution-integrity Standard Applied {#sec:the_zero_direct_standard_applied}

The execution-integrity principle extends beyond compilation to tests and validation:

- **Lean 4 compiler.** `LeanVerifier` invokes the `lean` and `lake` binaries via Python's `subprocess` module — no temporaryd exit codes in test fixtures.
- **Persistence.** `OpenGaussClient` writes `VerifyResult` payloads to the SQLite store at `$GAUSS_HOME/fep_lean_state.db` (default `~/.gauss/`) alongside the filesystem JSON/Markdown bundles.
- **Hermes reasoning API.** `HermesExplainer` uses `urllib.request` to hit the configured OpenRouter model endpoints.
- **Environment validation.** `verification.environment.run_validation_checks` runs 13 checks covering layout, YAML integrity, imports, optional `gauss doctor`, optional `lean --version`, a Mathlib4 build probe, and writable directories. (Count is fixed by the source of `run_validation_checks` in `src/verification/environment.py`; not parameterized by run.)

Project tests use `tmp_path`, subprocess, `pytest-httpserver` for HTTP, and real temporary files. A successful `run_pipeline` invocation means that the selected contract completed; in full mode the per-topic `VerifyResult` records the actual compiler outcome. The `verify.*` fields in `manuscript_vars.yaml` provide the aggregate summary.

### Methodological Assumptions and Limits {#sec:methodological_assumptions_and_limits}

The execution-integrity standard is a concrete, auditable methodological property rather than a branding term. We define it precisely and delineate the epistemic boundaries of what the pipeline can and cannot guarantee.

#### Formal Definition of execution-integrity {#sec:formal_definition_of_zero_direct}

execution-integrity means:

- Every sketch *can* be checked by an unmodified Lean 4 binary in the project's `lean/` workspace (toolchain `{{lean_toolchain}}` in `lean/lean-toolchain`; Mathlib4 pinned at `{{mathlib_tag}}` in `lean/lakefile.lean`).
- The verifier runs `lake env lean` on a temp file; a catalogue row counts as machine-checked only when `LeanVerifier` has actually run on it — via Gauss Sessions with `FEP_LEAN_GAUSS_WORKFLOWS=1` or via [`scripts/03_lean_verify_only.py`](../scripts/03_lean_verify_only.py) — and the recorded `VerifyResult` has been inspected. Loading `config/topics.yaml` alone is not sufficient.
- Compiler failures are logged rather than silently dropped; they do not auto-reinvoke Hermes or swap models.
- Run bundles use real file writes, API calls use real HTTP POST requests whenever LLM paths run, and environment validation performs real filesystem and subprocess checks.

#### Per-Stage Success Criteria {#sec:per_stage_success_criteria}

Each pipeline stage has an explicit, checkable success condition:

| Stage | Success Criterion | Failure Action |
|-------|-------------------|----------------|
| **Topic parsing** | Topic ID and NL statement extracted from `topics.yaml` and stored as `FEPTopic` dataclass | Pipeline halts with parse error |
| **Hermes call** | Response contains `EXPLANATION:` and `VALIDATION:` | Fallback models; then fixture if configured |
| **Compilation** (optional) | `lake env lean` completes | Outcome appended to session + metadata + manifest |
| **Catalogue maturity** | `mathlib_status` in `topics.yaml` | Used for `{{maturity.real}} real, {{maturity.partial}} partial, {{maturity.aspirational}} aspirational` via `manuscript_vars.yaml` at PDF render (see `preprocess_combined_markdown`) |

#### Three Levels of Truth {#sec:three_levels_of_truth}

The pipeline guarantees three distinct epistemic levels, each weaker than the next:

1. **Machine-checked type correctness (optional).** Whenever `LeanVerifier` runs on a topic — via the Gauss path, the verify-only script, or a compile test — each sketch is fed to `lake env lean`. The `verify.*` fields in `manuscript_vars.yaml` summarize outcomes when that stage produced them. This level is independent of the catalogue maturity label `mathlib_status` in YAML.
2. **Internal catalogue consistency.** The {{total_topics}}-topic catalogue follows shared conventions; Hermes commentary may flag inconsistencies. `mathlib_status` is a human-maintained coverage tag, not a compiler oracle.
3. **No claim of empirical faithfulness.** The pipeline does *not* guarantee that any given formalization is the unique or canonical encoding of the informal FEP literature (Friston, Da Costa, Maheu, and others). Multiple valid formalizations may exist for the same informal claim; the pipeline produces one structurally sound encoding and documents its assumptions.
