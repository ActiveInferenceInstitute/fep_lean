# Horizon 1 choices ledger

This ledger records decisions made where the research program did not already
fix the answer: the completed H1.0 barrier, the warning-free H1.2
decision-risk implementation, and subsequent Horizon integration choices. It
is grouped by verdict. Review the rejected KL orientation, the H1.2 ownership
split, the historical-digest treatment, the family-projection deferral, and the
bounded negative probe first.

## Needs-user

None.

## Unsound

### Identify recognition-to-posterior KL with truth-to-report log-score risk

- **When:** H1.2 decision-risk preflight after H1.0 closed.
- **The choice:** The original target
  `finiteLogLoss_vfeGap_eq_excessPosteriorRisk` joined two quantities with
  opposite argument order. For posterior or truth law `P` and reported or
  recognition law `Q`, proper logarithmic-score excess risk is `finiteKL P Q`,
  while the active-inference VFE gap is `finiteKL Q P`. An asymmetric
  full-support Boolean pair makes the two values unequal. The rejected
  alternative was to keep the joint target and hide the orientation inside a
  newly chosen definition.
- **The gap:** The original target did not state which law supplies the
  expectation, which law is reported, or that KL divergence is asymmetric.
- **The reach:** Keeping it would make the decision-theory bridge scientifically
  false and would let H1.4 inherit a spurious VFE/risk equivalence.
- **Verdict:** Unsound. H1.2 instead owns
  `properLogScore_excessRisk_eq_finiteKL_truth_report` and the Boolean
  `finiteKL_asymmetric_bool` guard; H1.4 separately owns the
  recognition-to-posterior VFE-gap corollary. These names encode argument roles
  rather than choosing a convention-dependent “forward” or “reverse” label.
- **Confidence:** High.

## Sound

### Remove the artificial H1.2 dependency from H1.6

- **When:** First-wave source/import reconciliation before H1.6 opened.
- **The choice:** H1.6 depends on H1.1 only. Its blanket-mixture, invariance,
  and causal-identification targets extend `native_blanket`,
  `causal_dynamics`, and the H1.1 composition leaf; none consumes a
  `decision_risk` declaration. The rejected alternative was to preserve the
  diagram edge and later satisfy it with an unused import or dummy theorem
  reference.
- **The gap:** The prose DAG had acquired an H1.2 edge without a target theorem
  or direct-import consequence.
- **The reach:** H1.6 waited only for the implication vocabulary and
  countermodels it genuinely used, while H1.2 remained independently required
  by H1.3, H1.4, H1.7, and the terminal merge.
- **Verdict:** Sound. The scheduling graph now follows the scientific and
  compilation graph rather than an accidental wave grouping.
- **Confidence:** High.

### Reuse intrinsic H1.1 predicates instead of leaf-local aliases

- **When:** H1.1 single-owner review before native compilation.
- **The choice:** The composition leaf owns only
  `RecognitionMatchesPosterior` and `LocalFreeEnergyDescent`. It states
  invariance, row factorization, absent coupling, conditional independence,
  and intervention equality directly in their foundation vocabulary. The
  rejected alternative was seven convenient generic aliases that would create
  a second semantic owner.
- **The gap:** Alias-like predicates looked readable but could drift from the
  maintained carrier definitions while still letting implication names compile.
- **The reach:** H1.6 and H1.8 consume one auditable vocabulary, and relation or
  coverage evidence can resolve the exact foundation declaration.
- **Verdict:** Sound. Focused mutation tests reject reintroduced intrinsic
  aliases.
- **Confidence:** High.

### Represent the finite stationary blanket with an explicit unit conditioner

- **When:** H1.1 skeptical semantic review of the Boolean countermodels.
- **The choice:** Use `ConditionalBlanketModel Unit Bool Bool`, prove its sole
  blanket mass is one and its conditional row is the named invariant law, and
  state conditional independence through `FEP.CausalDynamics.Factorizes`.
  The rejected alternative called bare unconditional marginal factorization a
  stationary blanket without representing a conditioning variable.
- **The gap:** An unconditional product law is mathematically the unit-blanket
  special case, but that specialization was implicit and therefore easy to
  overread as a general blanket theorem.
- **The reach:** The countermodels remain minimal while the conditioning
  semantics and nondegeneracy evidence are inspectable in every theorem.
- **Verdict:** Sound. The public statements no longer relabel a two-coordinate
  equality as conditional independence.
- **Confidence:** High.

### Import only the five actual H1.1 declaration owners

- **When:** H1.1 source/import closure review.
- **The choice:** Import `finite_probability`, `causal_dynamics`,
  `finite_markov_dynamics`, `active_inference`, and `information_geometry`
  directly. Remove unused `markov_blanket`, `native_blanket`,
  `finite_information`, and `continuous_time_markov` imports. The rejected
  alternative kept broad transitive owners because the original design ledger
  listed seven modules.
- **The gap:** Broad imports hid the real call graph and would couple H1.1 to
  evolving H1.2/H1.7 work without using any of its declarations.
