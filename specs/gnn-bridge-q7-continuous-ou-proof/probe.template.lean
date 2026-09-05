import FepSketches.compositions.smooth_reference_kernel
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Tactic

/-! Q7 draft: static coefficient approximation, not floating execution semantics.
The F/Q literals below are exact rational values of the retained binary64 data.
No hypothesis assumes the desired rounding bounds. -/

open MeasureTheory ProbabilityTheory
open FEP.ScalarGaussianSemigroup
open FEPComposed.SmoothReferenceKernel

namespace FEPProbe.Q7ContinuousOU

noncomputable section

def a : ℝ := Real.exp (-1)
def q : ℝ := 1 - a ^ 2
def epsilon : ℝ := 1 / 10 ^ 15
def artifactF : ℝ := @@F@@
def artifactQ : ℝ := @@Q@@
def artifactH : ℝ := @@H@@
def artifactR : ℝ := @@R@@
def artifactPriorMean : ℝ := @@MEAN@@
def artifactPriorCov : ℝ := @@COV@@

theorem artifact_exact_parameters :
    artifactH = 1 ∧
    artifactR = (selectedFilter.observationNoise.variance : ℝ) ∧
    artifactPriorMean = selectedPrior.mean ∧
    artifactPriorCov = (selectedPrior.family.variance : ℝ) ∧
    selectedFilter.stepDuration = 1 := by
  norm_num [artifactH, artifactR, artifactPriorMean, artifactPriorCov,
    selectedFilter, selectedPrior, FEP.PosteriorConvergence.selectedGaussianFamily]

theorem exact_noise_formula : q = 1 - Real.exp (-2) := by
  have h : Real.exp (-2) = a * a := by
    rw [show (-2 : ℝ) = -1 + -1 by norm_num, Real.exp_add]
    rfl
  rw [h, q, pow_two]

private theorem a_pos : 0 < a := Real.exp_pos _

private theorem a_lt_one : a < 1 := by
  rw [a, Real.exp_lt_one_iff]
  norm_num

private theorem q_pos : 0 < q := by
  dsimp [q]
  nlinarith [a_pos, a_lt_one]

def exactNoise : NNReal := ⟨q, q_pos.le⟩

theorem selected_decay : selectedDynamics.decay 1 = a := by
  norm_num [selectedDynamics, ScalarOUParameters.decay, a]

theorem selected_transitionVariance :
    (selectedDynamics.transitionVariance 1 : ℝ) = q := by
  change (selectedDynamics.stationaryVariance : ℝ) *
    (1 - selectedDynamics.decay 1 ^ 2) = q
  rw [selectedDynamics_stationaryVariance, selected_decay]
  simp [q]

theorem exact_row_eq_selected (state : ℝ) :
    selectedDynamics.ouTransition 1 state = gaussianReal (a * state) exactNoise := by
  change gaussianReal (selectedDynamics.transitionMean 1 state)
    (selectedDynamics.transitionVariance 1) = gaussianReal (a * state) exactNoise
  congr 1
  · norm_num [ScalarOUParameters.transitionMean, selectedDynamics,
      ScalarOUParameters.decay, a]
  · apply NNReal.eq
    exact selected_transitionVariance

private def eLower : ℝ := 363916618873 / 133877442384 - 1 / 10 ^ 20
private def eUpper : ℝ := 363916618873 / 133877442384 + 1 / 10 ^ 20
private def aLower : ℝ := 1 / eUpper
private def aUpper : ℝ := 1 / eLower

private theorem a_enclosure : aLower ≤ a ∧ a ≤ aUpper := by
  have hexp := abs_sub_le_iff.mp Real.exp_one_near_20
  have hlo : eLower ≤ Real.exp 1 := by dsimp [eLower]; linarith
  have hhi : Real.exp 1 ≤ eUpper := by dsimp [eUpper]; linarith
  have ha : a = 1 / Real.exp 1 := by rw [a, Real.exp_neg, one_div]
  rw [ha]
  exact ⟨one_div_le_one_div_of_le (Real.exp_pos _) hhi,
    one_div_le_one_div_of_le (by norm_num [eLower]) hlo⟩

