import FepSketches.gnn_denotation
import FepSketches.gnn_render_statements

/-! Q6 concrete raw embedded input, not runtime-consumed C.
Source SHA256: f2839a599301f0a26d6d382a7dc81ea666324c0af47c4e4648ccd37b995dbabf.
The actual Julia runner applies softmax(C). Q4 below is an abstract
matrix implication; no Julia execution or EFE equivalence is established. -/
namespace FEPProbe.Q6JuliaEmbeddedInput
open FEP.GnnDenotation FEP.GnnRenderStatements
noncomputable def symEmbeddedInput : DiscreteTargetTables Bool Bool Bool where
  aMat := fun b0 b1 => (if b0 then if b1 then (1 / 2 : ℝ) else (1 / 2 : ℝ) else if b1 then (1 / 2 : ℝ) else (1 / 2 : ℝ))
  bMat := fun b0 b1 b2 => (if b0 then (if b1 then if b2 then (1 / 2 : ℝ) else (1 / 2 : ℝ) else if b2 then (1 / 2 : ℝ) else (1 / 2 : ℝ)) else (if b1 then if b2 then (1 / 2 : ℝ) else (1 / 2 : ℝ) else if b2 then (1 / 2 : ℝ) else (1 / 2 : ℝ)))
  cVec := fun b0 => if b0 then (1 / 2 : ℝ) else (1 / 2 : ℝ)
  dVec := fun b0 => if b0 then (1 / 2 : ℝ) else (1 / 2 : ℝ)
  eVec := fun b0 => if b0 then (3 / 4 : ℝ) else (1 / 4 : ℝ)

theorem symEmbeddedInput_eq_Q2 :
    DiscreteTargetFaithful symEmbeddedInput symBoolPayload := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro v0 v1
    cases v0 <;> cases v1 <;> norm_num [symEmbeddedInput, symBoolPayload]
  · intro v0 v1 v2
    cases v0 <;> cases v1 <;> cases v2 <;> norm_num [symEmbeddedInput, symBoolPayload]
  · intro v0
    cases v0 <;> norm_num [symEmbeddedInput, symBoolPayload]
  · intro v0
    cases v0 <;> norm_num [symEmbeddedInput, symBoolPayload]
  · intro v0
    cases v0 <;> norm_num [symEmbeddedInput, symBoolPayload]

/-- Abstract conditional matrix statement, not runtime C equality. -/
theorem symEmbeddedInput_Q4_conditional :
    Statement5ActiveInferenceJl symBoolDoc symBoolPayload symBoolConforms
      symEmbeddedInput := statement5DiscreteMatrices_holds _ _ _ _

/-- The five raw inputs equal the Q2 carrier masses. -/
theorem symEmbeddedInput_Q2_carrierMasses :
    (∀ state outcome : Bool, symEmbeddedInput.aMat outcome state =
      (denoteDiscrete symBoolDoc symBoolPayload symBoolConforms).likelihood.mass state outcome) ∧
    (∀ policy previous next : Bool, symEmbeddedInput.bMat next previous policy =
      ((denoteDiscrete symBoolDoc symBoolPayload symBoolConforms).transition policy).mass previous next) ∧
    (∀ outcome : Bool, symEmbeddedInput.cVec outcome =
      (denoteDiscrete symBoolDoc symBoolPayload symBoolConforms).preferences.mass outcome) ∧
    (∀ state : Bool, symEmbeddedInput.dVec state =
      (denoteDiscrete symBoolDoc symBoolPayload symBoolConforms).initialState.mass state) ∧
    (∀ policy : Bool, symEmbeddedInput.eVec policy =
      (denoteDiscrete symBoolDoc symBoolPayload symBoolConforms).policyPrior.mass policy) :=
  statement5DiscreteMatrices_holds _ _ _ _ symEmbeddedInput_eq_Q2

end FEPProbe.Q6JuliaEmbeddedInput