- **The reach:** The H1.1 leaf has a smaller, cycle-resistant closure and H1.6
  remains the owner of later native-blanket transfer claims.
- **Verdict:** Sound. The exact-import test went red before the narrowed roster
  and is now green.
- **Confidence:** High.

### Preserve the exact native-KL support and codomain boundaries

- **When:** H1.2 native-KL and proper-score tracer gates.
- **The choice:** Keep native `klDiv` in `ℝ≥0∞`: prove equality to
  `ENNReal.ofReal (finiteKL p q)` under explicit full reference support and
  prove native infinity when absolute continuity fails. The proper-score
  theorem requires report positivity only on truth support, not unnecessary
  global support. The rejected alternative was an unconditional real/native
  equality or a totalized singular value.
- **The gap:** Project `finiteKL` is real-valued and totalized at zero reference
  mass; Mathlib native KL preserves infinity.
- **The reach:** H1.3/H1.4/H1.6 receive an orientation- and support-correct
  bridge without collapsing `Real` and `ENNReal`.
- **Verdict:** Sound. Supported and singular Boolean cases compile, and the
  proper-score theorem exposes the minimal atomwise premise.
- **Confidence:** High.

### Make the Boolean Bayes-risk witness genuinely decision-theoretic

- **When:** H1.2 two-experiment Bayes-risk tracer gate.
- **The choice:** Use a fair native Boolean prior, the identity experiment, an
  input-independent Boolean garbling, and native zero-one loss. Prove Bayes
  risks exactly zero and one half and derive a Mathlib `IsBayesEstimator` from
  an explicit `IsArgminEstimator`. The rejected alternative was a local risk
  surrogate, an assumed optimum, or two experiments with equal risk.
- **The gap:** Generic Bayes-risk data processing alone does not show that the
  direction is nonvacuous or that an estimator attains the infimum.
- **The reach:** The bridge exercises Mathlib posterior, estimator, `avgRisk`,
  and `bayesRisk` APIs on one inspectable carrier.
- **Verdict:** Sound. The strict zero-versus-one-half witness proves that
  information erasure changes decision quality.
- **Confidence:** High.

### Take the mutual-information product/pushforward gate to GO

- **When:** H1.2 optional gate after the base compiled warning-free.
- **The choice:** Define native channel mutual information as KL from the
  experiment joint to the prior-product predictive law. Prove observation
  garbling monotonicity by pushing both measures through
  `Kernel.id ∥ₖ garbling`, rewriting both joint constructions, and applying
  `InformationTheory.klDiv_comp_right_le`. The rejected alternative was to
  restate finite DPI as a premise or call KL against an unverified reference
  measure mutual information.
- **The gap:** Native DPI was insufficient until both reference measures were
  shown to commute with the same pushforward.
- **The reach:** H1.4 may now prove its separately owned epistemic corollary;
  H1.2 itself introduces no active-inference vocabulary.
- **Verdict:** Sound. The exact pinned product/pushforward seam compiles with
  zero warnings.
- **Confidence:** High.

### Make KL asymmetry executable without convention-dependent names

- **When:** H1.2 proper-score orientation tracer.
- **The choice:** Name truth/report laws by argument role and prove
  `finiteKL truth report ≠ finiteKL report truth` on explicit full-support
  Boolean masses. The rejected alternative was prose-only orientation or
  ambiguous forward/reverse labels.
- **The gap:** KL direction can otherwise be swapped unnoticed across scoring
  and variational-inference conventions.
- **The reach:** Downstream VFE work must state recognition/posterior order and
  cannot reuse the proper-score theorem backwards.
- **Verdict:** Sound. The executable guard closes the identified naming risk.
- **Confidence:** High.

### Import the Mathlib decision-risk owner directly

- **When:** H1.2 pinned-API preflight after the H1.0 probe went green.
- **The choice:** `decision_risk.lean` must directly import
  `Mathlib.Probability.Decision.Risk.Basic` alongside
  `Mathlib.Probability.Decision.BayesEstimator`. The unbuilt alternative was to
  rely on a private or transitive import from another decision module because
  the probe happened to compile in a broader environment.
- **The gap:** The design ledger named the Bayes-estimator surface but omitted
  the exact owner needed by the risk declarations H1.2 uses.
- **The reach:** The H1.2 source exposes its actual dependency and remains
  robust if Mathlib changes a transitive-import implementation detail.
- **Verdict:** Sound. The direct import matches the exact pinned owner verified
  by the completed H1.0 probe.
- **Confidence:** High.

### Remove the unused measure-Bayes dependency from H1.2

- **When:** H1.2 post-compile single-owner review.
- **The choice:** Import only `native_blanket`, `finite_information`, and the
  three exact Mathlib KL/decision owners used by `decision_risk.lean`. Remove
  `FepSketches.measure_bayes` instead of retaining it as an aspirational or
  transitive dependency.
- **The gap:** No H1.2 declaration referenced `FEP.MeasureBayes`; leaving the
  import in place falsely widened the dependency graph and coupled H1.2 to an
  unrelated posterior-measure foundation.
