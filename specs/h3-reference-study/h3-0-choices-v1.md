# Horizon 3.0 choices ledger

This ledger audits implementation choices in the synthetic-only H3.0
preregistration candidate. It does not approve the candidate. Entries are
ordered from least to most confident within each verdict. Exact reviewers bind
this file together with the candidate and its test before any acceptance event.

## Needs exact review

### Define conditional-action p-values before the proof gates can activate

- **When:** Encoding the six tests that exist only after exact H3.2d and H3.4
  proof receipts pass.
- **Choice:** Define response at both action steps as next-observation prediction
  against the exact selected-center kernel, with RMSE over eight axis-step
  components per trajectory and 90% marginal coverage over 1,024 components
  per setting. Propose a maximum of three predeclared response p-values, a
  paired whole-trajectory bootstrap p-value for noninferiority, and an exact
  sign-test p-value for superiority. For example, the omitted-effect control
  keeps the same trajectories but substitutes the base center in prediction;
  a later run may not select whichever component or tail looks best.
- **Gap:** The supplied operating contract fixes action thresholds and the six
  test IDs, but it does not yet derive every action p-value from an accepted
  exact statistical definition.
- **Reach:** Statistical and model/domain/action reviewers must either approve
  the target, normalization, coverage denominator, omitted-effect mutation, and
  p-values or require a preserved v2 before execution. Until then, null action
  remains the only protocol and the action family is structurally absent.
- **Verdict:** Needs exact review. The proposed definitions fail closed and cannot
  authorize action execution.
- **Confidence:** Low.

### Diagnose blanket and stationarity on observed transition destinations

- **When:** Turning the named blanket correlation and first-versus-last
  stationarity checks into executable estimands without assuming H3.3 recovery.
- **Choice:** Use the 256 observed destination vectors `Y[t+1]` from each
  held-out trajectory. For the blanket check, invert their pooled sample
  covariance and cluster-bootstrap whole trajectories. For stationarity,
  calculate per-trajectory first/last mean and unbiased-variance contrasts,
  then use the same trajectory-level BCa rule. The unbuilt alternative was to
  diagnose an inferred latent path before H3.3 has proved or implemented one.
- **Gap:** The supplied contract names `rho_EI|SA`, margins, block counts, and
  confidence levels but does not choose observed values, true latent values,
  posterior means, or posterior draws as the diagnostic sample.
- **Reach:** Statistical and model/domain/action reviewers must approve the
  observed-data estimands. Passing permits only observed synthetic correlation
  and block-equivalence rows; it cannot be relabeled as the formal precision
  blanket, latent recovery, causality, or real stationarity.
- **Verdict:** Needs exact review. The choice is executable and avoids an
  unproved latent seam, but it is scientifically load-bearing.
- **Confidence:** Medium-low.

### Reserve versioned receipt paths for the conditional action seam

- **When:** Naming the evidence that would allow the default-disabled action
  family to exist.
- **Choice:** Propose `readiness/exits/02d-intervention.json` for H3.2d and
  `readiness/exits/04-action-control.json` for H3.4. For example, merely adding
  files at those paths is insufficient: both must carry the exact accepted
  decision and scope frozen in the candidate before any synthetic bytes run.
- **Gap:** Those later slices do not yet own accepted proof receipts, so their
  final schemas and immutable locations cannot be assumed here.
- **Reach:** Model/domain/action and implementation reviewers must approve the
  path-plus-scope contract. A missing, moved, or nonmatching receipt leaves the
  study at passive20 and cannot be repaired by changing v1 in place.
- **Verdict:** Needs exact review. The paths are prospective interfaces, not
  evidence that H3.2d or H3.4 is proved.
- **Confidence:** Medium-low.

### Use a deliberately misspecified independent-axis filter baseline

- **When:** Freezing the two passive comparators before development outcomes.
- **Choice:** Propose four scalar filters with rate 4, stationary marginal
  variance 7/24, and discarded cross-axis covariance. For example, each axis
  updates from its own observation while the H3 model retains the fixed full
  Fin4 precision and covariance.
- **Gap:** H2 supplies only scalar filter/control/grid APIs and the exact Fin4
  transition slices; it does not prove this four-axis executable baseline or
  its implementation.
- **Reach:** Exact model/domain/action and statistical reviews must accept the
  equations and eligibility. H3.3/H3.6S must later implement them; development
  validation may choose between this baseline and the stationary no-update
  predictor, but confirmatory results may not swap the comparator.
- **Verdict:** Needs exact review. It is an honest prospective baseline, not H2
  evidence or a fitted approximation to the H3 covariance.
- **Confidence:** Medium.

### Freeze asymmetric split lengths for equal stationarity blocks

- **When:** Resolving the earlier nondivisible held-out transition count against
  four nominal blocks of 64.
