"""verification — Lean 4 compilation checking and environment validation.

Provides the tools to verify Lean 4 theorem sketches through `lake env lean`
and to validate the overall fep_lean environment (OpenGauss, Lean CLI,
Mathlib caching).

`preflight.run_preflight` and the `fep-lean-preflight` console script live in
`verification.preflight` and are not re-exported here.

Public API
----------
    LeanVerifier            — main verification class
    VerifyResult            — structured compilation result
    run_validation_checks   — checks project layout and system tool presence
"""

from verification.environment import run_validation_checks
from verification.lean_verifier import LeanVerifier, VerifyResult

__all__ = ["LeanVerifier", "VerifyResult", "run_validation_checks"]
