# H3.0 v3 choice ledger

This is the append-only decision record for the current H3.0 v3 candidate. It
does not accept H3.0, open H3.1, or authorize outcome access. The exact v1
and v2 protocol, choices, tests, requests, transition snapshots, and WITHHOLD
records remain under versioned paths. The canonical unversioned protocol and
this ledger name the current v3 candidate; downstream authority resolves only
through a future final acceptance receipt.

## Withheld v1 decisions

### Unsound: duplicate-tolerant YAML

- **Decision:** V1 used `yaml.safe_load`, which silently resolved duplicate
  mapping keys by last value. V1 itself contains a repeated
  `paired_replicates_per_setting` key.
- **Judgment:** Unsound and WITHHELD. A fail-closed protocol cannot have two
  source-level meanings while tests validate only the constructed last value.
- **Source:** Independent implementation/provenance review; preserved v1 raw
  SHA-256 `103f9598…a5ca3` and test SHA-256 `434484f1…c289`.
- **Replacement:** V2 and the live G0 guard use a recursive duplicate-key-
  rejecting SafeLoader subclass. Top-level and nested duplicate probes fail.
- **Reach:** The strict loader owns both validation and canonical hashing.

### Unsound: underdefined observation law

- **Decision:** V1 froze `H` and `R` without stating the full observation law
  or its independence assumptions.
- **Judgment:** Unsound and WITHHELD. Fixed matrices alone do not determine a
  time-indexed stochastic observation process.
- **Source:** H3 Gate Audit model/domain/action WITHHOLD.
- **Replacement:** V2 states `Z[0] ~ N(c,Sigma)`, the accepted Fin4 transition,
  `Y[t] = H Z[t] + epsilon[t]`, iid multivariate-normal observation noise, and
  mutual independence across observation times and from `Z[0]` and every
  latent innovation. Each control has exact `H` and `R`.
- **Reach:** Path assembly remains prospective H3.6S; none of these clauses
  retroactively turns H2 into a four-dimensional executable study.

### Unsound: qualitative negative controls

- **Decision:** V1 named nonidentifiability and correlated-noise controls but
  did not uniquely define their sensitivity estimands and gates.
- **Judgment:** Unsound and WITHHELD.
- **Source:** H3 Gate Audit model/domain/action WITHHOLD.
- **Replacement:** The interface-only pair uses exact centers
  `base +/- (1/2)*(1,0,0,-1)`, common innovations and noise, two `1e-10`
  equality gates, and at least one failed external/internal recovery cell per
  setting. The correlated-noise control uses held-out oracle errors `e=Y-Z`,
  pooled sensory-active Pearson correlation, and a whole-trajectory 95% BCa
  lower bound greater than `0.10` per setting.
- **Reach:** Both gates are conjunctive and outside Holm. Insensitivity blocks
  only unique full-center recovery or diagonal-noise calibration,
  respectively.

### Unsound: cell-counted action coverage

- **Decision:** V1 treated 1,024 axis-step indicators as independent coverage
  observations.
- **Judgment:** Unsound and WITHHELD because the independent unit is a whole
  trajectory.
- **Source:** Independent statistical WITHHOLD.
- **Replacement:** V2 forms each trajectory's `q_i` as the mean of its eight
  axis-step indicators, equally averages 128 `q_i` values, and uses `B=9,999`
  whole-trajectory BCa resamples. The unadjusted 90% BCa interval must be
  strictly inside `[0.85,0.95]`; both add-one tails enter the response
  composite p-value.
- **Reach:** No axis-step pseudo-replication remains.

### Unsound: non-executable SBC and incomplete p-values

- **Decision:** V1 referred to an exact discrete rank test, a simulated ECDF
  envelope, and ESS-based thinning without defining a unique computation.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Independent statistical WITHHOLD.
- **Replacement:** V2 uses 255 independent analytic-Gaussian posterior draws,
  strict-less ranks with ties failing, 16-bin Pearson statistics, an exact
  multinomial tail, four-test Holm, the fixed DKW band
  `sqrt(log(160)/640)`, exact coverage tails, count bands, and an eight-test
  coverage Holm family. MCMC thinning and ESS are inapplicable.
- **Reach:** Any undefined, nonfinite, failed, retried, or omitted seed fails.

### Unsound: ambiguous bootstrap and recovery cells