theorem artifact_F_bound : |artifactF - a| ≤ epsilon := by
  have hlo : artifactF - epsilon ≤ aLower := by
    norm_num [artifactF, epsilon, aLower, eUpper]
  have hhi : aUpper ≤ artifactF + epsilon := by
    norm_num [artifactF, epsilon, aUpper, eLower]
  rcases a_enclosure with ⟨hal, hau⟩
  rw [abs_sub_le_iff]
  constructor <;> linarith

theorem artifact_Q_bound : |artifactQ - q| ≤ epsilon := by
  rcases a_enclosure with ⟨hal, hau⟩
  have hsl := mul_self_le_mul_self (show 0 ≤ aLower by
    norm_num [aLower, eUpper]) hal
  have hsu := mul_self_le_mul_self a_pos.le hau
  have hlo : artifactQ - epsilon ≤ 1 - aUpper ^ 2 := by
    norm_num [artifactQ, epsilon, aUpper, eLower]
  have hhi : 1 - aLower ^ 2 ≤ artifactQ + epsilon := by
    norm_num [artifactQ, epsilon, aLower, eUpper]
  rw [abs_sub_le_iff]
  dsimp [q]
  constructor <;> nlinarith

private theorem artifactF_unit : 0 ≤ artifactF ∧ artifactF ≤ 1 := by
  norm_num [artifactF]

private theorem square_error_bound : |artifactF ^ 2 - a ^ 2| ≤ 2 * epsilon := by
  have hsum : |artifactF + a| ≤ 2 := by
    rw [abs_of_nonneg (add_nonneg artifactF_unit.1 a_pos.le)]
    linarith [artifactF_unit.2, a_lt_one]
  calc
    |artifactF ^ 2 - a ^ 2| = |artifactF - a| * |artifactF + a| := by
      rw [← abs_mul]
      congr 1
      ring
    _ ≤ epsilon * 2 := mul_le_mul artifact_F_bound hsum (abs_nonneg _)
      (by norm_num [epsilon])
    _ = 2 * epsilon := by ring

theorem artifact_prediction_mean_bound (mean : ℝ) :
    |artifactF * mean - a * mean| ≤ epsilon * |mean| := by
  rw [show artifactF * mean - a * mean = (artifactF - a) * mean by ring,
    abs_mul]
  exact mul_le_mul_of_nonneg_right artifact_F_bound (abs_nonneg _)

theorem artifact_prediction_variance_bound (variance : ℝ) (hv : 0 ≤ variance) :
    |(artifactF ^ 2 * variance + artifactQ) - (a ^ 2 * variance + q)| ≤
      (2 * variance + 1) * epsilon := by
  calc
    |(artifactF ^ 2 * variance + artifactQ) - (a ^ 2 * variance + q)| =
        |(artifactF ^ 2 - a ^ 2) * variance + (artifactQ - q)| := by
      congr 1
      ring
    _ ≤ |(artifactF ^ 2 - a ^ 2) * variance| + |artifactQ - q| := abs_add_le _ _
    _ = |artifactF ^ 2 - a ^ 2| * variance + |artifactQ - q| := by
      rw [abs_mul, abs_of_nonneg hv]
    _ ≤ (2 * epsilon) * variance + epsilon :=
      add_le_add (mul_le_mul_of_nonneg_right square_error_bound hv) artifact_Q_bound
    _ = (2 * variance + 1) * epsilon := by ring

theorem artifact_stationary_defect_bound :
    |artifactF ^ 2 + artifactQ - 1| ≤ 3 * epsilon := by
  have h := artifact_prediction_variance_bound 1 (by norm_num)
  dsimp [q] at h
  ring_nf at h ⊢
  exact h

/-- The nonstationary mean-one witness cannot silently become a no-op. -/
theorem nonstationary_prediction_changes_mean : artifactF * 1 ≠ (1 : ℝ) := by
  norm_num [artifactF]

/-- Scalar Joseph covariance expression equals the exact conjugate formula. -/
theorem scalar_joseph_identity (predicted noise : ℝ)
    (hp : 0 < predicted) (hr : 0 < noise) :
    (1 - predicted / (predicted + noise)) ^ 2 * predicted +
      (predicted / (predicted + noise)) ^ 2 * noise =
        predicted * noise / (predicted + noise) := by
  have hne : predicted + noise ≠ 0 := ne_of_gt (add_pos hp hr)
  field_simp [hne]
  ring

end
end FEPProbe.Q7ContinuousOU
