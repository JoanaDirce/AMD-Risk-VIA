import pandas as pd
from risk_model import AMDRiskModel
from utils import legend, DISPLAY_NAMES


# --- Configuration ---

RESULTS_DIR = 'Influence Scores/'
TARGET_LABEL = 'ASMULTIMODALORRES_E1_C18'



# Define the patient profile (IDs corresponding to states)

patient_profile = {'age_E1': 1,
    'age_E0': 0,
    'bmi_E0': 1,
    'bmi_E1_C1': 1,
    'medSCORE_Mira': 0,
    'stage_before': 1,
    'ls_smoker_E1_C6': 0,
    'sex_E1_C1': 1,
    'ls_smoker_E0': 0,
    'diabetes_E1_C3': 0,
    'diabetes_E0': 0,
    'lh_phy_exercise_E1_C6': 0,
    'arterial_hypertension_E0': 1,
    'arterial_hypertension_E1_C3': 1,
    'rs35292876': 1,
    'rs8135665': 0,
    'rs10922109': 0,
    'rs10490924': 0,
    'rs1626340': 1,
    'rs429608': 0,
    'rs2230199': 0,
    'rs3750846': 0,
    'rs570618': 2
}



def main():

    # 1. Initialize Model
    print("Initializing model...")
    model = AMDRiskModel(results_path=RESULTS_DIR, amd_cutoff=patient_profile['stage_before'])
    model.load_model(label_col=TARGET_LABEL)
    
    # 2. Compute Risk Score
    print("Computing risk score...")
    score = model.calculate_risk(patient_profile, legend)
    
    print(f"\n--- Results ---")
    print(f"Patient Profile: {patient_profile}")
    print(f"Calculated AMD Risk Score: {score:.4f}")
    
    # 3. Counterfactual Example (What if it did exercise?)
    patient_profile['lh_phy_exercise_E1_C6'] = 1
    score_improved = model.calculate_risk(patient_profile, legend)
    print(f"Risk Score if she did exercise: {score_improved:.4f}")



if __name__ == "__main__":
    main()