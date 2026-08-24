import FepSketches.finite_information
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

/-!
# Finite variational duality and information bounds

The results here use the normalized `FiniteLaw`/`FiniteKernel` substrate.  All
logarithmic identities expose full-support premises.  In particular, no result
identifies the existing totalized real-valued KL with an extended divergence at
zero reference mass.
-/

namespace FEP.VariationalDuality

open FEP FEP.FiniteInformation Finset InformationTheory
open scoped BigOperators

variable {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]

/-- Expectation of a real potential under a finite law. -/
def expectation (law : FiniteLaw α) (potential : α → ℝ) : ℝ :=
  ∑ x, law x * potential x

/-- Data sufficient to certify a normalized finite Gibbs optimizer.  The
pointwise log-density identity is explicit, as are both support assumptions. -/
structure GibbsCertificate (α : Type*) [Fintype α] where
  reference : FiniteLaw α
  optimizer : FiniteLaw α
  potential : α → ℝ
  logPartition : ℝ
  reference_pos : ∀ x, 0 < reference x
  optimizer_pos : ∀ x, 0 < optimizer x
  log_optimizer : ∀ x,
    Real.log (optimizer x) =
      Real.log (reference x) + potential x - logPartition

/-- A closed non-vacuity witness: the uniform law is the Gibbs optimizer for a
zero potential, with log partition zero. -/
noncomputable def uniformZeroPotentialGibbs [Nonempty α] :
    GibbsCertificate α where
  reference := FiniteLaw.uniform
  optimizer := FiniteLaw.uniform
  potential _ := 0
  logPartition := 0
  reference_pos _ := by
    change 0 < ((Fintype.card α : ℝ)⁻¹)
    exact inv_pos.mpr (Nat.cast_pos.mpr Fintype.card_pos)
  optimizer_pos _ := by
    change 0 < ((Fintype.card α : ℝ)⁻¹)
    exact inv_pos.mpr (Nat.cast_pos.mpr Fintype.card_pos)
  log_optimizer _ := by simp

/-- Donsker--Varadhan objective for a finite potential and reference law. -/
noncomputable def dvObjective
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) : ℝ :=
  expectation candidate certificate.potential -
    finiteKL candidate certificate.reference

/-- Free-energy form of the same finite variational objective. -/
noncomputable def gibbsFreeEnergy
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) : ℝ :=
  finiteKL candidate certificate.reference -
    expectation candidate certificate.potential

/-- Exact finite Gibbs identity: the duality gap is KL to the certified Gibbs
optimizer. -/
theorem dvObjective_eq_logPartition_sub_kl
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) :
    dvObjective certificate candidate =
      certificate.logPartition -
        finiteKL candidate certificate.optimizer := by
  unfold dvObjective
  rw [finiteKL_eq_crossEntropy_sub_entropy candidate certificate.reference
      certificate.reference_pos,
    finiteKL_eq_crossEntropy_sub_entropy candidate certificate.optimizer
      certificate.optimizer_pos]
  simp only [expectation, crossEntropy, entropy]
  have hlog := certificate.log_optimizer
  simp_rw [hlog]
  simp_rw [mul_sub, mul_add]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]
  have hpartition :
      (∑ x, candidate x * certificate.logPartition) =
        certificate.logPartition := by
    rw [← Finset.sum_mul, candidate.sum_one, one_mul]
  have hneg (f : α → ℝ) :
      (∑ x, -candidate x * f x) = -(∑ x, candidate x * f x) := by
    simp_rw [neg_mul]
    rw [Finset.sum_neg_distrib]
  rw [hneg (fun x => Real.log (certificate.reference x)),
    hneg certificate.potential,
    hneg (fun _ => certificate.logPartition), hpartition]
  ring

/-- Finite Donsker--Varadhan upper bound. -/
theorem dvObjective_le_logPartition
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) :
    dvObjective certificate candidate ≤ certificate.logPartition := by
  rw [dvObjective_eq_logPartition_sub_kl]
  linarith [finiteKL_nonneg candidate certificate.optimizer]

/-- The explicit Gibbs optimizer attains the Donsker--Varadhan bound. -/
theorem dvObjective_optimizer (certificate : GibbsCertificate α) :
    dvObjective certificate certificate.optimizer =
      certificate.logPartition := by
  rw [dvObjective_eq_logPartition_sub_kl, finiteKL_self, sub_zero]

