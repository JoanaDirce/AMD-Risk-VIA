import numpy as np

def generate_graph_weights(nV):
    """Generates the factor graph structure for the weighted VIA model."""
    N = nV
    t = {i: [] for i in range(1, N + 1)}
    q = {i: 0 for i in range(1, N + 1)}
    vf = {i: [] for i in range(1, N + 1)}
    
    # Initialize fv keys
    # Note: Logic preserved from original, ensuring keys cover range
    fv = {f: [] for f in range(1, (nV - 1) * 2 + 2)}

    # Feature layer
    for i in range(1, (nV - 1) + 1):
        t[i] += [nV]
        fv[i] += [i]
        fv[(nV - 1) + i] += [i, nV]
        vf[i] += [i, (nV - 1) + i]

    # Target Node (e.g., AMD)
    t[nV] += list(range(1, (nV - 1) + 1))
    fv[(nV - 1) * 2 + 1] += [nV]
    vf[nV] += list(range(nV, (nV - 1) * 2 + 1)) + [(nV - 1) * 2 + 1]

    for i in range(1, N + 1):
        q[i] = len(t[i])

    Nf = len(fv.keys())
    return N, Nf, t, q, vf, fv

def initiate_bp_messages(N, Nf, vf, fv, vm, nv):
    """Initializes Belief Propagation messages."""
    nuja0 = {}
    for i in range(1, N + 1):
        nuja0[i] = {}
        for f in vf[i]:
            nuja0[i][f] = np.ones((nv[i], 1))

    nuaj0 = {}
    for f in range(1, Nf + 1):
        nuaj0[f] = {}
        if len(fv[f]) == 1:  # Root function
            vi = fv[f][0]
            nuaj0[f][vi] = vm[f].copy()
        else:
            for i in fv[f]:
                nuaj0[f][i] = np.ones((nv[i], 1))

    return nuja0, nuaj0

def run_belief_propagation(N, Nf, fv, vf, nuja0, nuaj0, precision, max_iter, vm, nv):
    """Runs the BP algorithm until convergence."""
    n_iter = 0
    converged = False
    error = 0.0

    while (not converged) and (n_iter < max_iter):
        n_iter += 1
        
        # Message: Variable to Function
        nuja1 = _mess_variable_to_function(N, vf, nuaj0, nv)
        
        # Message: Function to Variable
        nuaj1 = _mess_function_to_variable(Nf, fv, nuja1, vm, nv)

        # Check convergence
        converged = True
        error = 0.0
        for f in range(1, Nf + 1):
            for i in fv[f]:
                diff = abs(np.sum(nuaj0[f][i] - nuaj1[f][i]))
                if diff > error:
                    error = diff
        
        if error > precision:
            converged = False
        
        nuja0 = nuja1
        nuaj0 = nuaj1

    marginals = _calculate_marginals(N, vf, nuaj0)
    return nuja0, nuaj0, marginals, n_iter, error

# --- Internal Helper Functions ---

def _mess_variable_to_function(N, vf, nuaj0, nv):
    nuja1 = {}
    for i in range(1, N + 1):
        nuja1[i] = {}
        for idx_f in range(len(vf[i])):
            f = vf[i][idx_f]
            mess = np.ones((nv[i], 1))
            for idx_b in range(len(vf[i])):
                if idx_b != idx_f:
                    b = vf[i][idx_b]
                    mess *= nuaj0[b][i].copy()
            nuja1[i][f] = mess
    return nuja1

def _mess_function_to_variable(Nf, fv, nuja1, vm, nv):
    nuaj1 = {}
    for f in range(1, Nf + 1):
        nuaj1[f] = {}
        
        # Setup state space for neighbors
        neighbors = fv[f]
        ns_dims = [nv[v] - 1 for v in neighbors]
        
        # Iterate over neighbors
        for idx_i, i in enumerate(neighbors):
            mess_f_i = np.zeros((nv[i], 1))
            
            # Sum over all combinations (simplified for readbility, 
            # ideally use itertools.product for arbitrary dimensions)
            if len(neighbors) == 1:
                 # Single node factor (prior)
                 mess_f_i = vm[f] # Simplified logic for priors
            else:
                 # For logic preservation, we keep the original combinatorial logic structure
                 # but optimized generators would be better in a future version.
                 # Using the original ss2dec/dec2ss logic helper implicitly here for brevity.
                 pass 
                 # [NOTE]: To keep this snippet short, I am preserving your logic 
                 # but recommending you import itertools in the final file 
                 # to handle combinations instead of Dec2SS.
            
            # Re-inserting the specific logic required for your Factor Graph structure:
            # (See original mess_function_to_variable_fv implementation)
            nuaj1[f][i] = _compute_message_fv(nuja1, vm, f, i, idx_i, neighbors, nv)
            
    return nuaj1

def _compute_message_fv(nuja1, vm, f, i, idx_i, neighbors, nv):
    # This encapsulates your mess_function_to_variable_fv logic
    # Re-implemented to be cleaner if needed, or keep original logic.
    # For now, let's assume strict adherence to your logic for safety.
    from itertools import product
    
    mess = np.zeros((nv[i], 1))
    ranges = [range(nv[n]) for n in neighbors]
    
    for combo in product(*ranges):
        prob = vm[f][combo].copy()
        sigma_i = combo[idx_i]
        
        aux = prob
        for idx_j, j in enumerate(neighbors):
            if idx_i != idx_j:
                sigma_j = combo[idx_j]
                aux *= nuja1[j][f][sigma_j]
        
        mess[sigma_i] += aux
    return mess

def _calculate_marginals(N, vf, nuaj0):
    marginal = {}
    for i in range(1, N + 1):
        # Start with self-message
        # Note: Your original code used nuaj0[i][i], assuming f=i exists.
        # Ensure your factor graph generation guarantees this structure.
        
        # Fallback if specific structure is not guaranteed:
        marginal_i = 1.0 
        for f in vf[i]:
            marginal_i *= nuaj0[f][i]
            
        # Normalize
        if np.sum(marginal_i) != 0:
            marginal_i /= np.sum(marginal_i)
        marginal[i] = marginal_i
    return marginal