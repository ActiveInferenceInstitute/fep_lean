# Horizon 2 smooth and stochastic lifting

Status: **accepted and closed; every required slice through terminal H2.7 and
every required R0 proof gate have exited under the source-bound
[H2.7 receipt](readiness/exits/07-smooth-reference-kernel.json). H3.G0 is
accepted and closed under the prospective
[H3.G0 receipt](../h3-reference-study/carrier-acceptance.json); H3.0
preregistration is the sole open gate, and H3.1--H3.7 remain closed until it
freezes**. Last updated: 2026-08-24.

This accepted record implements the
[Horizon 2 design](../../docs/design/fep-research-program/horizon-2-smooth-stochastic.md)
under the shared [research contract](../../docs/design/fep-research-program/research-contract.md).
The accepted [Horizon 1 record](../done/horizon-1-finite-synthesis/README.md)
is the immutable predecessor boundary.

## Next Agent Prompt

Perform H3.0 only: freeze the formal/synthetic protocol for the continuous
branch selected by accepted H3.G0 before any outcome inspection. H2 is frozen
at exit receipt
`5bbee4453542c5e59a9fdb1db50d41327b5f2e0ffeede3f87097611ff798190e`.
Optional H2.2b remains unopened outside the accepted H2 exit. H3.1--H3.7 remain
closed until H3.0 freezes; the absent canonical `data-capability.yaml` keeps
H3.6E and causal claims blocked. `tests/test_h3_g0_carrier_acceptance.py` owns
the closed G0 gate, while `tests/test_h3_preregistration.py` belongs exclusively
to H3.0. The finite carrier remains fallback and negative-control evidence and
requires an explicit reviewed H2 terminal no-go plus reviewed H3 DAG revision.

Current checklist:

- [x] [H2.0](slices/00-pinned-readiness.md): exact pin, positive probes,
  bounded negative searches, and row-level decisions.
- [x] [H2.1a](slices/01a-gaussian-measure-kl.md): scalar Gaussian measure,
  density, support, and native KL.
- [x] [H2.1b](slices/01b-gaussian-coordinates.md): natural/mean coordinate
  score, Fisher, covariance, and Bregman identities.
- [x] [H2.2a](slices/02a-coordinate-duality.md): required local coordinate
  duality and rank boundary.
- [ ] [H2.2b](slices/02b-manifold-bundle.md): optional Mathlib manifold
  packaging, deliberately unopened and excluded from the accepted H2 exit.
- [x] [H2.3a](slices/03a-posterior-martingale.md): selected Gaussian posterior
  process and martingale limit.
- [x] [H2.3b](slices/03b-identifiability-risk.md): identification, consistency,
  bounded-continuous risk, and nonidentifiable boundary.
- [x] [H2.4a](slices/04a-embedded-kernel-functoriality.md): identity and
  composition preservation in the existing embedding owner.
- [x] [H2.4b](slices/04b-native-action-semigroup.md): native semigroup and
      exact H1 lift.
- [x] [H2.5a](slices/05a-scalar-ou.md): scalar OU transition law, invariant
  Gaussian, full-time weak limit, and native-KL monotonicity.
- [x] [H2.5b-R0](slices/05b-r0-transition-covariance.md): derive actual
  time-dependent transition-covariance PSD/PD before H2.5b opens.
- [x] [H2.5b](slices/05b-linear-gaussian.md): symmetric-precision linear
  Gaussian semigroup.
- [x] [H2.5c](slices/05c-fin4-carrier.md): exact four-coordinate export.
- [x] [H2.5d-R0](slices/05d-r0-gaussian-conditioning.md): fixed Fin4 native
  stationary-law conditioning repair gate.
- [x] [H2.5d](slices/05d-conditioning-precision.md): Gaussian
  conditioning/precision theorem.
- [x] [H2.6a-R0](slices/06a-r0-native-posterior.md): prove Gaussian density
  factorization and evidence-a.e. equality to Mathlib's native posterior.
