import streamlit as st
from risk_model import AMDRiskModel
from utils import legend, DISPLAY_NAMES

# --- Configuration ---
RESULTS_DIR = 'Influence Scores/' 
TARGET_LABEL = 'ASMULTIMODALORRES_E1_C18'

# --- DEFAULT PATIENT PROFILE ---
DEFAULT_PROFILE = {
    'age_E0': 0, 
    'bmi_E0': 1, 
    'medSCORE_Mira': 0,
    'stage_before': 1, 
    'sex_E1_C1': 1, 
    'ls_smoker_E0': 0,
    'diabetes_E0': 0, 
    'lh_phy_exercise_E1_C6': 0,
    'arterial_hypertension_E0': 1, 
    'rs35292876': 1, 'rs8135665': 0, 'rs10922109': 0, 'rs10490924': 0,
    'rs1626340': 1, 'rs429608': 0, 'rs2230199': 0, 'rs3750846': 0, 'rs570618': 2
}

# --- MAPPING: V0 (History) -> V1 (Future) ---
V0_TO_V1_MAP = {
    'age_E0': 'age_E1',
    'bmi_E0': 'bmi_E1_C1',
    'ls_smoker_E0': 'ls_smoker_E1_C6',
    'diabetes_E0': 'diabetes_E1_C3',
    'arterial_hypertension_E0': 'arterial_hypertension_E1_C3'
}

# --- SIMULATION VARIABLES ---
SIMULATION_VARIABLES = [
    'bmi_E1_C1', 
    'ls_smoker_E1_C6', 
    'diabetes_E1_C3', 
    'arterial_hypertension_E1_C3',
    'medSCORE_Mira',           
    'lh_phy_exercise_E1_C6'    
]

# --- CUTOFF DISPLAY MAPPING ---
# Translates the integer cutoff to the specific text you requested
CUTOFF_DISPLAY_MAP = {
    0: "1-4",
    1: "2-4",
    2: "3-4",
    3: "4"
}

# --- HELPER: 2 SIGNIFICANT DIGITS ---
def format_risk(val):
    if val == 0: return "0.00"
    if abs(val) >= 0.1: return f"{val:.2f}"
    else: return f"{val:.2g}"

