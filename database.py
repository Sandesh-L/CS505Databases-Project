import pymongo
import sqlite3
import pyorient

# Connect to MongoDB server
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["covid_database"]

# Create collections for testing and vaccination data
testing_collection = db["testing_data"]
vaccination_collection = db["vaccination_data"]

# Connect to SQLite database
sqlite_conn = sqlite3.connect("covid_hospital_data.db")

# Create a table for hospital data if it doesn't exist
sqlite_conn.execute('''
CREATE TABLE IF NOT EXISTS hospital_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER,
    patient_name TEXT,
    patient_mrn TEXT,
    patient_status INTEGER
)
''')

# Set up the OrientDB connection
orient_client = pyorient.OrientDB("0.0.0.0", 2424)
user = "root"
password = "root"

# Connect to the OrientDB server
orient_client.connect(user, password)

# Create a new database (if it doesn't exist) and set it as the current one
database_name = "ContactTracing"
if not orient_client.db_exists(database_name, pyorient.STORAGE_TYPE_PLOCAL):
    orient_client.db_create(database_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)

orient_client.db_open(database_name, user, password)

# Define the classes and properties
# Patient class
orient_client.command("CREATE CLASS Patient IF NOT EXISTS EXTENDS V")
orient_client.command("CREATE PROPERTY Patient.mrn IF NOT EXISTS STRING")
orient_client.command("CREATE PROPERTY Patient.name IF NOT EXISTS STRING")
orient_client.command("CREATE PROPERTY Patient.zipcode IF NOT EXISTS INTEGER ")
orient_client.command("CREATE PROPERTY Patient.status IF NOT EXISTS STRING")
try:
    orient_client.command("CREATE INDEX Patient.mrn ON Patient (mrn) UNIQUE_HASH_INDEX")
except pyorient.exceptions.PyOrientIndexException as e:
    if 'com.orientechnologies.orient.core.index.OIndexException' in str(e):
        print("Index for Patient.mrn already exists, skipping index creation.")
    else:
        raise

# Event class
orient_client.command("CREATE CLASS Event IF NOT EXISTS EXTENDS V")
orient_client.command("CREATE PROPERTY Event.event_id IF NOT EXISTS STRING")
try:
    orient_client.command("CREATE INDEX Event.event_id ON Event (event_id) UNIQUE_HASH_INDEX")
except pyorient.exceptions.PyOrientIndexException as e:
    if 'com.orientechnologies.orient.core.index.OIndexException' in str(e):
        print("Index for Event.event_id already exists, skipping index creation.")
    else:
        raise

# Close the connection
orient_client.db_close()