- [x] [H2.6a](slices/06a-gaussian-filter.md): exact scalar filter.
- [x] [H2.6b](slices/06b-gaussian-control.md): filter-consuming finite control.
- [x] [H2.6c](slices/06c-finite-grid-path.md): monotone finite-grid path laws,
  coordinate reversal, and support-aware native KL boundaries.
- [x] [H2.7-R0](slices/07-r0-gaussian-vfe-natural-gradient.md): continuous
  density-relative VFE, exact-posterior gap, mean-coordinate natural gradient,
  and strict local descent proof gate.
- [x] [H2.7](slices/07-terminal-certificate.md): accepted terminal scalar
  theorem, separate four-coordinate export, and independent review quorum;
  see the [exit receipt](readiness/exits/07-smooth-reference-kernel.json).

The accepted generated exit snapshot contains 52 maintained modules: 33
foundations, 18 compositions, and one declaration-free aggregate, with 1,477
theorem declarations. The exit receipt, rather than these human-readable
counts, is the source-bound H2 closure authority.

## Outcome

Horizon 2 lifts the reusable H1 interfaces to native measures and kernels on a
single fixed-variance scalar Gaussian location/OU carrier. The distinct exact
four-coordinate symmetric-precision Gaussian export was required and accepted
before the H2 exit so H3 never invents its continuous carrier after
preregistration.

The terminal result is not an SDE solution, Itô theorem, Fokker--Planck
solution, continuous-path thermodynamic law, global statistical-manifold
theory, empirical result, or universal FEP theorem. Those names remain absent
unless a separately accepted upstream or local theorem supplies their actual
mathematics.

## Why the plan is more finely sliced than the design

Three independent Codex drafts optimized respectively for the fewest slices,
fatal-risk ordering, and seam quality. They agreed on the H2.0 kill gates,
H2.4's exact H1 lift, the scalar/four-coordinate distinction, and the need to
split H2.5. The seam review additionally showed that conditioning, filtering,
control, and path laws are independent owners. The canonical plan therefore
uses more modules than the initial design rather than letting one file hide
several unreviewable proof packages.

A required Claude-family draft was attempted read-only, but the local Claude
OAuth session had expired and could not be refreshed. No credential repair was
attempted. The synthesis compensates with three blind high-effort Sol drafts
and explicit source verification of every accepted divergence.

## Dependency graph

Solid edges are merge barriers. The manifold bundle is the only optional H2
implementation lane.

```text
accepted H1
  -> H2.0 readiness
     -> H2.1a -> H2.1b -> H2.2a -.-> H2.2b optional
              -> H2.3a -> H2.3b
     -> H2.4a -> H2.4b
     -> {H2.1a, H2.4b} -> H2.5a -> H2.5b-R0 -> H2.5b -> H2.5c
        -> H2.5d-R0 -> H2.5d
     -> {H2.1a, H2.5a} -> H2.6a-R0 -> H2.6a
     -> {H2.4b, H2.6a} -> H2.6b
     -> {H2.4b, H2.5a} -> H2.6c
     -> {H2.1b, H2.6a} -> H2.7-R0
     -> {H2.1b, H2.2a, H2.3b, H2.4b,
         H2.5a, H2.5c, H2.5d, H2.6a, H2.6b, H2.6c,
         H2.7-R0} -> H2.7
H2.7 -> H3.G0 accepted continuous branch -> H3.0 preregistration open
```

H2.3 parameter learning and H2.6 latent-state filtering remain separate. The
filter does not wait on the parameter-consistency theorem merely because both
use the word posterior; they meet only in H2.7.

## Single-owner end state