- **The reach:** H1.3, H1.4, and H1.7 consume a smaller, source-true H1.2 API;
  H1.8 must import `measure_bayes` itself only if its own theorem needs it.
- **Verdict:** Sound. The exact-import test went red before the source change,
  and H1.2 plus its H1.7 dependent recompiled warning-free after removal.
- **Confidence:** High.

### Separate generic information results and reject an unsupported epistemic translation

- **When:** H1.2 scientific-ownership preflight.
- **The choice:** H1.2 owns the native-KL transfer, proper log-score excess
  risk, Bayesian garbling result, and the generic native mutual-information
  garbling theorem. H1.4 owns
  `vfeGap_eq_finiteKL_recognition_posterior`. The proposed
  `epistemicValue_mono_under_observationGarbling` does not ship because no
  maintained theorem identifies H1.2's native extended-KL channel information
  with H1.4's real-valued finite `epistemicValue`. The rejected alternatives
  were to rename the native theorem, restate data processing as an assumption,
  or put active-inference vocabulary in `decision_risk.lean`.
- **The gap:** The design assigned the epistemic declaration to H1.2 even though
  the H1.2 import ledger deliberately excludes `active_inference`.
- **The reach:** The dependency graph stays acyclic: H1.4 consumes H1.2, never
  the reverse, and downstream work cannot cite a finite/native information
  bridge that has not been proved.
- **Verdict:** Sound. Generic probability and decision facts remain reusable;
  the VFE statement remains in the composition leaf, while the missing
  epistemic carrier translation is explicit evidence rather than a theorem
  name.
- **Confidence:** High.

### Split the H1.2 stop/go gate at the optional information-pushforward seam

- **When:** H1.2 risk-first scheduling preflight.
- **The choice:** Supported/singular native KL, the two-experiment Bayes-risk
  witness, proper log-score orientation, and the Boolean asymmetry guard form
  the base gate. Failure there blocks H1.2 and its solid dependents. The generic
  mutual-information product/pushforward proof is a later gate: failure blocks
  that theorem and H1.4's epistemic corollary, but not the already proved
  decision-risk core. The unbuilt alternative was one all-or-nothing gate that
  let an optional kernel-construction difficulty erase independent results.
- **The gap:** The dependency graph marked H1.2 as a single solid node while its
  epistemic pushforward was already described as removable.
- **The reach:** H1.3 and the non-epistemic parts of H1.4/H1.6 can consume a
  sound base bridge without pretending the missing information theorem exists.
- **Verdict:** Sound. The split is fail-closed at each actual dependency seam.
- **Confidence:** High.

### Preserve the released digest through one exact, named correction

- **When:** H1.0 KL-DPI correction.
- **The choice:** The released 120-topic baseline remains an immutable record
  of the old release. The live fep-014 row must contain the exact corrected
  sentence; for the historical checksum test only, that one sentence is
  replaced with its released value before recomputing the old digest. In a
  concrete future edit, changing any other character in those 120 rows still
  fails. The unbuilt alternative was to overwrite the old baseline so every
  current row passed, but then it would no longer prove what v1.1.0 contained.
- **The gap:** The program required the stale claim to be corrected but did not
  say how an intentional post-release correction should coexist with the
  immutable released-row checksum.
- **The reach:** Future corrections to released rows must be named and tested
  as explicit exceptions; silently refreshing the historical baseline is not
  acceptable.
- **Verdict:** Sound. It preserves both current factual accuracy and the
  evidentiary meaning of the released digest.
- **Confidence:** Medium.

### Defer family-level Lean projections instead of inventing a second owner

- **When:** H1.0 projection audit.
- **The choice:** The catalogue continues to expose its existing `fep_all`
  whole-catalogue Lean projection. For example, a future family-specific
  consumer still follows the current proof-reference rule instead of receiving
  a newly generated family module. The unbuilt alternative was to add family
  files now, which would also require choosing a generator, output path,
  fallback rules, and byte-stability contract that H1.0 never specified.
- **The gap:** The design asked H1.0 to assess projection debt but did not define
  an owner or contract for family-level generated Lean modules.
- **The reach:** Later work may add family projections only as a separately
  specified architecture change; H1.1/H1.2/H1.7 do not depend on them.
- **Verdict:** Sound. It keeps a noncritical architecture choice off the
  readiness path while recording the debt explicitly.
- **Confidence:** Medium.

### Keep absence evidence bounded and the durable Lean probe warning-free

- **When:** H1.0 Mathlib availability audit.
- **The choice:** The repository keeps one durable positive probe containing
  APIs that compile. Missing integrated stochastic-calculus, Itô/SDE, and
  Fokker--Planck interfaces are supported by source searches and a transient
  `import Mathlib` probe of representative names; the deliberately failing
  file was removed. The unbuilt alternative was to track a file that must fail,
  which would make a normal Lean sweep red or require a special failure
  harness.
- **The gap:** The design required bounded negative evidence but did not choose
  whether intentional compiler failures belonged in the tracked tree.
- **The reach:** Absence claims remain explicitly limited to the searched pin
  and names. Future work must repeat the bounded audit rather than treating it
  as proof that no possible upstream formulation exists.
