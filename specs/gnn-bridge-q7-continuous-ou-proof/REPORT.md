# Q7: scalar OU coefficient bounds

Verified locally on 2026-09-04. The current [schema-2 native receipt](native_receipt.json)
passes independent retained validation after explicit source pinning, canonical
rendering, deterministic probe regeneration, and native compilation.

## Claim and scope

The decoded binary64 coefficients of the canonical scalar-OU JAX render have exact-real error bounds of 10^-15 against the selected OU formulas. The proof also bounds one-step prediction and stationary defects and proves a scalar Joseph identity.

These are real-arithmetic bounds over decoded coefficients. They do not bound JAX arithmetic, accumulated trajectory error, arbitrary LGSSMs, SDE solutions, or empirical behavior.

## Retained evidence

- [Canonical render provenance](render_provenance.json) binds the actual renderer command, input/output bytes, source pin, and unchanged owners.
- [Generated proof manifest](generated/artifact_proof_manifest.json) binds extraction and probe generation separately from native evidence.
- [Native receipt](native_receipt.json) binds the immutable slice contract, shared engine, exact checked Python/probe buffers, recursive formal imports, resolved compiler binaries, commands, and native transcripts.
- The 1 positive probe(s) compiled without warnings or `sorryAx`; all 12 named theorem reports use only standard axioms.
- Receipt SHA-256: `70f6e8b267c44189aa41e6b2adf3e777ad4ed51f60dfc8500e70c2110417c4a5`.

| Theorem | Native axiom result |
| --- | --- |
| `FEPProbe.Q7ContinuousOU.artifact_F_bound` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.artifact_Q_bound` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.artifact_exact_parameters` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.artifact_prediction_mean_bound` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.artifact_prediction_variance_bound` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.artifact_stationary_defect_bound` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.exact_noise_formula` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.exact_row_eq_selected` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.nonstationary_prediction_changes_mean` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.scalar_joseph_identity` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.selected_decay` | standard axioms only |
| `FEPProbe.Q7ContinuousOU.selected_transitionVariance` | standard axioms only |

## Regression evidence

Q6 passed both positive probes and the normalized previous/action-axis rejection.
Q7 passed its positive 12-theorem census and both wrong-coefficient rejections.
Its initial notation-scope and tactic-linter defects were repaired without
changing theorem statements, bounds, or warning policy. The independent read-only
review confirmed that scope and the repair. Q5's native regressions passed in
the frozen full baseline; its schema-2 receipt was then freshly compiled.

The final integrated nonserial Python suite passed 1,460 tests with seven skips,
529 native deselections, and 89.83% coverage. See the
[coordinated wave-2 report](../gnn-bridge-w2-source-custody/WAVE2-REPORT.md) for
exact test scopes, source-freeze evidence, and the separate H2 acceptance record.

## Reproduction

Follow [the slice README](README.md) to refresh canonical rendering and regenerate
probes after source changes. Native compilation is explicit and serialized:

```bash
uv run python specs/gnn-bridge-q7-continuous-ou-proof/verify_native.py --compile --gnn-root GNN_PATH --receipt specs/gnn-bridge-q7-continuous-ou-proof/native_receipt.json
uv run python specs/gnn-bridge-q7-continuous-ou-proof/verify_native.py --check --gnn-root GNN_PATH --receipt specs/gnn-bridge-q7-continuous-ou-proof/native_receipt.json
```

Default and `--check` validation are read-only. A source, contract, artifact,
import, or toolchain change invalidates the corresponding receipt. Content
custody assumes trusted local Python and toolchain binaries; it is not a sandbox
or independent host/compiler authentication. Publication and provider-backed
execution retain their separate acceptance requirements.
