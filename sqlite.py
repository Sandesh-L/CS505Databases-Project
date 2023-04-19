import sqlite3

def sqlite_connection():
    sqlite_conn = sqlite3.connect("covid_hospitals.db")
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS hospital_data
                             (hospital_id INTEGER, patient_mrn TEXT, patient_name TEXT, patient_status INTEGER)''')
    return sqlite_conn, sqlite_cursor

def insert_hospital_data(hospital_data, sqlite_conn, sqlite_cursor):
    sqlite_cursor.executemany("INSERT INTO hospital_data VALUES (?, ?, ?, ?)",
                              [(item['hospital_id'], item['patient_mrn'], item['patient_name'], item['patient_status']) for item in hospital_data])
    sqlite_conn.commit()

def close_sqlite_connection(sqlite_conn):
    sqlite_conn.close()
