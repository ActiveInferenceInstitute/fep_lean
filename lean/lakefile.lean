import Lake
open Lake DSL

/-- FEP Lean Sketches — FEP/Active Inference theorem skeletons backed by full Mathlib4.

    Add `require mathlib` so that `lake env lean <file>` resolves every
    `import Mathlib.*` module used in the 50-topic catalogue.

    Run setup once in a non-sandboxed terminal:
        cd lean && lake exe cache get && lake build
    Then the LeanVerifier can call `lake env lean <sketch.lean>` for each topic.
-/
package «FepSketches»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.29.0"

@[default_target]
lean_lib «FepSketches» where
  globs := #[.andSubmodules `FepSketches]
