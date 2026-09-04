#!/usr/bin/env julia
# RxInfer.jl linear-Gaussian state-space simulation — genuine @model + infer()
# Generated from GNN Model: FepLean Continuous OU Linear-Gaussian Model
# Generated: 2026-09-04 12:18:42
#
# Structure (the continuous parameterization the GNN file declares):
#   x[1]  ~ MvNormal(prior_mean, prior_cov)
#   x[t]  = F * x[t-1] + u[t-1] + N(0, Q)     (1-dim latent state)
#   y[t]  = H * x[t]           + N(0, R)      (1-dim observation)
#
# Control input u: when the GNN declares goal_mean + control_gain the
# forward simulation closes the loop on beliefs, u[t] = gain * (goal - mu[t])
# with mu[t] the online Kalman-filtered mean (same contract as the JAX /
# NumPyro / PyTorch / Stan continuous scripts); otherwise u is all zeros and
# the dynamics run passively. infer() then conditions on the known controls.
# No EFE, policy posterior, or discrete action trace is emitted — none is
# defined for a linear-Gaussian model.
#
# continuous_pomdp_model is fully conjugate, so infer() needs neither
# constraints nor initialization and the free-energy trace is flat after one
# sweep (empirically verified against RxInfer 5.5).

using Pkg
using RxInfer
using Distributions
using LinearAlgebra
using Random
using SHA
using StatsBase
using JSON
using Base64
using Dates

const PLOTS_READY = try
@eval using Plots
true
catch e
println("⚠️ Plots unavailable; PNG plotting disabled: $e")
false
end

