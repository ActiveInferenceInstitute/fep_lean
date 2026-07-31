# Quality-gate decision record (updated 2026-07-31)

**Decision date:** 2026-07-31<br>
**Owner:** fep_lean repository maintainers<br>
**Decision:** Ruff is a pinned supported gate as of revision 2.

## Revision 2 — 2026-07-31

Ruff is now pinned in the `dev` extra at `ruff>=0.15.0` and enforced in CI:

```bash
uv run ruff check src tests scripts docs
```

The current baseline is **216 findings** (`123` fixable with safe fixes).
These are explicitly non-gating until the staged debt plan is executed (see below).
The Ruff *version* is pinned so findings are reproducible, even though the finding
count is not yet zero.

CI runs `ruff check` in informational mode: a non-zero exit records findings but
does not fail the pipeline. Once the baseline reaches zero, promotion to a
blocking gate is automatic (remove `--exit-zero`).

## Revision 1 — 2026-07-31 (prior handoff)

Ruff was informational and non-gating. The baseline was 222 findings before
import-only cleanup reduced it to 216. Ruff version was not pinned.

## Staged debt plan

1. ✅ **Pin a reviewed Ruff version** in the `dev` extra and capture a baseline file
   before changing findings. (Done: `pyproject.toml` + `.ruff_baseline.txt`)
2. [ ] Clear source and maintenance-script findings in small, reviewable batches,
   starting with import hygiene, unused symbols, and unsafe closure patterns.
   Each batch must keep the existing test, type, and native Lean gates green.
3. [ ] Review test and documentation findings separately, preserving intentional
   theorem notation and generated-text contracts. Do not apply a repository-wide
   formatter rewrite as a single change.
4. [ ] Promote `ruff check src tests scripts docs` and
   `ruff format --check src tests scripts docs` to supported gates only after
   the pinned baseline reaches zero and CI runs the exact pinned commands.

**Deadline for step 2:** 2026-08-15 (2 weeks).
**Deadline for step 4:** before next publication.

## Related contracts

- [Ideal-state assessment](../ISA.md)
- [Canonical backlog](../TODO.md)
- [Development checks](development.md)