/-- The uniform zero-potential certificate attains objective value zero. -/
theorem uniformZeroPotentialGibbs_objective [Nonempty α] :
    dvObjective (uniformZeroPotentialGibbs (α := α))
        (uniformZeroPotentialGibbs (α := α)).optimizer = 0 := by
  exact dvObjective_optimizer (uniformZeroPotentialGibbs (α := α))

/-- Attainment uniquely identifies the normalized Gibbs optimizer. -/
theorem dvObjective_eq_logPartition_iff
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) :
    dvObjective certificate candidate = certificate.logPartition ↔
      candidate = certificate.optimizer := by
  rw [dvObjective_eq_logPartition_sub_kl]
  constructor
  · intro h
    have hzero : finiteKL candidate certificate.optimizer = 0 := by
      linarith
    exact (finiteKL_eq_zero_iff candidate certificate.optimizer).mp hzero
  · rintro rfl
    rw [finiteKL_self, sub_zero]

/-- Gibbs' variational principle in free-energy form. -/
theorem neg_logPartition_le_gibbsFreeEnergy
    (certificate : GibbsCertificate α) (candidate : FiniteLaw α) :
    -certificate.logPartition ≤ gibbsFreeEnergy certificate candidate := by
  have h := dvObjective_le_logPartition certificate candidate
  simpa [dvObjective, gibbsFreeEnergy] using neg_le_neg h

/-- The Gibbs optimizer exactly minimizes finite free energy. -/
theorem gibbsFreeEnergy_optimizer (certificate : GibbsCertificate α) :
    gibbsFreeEnergy certificate certificate.optimizer =
      -certificate.logPartition := by
  have h := dvObjective_optimizer certificate
  simpa [dvObjective, gibbsFreeEnergy] using congrArg Neg.neg h

/-! ## Coordinate and mean-field decompositions -/

/-- An ELBO-like score defined as negative divergence from a reference joint. -/
noncomputable def jointELBO
    (actualPrior referencePrior : FiniteLaw α)
    (actualKernel referenceKernel : FiniteKernel α β) : ℝ :=
  -finiteKL (actualKernel.joint actualPrior)
    (referenceKernel.joint referencePrior)

/-- Coordinate ELBO decomposition into a marginal score and expected
conditional divergence. -/
theorem jointELBO_coordinate_decomposition
    (actualPrior referencePrior : FiniteLaw α)
    (actualKernel referenceKernel : FiniteKernel α β)
    (hprior : ∀ x, 0 < referencePrior x)
    (hkernel : ∀ x y, 0 < referenceKernel x y) :
    jointELBO actualPrior referencePrior actualKernel referenceKernel =
      -finiteKL actualPrior referencePrior -
        conditionalKL actualPrior actualKernel referenceKernel := by
  rw [jointELBO,
    finiteKL_joint_chain_rule actualPrior referencePrior actualKernel
      referenceKernel hprior hkernel]
  ring

/-- Mean-field coordinate free energy with one factor held fixed. -/
noncomputable def meanFieldCoordinateFreeEnergy
    (fixed : FiniteLaw α) (candidate target : FiniteLaw β) : ℝ :=
  finiteKL (fixed.product candidate) (fixed.product target)

/-- With full support, the mean-field coordinate objective reduces exactly to
KL of the varying factor. -/
theorem meanFieldCoordinateFreeEnergy_eq
    (fixed : FiniteLaw α) (candidate target : FiniteLaw β)
    (hfixed : ∀ x, 0 < fixed x) (htarget : ∀ y, 0 < target y) :
    meanFieldCoordinateFreeEnergy fixed candidate target =
      finiteKL candidate target := by
  rw [meanFieldCoordinateFreeEnergy,
    finiteKL_product fixed fixed candidate target hfixed htarget,
    finiteKL_self, zero_add]

/-- The target factor is the unique optimum of the supported mean-field
coordinate objective. -/
theorem meanFieldCoordinate_optimum_iff
    (fixed : FiniteLaw α) (candidate target : FiniteLaw β)
    (hfixed : ∀ x, 0 < fixed x) (htarget : ∀ y, 0 < target y) :
    meanFieldCoordinateFreeEnergy fixed candidate target = 0 ↔
      candidate = target := by
  rw [meanFieldCoordinateFreeEnergy_eq fixed candidate target hfixed htarget,
    finiteKL_eq_zero_iff]

/-! ## Fixed-sample Jensen bound -/

