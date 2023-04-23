import pyorient

def orient_connection():
    # Set up the OrientDB connection
    orient_client = pyorient.OrientDB("0.0.0.0", 2424)
    user = "root"
    password = "root"

    # Connect to the OrientDB server
    client = orient_client.connect(user, password)

    return(client)


def create_contact_edges(patient_contacts):

    """
    Do not send unprocessed data here!
    patient_contacts must be a list of mrns
    """
    
    try:
        orient_client = orient_connection

        for i, patient_mrn1 in enumerate(patient_contacts):
            for patient_mrn2 in patient_contacts[i+1:]:
                query = f"CREATE EDGE Contact FROM (SELECT FROM Patient WHERE mrn = '{patient_mrn1}') TO (SELECT FROM Patient WHERE mrn = '{patient_mrn2}')"
                orient_client.command(query)
                query = f"CREATE EDGE Contact FROM (SELECT FROM Patient WHERE mrn = '{patient_mrn2}') TO (SELECT FROM Patient WHERE mrn = '{patient_mrn1}')"
                orient_client.command(query)

        orient_client.db_close()
        
    except Exception as e:
        print("\n ran into error while trying create_contact_edges: \n", e)

# Example usage with a list of patient MRNs
patient_contacts = ['MRN001', 'MRN002', 'MRN003']
create_contact_edges(patient_contacts)