- **Decision:** V1 named BCa but did not pin tie handling, acceleration,
  quantiles, recovery-cell aggregation, or add-one tails.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Independent statistical WITHHOLD.
- **Replacement:** V2 freezes `n=128` independent whole-trajectory units,
  `B=9,999` resamples of size 128, half-weight bias-correction ties,
  leave-one-of-128 acceleration, linear quantiles, and denominator 10,000
  add-one tails. Recovery is separate for two settings by four axes; the p90
  is nearest-rank order statistic 116 of 128. Latent RMSE uses held-out
  destinations 1 through 256.
- **Reach:** Undefined acceleration or an invalid denominator fails.

### Unsound: tuning budget around analytic solves

- **Decision:** V1 combined Sobol configurations, multiple starts, and
  evaluation budgets with an analytic Gaussian fitting contract.
- **Judgment:** Unsound and WITHHELD as contradictory and outcome-flexible.
- **Source:** Independent statistical WITHHOLD.
- **Replacement:** V2 has no tuning search. The selected method and each
  passive baseline receive one exact analytic Gaussian solve per fit. Training
  alone fits the four center components; validation and held-out evaluation
  restart from a frozen stationary state prior and integrate training center
  uncertainty.
- **Reach:** Failed or nonfinite analytic solves are retained and fail.

### Unsound: incomplete Holm component construction

- **Decision:** V1 sent sign tests or vaguely named maximum p-values to Holm
  without fully defining every component.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Independent statistical WITHHOLD.
- **Replacement:** Every composite is the maximum of all required component
  p-values. Predictive and superiority rows combine an add-one SESOI tail with
  the exact `Binomial(128,0.75)` upper tail. Noninferiority uses the add-one
  `-0.02` tail. Equivalence and action-response rows use all predeclared
  one-sided components.
- **Reach:** The passive order is exactly 20 unique IDs. The conditional family
  is exactly those 20 plus six unique action IDs.

### Unsound: ambiguous action improvement sign

- **Decision:** V1 described `selected_policy_minus_baseline` while the
  objective is a cost and positive thresholds were called improvement.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Root pre-freeze model/statistical read-through.
- **Replacement:** Every action improvement estimand is explicitly
  `baseline_cost_minus_selected_policy_cost`; positive means lower selected
  cost. The noninferiority and superiority thresholds retain `-0.02` and
  `0.10` under that sign convention.
- **Reach:** Mutation tests reject reversing the estimand without changing the
  full protocol version.

### Unsound: underdefined RNG construction

- **Decision:** V1 pinned a digest recipe and PCG64 name but did not define the
  integer conversion, stream separation, complete zero-based domains, or raw
  known answers.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Independent implementation/provenance WITHHOLD.
- **Replacement:** V2 uses a v2 root prefix, unsigned big-endian 64-bit
  indices, full-digest big-endian seed integers, `Generator(PCG64(seed_int))`,
  distinct split and latent/observation namespaces, exact domains, and two
  digest plus `random_raw` vectors. Exact NumPy/environment versions wait for
  the pre-run lock.
- **Reach:** Reuse, retry, aliasing, and namespace substitution are forbidden.

### Unsound: unreachable final acceptance

- **Decision:** V1's live test required the final receipt to remain absent.
- **Judgment:** Unsound and WITHHELD because acceptance would require editing
  the already-reviewed test and invalidate its reviewed hash.
- **Source:** Independent implementation/provenance WITHHOLD.
- **Replacement:** The v2 live test validates the current candidate branch and
  the exact future accepted branch without modification. A final receipt must
  bind the raw v2 request, canonical reviewed binding, candidate, choices,
  live test, transition snapshot, G0 receipt, and three distinct review
  identities, decisions, tokens, and identical approved-hash maps.
- **Reach:** A valid receipt opens H3.1 only.

### Unsound: file-presence pre-run unlock

- **Decision:** V1 named a pre-run file without an exact schema, dependency
  decisions, protected namespaces, or one-shot semantics.
- **Judgment:** Unsound and WITHHELD.
- **Source:** Independent implementation/provenance WITHHOLD.
- **Replacement:** V2 freezes exact top-level fields, accepted decisions, raw
  and canonical protocol hashes, implementation/config/environment/baseline/
  development-selection/seed/metric hashes, exact NumPy and PCG64 binding,
  action-family status, three protected namespaces, and a one-shot execution
  identifier and atomic result receipt.
- **Reach:** Premature or malformed pre-run files and protected outputs fail.
  Mere file presence never unlocks SBC or confirmatory execution.