/-- Finite weighted Jensen inequality for positive importance weights.  A
product-law IWAE construction can instantiate `sampling` with its fixed-size
sample law; positivity prevents use of `Real.log 0 = 0`. -/
theorem expected_log_weight_le_log_expected_weight
    (sampling : FiniteLaw α) (weight : α → ℝ)
    (hweight : ∀ x, 0 < weight x) :
    ∑ x, sampling x * Real.log (weight x) ≤
      Real.log (∑ x, sampling x * weight x) := by
  have h := strictConcaveOn_log_Ioi.concaveOn.le_map_sum
    (t := Finset.univ) (w := fun x => sampling x) (p := weight)
    (fun x _ => sampling.nonneg x) sampling.sum_one
    (fun x _ => hweight x)
  simpa [smul_eq_mul, Function.comp_def] using h

/-- Independent product law for a fixed number of finite samples. -/
def iidProductLaw (base : FiniteLaw α) (sampleCount : ℕ) :
    FiniteLaw (Fin sampleCount → α) where
  mass sample := ∏ index, base (sample index)
  nonneg sample := Finset.prod_nonneg fun index _ =>
    base.nonneg (sample index)
  sum_one := by
    rw [← Fintype.prod_sum]
    simp [base.sum_one]

@[simp]
theorem iidProductLaw_mass
    (base : FiniteLaw α) (sampleCount : ℕ)
    (sample : Fin sampleCount → α) :
    iidProductLaw base sampleCount sample =
      ∏ index, base (sample index) :=
  rfl

/-- Arithmetic mean of importance weights in one fixed-size sample tuple. -/
noncomputable def sampleMeanWeight (sampleCount : ℕ) (weight : α → ℝ)
    (sample : Fin sampleCount → α) : ℝ :=
  (∑ index, weight (sample index)) / sampleCount

omit [Fintype α] in
/-- A positive sample count and pointwise positive weights make every sample
mean positive. -/
theorem sampleMeanWeight_pos
    (sampleCount : ℕ) [NeZero sampleCount]
    (weight : α → ℝ) (hweight : ∀ x, 0 < weight x)
    (sample : Fin sampleCount → α) :
    0 < sampleMeanWeight sampleCount weight sample := by
  have hcountNat : 0 < sampleCount := Nat.pos_of_ne_zero (NeZero.ne sampleCount)
  have hcountReal : 0 < (sampleCount : ℝ) := by
    exact_mod_cast hcountNat
  exact div_pos
    (Finset.sum_pos (fun index _ => hweight (sample index))
      Finset.univ_nonempty)
    hcountReal

/-- Fixed-sample IWAE Jensen component under the explicit IID product law.
This proves only the finite Jensen bound; identifying the expected sample mean
with model evidence requires a separate importance-ratio theorem. -/
theorem fixedSampleImportanceJensen
    (base : FiniteLaw α) (sampleCount : ℕ) [NeZero sampleCount]
    (weight : α → ℝ) (hweight : ∀ x, 0 < weight x) :
    ∑ sample, iidProductLaw base sampleCount sample *
        Real.log (sampleMeanWeight sampleCount weight sample) ≤
      Real.log (∑ sample, iidProductLaw base sampleCount sample *
        sampleMeanWeight sampleCount weight sample) :=
  expected_log_weight_le_log_expected_weight
    (iidProductLaw base sampleCount)
    (sampleMeanWeight sampleCount weight)
    (sampleMeanWeight_pos sampleCount weight hweight)

/-! ## Finite-channel data processing -/

/-- Swap the coordinates of a finite joint law. -/
def swapLaw (joint : FiniteLaw (α × β)) : FiniteLaw (β × α) where
  mass pair := joint (pair.2, pair.1)
  nonneg pair := joint.nonneg (pair.2, pair.1)
  sum_one := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    simpa [Fintype.sum_prod_type] using joint.sum_one

/-- Totalized finite KL is invariant under coordinate swap. -/
theorem finiteKL_swap (actual reference : FiniteLaw (α × β)) :
    finiteKL (swapLaw actual) (swapLaw reference) =
      finiteKL actual reference := by
  unfold finiteKL
  simp only [swapLaw]
  rw [Fintype.sum_prod_type, Fintype.sum_prod_type]
  rw [Finset.sum_comm]