- **Verdict:** Sound. It gives reproducible boundaries without poisoning the
  warning-free compilation surface.
- **Confidence:** Medium.

### Make declaration ownership a required constructor input

- **When:** H1.0 manifest-schema pass.
- **The choice:** Every foundation or composition constructor must state a
  declaration namespace, while the aggregate must state `None`. For example,
  adding a future composition without its namespace fails at construction
  instead of quietly inheriting a default. The unbuilt alternative was an
  optional default that would preserve old call sites but allow new unowned
  modules to enter the roster.
- **The gap:** The program required a namespace owner but did not specify
  whether omission should be backward-compatible or fail closed.
- **The reach:** Every future `FormalModule` caller must make ownership explicit,
  and aggregate modules cannot accidentally become declaration owners.
- **Verdict:** Sound. Required data is safer than an implicit migration default
  at this small, fully enumerated API boundary.
- **Confidence:** High.

### Treat one outer namespace as the owner and allow namespaces nested inside it

- **When:** H1.0 namespace-drift pass.
- **The choice:** A file may reopen its declared outer namespace and may create
  nested namespaces inside it, but every outer namespace block must name the
  same owner. A comment saying `namespace FEP.X` does not count, and a later
  `namespace Wrong.Owner` makes the file drift. The unbuilt alternative was to
  inspect only the first namespace line, which would let declarations escape
  into an extra owner later in the file.
- **The gap:** The owner field did not itself define how repeated, nested,
  commented, or additional namespace blocks should be interpreted.
- **The reach:** New Lean files can organize declarations below their owner but
  cannot smuggle an unrelated top-level declaration namespace past the
  manifest.
- **Verdict:** Sound. It implements the declared single-owner contract while
  preserving ordinary nested Lean organization.
- **Confidence:** High.

### Centralize comment and namespace scope parsing in `lean_source.py`

- **When:** H1.0 refactor-clean pass.
- **The choice:** Declaration qualification and manifest ownership now consume
  one conservative namespace/section/end iterator. For example, both checks
  interpret a named `section` or `end Nested` the same way. The unbuilt
  alternative was to leave two similar regular-expression parsers in separate
  formal modules, where a later syntax fix could update one and silently drift
  the other.
- **The gap:** The program named the new ownership behavior but not the internal
  owner for shared Lean source parsing.
- **The reach:** Future structural source validators should extend the shared
  parser rather than copy its namespace stack.
- **Verdict:** Sound. The helper owns a coherent parsing responsibility and
  removes a real duplicate rather than adding an adapter.
- **Confidence:** High.

### Seal the legacy shared namespace to the released resource roster

- **When:** H1.0 compatibility-hardening pass.
- **The choice:** Exactly eleven released composition resources may use the
  flat `FEPComposed` namespace. A future resource with that string fails even
  if it is otherwise a valid composition; it must use a unique child such as
  `FEPComposed.FiniteScientificImplications`. The unbuilt alternative was a
  global string exemption that any new file could select, bypassing new-owner
  uniqueness.
- **The gap:** Existing released files share one public namespace, so enforcing
  uniqueness required deciding how compatibility would be represented.
- **The reach:** Released import/declaration compatibility is preserved while
  every new leaf receives a unique, auditable owner.
- **Verdict:** Sound. The exception is explicit, finite, and closed to future
  resources.
- **Confidence:** High.

### Make H1.2 a solid incoming gate for H1.7

- **When:** First-wave dependency reconciliation after H1.0.
- **The choice:** H1.7 may prepare additions to the existing continuous-time
  module while H1.2 is being built, but it cannot close until H1.2 is green.
  Concretely, H1.7's maintained resource must directly import the new
  `decision_risk` foundation to prove its native-KL contract. The rejected
  alternative called H1.7 independent of H1.2 while simultaneously requiring
  that import, leaving an implementer to rely on a file that did not yet exist.
- **The gap:** The import ledger and the dependency diagram contradicted one
  another about whether H1.7 consumed H1.2.
- **The reach:** H1.7 source preparation can remain parallel, but its compile,
  evidence, and downstream H1.8/H2.4 edges now wait for the theorem owner they
  actually use. Future scheduling must derive dependencies from direct imports
  rather than treating the prose wave label as authoritative.
- **Verdict:** Sound. The graph now states the real compile and scientific
  dependency instead of presenting unavailable parallelism.
- **Confidence:** High.

### Keep generator exponentiation algebraic until stochasticity is certified

- **When:** H1.7 matrix-exponential constructor spike.
- **The choice:** Expose the finite rate matrix and its matrix-exponential
  candidate, but require a separate `FiniteMarkovSemigroup` certificate for
  nonnegative normalized slices, semigroup composition, and both master
  equations. Do not coerce the candidate into a `FiniteKernel` without an
  entrywise positivity proof.
- **The gap:** The pinned matrix-exponential API supplies algebra and
  differentiation but no clean project-usable theorem that a general Metzler
  generator has entrywise nonnegative exponential.
