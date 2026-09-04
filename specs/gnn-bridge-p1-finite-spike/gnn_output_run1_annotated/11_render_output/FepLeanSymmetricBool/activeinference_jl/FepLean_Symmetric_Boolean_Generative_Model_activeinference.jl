#!/usr/bin/env julia
# ActiveInference.jl discrete POMDP simulation
# Generated from GNN Model: FepLean Symmetric Boolean Generative Model

using Pkg
using ActiveInference
using Distributions
using LinearAlgebra
using Random
using StatsBase
using JSON
using Base64
using Dates

const SCHEMA_VERSION = "activeinference_jl_simulation_v1"
const MODEL_NAME = "FepLean Symmetric Boolean Generative Model"
const NUM_STATES = 2
const NUM_OBSERVATIONS = 2
const NUM_ACTIONS = 2
const TIME_STEPS = 1
const RANDOM_SEED = 42
const ACTION_PRECISION = 4.0
const B_TENSOR_ORDER = "next_state_previous_state_action"
const GNN_SPEC_JSON_B64 = "eyJjYW5vbmljYWxfcG9tZHBfc2NoZW1hIjogImNhbm9uaWNhbF9wb21kcF92MSIsICJjb25uZWN0aW9ucyI6IFt7InJlbGF0aW9uIjogIj4iLCAic291cmNlIjogIkQiLCAidGFyZ2V0IjogInM6cHJpb3JfaW5pdGlhbGl6YXRpb24ifSwgeyJyZWxhdGlvbiI6ICItIiwgInNvdXJjZSI6ICJzIiwgInRhcmdldCI6ICJCOnRyYW5zaXRpb24ifSwgeyJyZWxhdGlvbiI6ICI+IiwgInNvdXJjZSI6ICJCIiwgInRhcmdldCI6ICJzX3ByaW1lOnN0YXRlX3ByZWRpY3Rpb24ifSwgeyJyZWxhdGlvbiI6ICItIiwgInNvdXJjZSI6ICJzX3ByaW1lIiwgInRhcmdldCI6ICJBOmxpa2VsaWhvb2QifSwgeyJyZWxhdGlvbiI6ICItIiwgInNvdXJjZSI6ICJBIiwgInRhcmdldCI6ICJvOm9ic2VydmF0aW9uX21hcHBpbmcifSwgeyJyZWxhdGlvbiI6ICI+IiwgInNvdXJjZSI6ICJFIiwgInRhcmdldCI6ICJcdTAzYzA6cHJpb3JfcG9saWN5In0sIHsicmVsYXRpb24iOiAiLSIsICJzb3VyY2UiOiAiXHUwM2MwIiwgInRhcmdldCI6ICJCOnBvbGljeV9jb25kaXRpb25lZF90cmFuc2l0aW9uIn0sIHsicmVsYXRpb24iOiAiPiIsICJzb3VyY2UiOiAiQyIsICJ0YXJnZXQiOiAiRzpwcmFnbWF0aWNfY29zdCJ9LCB7InJlbGF0aW9uIjogIj4iLCAic291cmNlIjogIkciLCAidGFyZ2V0IjogIlx1MDNjMDpwb2xpY3lfc2VsZWN0aW9uIn1dLCAiZGVzY3JpcHRpb24iOiAiQnJpZGdlIFAxIHNwaWtlOiB0aGUgZmVwX2xlYW4gYWN0aXZlX2luZmVyZW5jZS5sZWFuXG5HZW5lcmF0aXZlTW9kZWwgaW5zdGFuY2UgYHN5bW1ldHJpY0Jvb2xNb2RlbCB0cnVlQmlhc2VkUG9saWN5UHJpb3JgXG4odHdvIHBvbGljaWVzLCB0d28gaGlkZGVuIHN0YXRlcywgdHdvIG9ic2VydmF0aW9ucywgb25lIHN0ZXApXG5wcm9qZWN0ZWQgZGV0ZXJtaW5pc3RpY2FsbHkgdG8gR05OIHYxIHN5bnRheC5cbkV4dHJhY3Rpb24gcmVjb3JkIChmaWxlOmxpbmUgaW4gdGhlIGZlcF9sZWFuIGNoZWNrb3V0IGF0IHRoZVxuY29tbWl0IHJlY29yZGVkIHVuZGVyIFNpZ25hdHVyZSk6XG4tIEQgaW5pdGlhbFN0YXRlID0gZmFpckJvb2xMYXcgKDEvMiwgMS8yKVxuW2RlZiBhY3RpdmVfaW5mZXJlbmNlLmxlYW46NzE5LTcyMjsgdXNlIDo3NDVdXG4tIEIgdHJhbnNpdGlvbiA9IGZhaXJCb29sS2VybmVsLCBwb2xpY3ktaW5kZXhlZCwgYWxsIGVudHJpZXMgMS8yXG5bZGVmIGFjdGl2ZV9pbmZlcmVuY2UubGVhbjo3MjUtNzI4OyB1c2UgOjc0Nl1cbi0gQSBsaWtlbGlob29kID0gZmFpckJvb2xLZXJuZWwsIGFsbCBlbnRyaWVzIDEvMlxuW2RlZiBhY3RpdmVfaW5mZXJlbmNlLmxlYW46NzI1LTcyODsgdXNlIDo3NDddXG4tIEMgcHJlZmVyZW5jZXMgPSBmYWlyQm9vbExhdyAoMS8yLCAxLzIpXG5bZGVmIGFjdGl2ZV9pbmZlcmVuY2UubGVhbjo3MTktNzIyOyB1c2UgOjc0OF1cbi0gRSBwb2xpY3lQcmlvciA9IHRydWVCaWFzZWRQb2xpY3lQcmlvcjogRShmYWxzZSk9MS80LCBFKHRydWUpPTMvNFxuW2RlZiBhY3RpdmVfaW5mZXJlbmNlLmxlYW46NzMxLTczNDsgcGFyYW1ldGVyIDo3NDMsOjc0OV1cbi0gVGltZXNjYWxlOiBvbmUgdHJhbnNpdGlvbiBhcHBsaWNhdGlvbiBbYWN0aXZlX2luZmVyZW5jZS5sZWFuOjMwLTMyXVxuLSBUaGUgTGVhbiBHZW5lcmF0aXZlTW9kZWwgY2FycmllcyBubyBBY3Rpb24gdHlwZSwgc28gbm8gYHVgXG52YXJpYWJsZSBvciBhY3Rpb24gZWRnZXMgYXJlIGVtaXR0ZWQuIiwgImdubl9zZWN0aW9uIjogIkZlcExlYW5TeW1tZXRyaWNCb29sIiwgImluaXRpYWxfcGFyYW1ldGVyaXphdGlvbiI6IHsiQSI6IFtbMC41LCAwLjVdLCBbMC41LCAwLjVdXSwgIkIiOiBbW1swLjUsIDAuNV0sIFswLjUsIDAuNV1dLCBbWzAuNSwgMC41XSwgWzAuNSwgMC41XV1dLCAiQyI6IFswLjUsIDAuNV0sICJEIjogWzAuNSwgMC41XSwgIkUiOiBbMC4yNSwgMC43NV19LCAiaW5pdGlhbHBhcmFtZXRlcml6YXRpb24iOiB7IkEiOiBbWzAuNSwgMC41XSwgWzAuNSwgMC41XV0sICJCIjogW1tbMC41LCAwLjVdLCBbMC41LCAwLjVdXSwgW1swLjUsIDAuNV0sIFswLjUsIDAuNV1dXSwgIkMiOiBbMC41LCAwLjVdLCAiRCI6IFswLjUsIDAuNV0sICJFIjogWzAuMjUsIDAuNzVdfSwgIm1hdHJpeF9wcm92ZW5hbmNlIjogeyJBIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsyLCAyXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiQiI6IHsiY2Fub25pY2FsX29yZGVyIjogIm5leHRfc3RhdGVfcHJldmlvdXNfc3RhdGVfYWN0aW9uIiwgImNsYWltZWRfc2xpY2VfY29udmVudGlvbiI6IG51bGwsICJjb250cmFkaWN0aW9uIjogZmFsc2UsICJkZWNsYXJlZF9vcmRlciI6IFsibmV4dF9zdGF0ZSIsICJwcmV2aW91c19zdGF0ZSIsICJhY3Rpb24iXSwgImRlcml2ZWQiOiBmYWxzZSwgImRldGVjdGVkX29yZGVyIjogbnVsbCwgInJlYXNvbiI6IG51bGwsICJzaGFwZSI6IFsyLCAyLCAyXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiIsICJzb3VyY2Vfb3JkZXIiOiAibmV4dF9zdGF0ZV9wcmV2aW91c19zdGF0ZV9hY3Rpb24ifSwgIkMiOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzJdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn0sICJEIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsyXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiRSI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifX0sICJtb2RlbF9uYW1lIjogIkZlcExlYW4gU3ltbWV0cmljIEJvb2xlYW4gR2VuZXJhdGl2ZSBNb2RlbCIsICJtb2RlbF9wYXJhbWV0ZXJzIjogeyJiX3RlbnNvcl9vcmRlciI6ICJuZXh0X3N0YXRlX3ByZXZpb3VzX3N0YXRlX2FjdGlvbiIsICJjb250cm9sX2ZhY3RvcnMiOiBbeyJjb21tZW50IjogInBvbGljeSBwcmlvciAvIHBvc3RlcmlvciBvdmVyIHBvbGljaWVzIiwgImRpbWVuc2lvbnMiOiBbMl0sICJpbmRleCI6IDAsICJuYW1lIjogIlx1MDNjMCIsICJyb2xlIjogImJvb2trZWVwaW5nIiwgInNpemUiOiAyLCAidHlwZSI6ICJmbG9hdCJ9XSwgIm51bV9hY3Rpb25zIjogMiwgIm51bV9oaWRkZW5fc3RhdGVzIjogMiwgIm51bV9tb2RhbGl0aWVzIjogMSwgIm51bV9vYnMiOiAyLCAibnVtX3N0YXRlX2ZhY3RvcnMiOiAyLCAibnVtX3RpbWVzdGVwcyI6IDEsICJvYnNlcnZhdGlvbl9tb2RhbGl0aWVzIjogW3siY29tbWVudCI6ICJwcmVkaWN0ZWRPdXRjb21lIGRpc3RyaWJ1dGlvbiIsICJkaW1lbnNpb25zIjogWzIsIDFdLCAiaW5kZXgiOiAwLCAibmFtZSI6ICJvIiwgInJvbGUiOiAiZmFjdG9yIiwgInNpemUiOiAyLCAidHlwZSI6ICJmbG9hdCJ9XSwgInBhc3NpdmVfbW9kZWwiOiBmYWxzZSwgInNpbXVsYXRpb25fcGFyYW1zIjoge30sICJzdGF0ZV9mYWN0b3JzIjogW3siY29tbWVudCI6ICJpbml0aWFsU3RhdGUgZGlzdHJpYnV0aW9uIiwgImRpbWVuc2lvbnMiOiBbMiwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogInMiLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJwcmVkaWN0ZWRTdGF0ZSAob25lLXN0ZXApIiwgImRpbWVuc2lvbnMiOiBbMiwgMV0sICJpbmRleCI6IDEsICJuYW1lIjogInNfcHJpbWUiLCAicm9sZSI6ICJib29ra2VlcGluZyIsICJzaXplIjogMiwgInR5cGUiOiAiZmxvYXQifV19LCAibmFtZSI6ICJGZXBMZWFuIFN5bW1ldHJpYyBCb29sZWFuIEdlbmVyYXRpdmUgTW9kZWwiLCAib250b2xvZ3lfbWFwcGluZyI6IHsiQSI6ICJMaWtlbGlob29kTWF0cml4IiwgIkIiOiAiVHJhbnNpdGlvbk1hdHJpeCIsICJDIjogIlByZWZlcmVuY2VzIiwgIkQiOiAiUHJpb3JPdmVySGlkZGVuU3RhdGVzIiwgIkUiOiAiSGFiaXQiLCAiRiI6ICJWYXJpYXRpb25hbEZyZWVFbmVyZ3kiLCAiRyI6ICJFeHBlY3RlZEZyZWVFbmVyZ3kiLCAibyI6ICJPYnNlcnZhdGlvbiIsICJzIjogIkhpZGRlblN0YXRlIiwgInNfcHJpbWUiOiAiTmV4dEhpZGRlblN0YXRlIiwgInQiOiAiVGltZSIsICJcdTAzYzAiOiAiUG9saWN5VmVjdG9yIn0sICJzdHJ1Y3R1cmVkX3BvbWRwIjogeyJhZGFwdGVyX25vdGVzIjogW10sICJjYW5vbmljYWxfYl9vcmRlciI6ICJuZXh0X3N0YXRlX3ByZXZpb3VzX3N0YXRlX2FjdGlvbiIsICJjb250cm9sX2ZhY3RvcnMiOiBbeyJjb21tZW50IjogInBvbGljeSBwcmlvciAvIHBvc3RlcmlvciBvdmVyIHBvbGljaWVzIiwgImRpbWVuc2lvbnMiOiBbMl0sICJpbmRleCI6IDAsICJuYW1lIjogIlx1MDNjMCIsICJyb2xlIjogImJvb2trZWVwaW5nIiwgInNpemUiOiAyLCAidHlwZSI6ICJmbG9hdCJ9XSwgIm1hdHJpY2VzIjogeyJBIjogW1swLjUsIDAuNV0sIFswLjUsIDAuNV1dLCAiQiI6IFtbWzAuNSwgMC41XSwgWzAuNSwgMC41XV0sIFtbMC41LCAwLjVdLCBbMC41LCAwLjVdXV0sICJDIjogWzAuNSwgMC41XSwgIkQiOiBbMC41LCAwLjVdLCAiRSI6IFswLjI1LCAwLjc1XX0sICJtYXRyaXhfcHJvdmVuYW5jZSI6IHsiQSI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMiwgMl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIkIiOiB7ImNhbm9uaWNhbF9vcmRlciI6ICJuZXh0X3N0YXRlX3ByZXZpb3VzX3N0YXRlX2FjdGlvbiIsICJjbGFpbWVkX3NsaWNlX2NvbnZlbnRpb24iOiBudWxsLCAiY29udHJhZGljdGlvbiI6IGZhbHNlLCAiZGVjbGFyZWRfb3JkZXIiOiBbIm5leHRfc3RhdGUiLCAicHJldmlvdXNfc3RhdGUiLCAiYWN0aW9uIl0sICJkZXJpdmVkIjogZmFsc2UsICJkZXRlY3RlZF9vcmRlciI6IG51bGwsICJyZWFzb24iOiBudWxsLCAic2hhcGUiOiBbMiwgMiwgMl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24iLCAic291cmNlX29yZGVyIjogIm5leHRfc3RhdGVfcHJldmlvdXNfc3RhdGVfYWN0aW9uIn0sICJDIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFsyXSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiRCI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbMl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIkUiOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzJdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn19LCAib2JzZXJ2YXRpb25fbW9kYWxpdGllcyI6IFt7ImNvbW1lbnQiOiAicHJlZGljdGVkT3V0Y29tZSBkaXN0cmlidXRpb24iLCAiZGltZW5zaW9ucyI6IFsyLCAxXSwgImluZGV4IjogMCwgIm5hbWUiOiAibyIsICJyb2xlIjogImZhY3RvciIsICJzaXplIjogMiwgInR5cGUiOiAiZmxvYXQifV0sICJzdGF0ZV9mYWN0b3JzIjogW3siY29tbWVudCI6ICJpbml0aWFsU3RhdGUgZGlzdHJpYnV0aW9uIiwgImRpbWVuc2lvbnMiOiBbMiwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogInMiLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJwcmVkaWN0ZWRTdGF0ZSAob25lLXN0ZXApIiwgImRpbWVuc2lvbnMiOiBbMiwgMV0sICJpbmRleCI6IDEsICJuYW1lIjogInNfcHJpbWUiLCAicm9sZSI6ICJib29ra2VlcGluZyIsICJzaXplIjogMiwgInR5cGUiOiAiZmxvYXQifV19LCAidmFyaWFibGVzIjogW3siY29tbWVudCI6ICJpbml0aWFsU3RhdGUgZGlzdHJpYnV0aW9uIiwgImRpbWVuc2lvbnMiOiBbMiwgMV0sICJuYW1lIjogInMiLCAidHlwZSI6ICJmbG9hdCJ9LCB7ImNvbW1lbnQiOiAicHJlZGljdGVkU3RhdGUgKG9uZS1zdGVwKSIsICJkaW1lbnNpb25zIjogWzIsIDFdLCAibmFtZSI6ICJzX3ByaW1lIiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogImRpc2NyZXRlIHRpbWUgc3RlcCAob25lLXN0ZXAgbW9kZWwpIiwgImRpbWVuc2lvbnMiOiBbMV0sICJuYW1lIjogInQiLCAidHlwZSI6ICJmbG9hdCJ9LCB7ImNvbW1lbnQiOiAicHJlZGljdGVkT3V0Y29tZSBkaXN0cmlidXRpb24iLCAiZGltZW5zaW9ucyI6IFsyLCAxXSwgIm5hbWUiOiAibyIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJwb2xpY3kgcHJpb3IgLyBwb3N0ZXJpb3Igb3ZlciBwb2xpY2llcyIsICJkaW1lbnNpb25zIjogWzJdLCAibmFtZSI6ICJcdTAzYzAiLCAidHlwZSI6ICJmbG9hdCJ9XX0="
const GNN_SPEC = JSON.parse(String(base64decode(GNN_SPEC_JSON_B64)))