- **Choice:** Keep training at 512 observations and 511 transitions, but use
  257 observations and 256 transitions for both validation and held-out data.
  The held-out transition destinations then split exactly into four contiguous
  blocks of 64 with no dropped or duplicated transition.
- **Gap:** The observation-count asymmetry is an operating choice rather than a
  theorem or a consequence of H2.
- **Reach:** All predictive and stationarity denominators, block indices, seed
  workloads, review artifacts, and later implementation must use 256 held-out
  transitions. Changing back to a nondivisible count requires preserving v1
  and issuing v2 before any execution.
- **Verdict:** Needs exact review. The convention is coherent and explicit but
  remains discretionary.
- **Confidence:** Medium-high.

### Propose independent standard-normal center priors

- **When:** Restricting fitting and SBC to the smallest structural parameter
  set.
- **Choice:** Propose independent N(0,1) priors for exactly
  `center.external`, `center.sensory`, `center.active`, and
  `center.internal`. For example, the latent trajectory is inferred under
  these centers but is not relabeled as another fitted structural scalar.
- **Gap:** H2 does not select priors, and the prior scale is not a theory
  constant.
- **Reach:** The prior SD standardizes recovery thresholds and generates SBC
  truth. Statistical approval of the exact bound payload is required before
  acceptance; K, Sigma, H, R, dt, axis, and transition/stationary laws remain
  fixed or derived under every decision.
- **Verdict:** Needs exact review. The proposal is narrow, inspectable, and
  reversible only through a pre-execution v2.
- **Confidence:** High.

### Treat all numeric operating values as reviewed choices

- **When:** Serializing replicate counts, tolerances, BCa/SBC settings,
  equivalence margins, Holm families, and minimum effects.
- **Choice:** Mark every numeric threshold as
  `discretionary_pending_exact_review`. For example, a 0.01-nat predictive
  margin is a proposed decision rule, not a Fin4 theorem or universal cutoff.
- **Gap:** The numbers came from the supplied statistical review contract, not
  from the accepted formal carrier.
- **Reach:** The statistical reviewer must approve the exact candidate hash.
  No threshold, seed, comparator, or family may change after review or after an
  outcome; a legitimate revision preserves v1 and creates v2.
- **Verdict:** Needs exact review. The status prevents theory-strength claims
  while retaining a complete pre-outcome protocol.
- **Confidence:** High.

## Unsound

None retained.

## Sound

### Repeat complete Holm orders at each activation state

- **When:** Serializing passive20 alone and passive20 plus the conditional
  action6 family.
- **Choice:** Store the complete ordered test IDs in the passive analysis and
  in both action activation states, while the test independently requires all
  repeated lists to equal the same 20- and 26-item sequences. The unbuilt
  alternative was a custom path-reference language that every later consumer
  would have to resolve before knowing the tested family.
- **Gap:** YAML has no native reference semantics, yet reviewers and later
  executors need an exact order in each structurally possible state.
- **Reach:** Each activation state is self-contained and cannot silently reorder
  Holm ties. A future v2 must update every occurrence together and its test must
  reject any divergence.
- **Verdict:** Sound. Deliberate checked repetition is simpler than adding a new
  schema-resolution mechanism for two immutable families.
- **Confidence:** Medium-high.

### Bind the immutable G0 authority snapshot, not mutable status prose

- **When:** Choosing the scientific-design source for the H3.0 hash map.
- **Choice:** Bind the byte-identical G0-accepted authority snapshot and leave
  the live design and README outside the candidate source map. For example, a
  later truthful H3.0 status update can change navigation prose without
  retroactively invalidating the reviewed scientific authority bytes.
- **Gap:** Live lifecycle documents must change after review, while a reviewed
  candidate must not.
- **Reach:** Every bound source mismatch invalidates v1. Mutable navigation can
  advance only through later receipts and cannot silently change this
  candidate's authority.
- **Verdict:** Sound. Historical authority and live status have separate
  owners.
- **Confidence:** High.

### Bind raw files and canonical parsed payloads in one direction

- **When:** Building an immutable review request without making it hash itself
  or freezing the navigation README.
- **Choice:** Bind the candidate's raw SHA-256, its sorted compact canonical
  JSON payload digest, the raw choices/test hashes, and a canonical digest of
  that reviewed-binding object. Put the request's own raw hash only in the
  unbound README. The unbuilt alternative was a circular self-hash or a request
  tied to status prose that must change later.
- **Gap:** Raw bytes alone make harmless formatting indistinguishable from a
  semantic payload change, while a file cannot contain its own final hash.
- **Reach:** Reviewers can reproduce both exact bytes and parsed meaning, then
  bind the request hash out of band. A future receipt can append decisions
  without rewriting candidate v1 or creating a provenance cycle.
- **Verdict:** Sound. Each digest has one owner and the dependency graph is
  acyclic.