### Unsound: mutable transition provenance

- **Decision:** V1 bound selected mutable live sources directly and had no
  complete transition-state absence record.
- **Judgment:** Unsound and WITHHELD due to time-of-check/time-of-use drift.
- **Source:** Independent implementation/provenance WITHHOLD.
- **Replacement:** `transition-state-snapshot-v2.json` binds accepted G0
  authority, the manifest, formal projection generator, canonical/projection/
  aggregate parity inputs, and path-specific absence of H3 implementation,
  empirical owner, pre-run lock, final H3.0 receipt, and protected namespaces.
  The mutable live design and README are navigation-only and unbound.
- **Reach:** No global dataset-absence inference is made.

## V2 replacements

### Exact model and fitting boundary

- **Decision:** Freeze the exact Fin4 `K`, derived `Sigma`, axis order, `dt=1/4`,
  two passive identifiable centers, setting/control-specific `H` and `R`, and
  stationary starts. Fit exactly four center components under independent
  proposed `N(0,1)` priors.
- **Alternatives rejected:** Fitting `K`, `Sigma`, `H`, `R`, `dt`, an axis, or
  treating the latent path as a fitted structural scalar.
- **Rationale:** These would change the scientific model or inflate recovery
  degrees of freedom after protocol freeze.
- **Reversal condition:** A new preserved protocol version and all three exact
  re-reviews; never an outcome-aware v2 edit.

### Exact asymmetric split and stationarity blocks

- **Decision:** Train uses 512 observations and 511 transitions. Validation
  and held-out each use 257 observations and 256 transitions. Held-out
  destinations split exactly `[64,64,64,64]` with no remainder.
- **Alternative rejected:** 256 observations and 255 transitions with unequal
  block precision.
- **Rationale:** Equal contiguous blocks make the first-versus-last diagnostic
  exact. The asymmetry is a discretionary reviewed choice, not a theorem.
- **Reversal condition:** New version before protected execution.

### Passive primary and conditional action families

- **Decision:** The default family contains two predictive, two blanket, and
  sixteen stationarity rows. Null action is default. Only exact H3.2d and H3.4
  accepted proof receipts, both present before synthetic execution and locked
  pre-run, activate six action rows.
- **Alternatives rejected:** Hard state impulses, EFE, finite POMDP, RL, H2
  scalar LQ/MPC, and no-epistemic ablation.
- **Rationale:** The smallest prospective seam is same-`K` center selection
  from `{-1/2,0,1/2}` for one `dt`, with no reset and no guaranteed benefit.
- **Reach:** Controller baselines remain conditional; passive baselines are
  always the stationary-marginal/no-update predictor and prospective
  independent-axis diagonal filter.

### Full, distinct action proof receipts

- **Decision:** H3.2d and H3.4 each supply a full receipt surface covering
  compiler, owner, imports, declarations, evidence, independent review,
  downstream effects, excluded claims, and source hashes. H3.0 pins each
  receipt path, gate, scope, proof owner, focused validator, review token, and
  predecessor receipts, while the distinct focused validator owns the exact
  module/import/declaration roster.
- **Alternatives rejected:** The earlier six-field evidence-poor wrapper and a
  shared broad `h3_case_study` owner/import/test contract. Both would either be
  unreviewable or leak causal, finite, filter, control, and path imports into
  the narrow H3.2d seam.
- **Rationale:** H3.2d may use a dedicated center-selection owner with only the
  reference-model and Markov-semigroup imports; H3.4 necessarily has a
  different quadratic action-control owner. Both must remain noncausal and
  non-EFE. Source-bound focused-validator evidence keeps the roster exact at
  the slice that can prove it without H3.0 guessing future declaration names.
- **Dependencies:** H3.2d requires accepted H3.1 reference-model and H3.2a
  intrinsic-carrier receipts; H3.2b/c are parallel, not prerequisites. H3.4
  requires accepted H3.2d and H3.3 inference receipts.
- **Reach:** Neither proof receipt opens action execution alone. Both valid
  receipts must be bound into the later pre-run lock before action6 can exist.

### Development lane versus protected execution

- **Decision:** H3.0 acceptance opens H3.1 only. After separate H3.3 and H3.6S
  executable-owner acceptances, a deterministic unprotected development lane
  may use train and validation only for implementation debugging and baseline
  selection. SBC, confirmatory, held-out, and protected namespaces remain
  sealed until a valid pre-run lock.
