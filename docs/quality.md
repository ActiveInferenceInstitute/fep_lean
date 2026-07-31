# Quality-gate decision record

**Decision date:** 2026-07-31<br>
**Owner:** fep_lean repository maintainers<br>
**Decision:** Ruff is informational and non-gating for this checkout.

## Evidence boundary

The current local audit used Ruff `0.15.20` and ran:

```bash
uv run ruff check src tests scripts docs
```

It reported **216 findings** (`123` fixable with safe fixes); the prior handoff
recorded a 222-finding baseline before this extension's import-only cleanup.
The repository does not currently pin Ruff in its development dependencies or
expose a Ruff job in CI. Therefore this result is a measured debt baseline, not
a supported release gate. The passing `mypy`, pytest/coverage, Lean, and
documentation gates remain independent and are not weakened by this decision.

## Staged debt plan

1. Pin a reviewed Ruff version in the `dev` extra and capture a baseline file
   before changing findings. Keep mathematical Unicode and prose-string rules
   as explicit, narrow configuration decisions rather than broad suppression.
2. Clear source and maintenance-script findings in small, reviewable batches,
   starting with import hygiene, unused symbols, and unsafe closure patterns.
   Each batch must keep the existing test, type, and native Lean gates green.
3. Review test and documentation findings separately, preserving intentional
   theorem notation and generated-text contracts. Do not apply a repository-wide
   formatter rewrite as a single change.
4. Promote `ruff check src tests scripts docs` and
   `ruff format --check src tests scripts docs` to supported gates only after
   the pinned baseline reaches zero and CI runs the exact pinned commands.

Revisit this decision before the next release or when the baseline changes.
Until then, a Ruff failure must be reported as quality debt and must not be
described as a failed supported repository gate.

## Related contracts

- [Ideal-state assessment](../ISA.md)
- [Canonical backlog](../TODO.md)
- [Development checks](development.md)
