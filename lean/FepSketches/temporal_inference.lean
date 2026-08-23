import FepSketches.controlled_markov

/-!
# Finite temporal and hierarchical inference

This module develops normalized forward filtering, nonnegative backward
information messages, forward--backward smoothing, hierarchical prediction,
and Bayesian model averaging on the shared finite-law carrier.  Every
posterior or smoother exposes its positive-normalizer premise.  An asymmetric
Boolean HMM evaluates the filter, backward evidence, and smoother exactly.
-/

namespace FEP.TemporalInference

open FEP FEP.ControlledMarkov Finset
open scoped BigOperators

variable {State Observation Model Upper Middle : Type*}
  [Fintype State] [Fintype Observation] [Fintype Model]
  [Fintype Upper] [Fintype Middle]

/-- A time-homogeneous finite hidden Markov model. -/
structure FiniteHMM (State Observation : Type*)
    [Fintype State] [Fintype Observation] where
  initial : FiniteLaw State
  transition : FiniteKernel State State
  emission : FiniteKernel State Observation

/-- One hidden-state prediction step. -/
def forwardPrediction (prior : FiniteLaw State)
    (transition : FiniteKernel State State) : FiniteLaw State :=
  transition.predictive prior

/-- Evidence of one observation following a hidden-state transition. -/
def forwardEvidence (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation) : ℝ :=
  emission.predictive (forwardPrediction prior transition) observation

