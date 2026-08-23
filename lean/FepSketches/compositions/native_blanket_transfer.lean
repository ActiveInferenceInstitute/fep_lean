import FepSketches.fep_all
import FepSketches.native_blanket

/-!
# Finite-to-native blanket-transfer compositions

These bridges keep the finite and Mathlib-native carriers visible in honest
conjunctions.  In particular, the native conditional-independence rows use
`CondIndepFun` directly; finite conditional mutual information is retained
only as earlier topic evidence and is never substituted for the native
predicate.
-/

namespace FEPComposed

open FEP FEP.CausalDynamics FEP.MarkovBlanket FEP.NativeBlanket
open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal MeasureTheory ProbabilityTheory

/-- The embedded finite-law normalization is paired with fep-017's native
posterior-fibre normalization when the embedded law is used as the prior. -/
theorem fep135_embeddedLaw_extends_fep017
    {State Observation : Type*}
    [Fintype State] [Fintype Observation] [Nonempty State]
    [MeasurableSpace State] [MeasurableSpace Observation]
    [DiscreteMeasurableSpace State] [DiscreteMeasurableSpace Observation]
    (law : FiniteLaw State) (kernel : FiniteKernel State Observation)
    (observation : Observation) :
    embeddedLaw law Set.univ = 1 ∧
      fep_fep017.FEP017.fep017_posterior
          (embeddedKernel kernel) (embeddedLaw law) observation Set.univ = 1 := by
  exact
    ⟨fep_fep135.FEP135.fep135_embeddedLaw_normalized law,
      fep_fep017.FEP017.fep017_posterior_mass_one
        (embeddedKernel kernel) (embeddedLaw law) observation⟩

/-- The finite expectation transfer is instantiated at fep-015's measurable
variational integrand, keeping both integrability and measurability evidence. -/
theorem fep136_embeddedExpectation_extends_fep015
    {State : Type*} [Fintype State]
    [MeasurableSpace State] [DiscreteMeasurableSpace State]
    (law : FiniteLaw State)
    (energy logApproximation logGenerative : State → ℝ)
    (energyMeasurable : Measurable energy)
    (approximationMeasurable : Measurable logApproximation)
    (generativeMeasurable : Measurable logGenerative) :
    (∫ state,
        fep_fep015.FEP015.fep015_variationalIntegrand
          energy logApproximation logGenerative state ∂embeddedLaw law) =
          ∑ state, law state *
            fep_fep015.FEP015.fep015_variationalIntegrand
              energy logApproximation logGenerative state ∧
      Measurable
        (fep_fep015.FEP015.fep015_variationalIntegrand
          energy logApproximation logGenerative) := by
  exact
    ⟨fep_fep136.FEP136.fep136_embeddedLaw_expectation law
        (fep_fep015.FEP015.fep015_variationalIntegrand
          energy logApproximation logGenerative),
      fep_fep015.FEP015.fep015_variationalIntegrand_measurable
        energyMeasurable approximationMeasurable generativeMeasurable⟩

/-- Embedded finite prediction is native kernel composition, and fep-019's
native prior-predictive theorem certifies that this law remains normalized. -/
theorem fep137_embeddedPredictive_extends_fep019
    {Input Output : Type*} [Fintype Input] [Fintype Output]
    [MeasurableSpace Input] [MeasurableSpace Output]
    [DiscreteMeasurableSpace Input] [DiscreteMeasurableSpace Output]
    (prior : FiniteLaw Input) (kernel : FiniteKernel Input Output) :
    embeddedLaw (kernel.predictive prior) =
        embeddedKernel kernel ∘ₘ embeddedLaw prior ∧
      fep_fep019.FEP019.fep019_priorPredictive
          (embeddedKernel kernel) (embeddedLaw prior) Set.univ = 1 := by
  exact
    ⟨fep_fep137.FEP137.fep137_embeddedPredictive_eq_comp prior kernel,
      fep_fep019.FEP019.fep019_priorPredictive_mass_one
        (embeddedKernel kernel) (embeddedLaw prior)⟩

