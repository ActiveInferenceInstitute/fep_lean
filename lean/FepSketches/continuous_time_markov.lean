import FepSketches.finite_markov_dynamics

/-!
# Exact two-state continuous-time Markov thermodynamics

The construction is deliberately restricted to a two-state chain with two
strictly positive rates.  Its transition kernel is given in closed form, so
the semigroup, master equation, detailed balance, relaxation, and Lyapunov
law can all be proved entrywise without importing an SDE or PDE model.
-/

namespace FEP.ContinuousTimeMarkov

open FEP Finset
open scoped BigOperators

/-- Positive jump rates `false → true` and `true → false`. -/
structure TwoStateRates where
  forward : ℝ
  backward : ℝ
  forward_pos : 0 < forward
  backward_pos : 0 < backward

namespace TwoStateRates

def decayRate (rates : TwoStateRates) : ℝ :=
  rates.forward + rates.backward

theorem decayRate_pos (rates : TwoStateRates) : 0 < rates.decayRate :=
  add_pos rates.forward_pos rates.backward_pos

noncomputable def stationaryFalse (rates : TwoStateRates) : ℝ :=
  rates.backward / rates.decayRate

noncomputable def stationaryTrue (rates : TwoStateRates) : ℝ :=
  rates.forward / rates.decayRate

theorem stationaryFalse_pos (rates : TwoStateRates) :
    0 < rates.stationaryFalse :=
  div_pos rates.backward_pos rates.decayRate_pos

theorem stationaryTrue_pos (rates : TwoStateRates) :
    0 < rates.stationaryTrue :=
  div_pos rates.forward_pos rates.decayRate_pos

theorem stationary_sum_one (rates : TwoStateRates) :
    rates.stationaryFalse + rates.stationaryTrue = 1 := by
  unfold stationaryFalse stationaryTrue decayRate
  field_simp [ne_of_gt (add_pos rates.forward_pos rates.backward_pos)]
  ring

theorem stationaryTrue_mul_decayRate (rates : TwoStateRates) :
    rates.stationaryTrue * rates.decayRate = rates.forward := by
  unfold stationaryTrue
  exact div_mul_cancel₀ rates.forward (ne_of_gt rates.decayRate_pos)

theorem stationaryFalse_mul_decayRate (rates : TwoStateRates) :
    rates.stationaryFalse * rates.decayRate = rates.backward := by
  unfold stationaryFalse
  exact div_mul_cancel₀ rates.backward (ne_of_gt rates.decayRate_pos)

/-- Stationary law `(b/(a+b), a/(a+b))`. -/
noncomputable def stationaryLaw (rates : TwoStateRates) : FiniteLaw Bool where
  mass state := if state then rates.stationaryTrue else rates.stationaryFalse
  nonneg state := by
    cases state <;> simp [rates.stationaryFalse_pos.le,
      rates.stationaryTrue_pos.le]
  sum_one := by
    simpa [Fintype.sum_bool, add_comm] using rates.stationary_sum_one

/-- Exact exponential relaxation factor. -/
noncomputable def rho (rates : TwoStateRates) (time : ℝ) : ℝ :=
  Real.exp (-rates.decayRate * time)

theorem rho_pos (rates : TwoStateRates) (time : ℝ) : 0 < rates.rho time :=
  Real.exp_pos _

theorem rho_le_one (rates : TwoStateRates) {time : ℝ} (hTime : 0 ≤ time) :
    rates.rho time ≤ 1 := by
  rw [rho, Real.exp_le_one_iff]
  exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr rates.decayRate_pos.le)
    hTime

@[simp]
theorem rho_zero (rates : TwoStateRates) : rates.rho 0 = 1 := by
  simp [rho]

theorem rho_add (rates : TwoStateRates) (left right : ℝ) :
    rates.rho (left + right) = rates.rho left * rates.rho right := by
  rw [rho, rho, rho, ← Real.exp_add]
  congr 1
  ring