- **The reach:** H1.8 and H2.4 may consume certified semigroups now; a later
  upstream positivity theorem can construct the certificate without changing
  downstream carriers.
- **Verdict:** Sound. The explicit uniform-refresh and two-state certificates
  compile, while the unsupported generic implication remains absent.
- **Confidence:** High.

### Contract native KL against the same invariant reference

- **When:** H1.7 information-theoretic closure.
- **The choice:** First prove two-law contraction by pushing both embedded laws
  through one certified kernel and applying Mathlib DPI. Then derive the
  fixed-reference corollary only from an explicit `IsInvariant` equality.
  Keep the result in `ENNReal` and do not substitute the repository's
  totalized real KL.
- **The gap:** Kernel DPI alone compares two evolved laws; it does not justify
  calling the second argument a stationary reference until invariance is
  proved and rewritten.
- **The reach:** Every later dissipation claim must name both the certified
  slice and invariant law, preserving support and codomain boundaries.
- **Verdict:** Sound. Both the generic contraction and invariant-reference
  corollary compile warning-free.
- **Confidence:** High.

### Sample action-indexed semigroups through the existing action interface

- **When:** H1.7 control-carrier integration.
- **The choice:** Give each action one certified semigroup and nonnegative
  sample duration, then construct `ActiveInference.ActionInterface` using the
  sampled kernel and an explicit transition-consistency proof. Do not add a
  parallel action-transition carrier.
- **The gap:** A continuous-time action must determine both dynamics and the
  time slice; leaving either implicit would make H1.8's selected action and
  executed transition unrelated.
- **The reach:** H1.4 and H1.8 can prove that the emitted action executes the
  exact sampled semigroup kernel.
- **Verdict:** Sound. `selectedActionTransition_eq_sampledSemigroup` is a
  definitional equality over the maintained interface.
- **Confidence:** High.

### Separate nonreversible current from strict blanket KL decay

- **When:** H1.7 nonvacuity design.
- **The choice:** Use a directed unit-rate three-cycle only to witness a
  stationary law with nonzero probability current and failed detailed balance.
  Use a different, fully certified unit-rate uniform-refresh semigroup on the
  exact four-factor `DynamicState` carrier for positive transitions,
  stationarity, and strict KL decrease from an explicit Boolean point mass.
- **The gap:** The three-cycle generator has no proved stochastic exponential
  at the pin, and nonzero steady current does not itself imply the terminal
  blanket dissipation theorem.
- **The reach:** Nonequilibrium and blanket-dissipation claims remain separate,
  executable witnesses rather than one overloaded model.
- **Verdict:** Sound. The current is exactly `1/3`; the Boolean refresh proves
  strict real and native KL decrease at time one.
- **Confidence:** Medium-high because the unit rate, origin, alternative, and
  sample time are explicit modeling choices rather than inferred constants.

### Construct the H1.3 IID law instead of assuming independence

- **When:** H1.3 selected-model sampling gate.
- **The choice:** Use `Measure.infinitePi` over the embedded selected truth law,
  then derive coordinate independence and marginals with
  `iIndepFun_infinitePi` and `infinitePi_map_eval`. Reuse H1.2's fair Boolean
  law as the prior and import `native_blanket` directly for the finite-to-native
  measure bridge.
- **The gap:** An abstract IID premise would make the theorem easy to inhabit
  without showing that the same authored truth law drives concentration,
  posterior updating, and the strong law.
- **The reach:** H1.8 receives one concrete trajectory law and posterior
  carrier; H2.3 can reuse the proof boundary without inheriting an empirical-
  risk dependency that H1.3 never uses.
- **Verdict:** Sound. The exact five-owner import roster contains no
  aspirational `empirical_risk` edge, the constructed product law and all
  thirteen public endpoints compile warning-free, and the axiom audit reports
  only the approved foundational dependencies.
- **Confidence:** High.

### Keep finite-sample contraction and almost-sure convergence separate

- **When:** H1.3 likelihood-ratio proof design.
- **The choice:** Derive the bounded centered LLR MGF and one-sided bad-gap tail
  first, transfer its complement to a recursive posterior-odds bound, and prove
  eventual contraction separately through the maintained finite-alphabet
  strong law. Neither endpoint is used as a substitute for the other.
- **The gap:** A strong law gives no advertised finite-sample failure
  probability, while a single concentration bound does not by itself prove an
  almost-sure eventual statement.
- **The reach:** Downstream claims can name exactly which evidence mode they
  consume and cannot conflate rates, consistency, or calibration.
- **Verdict:** Sound at static review; both branches use the same likelihood,
  truth law, and recursive posterior.
- **Confidence:** High.

### Exclude vacuous zero-sample and nondecaying contraction parameters

- **When:** H1.3 refactor-clean semantic audit.
- **The choice:** Require positive sample count, positive deviation, and
  deviation strictly below the identification gap on finite contraction
  endpoints. Return positivity of the decay exponent together with the
  pathwise bound. Retain the zero-sample posterior definition without calling
  it contraction.
- **The gap:** The first statement admitted zero samples and deviations at or
  above the identification gap, where the exponential envelope was constant or
  increasing.