/-- The native singleton-rectangle factorization is paired with fep-079's
finite conditional-mutual-information certificate for the same static model. -/
theorem fep138_rectangleFactorization_extends_fep079
    {Internal Sensory Active External : Type*}
    [Fintype Internal] [Fintype Sensory] [Fintype Active] [Fintype External]
    [MeasurableSpace Internal] [MeasurableSpace Sensory]
    [MeasurableSpace Active] [MeasurableSpace External]
    [DiscreteMeasurableSpace Internal] [DiscreteMeasurableSpace Sensory]
    [DiscreteMeasurableSpace Active] [DiscreteMeasurableSpace External]
    (model : StaticModel Internal Sensory Active External)
    (blanket : Blanket Sensory Active) (internal : Internal)
    (external : External) :
    embeddedLaw (staticJoint model)
        (blanketCoordinate ⁻¹' {blanket} ∩
          internalCoordinate ⁻¹' {internal} ∩
          externalCoordinate ⁻¹' {external}) =
        ENNReal.ofReal (model.blanketLaw blanket) *
          ENNReal.ofReal (model.internalGiven blanket internal) *
            ENNReal.ofReal (model.externalGiven blanket external) ∧
      conditionalMutualInformation (ofStaticModel model) = 0 := by
  exact
    ⟨fep_fep138.FEP138.fep138_staticJoint_rectangle_factorization
        model blanket internal external,
      fep_fep079.FEP079.fep079_staticBlanket_conditionalMutualInformation_zero
        model⟩

/-- The fep-079 finite factorization is transferred by fep-139 to genuine
Mathlib `CondIndepFun`; alongside it, fep-009 supplies the corresponding
symmetry law for conditional independence of the coordinate sigma-algebras.
The conjunction does not identify finite conditional mutual information with
the native predicate. -/
theorem fep139_nativeCondIndep_connects_fep009_fep079
    {Internal Sensory Active External : Type*}
    [Fintype Internal] [Fintype Sensory] [Fintype Active] [Fintype External]
    [Nonempty Internal] [Nonempty External]
    [MeasurableSpace Internal] [MeasurableSpace Sensory]
    [MeasurableSpace Active] [MeasurableSpace External]
    [DiscreteMeasurableSpace Internal] [DiscreteMeasurableSpace Sensory]
    [DiscreteMeasurableSpace Active] [DiscreteMeasurableSpace External]
    (model : StaticModel Internal Sensory Active External) :
    CondIndepFun
        (MeasurableSpace.comap blanketCoordinate inferInstance)
        blanketCoordinate_measurable.comap_le
        internalCoordinate externalCoordinate
        (embeddedLaw (staticJoint model)) ∧
      (CondIndep
          (MeasurableSpace.comap blanketCoordinate inferInstance)
          (MeasurableSpace.comap internalCoordinate inferInstance)
          (MeasurableSpace.comap externalCoordinate inferInstance)
          blanketCoordinate_measurable.comap_le
          (embeddedLaw (staticJoint model)) →
        CondIndep
          (MeasurableSpace.comap blanketCoordinate inferInstance)
          (MeasurableSpace.comap externalCoordinate inferInstance)
          (MeasurableSpace.comap internalCoordinate inferInstance)
          blanketCoordinate_measurable.comap_le
          (embeddedLaw (staticJoint model))) := by
  refine
    ⟨fep_fep139.FEP139.fep139_staticJoint_condIndepFun model, ?_⟩
  intro sigmaIndependence
  exact
    fep_fep009.FEP009.fep009_condIndep_symm
      (Ω := StaticState Internal Sensory Active External)
      (MeasurableSpace.comap blanketCoordinate inferInstance)
      (MeasurableSpace.comap internalCoordinate inferInstance)
      (MeasurableSpace.comap externalCoordinate inferInstance)
      blanketCoordinate_measurable.comap_le
      (embeddedLaw (staticJoint model)) sigmaIndependence

/-- Native measurable coarsening is paired with fep-009's symmetry law at
the sigma-algebras generated by those same coarsened coordinates. -/
theorem fep140_measurableCoarsening_extends_fep009
    {Internal Sensory Active External InternalImage ExternalImage : Type*}
    [Fintype Internal] [Fintype Sensory] [Fintype Active] [Fintype External]
    [Nonempty Internal] [Nonempty External]
    [MeasurableSpace Internal] [MeasurableSpace Sensory]
    [MeasurableSpace Active] [MeasurableSpace External]
    [MeasurableSpace InternalImage] [MeasurableSpace ExternalImage]
    [DiscreteMeasurableSpace Internal] [DiscreteMeasurableSpace Sensory]
    [DiscreteMeasurableSpace Active] [DiscreteMeasurableSpace External]
    (model : StaticModel Internal Sensory Active External)
    (internalImage : Internal → InternalImage)
    (externalImage : External → ExternalImage)
    (internalMeasurable : Measurable internalImage)
    (externalMeasurable : Measurable externalImage) :
    CondIndepFun
        (MeasurableSpace.comap blanketCoordinate inferInstance)
        blanketCoordinate_measurable.comap_le
        (internalImage ∘ internalCoordinate)
        (externalImage ∘ externalCoordinate)
        (embeddedLaw (staticJoint model)) ∧
      (CondIndep
          (MeasurableSpace.comap blanketCoordinate inferInstance)
          (MeasurableSpace.comap (internalImage ∘ internalCoordinate) inferInstance)
          (MeasurableSpace.comap (externalImage ∘ externalCoordinate) inferInstance)
          blanketCoordinate_measurable.comap_le
          (embeddedLaw (staticJoint model)) →
        CondIndep
          (MeasurableSpace.comap blanketCoordinate inferInstance)
          (MeasurableSpace.comap (externalImage ∘ externalCoordinate) inferInstance)
          (MeasurableSpace.comap (internalImage ∘ internalCoordinate) inferInstance)
          blanketCoordinate_measurable.comap_le
          (embeddedLaw (staticJoint model))) := by
  refine
    ⟨fep_fep140.FEP140.fep140_condIndepFun_measurableImages
        model internalImage externalImage internalMeasurable externalMeasurable,
      ?_⟩
  intro sigmaIndependence
  exact
    fep_fep009.FEP009.fep009_condIndep_symm
      (Ω := StaticState Internal Sensory Active External)
      (MeasurableSpace.comap blanketCoordinate inferInstance)
      (MeasurableSpace.comap
        (internalImage ∘ internalCoordinate) inferInstance)
      (MeasurableSpace.comap
        (externalImage ∘ externalCoordinate) inferInstance)
      blanketCoordinate_measurable.comap_le
      (embeddedLaw (staticJoint model)) sigmaIndependence

/-- Rowwise native blanket closure is paired with fep-080's exact finite
mixture law for two blanket priors sharing that row's conditional pair kernel. -/
theorem fep141_blanketTransition_extends_fep080
    {Internal Sensory Active External : Type*}
    [Fintype Internal] [Fintype Sensory] [Fintype Active] [Fintype External]
    [Nonempty Internal] [Nonempty External]
    [MeasurableSpace Internal] [MeasurableSpace Sensory]
    [MeasurableSpace Active] [MeasurableSpace External]
    [DiscreteMeasurableSpace Internal] [DiscreteMeasurableSpace Sensory]
    [DiscreteMeasurableSpace Active] [DiscreteMeasurableSpace External]
    (dynamics : Dynamics Internal Sensory Active External)
    (current : DynamicState Internal Sensory Active External)
    (weight : ℝ) (weightNonnegative : 0 ≤ weight) (weightAtMostOne : weight ≤ 1)
    (left right : FiniteLaw (Blanket Sensory Active)) :
    CondIndepFun
        (MeasurableSpace.comap blanketCoordinate inferInstance)
        blanketCoordinate_measurable.comap_le
        internalCoordinate externalCoordinate
        (embeddedLaw (staticJoint (nextStaticModel dynamics current))) ∧
      (conditionalPairKernel (nextStaticModel dynamics current)).joint
          (mixLaw weight weightNonnegative weightAtMostOne left right) =
        mixLaw weight weightNonnegative weightAtMostOne
          ((conditionalPairKernel (nextStaticModel dynamics current)).joint left)
          ((conditionalPairKernel (nextStaticModel dynamics current)).joint right) := by
  exact
    ⟨fep_fep141.FEP141.fep141_prediction_preserves_nativeBlanket
        dynamics current,
      fep_fep080.FEP080.fep080_sharedConditional_mixture_preservation
        weight weightNonnegative weightAtMostOne left right
        (conditionalPairKernel (nextStaticModel dynamics current))⟩

end FEPComposed