/-- Closed-form two-state transition probability. -/
noncomputable def transition (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) : ℝ :=
  match source, target with
  | false, false => rates.stationaryFalse + rates.stationaryTrue * rates.rho time
  | false, true => rates.stationaryTrue * (1 - rates.rho time)
  | true, false => rates.stationaryFalse * (1 - rates.rho time)
  | true, true => rates.stationaryTrue + rates.stationaryFalse * rates.rho time

theorem transition_rowSum (rates : TwoStateRates) (time : ℝ)
    (source : Bool) :
    ∑ target, rates.transition time source target = 1 := by
  cases source <;> simp only [Fintype.sum_bool, transition]
  · calc
      rates.stationaryTrue * (1 - rates.rho time) +
          (rates.stationaryFalse + rates.stationaryTrue * rates.rho time) =
          rates.stationaryFalse + rates.stationaryTrue := by ring
      _ = 1 := rates.stationary_sum_one
  · calc
      rates.stationaryTrue + rates.stationaryFalse * rates.rho time +
          rates.stationaryFalse * (1 - rates.rho time) =
          rates.stationaryFalse + rates.stationaryTrue := by ring
      _ = 1 := rates.stationary_sum_one

theorem transition_nonneg (rates : TwoStateRates) {time : ℝ}
    (hTime : 0 ≤ time) (source target : Bool) :
    0 ≤ rates.transition time source target := by
  have hRho : 0 ≤ rates.rho time := (rates.rho_pos time).le
  have hOneSub : 0 ≤ 1 - rates.rho time := sub_nonneg.mpr (rates.rho_le_one hTime)
  cases source <;> cases target <;> simp only [transition]
  · exact add_nonneg rates.stationaryFalse_pos.le
      (mul_nonneg rates.stationaryTrue_pos.le hRho)
  · exact mul_nonneg rates.stationaryTrue_pos.le hOneSub
  · exact mul_nonneg rates.stationaryFalse_pos.le hOneSub
  · exact add_nonneg rates.stationaryTrue_pos.le
      (mul_nonneg rates.stationaryFalse_pos.le hRho)

/-- The normalized two-state finite kernel at nonnegative time. -/
noncomputable def kernel (rates : TwoStateRates) (time : ℝ)
    (hTime : 0 ≤ time) : FiniteKernel Bool Bool where
  mass := rates.transition time
  nonneg := rates.transition_nonneg hTime
  sum_one := rates.transition_rowSum time

theorem transition_zero (rates : TwoStateRates) (source target : Bool) :
    rates.transition 0 source target = if source = target then 1 else 0 := by
  cases source <;> cases target <;>
    simp [transition, rates.stationary_sum_one, add_comm]

/-- Chapman--Kolmogorov for the exact two-state transition function. -/
theorem transition_add (rates : TwoStateRates) (left right : ℝ)
    (source target : Bool) :
    rates.transition (left + right) source target =
      ∑ middle,
        rates.transition left source middle *
          rates.transition right middle target := by
  have hStationary := rates.stationary_sum_one
  have hTrue : rates.stationaryTrue = 1 - rates.stationaryFalse := by
    linarith
  cases source <;> cases target <;>
    simp only [Fintype.sum_bool, transition] <;>
    rw [rates.rho_add left right, hTrue] <;> ring

/-- Generator with rows `(-a,a)` and `(b,-b)`. -/
def generator (rates : TwoStateRates) (source target : Bool) : ℝ :=
  match source, target with
  | false, false => -rates.forward
  | false, true => rates.forward
  | true, false => rates.backward
  | true, true => -rates.backward

/-- Entrywise derivative of the closed-form transition matrix. -/
noncomputable def transitionDerivative (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) : ℝ :=
  match source, target with
  | false, false => -rates.forward * rates.rho time
  | false, true => rates.forward * rates.rho time
  | true, false => rates.backward * rates.rho time
  | true, true => -rates.backward * rates.rho time

theorem rho_hasDerivAt (rates : TwoStateRates) (time : ℝ) :
    HasDerivAt rates.rho (-rates.decayRate * rates.rho time) time := by
  change HasDerivAt
    (fun candidate ↦ Real.exp (-rates.decayRate * candidate))
    (-rates.decayRate * Real.exp (-rates.decayRate * time)) time
  simpa only [Function.id_def, one_mul, mul_one, mul_comm] using
    ((hasDerivAt_id time).const_mul (-rates.decayRate)).exp

