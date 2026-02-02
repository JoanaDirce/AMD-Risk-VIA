import pandas as pd
import numpy as np
import os
from via.engine import generate_graph_weights, initiate_bp_messages, run_belief_propagation

class AMDRiskModel:
    def __init__(self, results_path, amd_cutoff=3):
        self.results_path = results_path
        self.amd_cutoff = amd_cutoff
        self.model_params = None
        self.graph_structure = None
        
    def load_model(self, fixed_state=1, label_col='ASMULTIMODALORRES_E1_C18'):
        """Loads trained weights from the results Excel file."""
        
        file_path = os.path.join(self.results_path, f"InfluenceScores_fixedSate{fixed_state}_AMD_cutoff{self.amd_cutoff}.xlsx")
        data_csv = pd.read_excel(file_path)

        dummy_header = data_csv['event'].values
        
        # Extract weights
        x0_0 = data_csv['0_x=0'].values
        x1_0 = data_csv['0_x=1'].values
        x0_1 = data_csv['1_x=0'].values
        x1_1 = data_csv['1_x=1'].values

        self.dic_weights = {}
        self.node_states = {} # nsh in original code

        for i, h in enumerate(dummy_header):
            cut = h.find(':')
            feature = h[0:cut]
            value_range = h[cut+1:]
            
            if feature not in self.dic_weights:
                self.node_states[feature] = 1
                self.dic_weights[feature] = {}
            else:
                self.node_states[feature] += 1
                
            self.dic_weights[feature][value_range] = {0: [x0_0[i], x1_0[i]], 1: [x0_1[i], x1_1[i]]}

        self.node_states[label_col] = 2
        
        # Generate Graph Structure
        nV = len(self.dic_weights.keys()) + 1
        self.graph_structure = generate_graph_weights(nV)
        self.header_1 = list(self.node_states.keys())

    def calculate_risk(self, patient_profile, legend):
        """
        Calculates risk for a specific patient profile.
        
        Args:
            patient_profile (dict): Dictionary of feature values (e.g., {'age': 1, 'smoker': 0})
            population_data (dict): The full dataset to compute priors/marginals.
            legend (dict): Mapping of integer states to string descriptions.
        """
        N, Nf, t, q, vf, fv = self.graph_structure
        
        # Initialize Potential Matrix (vm)
        vm = {}
        
        for f in range(1, Nf + 1):
            v = fv[f][0]
            feature_name = self.header_1[v-1]
            
            # Check if this is a weight function node (connecting factor to Disease)
            is_weight_node = (f > (len(self.header_1)-1)) and (f < (len(self.header_1)-1)*2 + 1)
            
            if is_weight_node:
                # Compute joint occurrences from population data
                # (Logic simplified for brevity - assumes population_data is processed)
                num_states = self.node_states[feature_name]
                vm[f] = np.zeros((num_states, 2))
                
                # Apply weights loaded from model
                # Note: This logic requires matching the specific 'legend' string to the weight keys
                for state_idx in range(num_states):
                    state_str = legend[feature_name][state_idx]
                    if state_str in self.dic_weights[feature_name]:
                        # Example: Loading weight for Disease=1
                        vm[f][state_idx, 1] = self.dic_weights[feature_name][state_str][1][1] 
                        # Disease=0
                        vm[f][state_idx, 0] = self.dic_weights[feature_name][state_str][0][1] 

            else:
                # Leaf node: Set patient specific evidence
                num_states = self.node_states[feature_name]
                vm[f] = np.zeros((num_states, 1))
                
                if feature_name in patient_profile:
                    fixed_val = patient_profile[feature_name]
                    vm[f][fixed_val] = 1.0 # Clamp state
                else:
                    vm[f] = np.ones((num_states, 1)) # Unobserved

        # Run Inference
        nv_dict = {i: self.node_states[self.header_1[i-1]] for i in range(1, N+1)}
        nuja0, nuaj0 = initiate_bp_messages(N, Nf, vf, fv, vm, nv_dict)
        _, _, marginals, _, _ = run_belief_propagation(N, Nf, fv, vf, nuja0, nuaj0, 1e-7, 1000, vm, nv_dict)

        # Extract Risk Score
        # Assumes the last node is the Disease Node
        disease_node_idx = N 
        risk_score = marginals[disease_node_idx][1] # Probability of State 1 (Disease)
        
        return float(risk_score)