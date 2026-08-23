# Scripts contract

Public execution belongs to `src/fep_lean/cli.py` and the `fep-lean` console entry
point. Script files may only provide thin wrappers or deterministic maintenance
operations; they must not import packages outside this checkout.

Canonical authoring lives outside this wrapper directory: family-owned modules
under `src/fep_lean/catalogue/bodies/`, the validated catalogue registry,
`config/catalogue_metadata.yaml`, `config/theorem_maturity.yaml`,
`config/formalism_novelty.yaml`, and `config/formalism_relations.yaml`.
`_maint_build_topics_catalogue.py`,
`_maint_build_fep_all_lean.py`, `_maint_build_formal_modules.py`,
`build_formalism_coverage.py`, `build_formalism_atlas.py`, and
`build_formal_kernel_dashboard.py` are thin deterministic projection commands.
`audit_formalisms.py` is the native
declaration/axiom evidence adapter. The
`theorem_maturity_audit.py` maintenance command validates that review and
renders `docs/theorem-maturity-audit.md`.

`build_release_bundle.py` is a thin public wrapper over
`fep_lean.output.release_bundle`. It never reconstructs the archive roster,
renderer policy, manifest, checksum table, or evidence boundaries. `--check`
must remain non-mutating and bind an existing archive back to current sources.
Generated Lean output is tracked and must be regeneration-identical. The formal
resource manifest owns foundation, leaf-composition, and import-aggregate
projections; wrapper scripts must not reconstruct that roster independently.