- **Alternatives rejected:** Blocking development needed to form the lock, or
  letting development results mutate thresholds, metrics, seeds, comparators,
  the confirmatory plan, or claim matrix.
- **Rationale:** The state machine must make the pre-run dependency reachable
  without exposing confirmatory outcomes.
- **Reach:** Development produces no H3.6S acceptance claim.

### Synthetic-only claims and empirical no-go

- **Decision:** H3.0 v2 can support only the exact rows in its synthetic claim
  matrix. `data-capability.yaml` is absent; data-owner review is N/A.
- **Alternatives rejected:** Treating a statistical/model approval as real-data
  eligibility, or relabeling synthetic prediction as causal, energetic,
  biological, empirical, or universal-FEP evidence.
- **Rationale:** H3.6E has a separate canonical metadata owner and remains
  structurally blocked.
- **Reach:** No protected outcomes were inspected.

## Reversal and downstream boundary

- V1 is immutable WITHHELD history; it cannot be revived for acceptance.
- V2 numeric thresholds are `discretionary_pending_exact_review`, never theory
  constants.
- Any threshold, seed, metric, comparator, Holm, action, or source-map change
  creates v3 and preserves v2.
- Oracle or SBC failure blocks H3.6S. Recovery failure blocks the recovery row.
  Predictive failure remains a null result with no baseline swap. Diagnostic
  failures remove only their claim rows. Insensitive negative controls block
  their associated claims.
- The current v2 artifacts request three exact re-reviews. They do not accept
  H3.0, open H3.1, inspect outcomes, or create empirical eligibility.

## Withheld v2 decisions

The immutable v2 package is bound by raw candidate SHA-256
`f8e6ee11…cc797`, canonical payload SHA-256 `1af927e8…893f2`, choices
`12d62bc…e9a8b`, live-test snapshot `b1b349ac…aac95`, request
`26f2bf42…d8981`, transition snapshot `6e300d04…61747`, and reviewed-binding
digest `6e788d2d…d9d3`. It is not reusable for acceptance.

### Unsound and WITHHELD: ambiguous SBC allocation and coverage

- **Decision:** V2 pooled 320 SBC replications without an exact setting split
  and left analytic marginal intervals, endpoint inclusion, and exact-binomial
  tails incomplete.
- **Judgment:** Unsound and WITHHELD by `/root/h30_stats_final_review`.
- **V3 replacement:** Exactly 160 replications per setting, pooled A then B;
  255 strict-less analytic posterior draws only determine ranks. Coverage uses
  analytic Gaussian central marginal intervals with inclusive endpoints,
  exact inclusive binomial tails, fixed count bands, and exact Holm orders.

### Unsound and WITHHELD: incomplete estimators and bootstrap mechanics

- **Decision:** V2 did not uniquely define each center estimator, dense oracle,
  parameter/latent/nonidentifiability RMSE comparator, bootstrap interpolation,
  or trajectory-index draw.
- **Judgment:** Unsound and WITHHELD by `/root/h30_stats_final_review`.
- **V3 replacement:** Each estimator and oracle is explicit per setting and
  axis. BCa uses 128 whole-trajectory units, 9,999 PCG64-indexed resamples,
  half-weight ties, leave-one-trajectory acceleration, exact NumPy linear
  interpolation, and an exhaustive 76-ID stream roster. Each resample uses the
  pinned 128-index `Generator.integers` call and reuses that vector inside a
  composite row only.

### Unsound and WITHHELD: non-deterministic comparator selection

- **Decision:** V2 did not fully determine predictive/action wins, the
  strongest controller comparator, exact ties, or the selected open-loop pair.
- **Judgment:** Unsound and WITHHELD by both statistical and implementation
  reviewers.
- **V3 replacement:** Scores use locked `math.fsum` orders. Exact float ties
  select the lexicographically smallest baseline ID; the matched open-loop
  search selects the first pair in the registered nine-pair order. Wins require
  strict positive trajectory contrasts; exact zero is a nonwin and all 128
  trajectories stay in the denominator.

### Unsound and WITHHELD: mutable formal evidence and shallow predecessors

- **Decision:** V2 recomputed receipts against later mutable manifest/owner
  bytes, accepted four-field predecessor stubs, and trusted parity/manifest/
  roster booleans.
