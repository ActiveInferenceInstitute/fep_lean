import FepSketches.gnn_denotation
import FepSketches.gnn_render_statements

/-! Q6 concrete raw embedded input, not runtime-consumed C.
Source SHA256: f369dfd970150e9607666b9449f5134a09417098435e02baaf632a935e624ae2.
The actual Julia runner applies softmax(C). Q4 below is an abstract
matrix implication; no Julia execution or EFE equivalence is established. -/
namespace FEPProbe.Q6JuliaEmbeddedInputAsym
open FEP.GnnDenotation FEP.GnnRenderStatements
noncomputable def asymEmbeddedInput : DiscreteTargetTables Bool Bool Bool where
  aMat := fun b0 b1 => (if b0 then if b1 then (1 / 2 : ℝ) else (3 / 4 : ℝ) else if b1 then (1 / 2 : ℝ) else (1 / 4 : ℝ))
  bMat := fun b0 b1 b2 => (if b0 then (if b1 then if b2 then (7 / 8 : ℝ) else (1 / 4 : ℝ) else if b2 then (1 / 2 : ℝ) else (3 / 4 : ℝ)) else (if b1 then if b2 then (1 / 8 : ℝ) else (3 / 4 : ℝ) else if b2 then (1 / 2 : ℝ) else (1 / 4 : ℝ)))
  cVec := fun b0 => if b0 then (3 / 4 : ℝ) else (1 / 4 : ℝ)
  dVec := fun b0 => if b0 then (3 / 8 : ℝ) else (5 / 8 : ℝ)
  eVec := fun b0 => if b0 then (5 / 8 : ℝ) else (3 / 8 : ℝ)


noncomputable def asymExpectedPayload : DiscretePayload Bool Bool Bool where
  aLikelihood := fun outcome state =>
    if outcome then (if state then (1 / 2 : ℝ) else (3 / 4 : ℝ))
      else (if state then (1 / 2 : ℝ) else (1 / 4 : ℝ))
  bTransition := fun next previous policy =>
    if next then
      (if previous then (if policy then (7 / 8 : ℝ) else (1 / 4 : ℝ))
        else (if policy then (1 / 2 : ℝ) else (3 / 4 : ℝ)))
    else
      (if previous then (if policy then (1 / 8 : ℝ) else (3 / 4 : ℝ))
        else (if policy then (1 / 2 : ℝ) else (1 / 4 : ℝ)))
  cPreferences := fun outcome => if outcome then (3 / 4 : ℝ) else (1 / 4 : ℝ)
  dInitialState := fun state => if state then (3 / 8 : ℝ) else (5 / 8 : ℝ)
  eHabit := fun policy => if policy then (5 / 8 : ℝ) else (3 / 8 : ℝ)

theorem asymEmbeddedInput_eq_expected :
    DiscreteTargetFaithful asymEmbeddedInput asymExpectedPayload := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro v0 v1
    cases v0 <;> cases v1 <;> norm_num [asymEmbeddedInput, asymExpectedPayload]
  · intro v0 v1 v2
    cases v0 <;> cases v1 <;> cases v2 <;> norm_num [asymEmbeddedInput, asymExpectedPayload]
  · intro v0
    cases v0 <;> norm_num [asymEmbeddedInput, asymExpectedPayload]
  · intro v0
    cases v0 <;> norm_num [asymEmbeddedInput, asymExpectedPayload]
  · intro v0
    cases v0 <;> norm_num [asymEmbeddedInput, asymExpectedPayload]

theorem asymExpected_differs_from_Q2 :
    asymExpectedPayload.dInitialState false ≠ symBoolPayload.dInitialState false ∧
      asymExpectedPayload.aLikelihood false false ≠ symBoolPayload.aLikelihood false false := by
  norm_num [asymExpectedPayload, symBoolPayload]

end FEPProbe.Q6JuliaEmbeddedInputAsym