/-- Reverse finite channel at positive predictive mass. -/
noncomputable def reverseKernel
    (prior : FiniteLaw α) (channel : FiniteKernel α β)
    (hpredictive : ∀ y, 0 < channel.predictive prior y) :
    FiniteKernel β α where
  mass y x := channel.posterior prior y (hpredictive y) x
  nonneg y x := (channel.posterior prior y (hpredictive y)).nonneg x
  sum_one y := (channel.posterior prior y (hpredictive y)).sum_one

/-- Prediction followed by the reverse channel is the swapped original joint. -/
theorem reverseKernel_joint
    (prior : FiniteLaw α) (channel : FiniteKernel α β)
    (hpredictive : ∀ y, 0 < channel.predictive prior y) :
    (reverseKernel prior channel hpredictive).joint
        (channel.predictive prior) = swapLaw (channel.joint prior) := by
  apply FiniteLaw.ext_mass
  funext pair
  change channel.predictive prior pair.1 *
      channel.posterior prior pair.1 (hpredictive pair.1) pair.2 =
    prior pair.2 * channel pair.2 pair.1
  rw [mul_comm]
  exact channel.posterior_mul_predictive prior pair.1
    (hpredictive pair.1) pair.2

/-- The conditional KL of a channel with itself is zero. -/
theorem conditionalKL_self
    (prior : FiniteLaw α) (channel : FiniteKernel α β) :
    conditionalKL prior channel channel = 0 := by
  apply Finset.sum_eq_zero
  intro x _
  rw [finiteKL_self, mul_zero]

/-- A shared full-support channel preserves prior KL in the corresponding
joint laws. -/
theorem finiteKL_joint_sameKernel
    (actual reference : FiniteLaw α) (channel : FiniteKernel α β)
    (hreference : ∀ x, 0 < reference x)
    (hchannel : ∀ x y, 0 < channel x y) :
    finiteKL (channel.joint actual) (channel.joint reference) =
      finiteKL actual reference := by
  rw [finiteKL_joint_chain_rule actual reference channel channel hreference
      hchannel,
    conditionalKL_self, add_zero]

/-- Finite-channel KL data-processing inequality under explicit full support.
The assumptions justify both reverse kernels and every logarithmic chain rule;
no claim is made for extended divergence at a zero reference atom. -/
theorem finiteChannel_dataProcessing
    (actual reference : FiniteLaw α) (channel : FiniteKernel α β)
    [Nonempty α]
    (hactual : ∀ x, 0 < actual x)
    (hreference : ∀ x, 0 < reference x)
    (hchannel : ∀ x y, 0 < channel x y) :
    finiteKL (channel.predictive actual) (channel.predictive reference) ≤
      finiteKL actual reference := by
  have hactualPredictive : ∀ y, 0 < channel.predictive actual y := by
    intro y
    simp only [FiniteKernel.predictive_mass]
    exact Finset.sum_pos (fun x _ =>
      mul_pos (hactual x) (hchannel x y)) Finset.univ_nonempty
  have hreferencePredictive : ∀ y, 0 < channel.predictive reference y := by
    intro y
    simp only [FiniteKernel.predictive_mass]
    exact Finset.sum_pos (fun x _ =>
      mul_pos (hreference x) (hchannel x y)) Finset.univ_nonempty
  have hreverseReference : ∀ y x,
      0 < reverseKernel reference channel hreferencePredictive y x := by
    intro y x
    change 0 < reference x * channel x y /
      channel.predictive reference y
    exact div_pos (mul_pos (hreference x) (hchannel x y))
      (hreferencePredictive y)
  have hle := finiteKL_prior_le_joint
    (channel.predictive actual) (channel.predictive reference)
    (reverseKernel actual channel hactualPredictive)
    (reverseKernel reference channel hreferencePredictive)
    hreferencePredictive hreverseReference
  rw [reverseKernel_joint actual channel hactualPredictive,
    reverseKernel_joint reference channel hreferencePredictive,
    finiteKL_swap,
    finiteKL_joint_sameKernel actual reference channel hreference hchannel] at hle
  exact hle

/-! ## Finite constrained maximum entropy -/

/-- One affine equality constraint on a finite law.  Its statistic has the
prescribed expectation `target`; normalization remains owned by `FiniteLaw`. -/
structure AffineMomentConstraint (α : Type*) where
  statistic : α → ℝ
  target : ℝ

/-- Exact feasibility for a finite list of affine moment constraints. -/
def SatisfiesMomentConstraints
    (law : FiniteLaw α) (constraints : List (AffineMomentConstraint α)) : Prop :=
  ∀ constraint ∈ constraints,
    expectation law constraint.statistic = constraint.target