- **The reach:** Every theorem named contraction now certifies genuine decay;
  boundary behavior remains executable rather than hidden by terminology.
- **Verdict:** Sound. Source-contract tests went red on the old domains and
  green after tightening.
- **Confidence:** High.

### Fail closed on optional Beta/Binomial conjugacy

- **When:** H1.3 optional continuous-conjugacy branch.
- **The choice:** Retain the finite Boolean mainline and add no conjugacy
  theorem because the pinned primitives did not expose a clean normalized
  posterior measure equality with every endpoint condition visible. Do not
  introduce an unnormalized posterior expression merely to resemble the
  textbook algebra.
- **The gap:** Normalized Beta/Binomial laws exist, but that alone is not a
  proof that the project's posterior construction closes in the claimed
  family.
- **The reach:** H1.8 is unblocked by the finite result; continuous conjugacy
  remains a separately reviewable capability rather than hidden debt.
- **Verdict:** Sound no-go. No theorem or dependency was fabricated.
- **Confidence:** Medium because a future deeper Mathlib construction may make
  the optional branch feasible without changing this current boundary.

### Tie the concrete policy-tree update to the emitted controlled transition

- **When:** H1.4 transition/value seam review before H1.8.
- **The choice:** Keep `PolicyTreeModel` unchanged, but prove on the exact
  Boolean feedback trace that the belief index consumed by recursive value,
  interpreted through `boolBeliefInterpret`, equals prediction through the
  emitted action's `boolActionTransition`. The rejected alternatives were a
  second transition-bearing policy-tree carrier or declaring the entire H1.8
  transition/value seam impossible merely because the generic structure has
  no transition field.
- **The gap:** Action emission and generative transition consistency did not by
  themselves show that the updated belief used in the continuation represented
  that same executed transition.
- **The reach:** H1.8 may reuse this concrete equality while making no generic
  claim that every `PolicyTreeModel.update` is induced by an action kernel.
- **Verdict:** Sound. The strengthened three-theorem leaf compiles
  warning-free and the focused suite exercises the exact equality.
- **Confidence:** High.

### Keep constrained entropy certificate-based and boundary-aware

- **When:** H1.5 convex-analysis stop/go gate.
- **The choice:** Prove existence and uniqueness from a supplied positive-
  temperature, full-support finite Gibbs certificate with exact affine-moment
  feasibility. Handle the `Fin 3` support-forcing boundary directly, and keep
  zero temperature, infeasibility, and redundant equalities as separate
  theorems. The rejected alternative inferred multiplier existence, dual
  attainment, or a full-support Gibbs form from feasibility alone.
- **The gap:** The pin supplies enough finite entropy/KL algebra to verify a
  certificate but not the general relative-interior and compact-convex
  machinery needed for automatic strong duality in this owner.
- **The reach:** Downstream work may consume the exact optimizer certificate;
  it may not cite H1.5 as a general maximum-entropy duality theorem.
- **Verdict:** Sound. The seven new endpoints compile warning-free, including
  positive interior, infeasible, boundary, and redundant witnesses.
- **Confidence:** High for the theorem boundary; medium-high for choosing the
  zero-multiplier uniform `Fin 3` law as the minimal interior witness.

### Require a shared marginal before claiming mixture factorization

- **When:** H1.6 blanket-mixture stop/go gate.
- **The choice:** State an explicit sufficient condition: both factorized rows
  must share the same named right marginal. Prove the symmetric algebraic
  variant, then exhibit an equal positive mixture of two deterministic product
  rows whose marginal law is the correlated diagonal Boolean blanket. The
  rejected alternative asserted that arbitrary mixtures of independent rows
  remain independent.
- **The gap:** Mixtures introduce dependence through the latent regime unless
  one component marginal is compatible across regimes.
- **The reach:** H1.8 can use the sufficient condition and must retain the
  counterexample in the same aggregate; no necessity claim is inferred.
- **Verdict:** Sound. Both preservation and failure results compile against the
  maintained finite-law factorization carrier.
- **Confidence:** High.

### Identify interventions only from the maintained structural kernel

- **When:** H1.6 causal-identification boundary.
- **The choice:** Prove that a hard root intervention's mediator marginal is
  exactly the named `mediatorGivenRoot` row, and derive equality between models
  only when those structural kernels are equal. Keep the observationally
  equivalent but intervention-distinct Boolean pair as the executable
  countermodel. The rejected alternative inferred causal identification from
  equal observational mediator marginals.
- **The gap:** Observational equality does not determine response under an
  intervention without structural or experimental assumptions.
- **The reach:** Later causal claims must name the structural equality or an
  explicit intervention assumption rather than reuse observational blanket
  compatibility.
- **Verdict:** Sound. The structural identification and negative twin-model
  results compile in the same maintained owner/leaf closure.
- **Confidence:** High within the explicitly ordered finite model; it is not a
  general DAG-identification theorem.

### Fail closed on the first H1.8 carrier merge

- **When:** H1.8 terminal-certificate preflight after H1.3, H1.4, H1.6, and
  H1.7 became native-green.