- **Judgment:** Unsound and WITHHELD by `/root/h3_gate_audit` and
  `/root/h30_impl_review`.
- **V3 replacement:** Every gate owns an immutable source snapshot containing
  exactly common sources, canonical/projection owner bytes, validator, test
  transcript, build transcripts, import sources, and direct predecessor receipt
  bytes. The validator recursively checks full predecessor source/review
  schemas and recomputes parity, the literal manifest tuple, imports,
  declarations, and the import-source roster digest from immutable bytes only.

### Unsound and WITHHELD: inconsistent H3.3 owner and incomplete DAG

- **Decision:** V2 alternated between `h3_case_study` and `h3_inference`, and
  its formal gate surface could bypass H3.2b/H3.2c.
- **Judgment:** Unsound and WITHHELD by `/root/h3_gate_audit`.
- **V3 replacement:** The accepted G0 authority selects
  `compositions/h3_case_study.lean` as the sole H3.3 owner; the alternate owner
  is forbidden. H3.3 requires full H3.2b and H3.2c receipts. H3.2b is limited
  to the fixed Fin4 precision-zero conditional-independence statement plus a
  separate 2D perturbed unconditional-dependence diagnostic; no generic
  converse is allowed. H3.2c states exact conditional means, blanket-contrast
  noninjectivity, full-H rank 4, and interface-H rank 2 with the registered
  center pair; it makes no generic recognition-identifiability claim.

### Reviewed prospective authority delta: split action owners

- **Decision:** Accepted G0 named shared `h3_case_study` action ownership, while
  v3 proposes dedicated `h3_center_selection` for H3.2d and
  `h3_action_control` for H3.4.
- **Judgment:** This is an explicit prospective refinement, not inherited G0
  authority. It remains pending exact model/domain/action and implementation
  reviews over the v3 binding.
- **V3 boundary:** H3.4 must directly import both canonical H3.3 inference and
  H3.2d center selection. The two-step chronology is nonanticipating:
  `b0 -> a0 -> y1 -> b1 -> a1 -> z2/objective`. Neither action may condition
  on its resulting observation. No EFE, state reset, hard impulse, causal
  interpretation, or guaranteed benefit is permitted.

### Unsound and WITHHELD: incomplete protected one-shot lifecycle

- **Decision:** V2 lacked exact protected manifest/result schemas, full
  recomputation, crash semantics, and overwrite exclusion.
- **Judgment:** Unsound and WITHHELD by `/root/h30_impl_review`.
- **V3 replacement:** A safe-component execution ID and durable `O_EXCL` claim
  precede the first RNG draw. The writer fsyncs claim, staging, published files
  and directories, manifest, and result in the registered order; publish is
  no-overwrite. A no-follow re-enumeration must equal the exact manifest before
  the result commit marker. Only armed, consumed-incomplete, and completed
  states are valid. Any crash after claim consumes v3 permanently; there is no
  delete, retry, resume, overwrite, or second execution.

### Exact v2 WITHHOLD identities

- Statistical: `/root/h30_stats_final_review`, “Codex independent H3.0 v2
  statistical exact-hash reviewer,” raw decision `WITHHOLD`, token `null`.
- Model/domain/action: `/root/h3_gate_audit`, “H3 Gate Audit,” raw decision
  `WITHHOLD`, token `null`.
- Implementation/provenance/outcome-lock: `/root/h30_impl_review`, “Lovelace
  the 2nd,” raw decision `WITHHOLD`, literal decision token `withheld`.

## V3 replacement and review boundary

- The primary family remains passive20; action6 exists only after recursively
  valid H3.2d and H3.4 receipts are frozen before development.
- The development lane requires full H3.3 and H3.6S executable-owner receipts,
  uses train and validation only, selects comparators deterministically, and
  cannot alter thresholds, metrics, seeds, comparators, confirmatory plan,
  claims, or action status.
- SBC, confirmatory, held-out, and protected execution remain blocked until a
  full accepted H3.0 receipt and exact pre-run lock validate.
- H3.6E, empirical, causal, energetic, biological, and universal-FEP claims
  remain blocked. Data-owner review is N/A for this synthetic-only candidate.
- Every numeric threshold is `discretionary_pending_exact_review`, never a
  theory constant. Any revision creates v4 and preserves v3.
- V3 is a candidate until three distinct exact-hash APPROVE reviews issue the
  registered tokens and a separate final receipt is appended. That receipt may
  open H3.1 only.