const SCHEMA_VERSION = "rxinfer_simulation_v1"
const MODEL_NAME = "FepLean Continuous OU Linear-Gaussian Model"
const NUM_STATES = 1
const NUM_OBSERVATIONS = 1
const TIME_STEPS = 1
const RANDOM_SEED = 42
const INFERENCE_ITERATIONS = 20
const MODEL_KIND = "continuous"
const GNN_SPEC_JSON_B64 = "eyJjYW5vbmljYWxfcG9tZHBfc2NoZW1hIjogImNvbnRpbnVvdXNfbGdzc21fdjEiLCAiY29ubmVjdGlvbnMiOiBbeyJyZWxhdGlvbiI6ICI+IiwgInNvdXJjZSI6ICJGIiwgInRhcmdldCI6ICJ4In0sIHsicmVsYXRpb24iOiAiPiIsICJzb3VyY2UiOiAiUSIsICJ0YXJnZXQiOiAieCJ9LCB7InJlbGF0aW9uIjogIi0iLCAic291cmNlIjogIngiLCAidGFyZ2V0IjogIkgifSwgeyJyZWxhdGlvbiI6ICI+IiwgInNvdXJjZSI6ICJIIiwgInRhcmdldCI6ICJ5In0sIHsicmVsYXRpb24iOiAiPiIsICJzb3VyY2UiOiAiUiIsICJ0YXJnZXQiOiAieSJ9LCB7InJlbGF0aW9uIjogIj4iLCAic291cmNlIjogInByaW9yX21lYW4iLCAidGFyZ2V0IjogIngifSwgeyJyZWxhdGlvbiI6ICI+IiwgInNvdXJjZSI6ICJwcmlvcl9jb3YiLCAidGFyZ2V0IjogIngifV0sICJkZXNjcmlwdGlvbiI6ICJCcmlkZ2UgUDRiIHNsaWNlOiB0aGUgZmVwX2xlYW4gc2NhbGFyIE9VIGZpbHRlciBpbnN0YW5jZVxuKHJhdGU9MSwgY2VudGVyPTAsIGRpZmZ1c2lvblZhcmlhbmNlUmF0ZT0yLCBzdGVwRHVyYXRpb249MSxcbm9ic2VydmF0aW9uIG5vaXNlIHZhcmlhbmNlPTEpIHByb2plY3RlZCBkZXRlcm1pbmlzdGljYWxseSB0b1xuR05OIHYxIGNvbnRpbnVvdXMgbGluZWFyLUdhdXNzaWFuIHN5bnRheCB1bmRlciBjb250cmFjdCB2MC4yXG5yb3VuZGluZy4gRXh0cmFjdGlvbiByZWNvcmQgKGZpbGU6bGluZSBpbiB0aGUgZmVwX2xlYW5cbmNoZWNrb3V0IGF0IHRoZSBjb21taXQgcmVjb3JkZWQgdW5kZXIgU2lnbmF0dXJlKTpcbi0gRiBvbmUtc3RlcCBkZWNheSA9IGV4cCgtcmF0ZSp0KSA9IGV4cCgtMSlcbltzY2FsYXJfZ2F1c3NpYW5fc2VtaWdyb3VwLmxlYW46NDItNDNdXG4tIFEgb25lLXN0ZXAgdHJhbnNpdGlvbiBjb3ZhcmlhbmNlID0gcmF0ZV4tMSooMSAtIGV4cCgtMipyYXRlKnQpKVxuPSAxIC0gZXhwKC0yKSBbbGluZWFyX2dhdXNzaWFuX3NlbWlncm91cC5sZWFuOjEyMTctMTIzM11cbi0gSCBpZGVudGl0eSByZWFkb3V0IFtnYXVzc2lhbl9maWx0ZXIubGVhbjo0Ni00OV1cbi0gUiBvYnNlcnZhdGlvbiBub2lzZSB2YXJpYW5jZSA9IDFcbltwb3N0ZXJpb3JfY29udmVyZ2VuY2UubGVhbjozOC00MF1cbi0gcHJpb3JfbWVhbiA9IDAsIHByaW9yX2NvdiA9IHN0YXRpb25hcnkgdmFyaWFuY2UgPSAxIChwcm92ZWQpXG5bc21vb3RoX3JlZmVyZW5jZV9rZXJuZWwubGVhbjo2Ni02OCwgOTYtMTAxXSIsICJnbm5fc2VjdGlvbiI6ICJGZXBMZWFuQ29udGludW91c09VIGNvbnRpbnVvdXMiLCAiaW5pdGlhbF9wYXJhbWV0ZXJpemF0aW9uIjogeyJGIjogW1swLjM2Nzg3OTQ0MTE3MTQ0MjMzXV0sICJIIjogW1sxLjBdXSwgIlEiOiBbWzAuODY0NjY0NzE2NzYzMzg3M11dLCAiUiI6IFtbMS4wXV0sICJwcmlvcl9jb3YiOiBbWzEuMF1dLCAicHJpb3JfbWVhbiI6IFswLjBdfSwgImluaXRpYWxwYXJhbWV0ZXJpemF0aW9uIjogeyJGIjogW1swLjM2Nzg3OTQ0MTE3MTQ0MjMzXV0sICJIIjogW1sxLjBdXSwgIlEiOiBbWzAuODY0NjY0NzE2NzYzMzg3M11dLCAiUiI6IFtbMS4wXV0sICJwcmlvcl9jb3YiOiBbWzEuMF1dLCAicHJpb3JfbWVhbiI6IFswLjBdfSwgIm1hdHJpeF9wcm92ZW5hbmNlIjogeyJGIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsxLCAxXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiSCI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMSwgMV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIlEiOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzEsIDFdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn0sICJSIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsxLCAxXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAicHJpb3JfY292IjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsxLCAxXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAicHJpb3JfbWVhbiI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifX0sICJtb2RlbF9raW5kIjogImNvbnRpbnVvdXMiLCAibW9kZWxfbmFtZSI6ICJGZXBMZWFuIENvbnRpbnVvdXMgT1UgTGluZWFyLUdhdXNzaWFuIE1vZGVsIiwgIm1vZGVsX3BhcmFtZXRlcnMiOiB7ImRpZmZ1c2lvbl92YXJpYW5jZV9yYXRlIjogMiwgImR0IjogMS4wLCAibnVtX2FjdGlvbnMiOiAxLCAibnVtX2hpZGRlbl9zdGF0ZXMiOiAxLCAibnVtX29icyI6IDEsICJudW1fb2JzZXJ2YXRpb25zIjogMSwgIm51bV9zdGF0ZXMiOiAxLCAibnVtX3RpbWVzdGVwcyI6IDEsICJvYnNlcnZhdGlvbl9ub2lzZV92YXJpYW5jZSI6IDEsICJvdV9jZW50ZXIiOiAwLCAib3VfcmF0ZSI6IDEsICJwYXNzaXZlX21vZGVsIjogdHJ1ZSwgInJhbmRvbV9zZWVkIjogNDIsICJzaW11bGF0aW9uX3BhcmFtcyI6IHt9LCAic3RlcF9kdXJhdGlvbiI6IDF9LCAibmFtZSI6ICJGZXBMZWFuIENvbnRpbnVvdXMgT1UgTGluZWFyLUdhdXNzaWFuIE1vZGVsIiwgIm9udG9sb2d5X21hcHBpbmciOiB7IkYiOiAiU3RhdGVUcmFuc2l0aW9uTWF0cml4IiwgIkgiOiAiT2JzZXJ2YXRpb25NYXRyaXgiLCAiUSI6ICJQcm9jZXNzTm9pc2VDb3ZhcmlhbmNlIiwgIlIiOiAiT2JzZXJ2YXRpb25Ob2lzZUNvdmFyaWFuY2UiLCAicHJpb3JfY292IjogIlByaW9yQ292YXJpYW5jZSIsICJwcmlvcl9tZWFuIjogIlByaW9yTWVhbiIsICJ0IjogIlRpbWUiLCAieCI6ICJDb250aW51b3VzSGlkZGVuU3RhdGUiLCAieSI6ICJDb250aW51b3VzT2JzZXJ2YXRpb24ifSwgInN0cnVjdHVyZWRfcG9tZHAiOiB7ImFkYXB0ZXJfbm90ZXMiOiBbXSwgImNvbnRyb2xfZmFjdG9ycyI6IFt7ImNvbW1lbnQiOiAiY29udHJvbCBpbnB1dCAocGFzc2l2ZTogemVybykiLCAiZGltZW5zaW9ucyI6IFsxLCAxXSwgImluZGV4IjogMCwgIm5hbWUiOiAidSIsICJyb2xlIjogImZhY3RvciIsICJzaXplIjogMSwgInR5cGUiOiAiZmxvYXQifV0sICJtYXRyaWNlcyI6IHsiRiI6IFtbMC4zNjc4Nzk0NDExNzE0NDIzM11dLCAiSCI6IFtbMS4wXV0sICJRIjogW1swLjg2NDY2NDcxNjc2MzM4NzNdXSwgIlIiOiBbWzEuMF1dLCAicHJpb3JfY292IjogW1sxLjBdXSwgInByaW9yX21lYW4iOiBbMC4wXX0sICJtYXRyaXhfcHJvdmVuYW5jZSI6IHsiRiI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMSwgMV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIkgiOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzEsIDFdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn0sICJRIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsxLCAxXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiUiI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMSwgMV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgInByaW9yX2NvdiI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMSwgMV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgInByaW9yX21lYW4iOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzFdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn19LCAib2JzZXJ2YXRpb25fbW9kYWxpdGllcyI6IFtdLCAic3RhdGVfZmFjdG9ycyI6IFtdfSwgInZhcmlhYmxlcyI6IFt7ImNvbW1lbnQiOiAibGF0ZW50IHNjYWxhciBzdGF0ZSIsICJkaW1lbnNpb25zIjogWzEsIDFdLCAibmFtZSI6ICJ4IiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogInByb2Nlc3Mgbm9pc2UgY292YXJpYW5jZSIsICJkaW1lbnNpb25zIjogWzEsIDFdLCAibmFtZSI6ICJRIiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogInhfMSBtZWFuIiwgImRpbWVuc2lvbnMiOiBbMSwgMV0sICJuYW1lIjogInByaW9yX21lYW4iLCAidHlwZSI6ICJmbG9hdCJ9LCB7ImNvbW1lbnQiOiAieF8xIGNvdmFyaWFuY2UiLCAiZGltZW5zaW9ucyI6IFsxLCAxXSwgIm5hbWUiOiAicHJpb3JfY292IiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogImRpc2NyZXRlIHN0ZXAgaW5kZXgiLCAiZGltZW5zaW9ucyI6IFsxXSwgIm5hbWUiOiAidCIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJvYnNlcnZhdGlvbiIsICJkaW1lbnNpb25zIjogWzEsIDFdLCAibmFtZSI6ICJ5IiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogIm9ic2VydmF0aW9uIG1hdHJpeCAoaWRlbnRpdHkgcmVhZG91dCkiLCAiZGltZW5zaW9ucyI6IFsxLCAxXSwgIm5hbWUiOiAiSCIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJvYnNlcnZhdGlvbiBub2lzZSBjb3ZhcmlhbmNlIiwgImRpbWVuc2lvbnMiOiBbMSwgMV0sICJuYW1lIjogIlIiLCAidHlwZSI6ICJmbG9hdCJ9LCB7ImNvbW1lbnQiOiAiY29udHJvbCBpbnB1dCAocGFzc2l2ZTogemVybykiLCAiZGltZW5zaW9ucyI6IFsxLCAxXSwgIm5hbWUiOiAidSIsICJ0eXBlIjogImZsb2F0In1dfQ=="
const GNN_SPEC = JSON.parse(String(base64decode(GNN_SPEC_JSON_B64)))