- **The choice:** Record the current merge as uninhabited before attempting an
  upstream repair. H1.3's selected two-observation posterior has Boolean masses
  `1/10` and `9/10`, whereas H1.4's released feedback value recursion accepts a
  `Bool` belief interpreted only as a point mass. Independently, H1.4's
  controlled transition is a two-state kernel while H1.7's strict blanket
  witness is a kernel on the sixteen-state four-factor dynamic carrier. The
  rejected alternatives were an arbitrary coercion between the beliefs, an
  impossible kernel equality, or a coherence record whose fields merely assume
  the desired identifications.
- **The gap:** Shape-adjacent Boolean components do not make probability laws or
  transition kernels definitionally equal. The terminal theorem requires the
  same intermediate values and types, not a conjunction of predecessor facts.
- **The reach:** The blocked theorem becomes executable design evidence. A
  subsequent repair must put posterior-law policy evaluation and the selected
  semigroup transition on an explicitly shared carrier, or prove a named
  injective/lumping bridge and its commutation laws, before H1.8 can be retried.
- **Verdict:** Sound no-go for the current carrier roster; not a no-go for a
  separately reviewed upstream carrier repair.
- **Confidence:** High. Both obstructions follow from public exact-mass facts
  and incompatible maintained kernel types.

### Remove recognition nonvacuity that normalization already guarantees

- **When:** Independent semantic review of H1.1 after its native-green barrier.
- **The choice:** Delete `HasRecognitionMap` and remove it from the recovery
  theorem and Bernoulli witness. Keep the substantive
  `RecognitionMatchesPosterior`, full posterior support, identifiability,
  nonzero tangent, Fisher-natural alignment, derivative, and derivative-identity
  premises. The rejected alternative retained a named premise that every
  normalized finite law satisfies automatically.
- **The gap:** Existence of one positive atom is a consequence of finite-law
  normalization and says nothing about cross-carrier recognition or posterior
  synchronization.
- **The reach:** H1.1 now exposes only proof-relevant recognition vocabulary;
  H1.8 cannot cite normalization under a stronger-sounding name.
- **Verdict:** Sound. The repaired theorem and its concrete Bernoulli witness
  compile warning-free without the redundant premise.
- **Confidence:** High.

### Separate inequality from uniform from genuine non-invariance

- **When:** Independent semantic review of the H1.7 strict refresh witness.
- **The choice:** Rename the point-mass facts to `_ne_uniform` and add
  `boolBlanketInitial_not_invariant`, which derives failure of invariance from
  the already-proved strict finite-KL decrease. The rejected alternative called
  a law nonstationary merely because it differed from one stationary law.
- **The gap:** A Markov kernel can have more than one invariant law, so
  inequality from the uniform invariant law alone does not prove dynamical
  nonstationarity.
- **The reach:** Downstream terminal work may cite an actual transition-level
  non-invariance theorem while retaining the simpler support witness under its
  exact name.
- **Verdict:** Sound. Both the renamed inequalities and the new negated
  `IsInvariant` endpoint compile warning-free.
- **Confidence:** High.

### Index only the posterior laws reached by the finite policy witness

- **When:** H1.4 carrier repair after the first H1.8 merge failed.
- **The choice:** Replace the point-mass Boolean belief interpretation for the
  terminal path with a three-value `SelectedBeliefIndex`: one index denotes the
  exact H1.3 two-observation posterior and two terminal indices denote its one
  additional Boolean updates. Successors are absorbing because the maintained
  policy theorem owns one observation-contingent step only. The rejected
  alternatives were a fabricated `Fintype (FiniteLaw Bool)`, an unbounded
  posterior-history carrier, or another point-mass interpretation.
- **The gap:** H1.3's learned law has masses `1/10` and `9/10`, so no Boolean
  point mass can initialize the H1.4 value recursion. The full space of real-
  valued finite laws is not finite and cannot be smuggled into `PolicyTreeModel`.
- **The reach:** H1.8 can reuse the exact learned law and its exact next Bayes
  update, but it cannot claim closure under arbitrarily many later updates or
  infinite-horizon control.
- **Verdict:** Sound. The interpretation and reachable update commute exactly
  with H1.3, and both masses and non-Diracness compile as public endpoints.
- **Confidence:** High.

### Use an explicit asymmetric one-step decision problem for feedback

- **When:** H1.4 nonvacuity repair on the posterior-index carrier.
- **The choice:** Use zero cost for a correct report, false-positive cost `4`,
  and false-negative cost `1`. Its Bayes threshold `4/5` lies strictly between
  the two successor truth masses, so the observation-matching continuation is
  uniquely optimal and the feedback tree has value `13/40`, strictly below
  both fixed-report plans. The rejected alternative tuned an EFE or reward
  identity that the maintained carriers do not support.
- **The gap:** Symmetric zero-one loss would choose the same action at both
  highly true posteriors and make the observation-contingent branch vacuous.
- **The reach:** H1.8 obtains a real feedback advantage and an attained finite
  Bellman action without claiming reward--EFE equivalence, epistemic-value
  monotonicity, or infinite-horizon optimality.