/-- One normalized hidden-Markov forward-filtering update. -/
noncomputable def forwardFilter (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (hEvidence : 0 < forwardEvidence prior transition emission observation) :
    FiniteLaw State :=
  emission.posterior (forwardPrediction prior transition) observation hEvidence

/-- The forward filter reconstructs the predicted state-observation joint. -/
theorem forwardFilter_reconstruction (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (hEvidence : 0 < forwardEvidence prior transition emission observation)
    (state : State) :
    forwardFilter prior transition emission observation hEvidence state *
        forwardEvidence prior transition emission observation =
      forwardPrediction prior transition state * emission state observation := by
  exact FiniteKernel.posterior_mul_predictive
    (forwardPrediction prior transition) emission observation hEvidence state

/-- Every positive-evidence forward-filtering update is normalized. -/
theorem forwardFilter_sum_one (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (hEvidence : 0 < forwardEvidence prior transition emission observation) :
    ∑ state, forwardFilter prior transition emission observation hEvidence state =
      1 :=
  (forwardFilter prior transition emission observation hEvidence).sum_one

/-- Zero observation evidence is explicitly outside the normalized forward
filter's positive-denominator construction boundary. -/
theorem forwardEvidence_zero_boundary (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (hZero : forwardEvidence prior transition emission observation = 0) :
    ¬0 < forwardEvidence prior transition emission observation := by
  rw [hZero]
  exact lt_irrefl 0

/-- One backward information-message step. -/
noncomputable def backwardMessageStep (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (nextMessage : State → ℝ) (state : State) : ℝ :=
  ∑ nextState,
    transition state nextState * emission nextState observation *
      nextMessage nextState

/-- Backward recursion over a finite list of future observations. -/
noncomputable def backwardMessage (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) :
    List Observation → State → ℝ
  | [], _ => 1
  | observation :: future, state =>
      backwardMessageStep transition emission observation
        (backwardMessage transition emission future) state

/-- Exact successor equation for the backward information recursion. -/
theorem backwardMessage_cons (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (future : List Observation) (state : State) :
    backwardMessage transition emission (observation :: future) state =
      backwardMessageStep transition emission observation
        (backwardMessage transition emission future) state :=
  rfl

/-- Nonnegative next messages produce a nonnegative backward message. -/
theorem backwardMessage_nonneg (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation)
    (nextMessage : State → ℝ) (hMessage : ∀ state, 0 ≤ nextMessage state)
    (state : State) :
    0 ≤ backwardMessageStep transition emission observation nextMessage state := by
  exact Finset.sum_nonneg fun nextState _ =>
    mul_nonneg
      (mul_nonneg (transition.nonneg state nextState)
        (emission.nonneg nextState observation))
      (hMessage nextState)

/-- Evidence evaluated from the initial law and one backward message. -/
noncomputable def backwardEvidence (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation) : ℝ :=
  ∑ state, prior state *
    backwardMessageStep transition emission observation (fun _ => 1) state

/-- Forward marginalization and the one-step backward message compute the same
observation evidence. -/
theorem forward_backward_evidence_agree (prior : FiniteLaw State)
    (transition : FiniteKernel State State)
    (emission : FiniteKernel State Observation) (observation : Observation) :
    forwardEvidence prior transition emission observation =
      backwardEvidence prior transition emission observation := by
  simp only [forwardEvidence, forwardPrediction, backwardEvidence,
    backwardMessageStep, FiniteKernel.predictive_mass, mul_one]
  simp_rw [Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro state _
  apply Finset.sum_congr rfl
  intro nextState _
  ring

/-- Normalizer for a filtered law tilted by a backward information message. -/
noncomputable def smoothingNormalizer (filtered : FiniteLaw State)
    (backward : State → ℝ) : ℝ :=
  ∑ state, filtered state * backward state

/-- Normalized forward--backward smoothing marginal at positive normalizer. -/
noncomputable def forwardBackwardSmoothing (filtered : FiniteLaw State)
    (backward : State → ℝ) (hBackward : ∀ state, 0 ≤ backward state)
    (hNormalizer : 0 < smoothingNormalizer filtered backward) : FiniteLaw State where
  mass state := filtered state * backward state /
    smoothingNormalizer filtered backward
  nonneg state := div_nonneg
    (mul_nonneg (filtered.nonneg state) (hBackward state)) hNormalizer.le
  sum_one := by
    rw [← Finset.sum_div]
    exact div_self (ne_of_gt hNormalizer)

/-- Smoothing mass times its normalizer is the forward--backward product. -/
theorem forwardBackwardSmoothing_factorization (filtered : FiniteLaw State)
    (backward : State → ℝ) (hBackward : ∀ state, 0 ≤ backward state)
    (hNormalizer : 0 < smoothingNormalizer filtered backward) (state : State) :
    forwardBackwardSmoothing filtered backward hBackward hNormalizer state *
        smoothingNormalizer filtered backward =
      filtered state * backward state := by
  exact div_mul_cancel₀ _ (ne_of_gt hNormalizer)

/-- Every positive-normalizer smoothing marginal sums exactly to one. -/
theorem forwardBackwardSmoothing_sum_one (filtered : FiniteLaw State)
    (backward : State → ℝ) (hBackward : ∀ state, 0 ≤ backward state)
    (hNormalizer : 0 < smoothingNormalizer filtered backward) :
    ∑ state, forwardBackwardSmoothing filtered backward hBackward hNormalizer state =
      1 :=
  (forwardBackwardSmoothing filtered backward hBackward hNormalizer).sum_one

/-- A zero smoothing normalizer cannot satisfy the construction's required
positive-evidence boundary. -/
theorem smoothingNormalizer_zero_boundary (filtered : FiniteLaw State)
    (backward : State → ℝ)
    (hZero : smoothingNormalizer filtered backward = 0) :
    ¬0 < smoothingNormalizer filtered backward := by
  rw [hZero]
  exact lt_irrefl 0

/-- One normalized variational state update, expressed as a prior-weighted
Boltzmann tilt on the shared finite-law carrier. -/
noncomputable def variationalStateUpdate (prior : FiniteLaw State)
    (energy : State → ℝ) : FiniteLaw State :=
  boltzmannPosterior prior energy

/-- A one-step finite variational state update is normalized. -/
theorem variationalStateUpdate_sum_one (prior : FiniteLaw State)
    (energy : State → ℝ) :
    ∑ state, variationalStateUpdate prior energy state = 1 :=
  (variationalStateUpdate prior energy).sum_one

/-- A normalized variational state mass reconstructs its unnormalized tilt. -/
theorem variationalStateUpdate_reconstruction (prior : FiniteLaw State)
    (energy : State → ℝ) (state : State) :
    variationalStateUpdate prior energy state * boltzmannPartition prior energy =
      boltzmannWeight prior energy state :=
  boltzmannPosterior_mul_partition prior energy state

/-- Zero variational energy is the identity update on every finite prior. -/
theorem variationalStateUpdate_zero_energy (prior : FiniteLaw State) :
    variationalStateUpdate prior (fun _ => 0) = prior := by
  exact boltzmannPosterior_zero_energy prior

/-- Predict through a two-level finite hierarchy. -/
def hierarchicalPredictive (top : FiniteLaw Upper)
    (upperKernel : FiniteKernel Upper Middle)
    (lowerKernel : FiniteKernel Middle Observation) : FiniteLaw Observation :=
  lowerKernel.predictive (upperKernel.predictive top)

/-- Two-level hierarchical prediction is prediction through the composed
normalized kernel. -/
theorem hierarchicalPredictive_eq (top : FiniteLaw Upper)
    (upperKernel : FiniteKernel Upper Middle)
    (lowerKernel : FiniteKernel Middle Observation) :
    hierarchicalPredictive top upperKernel lowerKernel =
      (FiniteKernel.comp lowerKernel upperKernel).predictive top := by
  exact (FiniteKernel.predictive_comp top lowerKernel upperKernel).symm

/-- Pointwise two-level predictive factorization. -/
theorem hierarchicalPredictive_mass (top : FiniteLaw Upper)
    (upperKernel : FiniteKernel Upper Middle)
    (lowerKernel : FiniteKernel Middle Observation) (observation : Observation) :
    hierarchicalPredictive top upperKernel lowerKernel observation =
      ∑ middle,
        (∑ upper, top upper * upperKernel upper middle) *
          lowerKernel middle observation :=
  rfl

/-- Bayesian model-averaged predictive law. -/
def modelAverage (modelPrior : FiniteLaw Model)
    (modelPredictive : FiniteKernel Model Observation) : FiniteLaw Observation :=
  modelPredictive.predictive modelPrior

/-- Bayesian model averaging expands into its finite predictive mixture. -/
theorem modelAverage_mass (modelPrior : FiniteLaw Model)
    (modelPredictive : FiniteKernel Model Observation)
    (observation : Observation) :
    modelAverage modelPrior modelPredictive observation =
      ∑ model, modelPrior model * modelPredictive model observation :=
  rfl

/-- Every Bayesian model-averaged predictive law is normalized. -/
theorem modelAverage_sum_one (modelPrior : FiniteLaw Model)
    (modelPredictive : FiniteKernel Model Observation) :
    ∑ observation, modelAverage modelPrior modelPredictive observation = 1 :=
  (modelAverage modelPrior modelPredictive).sum_one

/-! ## Exact asymmetric Boolean HMM witness -/

/-- Boolean initial state with mass `3/4` on `true`. -/
noncomputable def boolInitialLaw : FiniteLaw Bool where
  mass state := if state then 3 / 4 else 1 / 4
  nonneg state := by cases state <;> norm_num
  sum_one := by rw [Fintype.sum_bool]; norm_num

/-- Sticky Boolean transition: stay with probability `3/4`. -/
noncomputable def boolStickyTransition : FiniteKernel Bool Bool where
  mass state nextState := if nextState = state then 3 / 4 else 1 / 4
  nonneg state nextState := by split <;> norm_num
  sum_one state := by cases state <;> rw [Fintype.sum_bool] <;> norm_num

/-- Accurate Boolean emission: report the state with probability `4/5`. -/
noncomputable def boolAccurateEmission : FiniteKernel Bool Bool where
  mass state observation := if observation = state then 4 / 5 else 1 / 5
  nonneg state observation := by split <;> norm_num
  sum_one state := by cases state <;> rw [Fintype.sum_bool] <;> norm_num

/-- Nontrivial asymmetric Boolean hidden Markov model. -/
noncomputable def boolHMM : FiniteHMM Bool Bool where
  initial := boolInitialLaw
  transition := boolStickyTransition
  emission := boolAccurateEmission

/-- The asymmetric Boolean model mixture predicts `true` with mass `13/20`. -/
theorem boolModelAverage_true_mass :
    modelAverage boolInitialLaw boolAccurateEmission true = 13 / 20 := by
  norm_num [modelAverage, FiniteKernel.predictive_mass, boolInitialLaw,
    boolAccurateEmission, Fintype.sum_bool]

/-- The asymmetric Boolean model mixture predicts `false` with mass `7/20`. -/
theorem boolModelAverage_false_mass :
    modelAverage boolInitialLaw boolAccurateEmission false = 7 / 20 := by
  norm_num [modelAverage, FiniteKernel.predictive_mass, boolInitialLaw,
    boolAccurateEmission, Fintype.sum_bool]

/-- After one sticky transition, predicted mass of `true` is `5/8`. -/
theorem boolPrediction_true_mass :
    forwardPrediction boolInitialLaw boolStickyTransition true = 5 / 8 := by
  norm_num [forwardPrediction, FiniteKernel.predictive_mass, boolInitialLaw,
    boolStickyTransition, Fintype.sum_bool]

/-- After one sticky transition, predicted mass of `false` is `3/8`. -/
theorem boolPrediction_false_mass :
    forwardPrediction boolInitialLaw boolStickyTransition false = 3 / 8 := by
  norm_num [forwardPrediction, FiniteKernel.predictive_mass, boolInitialLaw,
    boolStickyTransition, Fintype.sum_bool]

/-- Evidence of a `true` report is exactly `23/40`. -/
theorem boolForwardEvidence_true :
    forwardEvidence boolInitialLaw boolStickyTransition boolAccurateEmission true =
      23 / 40 := by
  norm_num [forwardEvidence, forwardPrediction, FiniteKernel.predictive_mass,
    boolInitialLaw, boolStickyTransition, boolAccurateEmission,
    Fintype.sum_bool]

/-- The Boolean witness's selected observation has positive evidence. -/
theorem boolForwardEvidence_true_pos :
    0 < forwardEvidence boolInitialLaw boolStickyTransition
      boolAccurateEmission true := by
  rw [boolForwardEvidence_true]
  norm_num

/-- Normalized forward filter after observing `true`. -/
noncomputable def boolForwardFilter : FiniteLaw Bool :=
  forwardFilter boolInitialLaw boolStickyTransition boolAccurateEmission true
    boolForwardEvidence_true_pos

/-- The filtered mass of `true` is exactly `20/23`. -/
theorem boolForwardFilter_true_mass :
    boolForwardFilter true = 20 / 23 := by
  have hReconstruction := forwardFilter_reconstruction boolInitialLaw
    boolStickyTransition boolAccurateEmission true
    boolForwardEvidence_true_pos true
  rw [boolForwardEvidence_true, boolPrediction_true_mass] at hReconstruction
  norm_num [boolForwardFilter, boolAccurateEmission] at hReconstruction ⊢
  linarith

/-- The filtered mass of `false` is exactly `3/23`. -/
theorem boolForwardFilter_false_mass :
    boolForwardFilter false = 3 / 23 := by
  have hReconstruction := forwardFilter_reconstruction boolInitialLaw
    boolStickyTransition boolAccurateEmission true
    boolForwardEvidence_true_pos false
  rw [boolForwardEvidence_true, boolPrediction_false_mass] at hReconstruction
  norm_num [boolForwardFilter, boolAccurateEmission] at hReconstruction ⊢
  linarith

/-- Exact Boolean forward-filter normalization. -/
theorem boolForwardFilter_sum_one :
    boolForwardFilter false + boolForwardFilter true = 1 := by
  rw [boolForwardFilter_false_mass, boolForwardFilter_true_mass]
  norm_num

/-- One-step Boolean backward information message for a `true` report. -/
noncomputable def boolBackwardMessage (state : Bool) : ℝ :=
  backwardMessageStep boolStickyTransition boolAccurateEmission true
    (fun _ => 1) state

/-- Backward message at `true` is exactly `13/20`. -/
theorem boolBackwardMessage_true_mass :
    boolBackwardMessage true = 13 / 20 := by
  norm_num [boolBackwardMessage, backwardMessageStep, boolStickyTransition,
    boolAccurateEmission, Fintype.sum_bool]

/-- Backward message at `false` is exactly `7/20`. -/
theorem boolBackwardMessage_false_mass :
    boolBackwardMessage false = 7 / 20 := by
  norm_num [boolBackwardMessage, backwardMessageStep, boolStickyTransition,
    boolAccurateEmission, Fintype.sum_bool]

/-- The Boolean backward message is nonnegative at every state. -/
theorem boolBackwardMessage_nonneg (state : Bool) :
    0 ≤ boolBackwardMessage state := by
  cases state <;>
    norm_num [boolBackwardMessage_false_mass, boolBackwardMessage_true_mass]

/-- The backward calculation agrees with forward evidence at `23/40`. -/
theorem boolBackwardEvidence_eq :
    backwardEvidence boolInitialLaw boolStickyTransition
        boolAccurateEmission true = 23 / 40 := by
  rw [← forward_backward_evidence_agree, boolForwardEvidence_true]

/-- The Boolean smoothing normalizer is the same `23/40` evidence. -/
theorem boolSmoothingNormalizer_eq :
    smoothingNormalizer boolInitialLaw boolBackwardMessage = 23 / 40 := by
  rw [smoothingNormalizer, Fintype.sum_bool,
    boolBackwardMessage_false_mass, boolBackwardMessage_true_mass]
  norm_num [boolInitialLaw]

/-- The Boolean smoothing normalizer is strictly positive. -/
theorem boolSmoothingNormalizer_pos :
    0 < smoothingNormalizer boolInitialLaw boolBackwardMessage := by
  rw [boolSmoothingNormalizer_eq]
  norm_num

/-- Smoothed initial-state law given the next `true` observation. -/
noncomputable def boolSmoothing : FiniteLaw Bool :=
  forwardBackwardSmoothing boolInitialLaw boolBackwardMessage
    boolBackwardMessage_nonneg boolSmoothingNormalizer_pos

/-- Smoothed mass of the initial `true` state is exactly `39/46`. -/
theorem boolSmoothing_true_mass :
    boolSmoothing true = 39 / 46 := by
  have hFactorization := forwardBackwardSmoothing_factorization
    boolInitialLaw boolBackwardMessage boolBackwardMessage_nonneg
    boolSmoothingNormalizer_pos true
  rw [boolSmoothingNormalizer_eq, boolBackwardMessage_true_mass]
    at hFactorization
  norm_num [boolSmoothing, boolInitialLaw] at hFactorization ⊢
  linarith

/-- Smoothed mass of the initial `false` state is exactly `7/46`. -/
theorem boolSmoothing_false_mass :
    boolSmoothing false = 7 / 46 := by
  have hFactorization := forwardBackwardSmoothing_factorization
    boolInitialLaw boolBackwardMessage boolBackwardMessage_nonneg
    boolSmoothingNormalizer_pos false
  rw [boolSmoothingNormalizer_eq, boolBackwardMessage_false_mass]
    at hFactorization
  norm_num [boolSmoothing, boolInitialLaw] at hFactorization ⊢
  linarith

/-- Exact Boolean forward--backward smoothing normalization. -/
theorem boolSmoothing_sum_one :
    boolSmoothing false + boolSmoothing true = 1 := by
  rw [boolSmoothing_false_mass, boolSmoothing_true_mass]
  norm_num

end FEP.TemporalInference
