package gnn.categorical

import cats._
import cats.implicits._
import cats.arrow.Category

object FepLeanSymmetricBooleanGenerativeModelModel {

  // State Space
  type A = Any
  type B = Any
  type C = Any
  type D = Any
  type E = Any
  type F = Any
  type G = Any
  type o = Any
  type s = Any
  type s_prime = Any
  type t = Any
  type π = Any

  // Morphisms
  val AToo:observation_mapping: A => o:observation_mapping = identity
  val BTos_prime:state_prediction: B => s_prime:state_prediction = identity
  val CToG:pragmatic_cost: C => G:pragmatic_cost = identity
  val DTos:prior_initialization: D => s:prior_initialization = identity
  val EToπ:prior_policy: E => π:prior_policy = identity
  val GToπ:policy_selection: G => π:policy_selection = identity
  val sToB:transition: s => B:transition = identity
  val s_primeToA:likelihood: s_prime => A:likelihood = identity
  val πToB:policy_conditioned_transition: π => B:policy_conditioned_transition = identity

}
// MODEL_DATA: {"model_name":"FepLean Symmetric Boolean Generative Model","annotation":"Bridge P1 spike: the fep_lean active_inference.lean\nGenerativeModel instance `symmetricBoolModel trueBiasedPolicyPrior`\n(two policies, two hidden states, two observations, one step)\nprojected deterministically to GNN v1 syntax.\nExtraction record (file:line in the fep_lean checkout at the\ncommit recorded under Signature):\n- D initialState = fairBoolLaw (1/2, 1/2)\n  [def active_inference.lean:719-722; use :745]\n- B transition = fairBoolKernel, policy-indexed, all entries 1/2\n  [def active_inference.lean:725-728; use :746]\n- A likelihood = fairBoolKernel, all entries 1/2\n  [def active_inference.lean:725-728; use :747]\n- C preferences = fairBoolLaw (1/2, 1/2)\n  [def active_inference.lean:719-722; use :748]\n- E policyPrior = trueBiasedPolicyPrior: E(false)=1/4, E(true)=3/4\n  [def active_inference.lean:731-734; parameter :743,:749]\n- Timescale: one transition application [active_inference.lean:30-32]\n- The Lean GenerativeModel carries no Action type, so no `u`\n  variable or action edges are emitted.","variables":[{"name":"A","var_type":"likelihood_matrix","data_type":"float","dimensions":[2,2]},{"name":"B","var_type":"transition_matrix","data_type":"float","dimensions":[2,2,2]},{"name":"C","var_type":"preference_vector","data_type":"float","dimensions":[2]},{"name":"D","var_type":"prior_vector","data_type":"float","dimensions":[2]},{"name":"E","var_type":"policy","data_type":"float","dimensions":[2]},{"name":"s","var_type":"hidden_state","data_type":"float","dimensions":[2,1]},{"name":"s_prime","var_type":"hidden_state","data_type":"float","dimensions":[2,1]},{"name":"o","var_type":"observation","data_type":"float","dimensions":[2,1]},{"name":"\u03c0","var_type":"policy","data_type":"float","dimensions":[2]},{"name":"F","var_type":"hidden_state","data_type":"float","dimensions":[1]},{"name":"G","var_type":"policy","data_type":"float","dimensions":[1]},{"name":"t","var_type":"hidden_state","data_type":"integer","dimensions":[1]}],"connections":[{"source_variables":["D"],"target_variables":["s:prior_initialization"],"connection_type":"directed"},{"source_variables":["s"],"target_variables":["B:transition"],"connection_type":"undirected"},{"source_variables":["B"],"target_variables":["s_prime:state_prediction"],"connection_type":"directed"},{"source_variables":["s_prime"],"target_variables":["A:likelihood"],"connection_type":"undirected"},{"source_variables":["A"],"target_variables":["o:observation_mapping"],"connection_type":"undirected"},{"source_variables":["E"],"target_variables":["\u03c0:prior_policy"],"connection_type":"directed"},{"source_variables":["\u03c0"],"target_variables":["B:policy_conditioned_transition"],"connection_type":"undirected"},{"source_variables":["C"],"target_variables":["G:pragmatic_cost"],"connection_type":"directed"},{"source_variables":["G"],"target_variables":["\u03c0:policy_selection"],"connection_type":"directed"}],"parameters":[{"name":"A","value":[[0.5,0.5],[0.5,0.5]],"param_type":"constant"},{"name":"B","value":[[[0.5,0.5],[0.5,0.5]],[[0.5,0.5],[0.5,0.5]]],"param_type":"constant"},{"name":"C","value":[[0.5,0.5]],"param_type":"constant"},{"name":"D","value":[[0.5,0.5]],"param_type":"constant"},{"name":"E","value":[[0.25,0.75]],"param_type":"constant"},{"name":"num_timesteps","value":1,"param_type":"constant"}],"equations":[],"time_specification":{"time_type":"Dynamic","discretization":null,"horizon":1,"step_size":null},"ontology_mappings":[{"variable_name":"A","ontology_term":"LikelihoodMatrix","description":null},{"variable_name":"B","ontology_term":"TransitionMatrix","description":null},{"variable_name":"C","ontology_term":"Preferences","description":null},{"variable_name":"D","ontology_term":"PriorOverHiddenStates","description":null},{"variable_name":"E","ontology_term":"Habit","description":null},{"variable_name":"F","ontology_term":"VariationalFreeEnergy","description":null},{"variable_name":"G","ontology_term":"ExpectedFreeEnergy","description":null},{"variable_name":"s","ontology_term":"HiddenState","description":null},{"variable_name":"s_prime","ontology_term":"NextHiddenState","description":null},{"variable_name":"o","ontology_term":"Observation","description":null},{"variable_name":"\u03c0","ontology_term":"PolicyVector","description":null},{"variable_name":"t","ontology_term":"Time","description":null}]}