theorem transition_hasDerivAt (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) :
    HasDerivAt (fun candidate ↦ rates.transition candidate source target)
      (rates.transitionDerivative time source target) time := by
  have hRho := rates.rho_hasDerivAt time
  cases source <;> cases target
  · change HasDerivAt
      (fun candidate ↦ rates.stationaryFalse +
        rates.stationaryTrue * rates.rho candidate)
      (-rates.forward * rates.rho time) time
    apply ((hasDerivAt_const time rates.stationaryFalse).add
      (hRho.const_mul rates.stationaryTrue)).congr_deriv
    rw [← rates.stationaryTrue_mul_decayRate]
    ring
  · change HasDerivAt
      (fun candidate ↦ rates.stationaryTrue * (1 - rates.rho candidate))
      (rates.forward * rates.rho time) time
    apply (((hasDerivAt_const time 1).sub hRho).const_mul
      rates.stationaryTrue).congr_deriv
    rw [← rates.stationaryTrue_mul_decayRate]
    ring
  · change HasDerivAt
      (fun candidate ↦ rates.stationaryFalse * (1 - rates.rho candidate))
      (rates.backward * rates.rho time) time
    apply (((hasDerivAt_const time 1).sub hRho).const_mul
      rates.stationaryFalse).congr_deriv
    rw [← rates.stationaryFalse_mul_decayRate]
    ring
  · change HasDerivAt
      (fun candidate ↦ rates.stationaryTrue +
        rates.stationaryFalse * rates.rho candidate)
      (-rates.backward * rates.rho time) time
    apply ((hasDerivAt_const time rates.stationaryTrue).add
      (hRho.const_mul rates.stationaryFalse)).congr_deriv
    rw [← rates.stationaryFalse_mul_decayRate]
    ring

theorem generator_mul_transition (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) :
    (∑ middle,
        rates.generator source middle * rates.transition time middle target) =
      rates.transitionDerivative time source target := by
  have hStationary := rates.stationary_sum_one
  have hTrue : rates.stationaryTrue = 1 - rates.stationaryFalse := by
    linarith
  cases source <;> cases target <;>
    simp only [Fintype.sum_bool, generator, transition, transitionDerivative] <;>
    simp only [← rates.stationaryTrue_mul_decayRate,
      ← rates.stationaryFalse_mul_decayRate] <;>
    rw [hTrue] <;> ring

theorem transition_mul_generator (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) :
    (∑ middle,
        rates.transition time source middle * rates.generator middle target) =
      rates.transitionDerivative time source target := by
  have hStationary := rates.stationary_sum_one
  have hTrue : rates.stationaryTrue = 1 - rates.stationaryFalse := by
    linarith
  cases source <;> cases target <;>
    simp only [Fintype.sum_bool, generator, transition, transitionDerivative] <;>
    simp only [← rates.stationaryTrue_mul_decayRate,
      ← rates.stationaryFalse_mul_decayRate] <;>
    rw [hTrue] <;> ring

/-- The derivative equals both generator products, entry by entry. -/
theorem transition_masterEquation (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) :
    HasDerivAt (fun candidate ↦ rates.transition candidate source target)
        (∑ middle,
          rates.generator source middle * rates.transition time middle target)
        time ∧
      HasDerivAt (fun candidate ↦ rates.transition candidate source target)
        (∑ middle,
          rates.transition time source middle * rates.generator middle target)
        time := by
  constructor
  · rw [rates.generator_mul_transition time source target]
    exact rates.transition_hasDerivAt time source target
  · rw [rates.transition_mul_generator time source target]
    exact rates.transition_hasDerivAt time source target

theorem transition_stationary (rates : TwoStateRates) (time : ℝ)
    (target : Bool) :
    (∑ source,
        rates.stationaryLaw source * rates.transition time source target) =
      rates.stationaryLaw target := by
  have hStationary := rates.stationary_sum_one
  have hTrue : rates.stationaryTrue = 1 - rates.stationaryFalse := by
    linarith
  cases target <;>
    simp only [Fintype.sum_bool, stationaryLaw,
      transition, Bool.false_eq_true, if_false, if_true] <;>
    rw [hTrue] <;> ring

