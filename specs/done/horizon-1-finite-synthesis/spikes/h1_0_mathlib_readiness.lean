import Mathlib.InformationTheory.KullbackLeibler.DataProcessing
import Mathlib.Probability.Decision.BayesEstimator
import Mathlib.Probability.Decision.Risk.Basic
import Mathlib.Probability.Distributions.Beta
import Mathlib.Probability.Distributions.Bernoulli
import Mathlib.Probability.Distributions.Binomial
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Probability.Kernel.Posterior
import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Independence.Conditional
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Metric
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion
import Mathlib.Probability.BrownianMotion.Basic
import Mathlib.Probability.Kernel.IonescuTulcea.Traj

/-!
H1.0 compile-only probe for the exact Lean 4.33.1 / Mathlib v4.33.1 pin.

This file proves availability and type compatibility only. It is not a project
theorem, a scientific claim, or evidence that any later H1/H2 construction is
complete.
-/

#check InformationTheory.klDiv_comp_right_le

#check ProbabilityTheory.bayesRisk_le_bayesRisk_comp
#check ProbabilityTheory.IsArgminEstimator
#check ProbabilityTheory.IsArgminEstimator.isBayesEstimator
#check ProbabilityTheory.IsBayesEstimator

#check ProbabilityTheory.betaMeasure
#check ProbabilityTheory.isProbabilityMeasureBeta
#check ProbabilityTheory.bernoulliMeasure
#check ProbabilityTheory.binomial
#check ProbabilityTheory.isProbabilityMeasure_binomial
#check ProbabilityTheory.binomial_one_eq_bernoulliMeasure

example (p : ↥unitInterval) :
    MeasureTheory.IsProbabilityMeasure
      (ProbabilityTheory.bernoulliMeasure true false p) :=
  inferInstance

#check NormedSpace.exp_zero
#check Matrix.exp_add_of_commute
#check hasDerivAt_exp_smul_const

open NormedSpace in
example : exp (0 : Matrix (Fin 2) (Fin 2) ℝ) = 1 := exp_zero

open NormedSpace in
example (A B : Matrix (Fin 2) (Fin 2) ℝ) (h : Commute A B) :
    exp (A + B) = exp A * exp B :=
  Matrix.exp_add_of_commute A B h

open scoped Matrix.Norms.Operator in
open NormedSpace in
example (A : Matrix (Fin 2) (Fin 2) ℝ) (t : ℝ) :
    HasDerivAt (fun u : ℝ => exp (u • A)) (exp (t • A) * A) t :=
  hasDerivAt_exp_smul_const A t

#check ProbabilityTheory.posterior
#check ProbabilityTheory.compProd_posterior_eq_map_swap
#check ProbabilityTheory.condDistrib
#check ProbabilityTheory.compProd_map_condDistrib
#check ProbabilityTheory.CondIndepFun

#check IsRiemannianManifold
#check IsContMDiffRiemannianBundle
#check Bundle.ContMDiffRiemannianMetric
#check IsCovariantDerivativeOn
#check CovariantDerivative
#check CovariantDerivative.ContMDiffCovariantDerivative
#check CovariantDerivative.IsMetricCompatible
#check CovariantDerivative.torsion

#check ProbabilityTheory.IsPreBrownianReal
#check ProbabilityTheory.IsPreBrownianReal.hasLaw
#check ProbabilityTheory.IsPreBrownianReal.hasLaw_eval
#check ProbabilityTheory.IsPreBrownianReal.hasLaw_sub

#check ProbabilityTheory.Kernel.traj
#check ProbabilityTheory.Kernel.trajMeasure
#check ProbabilityTheory.Kernel.map_traj_succ_self
#check ProbabilityTheory.Kernel.condDistrib_trajMeasure