- **Verdict:** Sound. Both branch risks, exact values, and the optimizer theorem
  compile on the maintained policy-tree recursion.
- **Confidence:** High for the theorem; medium-high for the minimal `4:1`
  witness chosen to separate these exact posterior masses.

### Lift the learned posterior into the exact blanket carrier

- **When:** H1.7 shared-carrier repair for H1.8.
- **The choice:** Embed the internal Boolean law as the first factor of the
  exact right-associated sixteen-state blanket carrier and keep the other
  three Boolean factors uniform. Lift the likelihood through the first
  projection, then prove preservation of the internal marginal, predictive
  law, and Bayes posterior. The rejected alternatives were `Bool` equivalence
  with the sixteen-state carrier, a second blanket type, or an assumed
  posterior-commutation field.
- **The gap:** An embedding of laws is useful only if prediction and posterior
  updating commute with it; matching cardinality or component names supplies
  neither fact.
- **The reach:** The H1.3 posterior, H1.4 belief update, and H1.7 generative
  posterior now denote the same derived law on one carrier. The uniform
  complement is a finite witness choice, not a general conditional-independence
  principle.
- **Verdict:** Sound. Marginal, predictive, and posterior commutation compile
  warning-free, and the carrier cardinality is proved to be exactly `16`.
- **Confidence:** High.

### Make hold and refresh the sole action-transition owner

- **When:** H1.7 action repair for the shared terminal model.
- **The choice:** Build the generative model directly from
  `ActionIndexedSemigroup`: `false` samples the certified refresh semigroup at
  time zero and is identity, while `true` samples it at the existing positive
  unit time. Derive the `ActionInterface` from that model definitionally. The
  rejected alternatives were a parallel controlled kernel, two unrelated
  models, or action labels with identical transitions.
- **The gap:** The earlier H1.4 and H1.7 witnesses used different state types
  and transitions, so an emitted action did not identify the terminal kernel.
- **The reach:** H1.8 can prove that the optimal continuation emits the exact
  sampled semigroup kernel. The time-zero action is explicitly a hold and does
  not receive a false strict-dissipation claim.
- **Verdict:** Sound. Identity and positive-refresh endpoints, kernel
  inequality, model transition, and action-interface consistency all compile.
- **Confidence:** High; the unit positive time is an explicit witness choice.

### Prove strict refresh contraction for every nonuniform finite law

- **When:** Final H1.8 review rejected substitution of the legacy point-mass
  strictness witness for the learned posterior.
- **The choice:** Prove a generic positive-time theorem: exact refresh is the
  convex mixture of the input and uniform laws; strict concavity of
  `Real.negMulLog` raises entropy at a nonuniform atom, while finite-KL
  separation shows the input entropy is strictly below uniform. Convert the
  resulting real-KL inequality to native `klDiv` through the existing
  full-support weighted-Dirac bridge. The rejected alternative cited strictness
  only for `boolBlanketInitialLaw`.
- **The gap:** Data processing supplies nonincrease but not strictness, and the
  terminal learned posterior is not the point-mass law from the original H1.7
  witness.
- **The reach:** H1.8 may instantiate strict finite and native KL on the same
  lifted learned posterior and true refresh action. The false hold action
  remains equality, as it must.
- **Verdict:** Sound. The generic theorem, its native corollary, and the lift of
  nonuniformity compile warning-free without extra axioms.
- **Confidence:** High.

### Repair H1.8 without erasing the first carrier no-go

- **When:** H1.8 terminal retry after the H1.4 posterior-index and H1.7
  shared-blanket carrier repairs.
- **The choice:** Preserve `FiniteReferenceCoherence` and its three no-go
  theorems as executable evidence about the rejected Boolean point-mass and
  two-state/sixteen-state identifications. Add one positive terminal theorem
  that instead lifts H1.3's exact learned and updated laws into the maintained
  sixteen-state blanket, consumes the repaired H1.4 policy law, and derives its
  model and `ActionInterface` from H1.7's action-indexed semigroup. The rejected
  alternatives were deleting the old no-go, weakening it, or presenting a
  conjunction of unrelated predecessor witnesses as a repaired agent.
- **The gap:** The first no-go was correct for its exact record, but did not
  preclude a separately reviewed carrier repair. A valid retry had to change
  the intermediate types and prove prediction, posterior, action, transition,
  invariance, and KL commutation rather than assert them.
- **The reach:** `finiteReferenceAgent_terminal` now uses one lifted updated
  posterior for exact-posterior VFE and both strict KL conclusions, one emitted
  true action for the selected sampled refresh kernel, and one stationary law
  for its locally constructed finite conditional factorization plus H1.7
  invariance. It does not claim paired
  dynamics, causal identification, physical dissipation, general tree
  learning, or a universal FEP.
- **Verdict:** Sound. The repaired theorem and all retained boundaries compile
  warning-free; the five public theorems use only the approved standard axioms.
- **Confidence:** High for the formal carrier repair; the scientific scope
  remains deliberately finite, synthetic, and model-specific.