function package_version(name::String)
    for (_, dep) in Pkg.dependencies()
        if dep.name == name
            return string(dep.version)
        end
    end
    return "unknown"
end

function to_float_matrix(raw)
    rows = collect(raw)
    matrix = zeros(Float64, length(rows), length(collect(rows[1])))
    for row in eachindex(rows)
        values = collect(rows[row])
        for column in eachindex(values)
            matrix[row, column] = Float64(values[column])
        end
    end
    return matrix
end

function to_float_tensor(raw)
    blocks = collect(raw)
    rows = length(blocks)
    columns = length(collect(blocks[1]))
    actions = length(collect(collect(blocks[1])[1]))
    tensor = zeros(Float64, rows, columns, actions)
    for next_state in 1:rows
        block = collect(blocks[next_state])
        for previous_state in 1:columns
            values = collect(block[previous_state])
            for action in 1:actions
                tensor[next_state, previous_state, action] = Float64(values[action])
            end
        end
    end
    return tensor
end

function normalize_vector(values)
    vector = Float64.(collect(values))
    total = sum(vector)
    if !isfinite(total) || total <= 0
        error("probability vector has invalid mass")
    end
    return vector ./ total
end

function normalize_columns!(matrix)
    for column in 1:size(matrix, 2)
        total = sum(matrix[:, column])
        if !isfinite(total) || total <= 0
            error("matrix column has invalid probability mass")
        end
        matrix[:, column] ./= total
    end
    return matrix
