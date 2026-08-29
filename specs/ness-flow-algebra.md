# Two-coordinate antisymmetric-dissipative algebra

Status: **accepted under the source-bound
[`ness-flow-algebra-acceptance.json`](ness-flow-algebra-acceptance.json)
receipt; this record is independent of Horizon 2.**

## Scope

The maintained `FEP.NessFlow` namespace owns a small algebraic example on
`Fin 2 → ℝ`.  It defines an antisymmetric rotation, an isotropic scalar map
that is dissipative when its coefficient is nonnegative, and their difference.
The public results establish only the following identities:

- squared norm is nonnegative;
- the rotation is antisymmetric and orthogonal to its input;
- the combined field has inner product `-γ * normSq g` with `g`;
- that inner product is nonpositive when `γ ≥ 0`;
- for a nonzero input, the rotation vanishes exactly when `ω = 0`.

The historical namespace and filename are retained for manifest stability.
They do not constitute a model of a non-equilibrium steady state.  No
probability law, stationary process, current, detailed-balance relation,
entropy-production functional, free-energy objective, gradient/chain-rule
certificate, thermodynamic work, or biological interpretation is supplied.

## Exact public surface

Definitions, in order:

1. `dot`
2. `normSq`
3. `solenoidal`
4. `dissipative`
5. `flow`

Theorems, in order:

1. `normSq_nonneg`
2. `solenoidal_antisymm`
3. `solenoidal_orthogonal`
4. `flow_inner_eq_neg_normSq`
5. `flow_inner_nonpos`
6. `solenoidal_eq_zero_iff`

## Acceptance

- The canonical source and generated workspace projection are byte-identical.
- The manifest retains exactly one `FOUNDATION` owner under `FEP.NessFlow`.
- The six theorem statements compile through independent typed consumers.
- Every public theorem uses only the repository's standard Lean axioms and no
  `sorryAx`.
- The former entropy-production, detailed-balance, free-energy, NESS-signature,
  and external-demo claims are absent from executable declarations.
- Coverage and atlas projections are regenerated after the public roster is
  narrowed.

The receipt binds the reviewed pre-receipt source, test, and specification
hashes; the final toolchain, canonical source, workspace projection, focused
test, and specification bytes; compiler evidence; and the independent
`approved_bounded_algebra_no_model_contract` verdict.  The focused test checks
the live manifest/projection boundary and records the generated module and
theorem counts as an acceptance snapshot.  Mutable aggregate and generated
coverage artifacts are deliberately not source-bound by this narrow receipt.
This acceptance does not refresh the repository's publication receipts.
