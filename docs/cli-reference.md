# CLI reference

The only public command is `fep-lean`.

```text
fep-lean setup       Acquire and build the pinned Lean workspace.
fep-lean preflight   Run read-only full-mode capability checks.
fep-lean catalogue   Generate deterministic offline artifacts.
fep-lean run         Execute Hermes, Lean, and SQLite verification.
fep-lean topic ID    Execute one topic in full mode.
fep-lean report      Generate the offline catalogue report.
```

Global options are `--project-root PATH` and `--verbose`. `catalogue`, `run`,
and `topic` accept topic/area filters where applicable. `run` and `topic` also
accept `verify`, `draft`, `prove`, or `review` workflows.

Exit status is zero only for a complete result. A full-mode capability failure,
topic failure, artifact failure, or unresolved report state returns non-zero.
