# `fep_lean.verification`

Lean compilation and read-only capability validation for the standalone
package. This layer does not import the LLM or pipeline packages and never
downloads or builds dependencies during validation.

## Modules

| Module | Owner |
| --- | --- |
| `environment.py` | Mode-aware `run_validation_checks(project_root, mode=...)` |
| `lean_verifier.py` | `LeanVerifier` and structured `VerifyResult` |
| `formalism_audit.py` | declaration resolution, evidence axiom inspection, and typed audit receipt |
| `_toolchain.py` | Exact pinned executable resolution shared by validation and verification |
| `preflight.py` | Adapter behind `fep-lean preflight` |

## Public boundary

```python
from fep_lean.verification import (
    FormalismAuditResult,
    LeanVerifier,
    VerifyResult,
    run_formalism_audit,
    run_validation_checks,
)
```

`LeanVerifier.verify_sketch(topic_id, lean_code)` writes a bounded temporary
file under the Lake workspace, invokes `lake env lean`, parses errors and
warnings, records `sorry`, and removes the temporary source before returning.
`verify_batch(items)` is deliberately serial because every item shares the same
Lake build tree.

`check_mathlib_built()` returns `(ok, message)`, not compilation evidence. The
native CLI receipt is the full-catalogue evidence boundary:

```bash
uv run fep-lean verify --fail-on-warnings \
  --receipt output/native-verification.json
uv run python scripts/audit_formalisms.py \
  --receipt output/formalism-audit.json
```

The native catalogue receipt and formalism audit answer different questions.
The former compiles all exact topic bodies; the latter resolves every primary
and graph-evidence declaration through the topic aggregate and the manifested
foundation/composition resources imported by `composed.lean`, and
requires a parsed `#print axioms` result for each declaration. Process success
without complete axiom output, actual compiler/pin parity, an exact resolved
Mathlib revision, or live projection parity makes the audit incomplete.
Warnings, `sorryAx`, and any axiom outside the versioned trusted set
(`propext`, `Classical.choice`, `Quot.sound`) also fail the audit.

`run_validation_checks` returns named rows appropriate to `catalogue` or
`full` mode. Full mode adds Gauss, writable state, exact toolchain, workspace,
Mathlib, and credential requirements. Callers must inspect the returned status
and rows; the number of checks is not an API constant.

Dependency acquisition is explicit:

```bash
uv run fep-lean setup
uv run fep-lean preflight
```

See the local [agent contract](AGENTS.md) and the package-level
[API reference](../../../docs/api.md).