def main():
    st.set_page_config(page_title="AMD Risk Calculator", layout="wide")
    st.title("AMD Risk Score Calculator")
    #st.markdown("Use the sidebar to set **Genetics & History**. Set the **Target Age** below to calculate risk.")

    # 1. Initialize Model
    @st.cache_resource
    def get_model():
        default_cutoff = DEFAULT_PROFILE.get('stage_before', 3)
        model = AMDRiskModel(results_path=RESULTS_DIR, amd_cutoff=default_cutoff) 
        model.load_model(label_col=TARGET_LABEL)
        return model

    model = get_model()

    # --- SIDEBAR: GENETICS & HISTORY (V0) ---
    st.sidebar.header("1. Patient Profile")
    st.sidebar.markdown("Set Genetic and Baseline ($V_0$) values.")
    
    user_profile = {}

    # 1A. Handle Stage
    stage_options = legend['stage_before']
    stage_vals = list(stage_options.values())
    
    def_stage_id = DEFAULT_PROFILE.get('stage_before', 0)
    def_stage_lbl = stage_options.get(def_stage_id, '0')
    stage_idx = stage_vals.index(def_stage_lbl) if def_stage_lbl in stage_vals else 0
    
    lbl_stage = DISPLAY_NAMES.get('stage_before', 'stage_before')
    stage_label = st.sidebar.selectbox(lbl_stage, stage_vals, index=stage_idx)
    
    stage_id = [k for k, v in stage_options.items() if v == stage_label][0]
    user_profile['stage_before'] = stage_id
    model.amd_cutoff = stage_id

    # 1B. Handle Features
    v0_keys = list(V0_TO_V1_MAP.keys())
    
    for feature, mapping in legend.items():
        if feature in ['ASMULTIMODALORRES_E1_C18', 'stage_before']: continue
        
        is_genetic = feature.startswith('rs')
        is_gender = feature == 'sex_E1_C1'
        is_v0_history = feature in v0_keys
        is_independent_lifestyle = feature in ['medSCORE_Mira', 'lh_phy_exercise_E1_C6']
        
        if not (is_genetic or is_gender or is_v0_history or is_independent_lifestyle):
            continue

        ui_mapping = mapping.copy()
        if -1 in ui_mapping: ui_mapping[-1] = "Unknown"
        options = list(ui_mapping.values())
        
        default_idx = 0
        if feature in DEFAULT_PROFILE:
            val = DEFAULT_PROFILE[feature]
            if val in ui_mapping:
                lbl = ui_mapping[val]
                if lbl in options: default_idx = options.index(lbl)

        display_label = DISPLAY_NAMES.get(feature, feature)
        selected = st.sidebar.selectbox(display_label, options, index=default_idx)
        
        label_to_id = {v: k for k, v in ui_mapping.items()}
        user_profile[feature] = label_to_id[selected]

    # --- AUTO-ASSIGNMENT (Copy V0 -> V1) ---
    for v0_key, v1_key in V0_TO_V1_MAP.items():
        if v0_key in user_profile:
            user_profile[v1_key] = user_profile[v0_key]

    # --- MAIN PANEL ---

    # 2. PREDICTION HORIZON
    st.subheader("2. Risk Assessment Horizon")
    #st.markdown("Select the **Target Age** ($V_1$) for the risk assessment.")
    
    age_feature = 'age_E1'
    mapping = legend[age_feature]
    ui_mapping = mapping.copy()
    if -1 in ui_mapping: ui_mapping[-1] = "Unknown"
    options = list(ui_mapping.values())
    
    # Smart Default Age Logic
    current_v0_age = user_profile.get('age_E0', 0)
    valid_age_ids = sorted([k for k in mapping.keys() if k != -1])
    default_v1_age = current_v0_age 
    if current_v0_age in valid_age_ids:
        idx_in_list = valid_age_ids.index(current_v0_age)
        if idx_in_list + 1 < len(valid_age_ids):
            default_v1_age = valid_age_ids[idx_in_list + 1]
    
    default_lbl = ui_mapping.get(default_v1_age, options[0])
    try:
        age_idx = options.index(default_lbl)
    except ValueError:
        age_idx = 0

    display_name = DISPLAY_NAMES.get(age_feature, age_feature)
    selected_age = st.selectbox(display_name, options, index=age_idx)
    
    label_to_id = {v: k for k, v in ui_mapping.items()}
    user_profile[age_feature] = label_to_id[selected_age]

    st.divider()

    # 3. RESULTS & SIMULATION
    baseline_score = model.calculate_risk(user_profile, legend)
    
    col_base, col_sim = st.columns([1, 2])
    
    with col_base:
        st.subheader("Current Risk")
        
        # --- CUTOFF DISPLAY LOGIC ---
        # Get the friendly name from the map, or fallback to the number if not found
        cutoff_text = CUTOFF_DISPLAY_MAP.get(model.amd_cutoff, str(model.amd_cutoff))
        #st.markdown(f"**For transitioning to stages** {cutoff_text}")
        # ----------------------------
        
        formatted_score = format_risk(baseline_score)
        st.metric(
            label=f"**For transitioning to stages** {cutoff_text}", 
            value=formatted_score,
            help=f"Assuming the patient profile is unchanged."
        )

    with col_sim:
        st.subheader("3. Risk After Changes")
        st.markdown("Adjust future changes.")
        
        with st.form("simulation_form"):
            cf_profile = user_profile.copy()
            cols_sim = st.columns(3)
            
            for i, feature in enumerate(SIMULATION_VARIABLES):
                with cols_sim[i % 3]:
                    mapping = legend[feature]
                    ui_mapping = mapping.copy()
                    if -1 in ui_mapping: ui_mapping[-1] = "Unknown"
                    options = list(ui_mapping.values())
                    
                    current_id = user_profile.get(feature, 0)
                    current_lbl = ui_mapping.get(current_id, options[0])
                    try:
                        idx = options.index(current_lbl)
                    except ValueError:
                        idx = 0
                    
                    display_name = DISPLAY_NAMES.get(feature, feature)
                    new_label = st.selectbox(f"Target {display_name}", options, index=idx)
                    
                    label_to_id = {v: k for k, v in ui_mapping.items()}
                    cf_profile[feature] = label_to_id[new_label]
            
            st.markdown("")
            submit = st.form_submit_button("Run Simulation", type="primary")

        if submit:
            sim_score = model.calculate_risk(cf_profile, legend)
            delta = sim_score - baseline_score
            
            f_sim_score = format_risk(sim_score)
            f_delta = format_risk(delta)
            
            st.divider()
            r_col1, r_col2 = st.columns(2)
            
            with r_col1:
                st.metric(
                    label=f"**For transitioning to stages** {cutoff_text}", 
                    value=f_sim_score, 
                    delta=f_delta,
                    delta_color="inverse"
                )
            
            with r_col2:
                abs_delta = format_risk(abs(delta))
                if delta < -0.001: 
                    st.success(f"📉 This scenario reduces risk by **{abs_delta}**.")
                elif delta > 0.001:
                    st.warning(f"📈 This scenario increases risk by **{abs_delta}**.")
                else:
                    st.info("No significant change in risk.")

if __name__ == "__main__":
    main()