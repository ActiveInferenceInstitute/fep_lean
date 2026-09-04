## GNNVersionAndFlags
Version: 1.0

## ModelName
FepLean Continuous OU Linear-Gaussian Model

## ModelAnnotation
Bridge P4b slice: the fep_lean scalar OU filter instance
(rate=1, center=0, diffusionVarianceRate=2, stepDuration=1,
observation noise variance=1) projected deterministically to
GNN v1 continuous linear-Gaussian syntax under contract v0.2
rounding. Extraction record (file:line in the fep_lean
checkout at the commit recorded under Signature):
- F one-step decay = exp(-rate*t) = exp(-1)
  [scalar_gaussian_semigroup.lean:42-43]
- Q one-step transition covariance = rate^-1*(1 - exp(-2*rate*t))
  = 1 - exp(-2) [linear_gaussian_semigroup.lean:1217-1233]
- H identity readout [gaussian_filter.lean:46-49]
- R observation noise variance = 1
  [posterior_convergence.lean:38-40]
- prior_mean = 0, prior_cov = stationary variance = 1 (proved)
  [smooth_reference_kernel.lean:66-68, 96-101]

## StateSpaceBlock
x[1,1],float
y[1,1],float
F[1,1],float
Q[1,1],float
H[1,1],float
R[1,1],float
prior_mean[1,1],float
prior_cov[1,1],float
u[1,1],float
t[1],integer

## Connections
F>x
Q>x
x-H
H>y
R>y
prior_mean>x
prior_cov>x

## InitialParameterization
F = [[[0.36787944117144233]]]
Q = [[[0.8646647167633873]]]
H = [[[1.0]]]
R = [[[1.0]]]
prior_mean = [[0.0]]
prior_cov = [[[1.0]]]
ou_rate = 1
ou_center = 0
diffusion_variance_rate = 2
step_duration = 1
observation_noise_variance = 1
num_timesteps = 1

## Time
Dynamic
ModelTimeHorizon = 1

## ActInfOntologyAnnotation
F = StateTransitionMatrix
H = ObservationMatrix
Q = ProcessNoiseCovariance
R = ObservationNoiseCovariance
prior_mean = PriorMean
prior_cov = PriorCovariance
x = ContinuousHiddenState
y = ContinuousObservation
t = Time

## Footer
Generated: 2026-09-04T12:18:41.315609

## Signature