end

function normalize_tensor!(tensor)
    for action in 1:size(tensor, 3)
        for previous_state in 1:size(tensor, 2)
            total = sum(tensor[:, previous_state, action])
            if !isfinite(total) || total <= 0
                error("transition column has invalid probability mass")
            end
            tensor[:, previous_state, action] ./= total
        end
    end
    return tensor
end

function softmax(values)
    shifted = values .- maximum(values)
    weights = exp.(shifted)
    return weights ./ sum(weights)
end

function categorical_index(probabilities)
    safe_probs = max.(probabilities, 1e-16)
    safe_probs ./= sum(safe_probs)
    return rand(Categorical(safe_probs))
end

function compute_efe(belief, action, A, B, C_pref)
    predicted_state = B[:, :, action] * belief
    predicted_state = max.(predicted_state, 1e-16)
    predicted_state ./= sum(predicted_state)
    predicted_obs = A * predicted_state
    predicted_obs = max.(predicted_obs, 1e-16)
    predicted_obs ./= sum(predicted_obs)

    ambiguity = 0.0
    for state in eachindex(predicted_state)
        likelihood = max.(A[:, state], 1e-16)
        ambiguity -= predicted_state[state] * sum(likelihood .* log.(likelihood))
    end

    preferred = max.(C_pref, 1e-16)
    risk = sum(predicted_obs .* (log.(predicted_obs) .- log.(preferred)))
    return ambiguity + risk
