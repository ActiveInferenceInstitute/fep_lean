# Execution integrity {#sec:execution_integrity}

Every success claim in this project is tied to a concrete artifact or an
observable computation. Catalogue mode validates and renders the 50 source
entries, but it makes no Lean or Hermes claim. Full mode first validates every
required capability and then records the Hermes response, refined Lean source,
compiler result, SQLite session, and report manifest for each selected topic.

## Evidence boundaries

The evidence boundary is deliberately explicit:

1. YAML is loaded by the strict catalogue schema and checked against the
   canonical sketch dictionary and generated aggregate.
2. Lean evidence comes only from `lake env lean` using the pinned workspace.
3. Hermes evidence comes from an HTTP response accepted by the configured
   response parser; a missing credential or invalid response is an error.
4. SQLite evidence is written transactionally and exported files are checked
   against their recorded hashes.
5. Report manifests bind the run to source and configuration digests, the
   Lean/Mathlib pins, capabilities, topic counts, and artifact hashes.

An unavailable capability therefore ends a full run before a success report is
created. The result is diagnostic JSON with `complete: false` and a structured
`failure_reason`. Offline work is available only through the explicitly named
`catalogue` mode, whose result always reports zero verified topics.

## Lean verification

`LeanVerifier` writes a temporary source file, invokes the real Lake command,
captures diagnostics, removes the temporary file, and records the result. A
topic is verified only when the refined Hermes source compiles without a proof
placeholder. The original YAML sketch and the refined source are retained as
separate fields; the original is never presented as the refined result.

The committed `lean/FepSketches/fep_all.lean` is generated from the canonical
catalogue source. A regeneration check fails when the generated file differs,
and the Lean CI job compiles the aggregate with the exact pinned toolchain.

## HTTP and persistence

Hermes tests use a real loopback HTTP server and exercise response parsing,
timeouts, retries, model-chain advancement, and review calls over sockets.
SQLite tests use temporary on-disk databases, concurrent writers, atomic file
publication, restart recovery, and SHA-256 consistency checks. These boundaries
make provider, compiler, and filesystem drift visible in test results.

## Reproducibility

Use `uv.lock`, `fep-lean setup`, and the documented `fep-lean preflight` command
to reproduce the pinned environment. A complete run produces
`run_manifest.json`, `verification_manifest.json`, `summary.json`, Markdown
reports, deterministic figures, and manuscript projections. The manifest is
the authoritative record of what was actually available and verified.
