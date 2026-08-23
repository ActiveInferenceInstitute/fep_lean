import FepSketches.learning_theory

/-!
# Finite empirical risk and Laplace calibration

This module keeps sample counts finite and evaluates pointwise losses under the
shared normalized `FiniteLaw` carrier.  Laplace smoothing is treated as an
explicit affine transformation of the empirical rate; concentration transfer
therefore follows from deterministic event containment rather than an
unrestricted posterior-contraction claim.
-/

namespace FEP.EmpiricalRisk

open FEP Finset
open FEP.VariationalDuality
open scoped BigOperators

variable {Ω : Type*} [Fintype Ω]

/-! ## Empirical and Laplace rates -/

/-- Empirical success rate for a positive finite sample count. -/
noncomputable def empiricalRate (successes sampleCount : ℕ) : ℝ :=
  (successes : ℝ) / sampleCount

/-- Add-one (Laplace) estimate of a Bernoulli success probability. -/
noncomputable def laplaceEstimate (successes sampleCount : ℕ) : ℝ :=
  ((successes : ℝ) + 1) / ((sampleCount : ℝ) + 2)

/-- Multiplicative shrinkage applied to empirical error by Laplace smoothing. -/
noncomputable def shrinkage (sampleCount : ℕ) : ℝ :=
  (sampleCount : ℝ) / ((sampleCount : ℝ) + 2)

/-- Target-dependent affine offset in the Laplace error identity. -/
noncomputable def laplaceBias (sampleCount : ℕ) (target : ℝ) : ℝ :=
  (1 - 2 * target) / ((sampleCount : ℝ) + 2)

theorem shrinkage_nonneg (sampleCount : ℕ) :
    0 ≤ shrinkage sampleCount := by
  unfold shrinkage
  positivity

theorem shrinkage_le_one (sampleCount : ℕ) :
    shrinkage sampleCount ≤ 1 := by
  unfold shrinkage
  apply (div_le_one (by positivity : (0 : ℝ) < (sampleCount : ℝ) + 2)).2
  norm_num

/-- Laplace error is a contracted empirical error plus an explicit bias. -/
theorem laplaceError_identity (successes sampleCount : ℕ) (target : ℝ)
    (sampleCountPositive : 0 < sampleCount) :
    laplaceEstimate successes sampleCount - target =
      shrinkage sampleCount * (empiricalRate successes sampleCount - target) +
        laplaceBias sampleCount target := by
  have sampleCountNonzero : (sampleCount : ℝ) ≠ 0 := by
    exact_mod_cast Nat.ne_of_gt sampleCountPositive
  have denominatorNonzero : (sampleCount : ℝ) + 2 ≠ 0 := by
    positivity
  unfold laplaceEstimate shrinkage empiricalRate laplaceBias
  field_simp [sampleCountNonzero, denominatorNonzero]
  ring

/-- The affine Laplace offset is uniformly at most one pseudo-count over the
smoothed denominator for targets in the unit interval. -/
theorem laplaceBias_abs_le (sampleCount : ℕ) (target : ℝ)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1) :
    |laplaceBias sampleCount target| ≤
      1 / ((sampleCount : ℝ) + 2) := by
  have denominatorPositive : (0 : ℝ) < (sampleCount : ℝ) + 2 := by
    positivity
  rw [laplaceBias, abs_div, abs_of_pos denominatorPositive]
  apply (div_le_div_iff_of_pos_right denominatorPositive).2
  exact abs_le.2 ⟨by linarith [targetBounds.2], by linarith [targetBounds.1]⟩