- **Confidence:** High.

### Give H3.0 its own append-only choices owner

- **When:** Starting H3.0 after the accepted H3.G0 lifecycle closed.
- **Choice:** Record H3.0 decisions in `h3-0-choices.md` and leave the G0
  `choices.md` byte-for-byte outside this edit. For example, a later H3.0
  reviewer can audit these decisions without rewriting what G0 reviewers
  approved.
- **Gap:** Reusing one mutable ledger would blur gate ownership and break the
  provenance of the closed G0 receipt.
- **Reach:** The H3.0 review request binds this ledger separately; a later
  acceptance receipt can append review decisions without altering either
  gate's history.
- **Verdict:** Sound. Each lifecycle owns its own immutable decision record.
- **Confidence:** High.

### Serialize exact nonidentifiable center pairs

- **When:** Defining the interface-only negative control for each passive
  setting.
- **Choice:** Store each base center and both exact centers obtained as
  `base +/- (1/2)*(1,0,0,-1)`. For example, setting A uses
  `(1/2,0,0,-1/2)` and `(-1/2,0,0,1/2)`, which share the same observed sensory
  and active coordinates under the fixed interface-only H.
- **Gap:** Shorthand labels alone could be interpreted with the wrong axis
  order, sign, or coefficient.
- **Reach:** H3.2c must later prove the rank/identifiability boundary, and
  H3.6S must generate the paired control exactly. Insensitivity blocks only the
  associated unique-full-center-recovery claim.
- **Verdict:** Sound. The control is exact, local, and makes no claim before its
  prospective owners land.
- **Confidence:** High.

### Make stationarity controls paired axis-and-block transformations

- **When:** Making the 0.25-SD drift and 1.25 variance-ratio controls
  reproducible.
- **Choice:** For one setting and axis at a time, transform only the last
  64 transition-destination observations. Add 0.25 exact observed stationary
  SD for the mean control, or scale deviations from the fixed center by
  `sqrt(1.25)` for the variance control; leave every other axis and the first
  three blocks unchanged.
- **Gap:** Naming only a drift or ratio would not specify which samples change
  or preserve paired common input bytes.
- **Reach:** Each associated diagnostic must trigger on its control or lose
  only that stationarity claim row. The rule cannot create empirical,
  causal, energetic, biological, or universal-FEP support.
- **Verdict:** Sound. The negative check is deterministic and scoped to the
  exact estimand it is meant to challenge.
- **Confidence:** High.

### Keep action null unless two later proof gates pass exactly

- **When:** Reconciling a prospective action analysis with unproved H3.2d and
  H3.4 seams.
- **Choice:** Default to null action and omit all six action tests. If both
  exact proof receipts pass before any synthetic execution, the only action is
  same-K center-selection from `{-1/2,0,1/2}` for one dt; there is no state
  reset or hard impulse.
- **Gap:** H2 provides no Fin4 intervention, multivariate belief, or two-step
  controller implementation.
- **Reach:** A valid activation expands passive20 to a single Holm family of
  26. Even a passing result permits only constructed-simulator noninferiority
  or objective superiority, never EFE equivalence, causality, or guaranteed
  benefit.
- **Verdict:** Sound. Unproved action structure is absent rather than assumed.
- **Confidence:** High.

### Lock outcomes, implementation, environment, and comparators before use

- **When:** Separating development work from SBC and confirmatory execution.
- **Choice:** Allow development outcomes only for implementation and baseline
  selection, then require a separate pre-run receipt binding accepted H3.0,
  sources/configuration, selected baselines, environment, seed map, metrics,
  and multiplicity. For example, a failed predictive result is retained as a
  null and cannot trigger a baseline swap.
- **Gap:** A preregistration candidate cannot bind implementation or environment
  bytes that do not yet exist.
- **Reach:** SBC and confirmatory execution remain blocked until the pre-run
  receipt exists. Any post-lock change invalidates the run; undefined,
  nonfinite, failed, or omitted seeds fail rather than disappearing.
- **Verdict:** Sound. The lifecycle prevents outcome-driven mutation.
- **Confidence:** High.

### Keep the synthetic and empirical branches separate

- **When:** Recording downstream eligibility with no canonical governed data
  owner.
- **Choice:** Mark data-owner review N/A for this synthetic-only candidate and
  keep H3.6E blocked. For example, a statistical or model approval here cannot
  authorize real-data access or turn repository data into an eligible dataset.
- **Gap:** `data-capability.yaml` is absent, and no protected outcomes were
  inspected.
- **Reach:** H3.6E remains blocked along with empirical, real causal,
  energetic, biological, and universal-FEP claims. Empirical work requires a
  new governed pre-outcome cycle rather than an H3.0 status edit.
- **Verdict:** Sound. Synthetic formal work grants no empirical eligibility.
- **Confidence:** High.