/-- The signed affine Lagrange potential associated with a finite constraint
list.  Positive temperature scales this potential in the certificate below. -/
noncomputable def constraintPotential
    (constraints : List (AffineMomentConstraint α))
    (multipliers : Fin constraints.length → ℝ) (x : α) : ℝ :=
  ∑ index : Fin constraints.length,
    multipliers index *
      ((constraints.get index).statistic x - (constraints.get index).target)

/-- Independently checkable data for a finite constrained-entropy optimum.
The Gibbs law has full support, the reference is exactly uniform, its signed
potential is a finite affine combination of the listed constraint residuals,
the temperature is strictly positive, and the optimizer is feasible.  This
structure supplies a multiplier; it does not assert automatic dual attainment
from affine feasibility or a Slater condition. -/
structure ConstrainedEntropyCertificate (α : Type*) [Fintype α] [Nonempty α]
    where
  constraints : List (AffineMomentConstraint α)
  multipliers : Fin constraints.length → ℝ
  temperature : ℝ
  temperature_pos : 0 < temperature
  gibbs : GibbsCertificate α
  reference_eq_uniform : gibbs.reference = FiniteLaw.uniform
  potential_eq : ∀ x,
    gibbs.potential x =
      constraintPotential constraints multipliers x / temperature
  optimizer_feasible :
    SatisfiesMomentConstraints gibbs.optimizer constraints

/-- Zero temperature is outside the supplied finite Gibbs-certificate regime.
No division-by-zero convention is used to manufacture a boundary optimizer. -/
theorem zeroTemperature_not_certified [Nonempty α]
    (certificate : ConstrainedEntropyCertificate α) :
    certificate.temperature ≠ 0 :=
  ne_of_gt certificate.temperature_pos

