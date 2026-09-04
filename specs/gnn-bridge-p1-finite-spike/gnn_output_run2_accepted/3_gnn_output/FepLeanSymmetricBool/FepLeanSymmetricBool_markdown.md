## GNNVersionAndFlags
Version: 1.0

## ModelName
FepLean Symmetric Boolean Generative Model

## ModelAnnotation
Bridge P1 spike: the fep_lean active_inference.lean
GenerativeModel instance `symmetricBoolModel trueBiasedPolicyPrior`
(two policies, two hidden states, two observations, one step)
projected deterministically to GNN v1 syntax.
Extraction record (file:line in the fep_lean checkout at the
commit recorded under Signature):
- D initialState = fairBoolLaw (1/2, 1/2)
  [def active_inference.lean:719-722; use :745]
- B transition = fairBoolKernel, policy-indexed, all entries 1/2
  [def active_inference.lean:725-728; use :746]
- A likelihood = fairBoolKernel, all entries 1/2
  [def active_inference.lean:725-728; use :747]
- C preferences = fairBoolLaw (1/2, 1/2)
  [def active_inference.lean:719-722; use :748]
- E policyPrior = trueBiasedPolicyPrior: E(false)=1/4, E(true)=3/4
  [def active_inference.lean:731-734; parameter :743,:749]
- Timescale: one transition application [active_inference.lean:30-32]
- The Lean GenerativeModel carries no Action type, so no `u`
  variable or action edges are emitted.

## StateSpaceBlock
A[2,2],float
B[2,2,2],float
C[2],float
D[2],float
E[2],float
s[2,1],float
s_prime[2,1],float
o[2,1],float
π[2],float
F[1],float
G[1],float
t[1],integer

## Connections
D>s
s-B
B>s_prime
s_prime-A
A-o
E>π
π-B
C>G
G>π

## InitialParameterization
A = [[0.5, 0.5], [0.5, 0.5]]
B = [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]]]
C = [[0.5, 0.5]]
D = [[0.5, 0.5]]
E = [[0.25, 0.75]]
num_timesteps = 1

## Time
Dynamic
ModelTimeHorizon = 1

## ActInfOntologyAnnotation
A = LikelihoodMatrix
B = TransitionMatrix
C = Preferences
D = PriorOverHiddenStates
E = Habit
F = VariationalFreeEnergy
G = ExpectedFreeEnergy
s = HiddenState
s_prime = NextHiddenState
o = Observation
π = PolicyVector
t = Time

## Footer
Generated: 2026-09-03T16:04:52.305424

## Signature
