

def verify_patient_data(patient_data):
    """
    patient data must be in it's original json format
    """
    keys = ['testing_id', 'patient_name', 'patient_mrn', 'patient_zipcode', 'patient_status', 'contact_list', 'event_list']

    for key in keys:
        if key not in patient_data:
            print(f"{key} not in patient_data")
            return 0
    return 1