| Package | Canonical resource | Role | Declaration namespace |
| --- | --- | --- | --- |
| H2.1a/b | `gaussian_information_geometry.lean` | foundation | `FEP.GaussianInformationGeometry` |
| H2.2a/b | `smooth_information_geometry.lean` | foundation | `FEP.SmoothInformationGeometry` |
| H2.3a/b | `posterior_convergence.lean` | foundation | `FEP.PosteriorConvergence` |
| H2.4b | `markov_semigroup.lean` | foundation | `FEP.MarkovSemigroup` |
| H2.5a | `scalar_gaussian_semigroup.lean` | foundation | `FEP.ScalarGaussianSemigroup` |
| H2.5b | `linear_gaussian_semigroup.lean` | foundation | `FEP.LinearGaussianSemigroup` |
| H2.5c | `fin4_gaussian_semigroup.lean` | foundation | `FEP.Fin4GaussianSemigroup` |
| H2.5d | `gaussian_precision_conditioning.lean` | foundation | `FEP.GaussianPrecisionConditioning` |
| H2.6a | `compositions/gaussian_filter.lean` | composition | `FEPComposed.GaussianFilter` |
| H2.6b | `compositions/gaussian_control.lean` | composition | `FEPComposed.GaussianControl` |
| H2.6c | `compositions/gaussian_grid_path.lean` | composition | `FEPComposed.GaussianGridPath` |
| H2.7 | `compositions/smooth_reference_kernel.lean` | composition | `FEPComposed.SmoothReferenceKernel` |

H2.4a deliberately extends `native_blanket.lean`, the existing owner of
`embeddedKernel`; it does not create a module. H2.0 and H3.G0 likewise own no
formal resource. The H2.5b-R0, H2.5d-R0, and H2.6a-R0 proof gates likewise
create only source-bound spike/decision evidence and no maintained module. At
the accepted H2 exit, the generated manifest contains 52 maintained modules:
33 foundations, 18 compositions, and one declaration-free aggregate, with
1,477 theorem declarations.

H2.0 froze the pinned external API routes. Each maintained slice file and
manifest test freezes its final source-true project direct-import tuple, with no
transitive or aspirational import retained.

## Scientific and architectural invariants

- The scalar Gaussian family uses fixed positive variance. With natural
  coordinate `eta = mu / variance`, its log-partition Hessian,
  natural-coordinate Fisher information, and covariance are the same variance.
  Mean-coordinate Fisher information is the reciprocal variance. No
  unqualified mean-coordinate “Fisher equals covariance” theorem is accepted.
- H2.4 owns native measure-kernel semigroups and reuses the exact H1 action,
  sample time, right-associated blanket carrier, and `embeddedKernel`. It adds
  no parallel action-transition field.
- Algebraic zero/addition laws may be structure fields. Measurability,
  stochasticity, invariance, reversibility, generator existence, covariance
  positivity, conditioning, convergence, and strictness are derived theorems,
  never certificate fields containing the desired conclusion.
- Time zero and positive time are separate theorem-visible branches. A Dirac
  identity kernel is not silently treated as a nondegenerate Gaussian.
- The scalar OU carrier and the exact `Fin 4` export are distinct. A scalar
  specialization must name an exact `Fin 1` equivalence or exact eigenmode;
  shape similarity is insufficient.
- The exact four-coordinate precision matrix owns standardized coordinates in
  the order external, sensory, active, internal. Covariance is defined as the
  inverse of precision, not stored independently.
- Precision-zero algebra is not conditional independence. H2.5d must derive a
  native conditional-law or factorization theorem before H2.7 or continuous H3
  eligibility.
- Parameter-posterior convergence, latent-state filtering, and control are
  distinct carriers connected only by named equalities.
- Weak convergence transfers bounded continuous observables. Entropy, log
  path ratios, and other unbounded quantities require explicit support and
  domination or uniform-integrability hypotheses.
- Finite-grid path results remain finite-grid. No Girsanov or continuous-path
  density language is inferred.
- No local homonym substitutes for a missing upstream interface. Project
  structures use native-specific names where ambiguity would hide provenance.
