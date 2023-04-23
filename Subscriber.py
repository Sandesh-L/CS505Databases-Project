#!/usr/bin/env python
import pika
import sys
import json
from controller import process_data
# from controllers import mongo
# from './controllers/mongo' import mongo_connection, insert_testing_data, insert_vaccination_data, close_mongo_connection

# Set the connection parameters to connect to rabbit-server1 on port 5672
username = 'team_11'
password = 'myPassCS505'
hostname = 'vbu231.cs.uky.edu'
virtualhost = '11'
port = 9099


# # Set up MongoDB
# mongo_client = mongo_connection()

# # Set up SQLite
# sqlite_conn, sqlite_cursor = sqlite_connection()


credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                           9099,
                                           virtualhost,
                                           credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
binding_keys = "#"        

result = channel.queue_declare('',exclusive=True)

queue_name = result.method.queue

print(f"\n \n {queue_name} \n\n")

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

exchanges = ['patient_data', 'hospital_data', 'vax_data']
routing_keys = ['patient.info', 'hospital.info', 'vax.info']

for exchange, routing_key in zip(exchanges, routing_keys):
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=routing_key)


print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.exchange, body))
    # print("----------------------------\n")
    # print(f"{method.routing_keys}")
    # print("----------------------------\n")

    # print(f"{dir(method)}")

    data = json.loads(body)

    for record in data:
        if 'vaccination_id' in record:
            print("*Python Class*")
            print("Vax list")
            print("\t vaccination_id: " + str(record['vaccination_id']))
            print("\t patient_name: " + str(record['patient_name']))
            print("\t patient_mrn: " + str(record['patient_mrn']))
            print("----------------------------\n"*3)
            patients = process_data.verify_patient_data()
        

        elif 'hospital_id' in record:
            print("*Python Class*")
            print("Hospital list")
            print("\thospital_id: " + str(record['hospital_id']))
            print("\tpatient_name: " + str(record['patient_name']))
            print("\tpatient_mrn: " + str(record['patient_mrn']))
            print("\tpatient_status: " + str(record['patient_status']))
            print("----------------------------\n"*3)
        elif 'testing_id' in record:
            print("*Python Class*")
            print("Patient list")
            print("\t testing_id: " + str(record['testing_id']))
            print("\t patient_name: " + str(record['patient_name']))
            print("\t patient_mrn: " + str(record['patient_mrn']))
            print("\t patient_zipcode: " + str(record['patient_zipcode']))
            print("\t patient_status: " + str(record['patient_status']))
            print("\t contact_list: " + str(record['contact_list']))
            print("\t event_list: " + str(record['event_list']))
            print("----------------------------\n"*3)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# close_sqlite_connection(sqlite_conn)
# close_mongo_connection(mongo_client)