function package_version(name::String)
for (_, dep) in Pkg.dependencies()
    if dep.name == name
        return string(dep.version)
    end
end
return "unknown"
end

# The linear-Gaussian @model is precompiled in the GnnRxInferModels package.
using GnnRxInferModels: continuous_pomdp_model

# --- Continuous parameterization loading ---------------------------------
# InitialParameterization matrices parse as [row][col]; vectors parse flat.

function read_matrix(raw, rows, cols, label)
if length(raw) != rows
    error("$label has $(length(raw)) rows, expected $rows")
end
M = zeros(Float64, rows, cols)
for r in 1:rows
    row = collect(raw[r])
    if length(row) != cols
        error("$label row $r has $(length(row)) entries, expected $cols")
    end
    for c in 1:cols
        M[r, c] = Float64(row[c])
    end
end
return M
end

function matrix_rows(M)
return [Float64.(collect(M[r, :])) for r in 1:size(M, 1)]
end

function load_continuous_parameters()
initial = GNN_SPEC["initialparameterization"]
F = read_matrix(initial["F"], NUM_STATES, NUM_STATES, "F")
H = read_matrix(initial["H"], NUM_OBSERVATIONS, NUM_STATES, "H")
Q = read_matrix(initial["Q"], NUM_STATES, NUM_STATES, "Q")
R = read_matrix(initial["R"], NUM_OBSERVATIONS, NUM_OBSERVATIONS, "R")
D_cov = read_matrix(initial["prior_cov"], NUM_STATES, NUM_STATES, "prior_cov")
D_mean = Float64.(collect(initial["prior_mean"]))
if length(D_mean) != NUM_STATES
    error("prior_mean length $(length(D_mean)) does not match expected $NUM_STATES")