- H2 resources remain outside the 155-topic roster. Capability/relation owners
  change only after a theorem is accepted, never merely because a spec opened.
- H3.G0 read accepted H1/H2 sources and evidence, selected the continuous
  formal/synthetic branch, and mutated no carrier or proof. H3.0 is the sole
  open gate.

## H2.0 risk barrier

The accepted readiness matrix owns exact pin identity, probe paths, intended
consumers, statuses, and no-go edges. Its
[receipt](readiness/acceptance.json) and
[validator](readiness/validate.py) bind the 34-test warning-free run to all
probe, test, validator, and toolchain bytes. Required groups cover scalar
Gaussian density/KL,
coordinate calculus, native kernel composition and H1 embedding, scalar and
multivariate state-dependent Gaussian kernels, weak convergence, posterior
martingales, local geometry, Gaussian conditioning, and finite-grid trajectory
laws. Bounded negative rows cover integrated stochastic calculus, Itô/SDE,
Fokker--Planck, Girsanov, continuous path-density, and general native
semigroup interfaces.

The pinned source exposes scalar and multivariate Gaussian measures, scalar
Gaussian parameter measurability and convolution, weak convergence, martingale
convergence, kernel composition/invariance, matrix exponential, positive-
definite matrix algebra, and trajectory kernels. Source inspection did not
locate ready-made native Gaussian KL, covariance-parameterized multivariate
measurability, or Gaussian conditioning theorems. H2.0 nevertheless derived a
nonzero-shift scalar native-KL formula and constructed a genuine state-dependent
multivariate Markov kernel. At that frozen H2.0 boundary it did not derive the
`K_star` dynamic transition covariance, Gaussian precision-conditioning
factorization, or selected closed-form filter posterior, so those rows remain
historically recorded as blocking no-go decisions. H2.5b-R0/H2.5b have since
repaired the selected transition-covariance seam and H2.6a-R0/H2.6a have
repaired the selected native-filter seam. H2.5d-R0 and maintained H2.5d now
repair the selected precision-conditioning seam with native joint
reconstruction, blanket-a.e. conditional laws, `CondIndepFun`, and a fixed
non-independence perturbation. The scalar-to-`Fin 4` row remains historically
`upstream_required`, while accepted H2.5c supplies the exact maintained
specialization that the frozen H2.0 probe did not.

## Evidence and review

Every implementation slice begins with a failing public-contract test and ends
with warning-free native compilation, an approved axiom probe, exact
manifest/namespace/import/projection checks, and scientific review. Numerical
diagnostics may consume exact theorem values but never replace proofs.

H2.7-R0 received independent Lean, probability/information-geometry, and
skeptical approvals for the continuous density-relative VFE and actual
natural-gradient seam. H2.7 then received its Lean, domain, and skeptical
approvals. The terminal module exposes one connected scalar theorem and a
separate formal four-coordinate export across a public roster of 10 definitions
and 30 theorems. The
[exit receipt](readiness/exits/07-smooth-reference-kernel.json) binds the
source, toolchain, imports, owner, projection, declaration census, focused
12-test evidence, and review decisions. Its publication scope is H2 formal
terminal acceptance only.

GitNexus cannot currently index this nested checkout. Source/import/consumer
tracing supplies the fallback evidence, so graph-completeness confidence is
reduced. Manifest, projection, compile, and focused-test contracts remain
directly verifiable.

## Compatibility and publication firewalls

H2 is additive. It introduces no compatibility aliases, data migrations,
preallocated topic identifiers, or alternate registries. Public H1 names and
the v1.1.0 release snapshot remain unchanged. The accepted post-v1.1.0 H2
source invalidates the retained publication receipts' current-source binding;
`FEP-EVIDENCE-CURRENT` and `FEP-FULL-155` remain open, and no publication claim
is implied by the H2 exit receipt.