theorem transition_detailedBalance (rates : TwoStateRates) (time : ℝ)
    (source target : Bool) :
    rates.stationaryLaw source * rates.transition time source target =
      rates.stationaryLaw target * rates.transition time target source := by
  cases source <;> cases target <;>
    simp [stationaryLaw, transition] <;> ring

/-- True-state mass after evolving an arbitrary initial law. -/
noncomputable def trueMass (rates : TwoStateRates)
    (initial : FiniteLaw Bool) (time : ℝ) : ℝ :=
  ∑ source, initial source * rates.transition time source true

/-- Exact exponential relaxation of the nonstationary coordinate. -/
theorem relaxation_exact (rates : TwoStateRates)
    (initial : FiniteLaw Bool) (time : ℝ) :
    rates.trueMass initial time - rates.stationaryTrue =
      rates.rho time * (initial true - rates.stationaryTrue) := by
  have hInitial : initial false + initial true = 1 := by
    simpa [Fintype.sum_bool, add_comm] using initial.sum_one
  have hStationary := rates.stationary_sum_one
  have hInitialFalse : initial false = 1 - initial true := by
    linarith
  have hStationaryFalse :
      rates.stationaryFalse = 1 - rates.stationaryTrue := by
    linarith
  simp only [trueMass, Fintype.sum_bool, transition]
  rw [hInitialFalse, hStationaryFalse]
  ring

/-- Quadratic distance of the true-state mass from stationarity. -/
noncomputable def lyapunov (rates : TwoStateRates)
    (initial : FiniteLaw Bool) (time : ℝ) : ℝ :=
  (rates.trueMass initial time - rates.stationaryTrue) ^ 2

theorem lyapunov_exact (rates : TwoStateRates)
    (initial : FiniteLaw Bool) (time : ℝ) :
    rates.lyapunov initial time =
      rates.rho time ^ 2 *
        (initial true - rates.stationaryTrue) ^ 2 := by
  rw [lyapunov, rates.relaxation_exact initial time]
  ring

theorem lyapunov_hasDerivAt (rates : TwoStateRates)
    (initial : FiniteLaw Bool) (time : ℝ) :
    HasDerivAt (rates.lyapunov initial)
      (-2 * rates.decayRate * rates.lyapunov initial time) time := by
  have hLyapunov : rates.lyapunov initial = fun candidate ↦
      rates.rho candidate ^ 2 *
        (initial true - rates.stationaryTrue) ^ 2 := by
    funext candidate
    exact rates.lyapunov_exact initial candidate
  rw [hLyapunov]
  apply (((rates.rho_hasDerivAt time).pow 2).mul_const
    ((initial true - rates.stationaryTrue) ^ 2)).congr_deriv
  ring

/-! ## Plot-ready rates and a strict nonstationary witness -/

noncomputable def benchmarkRates : TwoStateRates where
  forward := 7 / 10
  backward := 3 / 10
  forward_pos := by norm_num
  backward_pos := by norm_num

noncomputable def benchmarkInitial : FiniteLaw Bool :=
  FiniteLaw.pointMass false

theorem benchmarkRates_exact :
    benchmarkRates.forward = 0.7 ∧ benchmarkRates.backward = 0.3 := by
  norm_num [benchmarkRates, OfScientific.ofScientific]

theorem benchmarkInitial_nonstationary :
    benchmarkInitial true ≠ benchmarkRates.stationaryTrue := by
  norm_num [benchmarkInitial, benchmarkRates, stationaryTrue, decayRate,
    FiniteLaw.pointMass]

theorem benchmarkLyapunov_deriv_zero_neg :
    -2 * benchmarkRates.decayRate * benchmarkRates.lyapunov benchmarkInitial 0 < 0 := by
  norm_num [benchmarkRates, benchmarkInitial, decayRate, lyapunov, trueMass,
    transition, stationaryTrue, stationaryFalse, rho, FiniteLaw.pointMass,
    Fintype.sum_bool]

end TwoStateRates

end FEP.ContinuousTimeMarkov
