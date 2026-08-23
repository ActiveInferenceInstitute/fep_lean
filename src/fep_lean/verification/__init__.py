"""verification — Lean 4 compilation checking and environment validation.

Provides the tools to verify Lean 4 theorem sketches through `lake env lean`
and to validate the overall fep_lean environment (OpenGauss, Lean CLI,
Mathlib caching).

`preflight.run_preflight` backs the `fep-lean preflight` command and is not
re-exported here.

Public API
----------
    LeanVerifier            — main verification class
    VerifyResult            — structured compilation result
    run_validation_checks   — checks project layout and system tool presence
"""

from fep_lean.verification.environment import run_validation_checks
from fep_lean.verification.formalism_audit import (
    FormalismAuditResult,
    FormalismEvidenceRecord,
    build_formalism_probe,
    run_formalism_audit,
    validate_formalism_audit_receipt,
    write_formalism_audit_receipt,
)
from fep_lean.verification.lean_verifier import LeanVerifier, VerifyResult

__all__ = [
    "FormalismAuditResult",
    "FormalismEvidenceRecord",
    "LeanVerifier",
    "VerifyResult",
    "build_formalism_probe",
    "run_formalism_audit",
    "run_validation_checks",
    "validate_formalism_audit_receipt",
    "write_formalism_audit_receipt",
]
