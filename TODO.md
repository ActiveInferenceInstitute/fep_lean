# fep_lean — canonical backlog

Only open work belongs here. Completed work is represented by passing evidence
in the repository history or an eventual changelog; do not add struck-through
rows or a completed-work archive here.

| ID | Open work | Acceptance probe |
| --- | --- | --- |
| FEP-FULL-155 | Refresh optional external full-mode evidence for the expanded source. Historical 50-topic and one-topic provider reports must remain historical. | Under a separately confirmed credential and spend boundary, a 155-topic Hermes/OpenGauss run completes and `validate_report_receipt(..., require_complete=True, project_root=...)` reports `valid`, `source_bound`, and `claim_ready`, with the exact live roster and no validation errors. |
| FEP-EVIDENCE-CURRENT | Refresh deterministic native, declaration/axiom, Python, browser, and publication evidence for the accepted post-v1.1.0 H1/H2 and publication source wave after all canonical projections and publication owners settle. Retained receipts from an older owner manifest or source digest remain historical, never current evidence. | Native validation is `valid`, `source_bound`, and `native_claim_ready`; formal-audit, Python-acceptance, and browser-replay validators return no errors; manuscript/publication drift checks pass; and a deterministic release bundle validates as source-bound and claim-ready against the same final owner roster. |
| FEP-H3-SCIENCE | Proceed next with H3.0 preregistration for the accepted continuous formal H3.1--H3.5 and synthetic H3.6S branch of the [Horizon 3 scientific case study](docs/design/fep-research-program/horizon-3-scientific-case-study.md). H3.1--H3.7 remain closed until H3.0 freezes; H3.6E and causal claims remain blocked while the canonical `data-capability.yaml` owner is absent. | `tests/test_h3_preregistration.py`, owned exclusively by H3.0, validates a pre-outcome frozen protocol that names the prospective [H3.G0 acceptance receipt](specs/h3-reference-study/carrier-acceptance.json) and continuous branch without inspecting protected outcomes. Only after that freeze may H3.1 begin; the finite fallback still requires an explicit reviewed H2 terminal no-go and reviewed H3 DAG revision. |

`FEP-FULL-002` and `FEP-PROV-003` remain completed for their exact 2026-08-20
source snapshot; their evidence is recorded in [CHANGELOG.md](CHANGELOG.md),
[HANDOFF.md](HANDOFF.md), and [ISA.md](ISA.md). They do not substitute for
`FEP-FULL-155`. The release-recorded native and declaration/axiom probes remain
evidence for their exact source snapshot. The accepted post-v1.1.0 Horizon
1/Horizon 2 and publication source wave invalidated their current-source binding;
`FEP-EVIDENCE-CURRENT` owns the next deterministic refresh. Completed
engineering tasks belong to repository history, not this open-only backlog.

## Closure rule

An item leaves this backlog only when its acceptance probe passes in the current
checkout, the evidence is retained in a test/report/documentation change where
appropriate, and the result is recorded in the repository's changelog or
release notes. Until then, the row remains open even if a partial local probe
looks promising.