/-- Absolute empirical error transfers through Laplace smoothing with the
exact shrinkage coefficient and one-pseudo-count offset. -/
theorem laplaceAbsoluteError_le (successes sampleCount : ℕ) (target error : ℝ)
    (sampleCountPositive : 0 < sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1)
    (empiricalErrorBound :
      |empiricalRate successes sampleCount - target| ≤ error) :
    |laplaceEstimate successes sampleCount - target| ≤
      shrinkage sampleCount * error + 1 / ((sampleCount : ℝ) + 2) := by
  rw [laplaceError_identity successes sampleCount target sampleCountPositive]
  calc
    |shrinkage sampleCount *
          (empiricalRate successes sampleCount - target) +
        laplaceBias sampleCount target| ≤
        |shrinkage sampleCount *
          (empiricalRate successes sampleCount - target)| +
          |laplaceBias sampleCount target| := abs_add_le _ _
    _ = shrinkage sampleCount *
          |empiricalRate successes sampleCount - target| +
          |laplaceBias sampleCount target| := by
      rw [abs_mul, abs_of_nonneg (shrinkage_nonneg sampleCount)]
    _ ≤ shrinkage sampleCount * error +
          1 / ((sampleCount : ℝ) + 2) :=
      add_le_add
        (mul_le_mul_of_nonneg_left empiricalErrorBound
          (shrinkage_nonneg sampleCount))
        (laplaceBias_abs_le sampleCount target targetBounds)