/-- A supplied full-support finite-multiplier certificate exhibits a feasible
entropy maximizer and proves that it is unique.  This is a KKT/certificate
result: neither multiplier existence nor strong duality is inferred from
feasibility. -/
theorem constrainedEntropy_existsUnique_of_certificate [Nonempty α]
    (certificate : ConstrainedEntropyCertificate α) :
    SatisfiesMomentConstraints certificate.gibbs.optimizer
        certificate.constraints ∧
      ∀ candidate : FiniteLaw α,
        SatisfiesMomentConstraints candidate certificate.constraints →
          entropy candidate ≤ entropy certificate.gibbs.optimizer ∧
            (entropy candidate = entropy certificate.gibbs.optimizer ↔
              candidate = certificate.gibbs.optimizer) := by
  have hUniformPos :
      ∀ x, 0 < (FiniteLaw.uniform : FiniteLaw α) x := by
    intro x
    change 0 < ((Fintype.card α : ℝ)⁻¹)
    exact inv_pos.mpr (Nat.cast_pos.mpr Fintype.card_pos)
  have hUniformCrossEntropy :
      ∀ law : FiniteLaw α,
        crossEntropy law (FiniteLaw.uniform : FiniteLaw α) =
          -Real.log ((Fintype.card α : ℝ)⁻¹) := by
    intro law
    unfold crossEntropy FiniteLaw.uniform
    simp_rw [neg_mul]
    rw [Finset.sum_neg_distrib, ← Finset.sum_mul, law.sum_one, one_mul]
  have hFeasiblePotentialZero :
      ∀ law : FiniteLaw α,
        SatisfiesMomentConstraints law certificate.constraints →
          expectation law certificate.gibbs.potential = 0 := by
    intro law hFeasible
    have hConstraintPotential :
        expectation law
            (constraintPotential certificate.constraints
              certificate.multipliers) = 0 := by
      unfold expectation constraintPotential
      simp_rw [Finset.mul_sum]
      rw [Finset.sum_comm]
      apply Finset.sum_eq_zero
      intro index _
      have hMoment := hFeasible
        (certificate.constraints.get index)
        (List.get_mem certificate.constraints index)
      simp only [expectation] at hMoment
      have hCentered :
          (∑ x, law x *
            ((certificate.constraints.get index).statistic x -
              (certificate.constraints.get index).target)) = 0 := by
        simp_rw [mul_sub]
        rw [Finset.sum_sub_distrib, ← Finset.sum_mul, law.sum_one,
          one_mul, hMoment, sub_self]
      calc
        (∑ x, law x *
            (certificate.multipliers index *
              ((certificate.constraints.get index).statistic x -
                (certificate.constraints.get index).target))) =
            certificate.multipliers index *
              ∑ x, law x *
                ((certificate.constraints.get index).statistic x -
                  (certificate.constraints.get index).target) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro x _
              ring
        _ = 0 := by rw [hCentered, mul_zero]
    unfold expectation at hConstraintPotential ⊢
    calc
      (∑ x, law x * certificate.gibbs.potential x) =
          ∑ x, (law x *
            constraintPotential certificate.constraints
              certificate.multipliers x) / certificate.temperature := by
            apply Finset.sum_congr rfl
            intro x _
            rw [certificate.potential_eq x]
            ring
      _ = (∑ x, law x *
          constraintPotential certificate.constraints
            certificate.multipliers x) / certificate.temperature := by
            rw [Finset.sum_div]
      _ = 0 := by rw [hConstraintPotential, zero_div]
  refine ⟨certificate.optimizer_feasible, ?_⟩
  intro candidate hCandidateFeasible
  have hCandidatePotential :=
    hFeasiblePotentialZero candidate hCandidateFeasible
  have hOptimizerPotential :=
    hFeasiblePotentialZero certificate.gibbs.optimizer
      certificate.optimizer_feasible
  have hCandidateBound :=
    dvObjective_le_logPartition certificate.gibbs candidate
  have hOptimizerValue := dvObjective_optimizer certificate.gibbs
  have hKLDominates :
      finiteKL certificate.gibbs.optimizer
          (FiniteLaw.uniform : FiniteLaw α) ≤
        finiteKL candidate (FiniteLaw.uniform : FiniteLaw α) := by
    rw [dvObjective, hCandidatePotential,
      certificate.reference_eq_uniform] at hCandidateBound
    rw [dvObjective, hOptimizerPotential,
      certificate.reference_eq_uniform] at hOptimizerValue
    linarith
  constructor
  · rw [finiteKL_eq_crossEntropy_sub_entropy candidate
        (FiniteLaw.uniform : FiniteLaw α) hUniformPos,
      finiteKL_eq_crossEntropy_sub_entropy certificate.gibbs.optimizer
        (FiniteLaw.uniform : FiniteLaw α) hUniformPos,
      hUniformCrossEntropy candidate,
      hUniformCrossEntropy certificate.gibbs.optimizer] at hKLDominates
    linarith
  · constructor
    · intro hEntropy
      have hKLEq :
          finiteKL candidate (FiniteLaw.uniform : FiniteLaw α) =
            finiteKL certificate.gibbs.optimizer
              (FiniteLaw.uniform : FiniteLaw α) := by
        rw [finiteKL_eq_crossEntropy_sub_entropy candidate
              (FiniteLaw.uniform : FiniteLaw α) hUniformPos,
          finiteKL_eq_crossEntropy_sub_entropy certificate.gibbs.optimizer
            (FiniteLaw.uniform : FiniteLaw α) hUniformPos,
          hUniformCrossEntropy candidate,
          hUniformCrossEntropy certificate.gibbs.optimizer,
          hEntropy]
      have hAttains :
          dvObjective certificate.gibbs candidate =
            certificate.gibbs.logPartition := by
        calc
          dvObjective certificate.gibbs candidate =
              -finiteKL candidate
                (FiniteLaw.uniform : FiniteLaw α) := by
                  simp [dvObjective, hCandidatePotential,
                    certificate.reference_eq_uniform]
          _ = -finiteKL certificate.gibbs.optimizer
                (FiniteLaw.uniform : FiniteLaw α) := by rw [hKLEq]
          _ = dvObjective certificate.gibbs
                certificate.gibbs.optimizer := by
                  simp [dvObjective, hOptimizerPotential,
                    certificate.reference_eq_uniform]
          _ = certificate.gibbs.logPartition :=
            dvObjective_optimizer certificate.gibbs
      exact (dvObjective_eq_logPartition_iff certificate.gibbs candidate).mp
        hAttains
    · rintro rfl
      rfl

/-! ### A checkable relative-interior `Fin 3` certificate -/

/-- First moment on the ordered three-state carrier. -/
def fin3FirstMoment : Fin 3 → ℝ := ![0, 1, 2]

/-- Second moment on the ordered three-state carrier. -/
def fin3SecondMoment : Fin 3 → ℝ := ![0, 1, 4]

