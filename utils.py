legend = {
    'age_E1': {-1: '[-1,54[', 0: '[54,70[', 1: '[70,75[', 2: '[75,90['},
    'age_E0': {-1: '[-1,54[', 0: '[54,70[', 1: '[70,75[', 2: '[75,90['},
    'bmi_E0': {-1: '[-1,0[', 0: '[0,25[', 1: '[25,49['},
    'bmi_E1_C1': {-1: '[-1,0[', 0: '[0,25[', 1: '[25,49['},
    'medSCORE_Mira': {-1: '[-1,0[', 0: '[0,6[', 1: '[6,10['},
    'ASMULTIMODALORRES_E1_C18': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'},
    'stage_before': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'},
    'ls_smoker_E1_C6': {-1: -1, 0: 'Non-smoker', 1: 'Smoker'},
    'sex_E1_C1': {0: 'Male', 1: 'Female'},
    'ls_smoker_E0': {0: 'Non-smoker', 1: 'Smoker'},
    'diabetes_E1_C3': {-1: -1, 0: 'No', 1: 'Yes'},
    'diabetes_E0': {-1: -1, 0: 'No', 1: 'Yes'},
    'lh_phy_exercise_E1_C6': {-1: -1, 0: 'No', 1: 'Yes'},
    'arterial_hypertension_E0': {-1: -1, 0: 'No', 1: 'Yes'},
    'arterial_hypertension_E1_C3': {-1: -1, 0: 'No', 1: 'Yes'},
    'rs35292876': {0: '0', 1: '1', -1: '-1'},
    'rs8135665': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs10922109': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs10490924': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs1626340': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs429608': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs2230199': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs3750846': {0: '0', 1: '1', 2: '2', -1: '-1'},
    'rs570618': {0: '0', 1: '1', 2: '2', -1: '-1'}
}

DISPLAY_NAMES = {
    # --- Genetics (Formatted with Latex) ---
    'rs35292876': r'$CFH_{rs35292876}$',
    'rs8135665': r'$SLC16A8_{rs8135665}$',
    'rs10490924': r'$ARMS2_{rs10490924}$',
    'rs1626340': r'$TGFBR1_{rs1626340}$',
    'rs2230199': r'$C3_{rs2230199}$',
    'rs3750846': r'$ARMS2 / HTRA1_{rs3750846}$',
    'rs570618': r'$CFH_{rs570618}$',
    'rs429608': r'$C2 / CFB / SKIV2L_{rs429608}$',
    'rs10922109': r'$CFH_{rs10922109}$',

    # --- Clinical / Demographics ---
    'stage_before': r'$AMD_{V0}$ (Baseline Stage)',
    
    'ls_smoker_E1_C6': r'Smoking Status ($V_1$)',
    'ls_smoker_E0': r'Smoking Status ($V_0$)',
    
    'sex_E1_C1': 'Gender',
    
    'diabetes_E1_C3': r'Diabetes ($V_1$)',
    'diabetes_E0': r'Diabetes ($V_0$)',
    
    'arterial_hypertension_E0': r'Arterial Hypertension ($V_0$)',
    'arterial_hypertension_E1_C3': r'Arterial Hypertension ($V_1$)',
    
    'lh_phy_exercise_E1_C6': 'Physical Exercise',
    
    'age_E1': r'$Age_{V1}$',
    'age_E0': r'$Age_{V0}$',
    
    'bmi_E0': r'$bmi_{V0}$',
    'bmi_E1_C1': r'$bmi_{V1}$',
    
    'medSCORE_Mira': 'Mediterranean Diet Score',
    
    'ASMULTIMODALORRES_E1_C18': r'$AMD_{V1}$ (Outcome)'
}