end

function select_action(belief, A, B, C_pref)
    efe_values = [compute_efe(belief, action, A, B, C_pref) for action in 1:size(B, 3)]
    policy = softmax(-ACTION_PRECISION .* efe_values)
    action = categorical_index(policy)
    return action, efe_values, policy
end

function validate_dimensions(A, B, C, D)
    if size(A) != (NUM_OBSERVATIONS, NUM_STATES)
        error("A shape $(size(A)) does not match expected ($NUM_OBSERVATIONS, $NUM_STATES)")
    end
    if size(B) != (NUM_STATES, NUM_STATES, NUM_ACTIONS)
        error("B shape $(size(B)) does not match expected ($NUM_STATES, $NUM_STATES, $NUM_ACTIONS)")
    end
    if length(C) != NUM_OBSERVATIONS
        error("C length $(length(C)) does not match expected $NUM_OBSERVATIONS")
    end
    if length(D) != NUM_STATES
        error("D length $(length(D)) does not match expected $NUM_STATES")
    end
end

function run_simulation()
    Random.seed!(RANDOM_SEED)
    initial = GNN_SPEC["initialparameterization"]
    A = normalize_columns!(to_float_matrix(initial["A"]))
    B = normalize_tensor!(to_float_tensor(initial["B"]))
    C = Float64.(collect(initial["C"]))
    D = normalize_vector(initial["D"])
    E = haskey(initial, "E") ? normalize_vector(initial["E"]) : fill(1.0 / NUM_ACTIONS, NUM_ACTIONS)
    validate_dimensions(A, B, C, D)

    C_pref = softmax(C)
    current_state = categorical_index(D)
    current_belief = copy(D)

    observations = Int[]
    true_states = Int[]
    actions = Int[]
    beliefs = Vector{Vector{Float64}}()
    efe_per_action = Vector{Vector{Float64}}()
    selected_efe = Float64[]
    policy_posterior = Vector{Vector{Float64}}()

    for step in 1:TIME_STEPS
        observation = categorical_index(A[:, current_state])
        likelihood = A[observation, :]
        updated = current_belief .* likelihood
        if sum(updated) <= 0
            error("belief update produced zero mass at step $step")
        end
        current_belief = updated ./ sum(updated)

        action, efe_values, policy = select_action(current_belief, A, B, C_pref)
        next_probs = B[:, current_state, action]
        current_state = categorical_index(next_probs)
        predicted = B[:, :, action] * current_belief
        current_belief = predicted ./ sum(predicted)

        push!(observations, observation - 1)
        push!(true_states, current_state - 1)
        push!(actions, action - 1)
        push!(beliefs, copy(current_belief))
        push!(efe_per_action, copy(efe_values))
        push!(selected_efe, efe_values[action])
        push!(policy_posterior, copy(policy))
    end

    validation = Dict(
        "all_beliefs_valid" => all(b -> all(v -> 0.0 <= v <= 1.0, b), beliefs),
        "beliefs_sum_to_one" => all(b -> isapprox(sum(b), 1.0; atol=1e-6), beliefs),
        "actions_in_range" => all(a -> 0 <= a < NUM_ACTIONS, actions),
        "all_valid" => true
    )
    validation["all_valid"] = validation["all_beliefs_valid"] &&
        validation["beliefs_sum_to_one"] &&
        validation["actions_in_range"]

    return Dict(
        "schema_version" => SCHEMA_VERSION,
        "success" => true,
        "framework" => "ActiveInference.jl",
        "model_name" => MODEL_NAME,
        "num_timesteps" => TIME_STEPS,
        "observations_by_modality" => Dict("joint_observation" => observations),
        "hidden_states_by_factor" => Dict("joint_state" => true_states),
        "actions_by_control_factor" => Dict("joint_action" => actions),
        "beliefs_by_factor" => Dict("joint_state" => beliefs),
        "expected_free_energy" => selected_efe,
        "efe_per_action" => efe_per_action,
        "variational_free_energy" => Float64[],
        "policy_posterior" => policy_posterior,
        "observations" => observations,
        "true_states" => true_states,
        "actions" => actions,
        "beliefs" => beliefs,
        "model_parameters" => Dict(
            "A_shape" => collect(size(A)),
            "B_shape" => collect(size(B)),
            "C_shape" => [length(C)],
            "D_shape" => [length(D)],
            "E_shape" => [length(E)],
            "num_states" => NUM_STATES,
            "num_observations" => NUM_OBSERVATIONS,
            "num_actions" => NUM_ACTIONS
        ),
        "matrix_provenance" => get(GNN_SPEC, "matrix_provenance", Dict()),
        "runtime_metadata" => Dict(
            "random_seed" => RANDOM_SEED,
            "schema_version" => SCHEMA_VERSION,
            "generated_at" => string(now()),
            "activeinference_jl_version" => package_version("ActiveInference"),
            "julia_version" => string(VERSION)
        ),
        "metrics" => Dict(
            "expected_free_energy" => selected_efe,
            "policy_posterior" => policy_posterior,
            "belief_confidence" => [maximum(b) for b in beliefs]
        ),
        "validation" => validation
    )
end

function main()
    results = run_simulation()
    open("simulation_results.json", "w") do file
        JSON.print(file, results, 2)
    end
    println("ActiveInference.jl simulation wrote simulation_results.json")
    return results["validation"]["all_valid"] ? 0 : 1
end

if abspath(PROGRAM_FILE) == @__FILE__
    exit(main())
end