end
return F, H, Q, R, D_mean, D_cov
end

# Optional closed-loop control declared by the GNN file (goal_mean + control_gain).
function load_control_parameters()
initial = GNN_SPEC["initialparameterization"]
if !(haskey(initial, "goal_mean") && haskey(initial, "control_gain"))
    return nothing, 0.0
end
goal = Float64.(collect(initial["goal_mean"]))
if length(goal) != NUM_STATES
    error("goal_mean length $(length(goal)) does not match expected $NUM_STATES")
end
gain_raw = initial["control_gain"]
while isa(gain_raw, AbstractVector) && length(gain_raw) == 1
    gain_raw = gain_raw[1]
end
return goal, Float64(gain_raw)
end

# One Kalman predict/update step (Joseph-form covariance update).
function kalman_step(mu, P, y, F, H, Q, R, u_prev, first)
if first
    mu_pred, P_pred = mu, P
else
    mu_pred = F * mu + u_prev
    P_pred = F * P * F' + Q
end
S = H * P_pred * H' + R
K = (P_pred * H') / S
mu_new = mu_pred + K * (y - H * mu_pred)
IKH = I - K * H
return mu_new, IKH * P_pred * IKH' + K * R * K'
end

# Take the LAST variational iteration's per-timestep marginals and fail loud
# if the chain length does not match the simulated horizon.
function last_iteration_marginals(posteriors, label)
final_iter = posteriors[end]
per_step = isa(final_iter, Vector) ? final_iter : [final_iter]
if length(per_step) != TIME_STEPS
    error("$label posterior has $(length(per_step)) marginals, expected $TIME_STEPS")
end
return per_step
end

function run_simulation()
Random.seed!(RANDOM_SEED)
F, H, Q, R, D_mean, D_cov = load_continuous_parameters()
goal_mean, control_gain = load_control_parameters()
closed_loop = goal_mean !== nothing

# --- Phase 1: Forward simulation of the true continuous trajectory ---
# Sampled from the generative model itself, so the posterior means can be
# scored against a known ground truth (rmse_vs_true below). When the GNN
# declares a goal, the control applied at each transition is computed from
# the online Kalman-filtered belief (closed loop on beliefs).
u_seq = [zeros(Float64, NUM_STATES) for _ in 1:TIME_STEPS]
process_noise = MvNormal(zeros(NUM_STATES), Q)
observation_noise = MvNormal(zeros(NUM_OBSERVATIONS), R)

true_states_continuous = Vector{Vector{Float64}}()
observations_continuous = Vector{Vector{Float64}}()
filtered_means = Vector{Vector{Float64}}()

x = rand(MvNormal(D_mean, D_cov))
y = H * x + rand(observation_noise)
push!(true_states_continuous, copy(x))
push!(observations_continuous, y)
mu_f, P_f = kalman_step(D_mean, D_cov, y, F, H, Q, R, zeros(NUM_STATES), true)
push!(filtered_means, copy(mu_f))
if closed_loop
    u_seq[1] = control_gain .* (goal_mean .- mu_f)
end
for t in 2:TIME_STEPS
    x = F * x + u_seq[t-1] + rand(process_noise)
    y = H * x + rand(observation_noise)
    push!(true_states_continuous, copy(x))
    push!(observations_continuous, y)
    mu_f, P_f = kalman_step(mu_f, P_f, y, F, H, Q, R, u_seq[t-1], false)
    push!(filtered_means, copy(mu_f))
    if closed_loop
        u_seq[t] = control_gain .* (goal_mean .- mu_f)
    end
end

# --- Phase 2: Real RxInfer inference (no fallback, no constraints) ---
# NO try/catch — if infer() fails, the script crashes with a clear error.
result = infer(
    model = continuous_pomdp_model(F = F, H = H, Q = Q, R = R,
                                   D_mean = D_mean, D_cov = D_cov,
                                   u = u_seq, T = TIME_STEPS),
    data = (y = observations_continuous,),
    iterations = INFERENCE_ITERATIONS,
    free_energy = true
)

uses_real_rxinfer = true

# --- Phase 3: Posterior mean/covariance extraction ---
q_s = last_iteration_marginals(result.posteriors[:s], "s")
posterior_means = [Float64.(collect(mean(m))) for m in q_s]
posterior_cov = [matrix_rows(Matrix(cov(m))) for m in q_s]

vfe_per_iteration = Float64.(result.free_energy)
variational_free_energy = copy(vfe_per_iteration)

if length(vfe_per_iteration) >= 5
    last_5 = vfe_per_iteration[end-4:end]
    inference_converged = (maximum(last_5) - minimum(last_5)) < 1e-4
elseif length(vfe_per_iteration) >= 2
    inference_converged = abs(vfe_per_iteration[end] - vfe_per_iteration[end-1]) < 1e-4
else
    inference_converged = false
end

# --- Validation ---
# Bethe free energy for a continuous model is routinely NEGATIVE (it
# carries differential-entropy terms), so the discrete generators'
# "vfe > 0" check is WRONG here. The correct invariant is finiteness.
vfe_finite = !isempty(vfe_per_iteration) && all(isfinite, vfe_per_iteration)
means_finite = all(m -> all(isfinite, m), posterior_means)

# Positive-definiteness via Cholesky with a 1e-12 jitter: smoothed
# covariances can be numerically singular to machine precision without
# being invalid.
posterior_cov_psd = all(
    m -> isposdef(Symmetric(Matrix(cov(m)) + 1e-12 * I)), q_s
)

squared_error = 0.0
element_count = 0
for t in 1:TIME_STEPS
    residual = posterior_means[t] .- true_states_continuous[t]
    squared_error += sum(residual .^ 2)
    element_count += length(residual)
end
rmse_vs_true = element_count > 0 ? sqrt(squared_error / element_count) : 0.0
rmse_finite = isfinite(rmse_vs_true)

validation = Dict(
    "vfe_finite" => vfe_finite,
    "means_finite" => means_finite,
    "posterior_cov_psd" => posterior_cov_psd,
    "inference_converged" => inference_converged,
    "rmse_vs_true" => rmse_vs_true,
    "rmse_finite" => rmse_finite
)
validation["all_valid"] = validation["vfe_finite"] &&
    validation["means_finite"] &&
    validation["posterior_cov_psd"] &&
    validation["inference_converged"] &&
    validation["rmse_finite"]

script_sha = try
    script_path = PROGRAM_FILE
    if isfile(script_path)
        open(script_path) do f
            bytes2hex(sha256(read(f)))
        end
    else
        "unknown"
    end
catch
    "unknown"
end

return Dict(
    "schema_version" => SCHEMA_VERSION,
    "success" => true,
    "framework" => "RxInfer.jl",
    "model_name" => MODEL_NAME,
    "num_timesteps" => TIME_STEPS,
    # "beliefs" carries the per-timestep posterior MEANS (T x n_states),
    # the continuous analogue of a belief trajectory. Uncertainty lives in
    # posterior_cov; the two together are the full Gaussian marginal.
    "beliefs" => posterior_means,
    "posterior_cov" => posterior_cov,
    "true_states_continuous" => true_states_continuous,
    "observations_continuous" => observations_continuous,
    "controls" => u_seq,
    "kalman_filter_means" => filtered_means,
    "control_mode" => closed_loop ? "closed_loop_proportional" : "passive",
    # Discrete-schema slots stay EMPTY: this model declares no discrete
    # observation indices, no action set, and therefore no expected free
    # energy or policy posterior. Emitting zeros here would be fabricated
    # data. The continuous data lives in the *_continuous keys above.
    "observations" => Int[],
    "true_states" => Int[],
    "actions" => Int[],
    "expected_free_energy" => Float64[],
    "efe_per_action" => Vector{Vector{Float64}}(),
    "policy_posterior" => Vector{Vector{Float64}}(),
    "variational_free_energy" => variational_free_energy,
    "vfe_per_iteration" => vfe_per_iteration,
    "model_parameters" => Dict(
        "F_shape" => collect(size(F)),
        "H_shape" => collect(size(H)),
        "Q_shape" => collect(size(Q)),
        "R_shape" => collect(size(R)),
        "prior_mean_shape" => [length(D_mean)],
        "prior_cov_shape" => collect(size(D_cov)),
        "num_continuous_states" => NUM_STATES,
        "num_continuous_observations" => NUM_OBSERVATIONS,
        "inference_iterations" => INFERENCE_ITERATIONS,
        # Deliberately EMPTY: the GNN spec's state_factors describe the
        # exemplar's DISCRETE dual parameterization, not the continuous
        # state — "beliefs" here are posterior mean vectors, so echoing
        # the discrete factorization would make downstream per-factor
        # recovery raise on a renderer/analyzer contract violation.
        "state_factors" => [],
        "observation_modalities" => []
    ),
    "matrix_provenance" => get(GNN_SPEC, "matrix_provenance", Dict()),
    "runtime_metadata" => Dict(
        "random_seed" => RANDOM_SEED,
        "schema_version" => SCHEMA_VERSION,
        "generated_at" => string(now()),
        "rxinfer_version" => package_version("RxInfer"),
        "julia_version" => string(VERSION),
        "script_sha256" => script_sha,
        "inference_converged" => inference_converged,
        "uses_real_rxinfer" => uses_real_rxinfer,
        "model_kind" => MODEL_KIND,
        "parameterization" => "linear_gaussian_state_space",
        "control_input" => closed_loop ? "closed_loop_proportional_on_beliefs" : "passive_zero_vector",
        "rmse_vs_true" => rmse_vs_true
    ),
    "metrics" => Dict(
        "expected_free_energy" => Float64[],
        "policy_posterior" => Vector{Vector{Float64}}(),
        "belief_confidence" => Float64[],
        "variational_free_energy" => variational_free_energy
    ),
    "validation" => validation
)
end

# --- Structured per-step execution log (JSON Lines) ---
function write_execution_log(results)
log_path = "simulation.log"
means = results["beliefs"]
covariances = results["posterior_cov"]
true_states = results["true_states_continuous"]
observations = results["observations_continuous"]
validation = get(results, "validation", Dict())

open(log_path, "w") do file
    for step in 1:TIME_STEPS
        record = Dict(
            "event" => "step",
            "step" => step,
            "model_name" => MODEL_NAME,
            "schema_version" => SCHEMA_VERSION,
            "posterior_mean" => means[step],
            "posterior_cov" => covariances[step],
            "true_state" => true_states[step],
            "observation" => observations[step],
            "validation" => validation
        )
        JSON.print(file, record)
        println(file)
    end
    summary = Dict(
        "event" => "summary",
        "schema_version" => SCHEMA_VERSION,
        "model_name" => MODEL_NAME,
        "num_steps" => TIME_STEPS,
        "validation" => validation
    )
    JSON.print(file, summary)
    println(file)
end

full_log = Dict(
    "schema_version" => SCHEMA_VERSION,
    "model_name" => MODEL_NAME,
    "format" => "jsonl",
    "num_steps" => TIME_STEPS,
    "validation" => validation,
    "log_file" => log_path
)
open("simulation_log.json", "w") do file
    JSON.print(file, full_log, 2)
end

println("RxInfer.jl simulation wrote $log_path and simulation_log.json")
return log_path
end

# --- Julia-native visualization (posterior mean vs true trajectory) ---
function write_plots(results)
if !PLOTS_READY
    println("⚠️ Skipping PNG plots (Plots backend not available)")
    return
end
try
    means = results["beliefs"]
    true_states = results["true_states_continuous"]
    vfe = results["vfe_per_iteration"]

    if !isempty(means)
        mean_mat = hcat(means...)
        true_mat = hcat(true_states...)
        steps = 1:size(mean_mat, 2)
        p1 = plot(
            title = "Posterior Mean vs True Continuous State",
            xlabel = "Time step",
            ylabel = "State value",
            legend = :outertopright,
            size = (900, 450),
            linewidth = 2
        )
        for dim in 1:size(mean_mat, 1)
            plot!(p1, steps, mean_mat[dim, :], label = "posterior x$dim")
            plot!(p1, steps, true_mat[dim, :], label = "true x$dim", linestyle = :dash)
        end
        savefig(p1, "belief_evolution.png")
    end

    if !isempty(vfe)
        p2 = plot(
            1:length(vfe), vfe,
            title = "Variational Free Energy per Iteration",
            xlabel = "Iteration",
            ylabel = "Bethe free energy (nats)",
            label = "VFE",
            legend = :topright,
            size = (900, 400),
            linewidth = 2
        )
        savefig(p2, "free_energy.png")
    end

    println("RxInfer.jl simulation wrote PNG plots (belief_evolution.png, free_energy.png)")
catch e
    println("⚠️ Plotting skipped (Plots backend unavailable): $e")
end
end

function main()
results = run_simulation()
function sanitize!(x)
    if isa(x, Float64)
        if isnan(x) || isinf(x)
            return 0.0
        end
        return x
    elseif isa(x, Vector)
        return [sanitize!(v) for v in x]
    elseif isa(x, Dict)
        for (k, v) in x
            x[k] = sanitize!(v)
        end
        return x
    end
    return x
end
results = sanitize!(results)
open("simulation_results.json", "w") do file
    JSON.print(file, results, 2)
end
println("RxInfer.jl simulation wrote simulation_results.json")
write_execution_log(results)
write_plots(results)
return results["validation"]["all_valid"] ? 0 : 1
end

if abspath(PROGRAM_FILE) == @__FILE__
exit(main())
end