/-- The uniform `Fin 3` law has first moment `1` and second moment `5 / 3`.
These two affine constraints give a concrete interior moment problem. -/
noncomputable def fin3InteriorMomentConstraints :
    List (AffineMomentConstraint (Fin 3)) :=
  [ { statistic := fin3FirstMoment, target := 1 },
    { statistic := fin3SecondMoment, target := 5 / 3 } ]

/-- Zero multipliers and unit positive temperature certify the full-support
uniform solution of the concrete two-moment `Fin 3` problem. -/
noncomputable def fin3InteriorMomentCertificate :
    ConstrainedEntropyCertificate (Fin 3) where
  constraints := fin3InteriorMomentConstraints
  multipliers _ := 0
  temperature := 1
  temperature_pos := by norm_num
  gibbs := uniformZeroPotentialGibbs
  reference_eq_uniform := rfl
  potential_eq x := by
    simp [uniformZeroPotentialGibbs, constraintPotential]
  optimizer_feasible := by
    intro constraint hConstraint
    simp only [fin3InteriorMomentConstraints, List.mem_cons,
      List.not_mem_nil, or_false] at hConstraint
    rcases hConstraint with rfl | rfl <;>
      norm_num [expectation, uniformZeroPotentialGibbs, FiniteLaw.uniform,
        fin3FirstMoment, fin3SecondMoment, Fin.sum_univ_succ]

/-- The explicit `Fin 3` optimizer is strictly positive, feasible, and the
unique maximum-entropy law among all laws satisfying both moments. -/
theorem fin3InteriorMoment_uniqueEntropyMaximizer :
    (∀ x, 0 < fin3InteriorMomentCertificate.gibbs.optimizer x) ∧
      SatisfiesMomentConstraints
        fin3InteriorMomentCertificate.gibbs.optimizer
        fin3InteriorMomentConstraints ∧
      ∀ candidate : FiniteLaw (Fin 3),
        SatisfiesMomentConstraints candidate fin3InteriorMomentConstraints →
          entropy candidate ≤
              entropy fin3InteriorMomentCertificate.gibbs.optimizer ∧
            (entropy candidate =
                entropy fin3InteriorMomentCertificate.gibbs.optimizer ↔
              candidate = fin3InteriorMomentCertificate.gibbs.optimizer) := by
  refine ⟨fin3InteriorMomentCertificate.gibbs.optimizer_pos, ?_⟩
  exact constrainedEntropy_existsUnique_of_certificate
    fin3InteriorMomentCertificate

/-! ### Boundary support without a full-support Gibbs form -/

/-- Requiring all mass at state zero is an affine boundary constraint. -/
def fin3BoundaryConstraint : AffineMomentConstraint (Fin 3) where
  statistic := ![1, 0, 0]
  target := 1

def fin3BoundaryConstraints : List (AffineMomentConstraint (Fin 3)) :=
  [fin3BoundaryConstraint]

/-- The boundary constraint forces the point mass at zero.  This theorem uses
the restricted feasible support directly and makes no finite-multiplier or
full-support Gibbs assertion. -/
theorem fin3Boundary_feasible_iff_pointMassZero (law : FiniteLaw (Fin 3)) :
    SatisfiesMomentConstraints law fin3BoundaryConstraints ↔
      law = FiniteLaw.pointMass (0 : Fin 3) := by
  constructor
  · intro hFeasible
    have hMoment := hFeasible fin3BoundaryConstraint (by
      simp [fin3BoundaryConstraints])
    norm_num [expectation, fin3BoundaryConstraint,
      Fin.sum_univ_succ] at hMoment
    have hSum := law.sum_one
    norm_num [Fin.sum_univ_succ] at hSum
    have hOne : law (1 : Fin 3) = 0 := by
      linarith [law.nonneg (1 : Fin 3), law.nonneg (2 : Fin 3)]
    have hTwo : law (2 : Fin 3) = 0 := by
      linarith [law.nonneg (1 : Fin 3), law.nonneg (2 : Fin 3)]
    apply FiniteLaw.ext_mass
    funext x
    fin_cases x
    · simp [FiniteLaw.pointMass, hMoment]
    · simp [FiniteLaw.pointMass, hOne]
    · simp [FiniteLaw.pointMass, hTwo]
  · rintro rfl
    intro constraint hConstraint
    simp only [fin3BoundaryConstraints, List.mem_singleton] at hConstraint
    subst constraint
    norm_num [expectation, fin3BoundaryConstraint, FiniteLaw.pointMass,
      Fin.sum_univ_succ]

