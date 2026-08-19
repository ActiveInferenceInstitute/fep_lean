# Scripts contract

Public execution belongs to `src/cli.py` and the `fep-lean` console entry
point. Script files may only provide thin wrappers or deterministic maintenance
operations; they must not import packages outside this checkout.

The canonical sources are `catalogue_sketches.py`,
`_maint_build_topics_catalogue.py`, `_maint_build_fep_all_lean.py`, and the
semantic review data in `config/theorem_maturity.yaml`. The
`theorem_maturity_audit.py` maintenance command validates that review and
renders `docs/theorem-maturity-audit.md`.
Generated Lean output is tracked and must be regeneration-identical.