/-- Squared Laplace error is bounded pointwise by twice the contracted
empirical squared error plus twice the squared pseudo-count offset. -/
theorem laplaceSquaredError_le (successes sampleCount : ℕ) (target : ℝ)
    (sampleCountPositive : 0 < sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1) :
    (laplaceEstimate successes sampleCount - target) ^ 2 ≤
      2 * shrinkage sampleCount ^ 2 *
          (empiricalRate successes sampleCount - target) ^ 2 +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
  have biasSquareBound :
      laplaceBias sampleCount target ^ 2 ≤
        (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
    rw [sq_le_sq, abs_of_pos (by positivity : (0 : ℝ) <
      1 / ((sampleCount : ℝ) + 2))]
    exact laplaceBias_abs_le sampleCount target targetBounds
  have sumSquareBound :
      (shrinkage sampleCount *
          (empiricalRate successes sampleCount - target) +
        laplaceBias sampleCount target) ^ 2 ≤
        2 * (shrinkage sampleCount *
          (empiricalRate successes sampleCount - target)) ^ 2 +
        2 * laplaceBias sampleCount target ^ 2 := by
    nlinarith [sq_nonneg
      (shrinkage sampleCount *
        (empiricalRate successes sampleCount - target) -
          laplaceBias sampleCount target)]
  rw [laplaceError_identity successes sampleCount target sampleCountPositive]
  calc
    (shrinkage sampleCount *
          (empiricalRate successes sampleCount - target) +
        laplaceBias sampleCount target) ^ 2 ≤
        2 * (shrinkage sampleCount *
          (empiricalRate successes sampleCount - target)) ^ 2 +
        2 * laplaceBias sampleCount target ^ 2 := sumSquareBound
    _ ≤ 2 * (shrinkage sampleCount *
          (empiricalRate successes sampleCount - target)) ^ 2 +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
      nlinarith
    _ = 2 * shrinkage sampleCount ^ 2 *
          (empiricalRate successes sampleCount - target) ^ 2 +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by ring

/-! ## Finite-law risks -/

theorem expectation_mono (sampling : FiniteLaw Ω) (left right : Ω → ℝ)
    (pointwise : ∀ outcome, left outcome ≤ right outcome) :
    VariationalDuality.expectation sampling left ≤
      VariationalDuality.expectation sampling right := by
  unfold VariationalDuality.expectation
  exact Finset.sum_le_sum fun outcome _ =>
    mul_le_mul_of_nonneg_left (pointwise outcome) (sampling.nonneg outcome)

theorem expectation_add (sampling : FiniteLaw Ω) (left right : Ω → ℝ) :
    VariationalDuality.expectation sampling (fun outcome =>
      left outcome + right outcome) =
      VariationalDuality.expectation sampling left +
        VariationalDuality.expectation sampling right := by
  simp [VariationalDuality.expectation, mul_add, Finset.sum_add_distrib]

theorem expectation_const_mul (sampling : FiniteLaw Ω) (constant : ℝ)
    (value : Ω → ℝ) :
    VariationalDuality.expectation sampling (fun outcome =>
      constant * value outcome) =
      constant * VariationalDuality.expectation sampling value := by
  unfold VariationalDuality.expectation
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro outcome _
  ring

theorem expectation_const (sampling : FiniteLaw Ω) (constant : ℝ) :
    VariationalDuality.expectation sampling (fun _ => constant) = constant := by
  unfold VariationalDuality.expectation
  rw [← Finset.sum_mul, sampling.sum_one, one_mul]

/-- The pointwise squared-error transfer integrates under any normalized
finite sampling law. -/
theorem laplaceSquaredRisk_le (sampling : FiniteLaw Ω)
    (successes : Ω → ℕ) (sampleCount : ℕ) (target : ℝ)
    (sampleCountPositive : 0 < sampleCount)
    (successesAtMost : ∀ outcome, successes outcome ≤ sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1) :
    VariationalDuality.expectation sampling (fun outcome =>
      (laplaceEstimate (successes outcome) sampleCount - target) ^ 2) ≤
      2 * shrinkage sampleCount ^ 2 *
          VariationalDuality.expectation sampling (fun outcome =>
            (empiricalRate (successes outcome) sampleCount - target) ^ 2) +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
  have pointwise : ∀ outcome,
      (laplaceEstimate (successes outcome) sampleCount - target) ^ 2 ≤
        2 * shrinkage sampleCount ^ 2 *
            (empiricalRate (successes outcome) sampleCount - target) ^ 2 +
          2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
    intro outcome
    have _ := successesAtMost outcome
    exact laplaceSquaredError_le (successes outcome) sampleCount target
      sampleCountPositive targetBounds
  calc
    VariationalDuality.expectation sampling (fun outcome =>
        (laplaceEstimate (successes outcome) sampleCount - target) ^ 2) ≤
        VariationalDuality.expectation sampling (fun outcome =>
          2 * shrinkage sampleCount ^ 2 *
              (empiricalRate (successes outcome) sampleCount - target) ^ 2 +
            2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2) :=
      expectation_mono sampling _ _ pointwise
    _ = VariationalDuality.expectation sampling (fun outcome =>
          2 * shrinkage sampleCount ^ 2 *
            (empiricalRate (successes outcome) sampleCount - target) ^ 2) +
        VariationalDuality.expectation sampling (fun _ =>
          2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2) :=
      expectation_add sampling _ _
    _ = 2 * shrinkage sampleCount ^ 2 *
          VariationalDuality.expectation sampling (fun outcome =>
            (empiricalRate (successes outcome) sampleCount - target) ^ 2) +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
      rw [expectation_const_mul, expectation_const]

/-! ## Bernoulli Brier risk -/

/-- Expected squared error of the Bernoulli probability forecast. -/
noncomputable def bernoulliBrierScore (target forecast : ℝ) : ℝ :=
  target * (1 - forecast) ^ 2 + (1 - target) * forecast ^ 2

/-- Bernoulli Brier excess risk is exactly squared probability error. -/
theorem brierExcess_eq_sqError (target forecast : ℝ) :
    bernoulliBrierScore target forecast - bernoulliBrierScore target target =
      (forecast - target) ^ 2 := by
  unfold bernoulliBrierScore
  ring

/-- Finite-law Brier excess risk of an arbitrary forecast. -/
noncomputable def brierExcessRisk (sampling : FiniteLaw Ω)
    (forecast : Ω → ℝ) (target : ℝ) : ℝ :=
  VariationalDuality.expectation sampling (fun outcome =>
    bernoulliBrierScore target (forecast outcome) -
      bernoulliBrierScore target target)

/-- The Laplace Brier excess risk inherits the finite-law squared-error bound. -/
theorem laplaceBrierRisk_le (sampling : FiniteLaw Ω)
    (successes : Ω → ℕ) (sampleCount : ℕ) (target : ℝ)
    (sampleCountPositive : 0 < sampleCount)
    (successesAtMost : ∀ outcome, successes outcome ≤ sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1) :
    brierExcessRisk sampling
        (fun outcome => laplaceEstimate (successes outcome) sampleCount) target ≤
      2 * shrinkage sampleCount ^ 2 *
          VariationalDuality.expectation sampling (fun outcome =>
            (empiricalRate (successes outcome) sampleCount - target) ^ 2) +
        2 * (1 / ((sampleCount : ℝ) + 2)) ^ 2 := by
  unfold brierExcessRisk
  simp_rw [brierExcess_eq_sqError]
  exact laplaceSquaredRisk_le sampling successes sampleCount target
    sampleCountPositive successesAtMost targetBounds

/-! ## Concentration-event transfer -/

/-- Probability of an event under a normalized finite law. -/
noncomputable def finiteEventProbability (sampling : FiniteLaw Ω)
    (event : Set Ω) : ℝ := by
  classical
  exact ∑ outcome, if outcome ∈ event then sampling outcome else 0

theorem finiteEventProbability_mono (sampling : FiniteLaw Ω)
    {left right : Set Ω} (subset : left ⊆ right) :
    finiteEventProbability sampling left ≤
      finiteEventProbability sampling right := by
  classical
  unfold finiteEventProbability
  apply Finset.sum_le_sum
  intro outcome _
  by_cases leftMembership : outcome ∈ left
  · have rightMembership := subset leftMembership
    simp [leftMembership, rightMembership]
  · by_cases rightMembership : outcome ∈ right
    · simp [leftMembership, rightMembership, sampling.nonneg outcome]
    · simp [leftMembership, rightMembership]

/-- Raw empirical deviation event at tolerance `error`. -/
def empiricalBadEvent (successes : Ω → ℕ) (sampleCount : ℕ)
    (target error : ℝ) : Set Ω :=
  {outcome |
    error < |empiricalRate (successes outcome) sampleCount - target|}

/-- Smoothed deviation event above the transferred tolerance. -/
def laplaceBadEvent (successes : Ω → ℕ) (sampleCount : ℕ)
    (target error : ℝ) : Set Ω :=
  {outcome |
    shrinkage sampleCount * error + 1 / ((sampleCount : ℝ) + 2) <
      |laplaceEstimate (successes outcome) sampleCount - target|}

omit [Fintype Ω] in
/-- Every Laplace deviation beyond the transferred threshold implies a raw
empirical deviation beyond the original threshold. -/
theorem laplaceBadEvent_subset (successes : Ω → ℕ) (sampleCount : ℕ)
    (target error : ℝ) (sampleCountPositive : 0 < sampleCount)
    (successesAtMost : ∀ outcome, successes outcome ≤ sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1) :
    laplaceBadEvent successes sampleCount target error ⊆
      empiricalBadEvent successes sampleCount target error := by
  intro outcome smoothedBad
  have _ := successesAtMost outcome
  by_contra rawNotBad
  have rawBound :
      |empiricalRate (successes outcome) sampleCount - target| ≤ error :=
    le_of_not_gt rawNotBad
  have transferred := laplaceAbsoluteError_le
    (successes outcome) sampleCount target error sampleCountPositive
    targetBounds rawBound
  exact (not_le_of_gt smoothedBad) transferred

/-- Event containment transfers any finite-law raw concentration bound to the
Laplace-smoothed event. -/
theorem laplaceBadEvent_probability_le (sampling : FiniteLaw Ω)
    (successes : Ω → ℕ) (sampleCount : ℕ) (target error failure : ℝ)
    (sampleCountPositive : 0 < sampleCount)
    (successesAtMost : ∀ outcome, successes outcome ≤ sampleCount)
    (targetBounds : target ∈ Set.Icc (0 : ℝ) 1)
    (rawProbabilityBound :
      finiteEventProbability sampling
        (empiricalBadEvent successes sampleCount target error) ≤ failure) :
    finiteEventProbability sampling
        (laplaceBadEvent successes sampleCount target error) ≤ failure :=
  (finiteEventProbability_mono sampling
    (laplaceBadEvent_subset successes sampleCount target error
      sampleCountPositive successesAtMost targetBounds)).trans rawProbabilityBound

/-! ## Boundary witness -/

/-- Laplace smoothing has a genuine nonzero offset at a boundary target. -/
theorem laplaceBias_nonzero_witness :
    laplaceBias 2 0 = 1 / 4 ∧ laplaceBias 2 0 ≠ 0 := by
  norm_num [laplaceBias]

end FEP.EmpiricalRisk
