# CLI reference

The only public command is `fep-lean`.

```text
fep-lean setup       Acquire and build the pinned Lean workspace.
fep-lean preflight   Run read-only full-mode capability checks.
fep-lean verify      Compile catalogue sketches with Lean only.
fep-lean catalogue   Generate deterministic offline artifacts.
fep-lean run         Execute Hermes, Lean, and SQLite verification.
fep-lean topic ID    Execute one topic in full mode.
fep-lean report      Generate the offline catalogue report.
```

For a generated report bundle, the read-only receipt checker is:

```bash
uv run python scripts/verify_report_receipt.py output/reports/run_...
uv run python scripts/verify_report_receipt.py output/reports/run_... --require-complete
```

It recomputes the listed artifact hashes and reconciles the summary, run, and
verification manifests. `--require-complete` additionally requires a non-empty
complete full-mode receipt; it never runs Hermes, OpenGauss, or Lean.

Global options are `--project-root PATH` and `--verbose`. `catalogue`, `verify`,
`run`, and `topic` accept topic/area filters where applicable. `run` and `topic` also
accept `verify`, `draft`, `prove`, or `review` workflows.

`verify` never calls Hermes, OpenGauss, or the full pipeline. It requires the
already-built pinned Mathlib cache and returns one native `lake env lean` result
per selected topic.

Exit status is zero only for a complete result. A full-mode capability failure,
topic failure, artifact failure, or unresolved report state returns non-zero.