/-- The support-forcing point mass is the unique feasible entropy maximizer.
This is the boundary result; it is intentionally separate from the positive-
temperature full-support certificate theorem. -/
theorem fin3Boundary_uniqueEntropyMaximizer :
    SatisfiesMomentConstraints (FiniteLaw.pointMass (0 : Fin 3))
        fin3BoundaryConstraints ∧
      ∀ candidate : FiniteLaw (Fin 3),
        SatisfiesMomentConstraints candidate fin3BoundaryConstraints →
          entropy candidate ≤ entropy (FiniteLaw.pointMass (0 : Fin 3)) ∧
            (entropy candidate = entropy (FiniteLaw.pointMass (0 : Fin 3)) ↔
              candidate = FiniteLaw.pointMass (0 : Fin 3)) := by
  constructor
  · exact (fin3Boundary_feasible_iff_pointMassZero
      (FiniteLaw.pointMass (0 : Fin 3))).2 rfl
  · intro candidate hFeasible
    have hCandidate :=
      (fin3Boundary_feasible_iff_pointMassZero candidate).1 hFeasible
    subst candidate
    exact ⟨le_rfl, ⟨fun _ => rfl, fun _ => rfl⟩⟩

/-! ### Infeasible and redundant constraints -/

/-- An impossible affine constraint: a probability law cannot place mass two
on one atom. -/
def fin3InfeasibleConstraint : AffineMomentConstraint (Fin 3) where
  statistic := ![1, 0, 0]
  target := 2

def fin3InfeasibleConstraints : List (AffineMomentConstraint (Fin 3)) :=
  [fin3InfeasibleConstraint]

/-- Infeasibility is discharged before any multiplier, entropy, or duality
claim is considered. -/
theorem fin3Infeasible_no_feasibleLaw :
    ¬ ∃ law : FiniteLaw (Fin 3),
      SatisfiesMomentConstraints law fin3InfeasibleConstraints := by
  rintro ⟨law, hFeasible⟩
  have hMoment := hFeasible fin3InfeasibleConstraint (by
    simp [fin3InfeasibleConstraints])
  norm_num [expectation, fin3InfeasibleConstraint,
    Fin.sum_univ_succ] at hMoment
  linarith [law.mass_le_one (0 : Fin 3)]

/-- The first-moment-equals-one constraint, named so duplication is visible. -/
def fin3MeanOneConstraint : AffineMomentConstraint (Fin 3) where
  statistic := fin3FirstMoment
  target := 1

/-- A finite list containing the same affine equality twice. -/
def fin3RedundantConstraints : List (AffineMomentConstraint (Fin 3)) :=
  [fin3MeanOneConstraint, fin3MeanOneConstraint]

/-- Duplicating an affine moment equality does not change the feasible set. -/
theorem fin3Redundant_feasible_iff (law : FiniteLaw (Fin 3)) :
    SatisfiesMomentConstraints law fin3RedundantConstraints ↔
      expectation law fin3FirstMoment = 1 := by
  simp [SatisfiesMomentConstraints, fin3RedundantConstraints,
    fin3MeanOneConstraint]

/-! ## Rate--distortion weak duality -/

/-- Expected distortion under a finite source--code joint law. -/
def expectedDistortion
    (joint : FiniteLaw (α × β)) (distortion : α → β → ℝ) : ℝ :=
  ∑ pair, joint pair * distortion pair.1 pair.2

/-- Finite rate--distortion Lagrangian. -/
noncomputable def rateDistortionLagrangian
    (joint : FiniteLaw (α × β)) (distortion : α → β → ℝ)
    (multiplier : ℝ) : ℝ :=
  mutualInformation joint + multiplier * expectedDistortion joint distortion

/-- Weak duality for any separately certified rate and distortion lower
bounds.  Optimizer existence is intentionally not asserted. -/
theorem rateDistortion_weak_duality
    (joint : FiniteLaw (α × β)) (distortion : α → β → ℝ)
    (multiplier rateLower distortionLower : ℝ)
    (hmultiplier : 0 ≤ multiplier)
    (hrate : rateLower ≤ mutualInformation joint)
    (hdistortion : distortionLower ≤ expectedDistortion joint distortion) :
    rateLower + multiplier * distortionLower ≤
      rateDistortionLagrangian joint distortion multiplier := by
  unfold rateDistortionLagrangian
  exact add_le_add hrate (mul_le_mul_of_nonneg_left hdistortion hmultiplier)

end FEP.VariationalDuality
