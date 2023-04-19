#!/usr/bin/env python
import pika
import sys
import json

from mongo import mongo_connection, insert_testing_data, insert_vaccination_data, close_mongo_connection
from sqlite import sqlite_connection, insert_hospital_data, close_sqlite_connection

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

for binding_key in binding_keys:
    for ex in ['patient_list', 'hospital_list', 'vax_list']:
        channel.exchange_declare(exchange=ex, exchange_type='topic')
        channel.queue_bind(
            exchange=ex, queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    print("----------------------------\n")
    # print(f"{method.exchange}")
    # print(f"{dir(method)}")
    
    data = json.loads(body)

    if method.exchange == "patient_list":
        # insert_testing_data(data)
        # print("Data: ", data)
        for d in data:
            print("*Python Class*")
            print("Patient list")
            print("\ttesting_id: " + str(d['testing_id']))
            print("\tpatient_name: " + str(d['patient_name']))
            print("\tpatient_mrn: " + str(d['patient_mrn']))
            print("\tpatient_zipcode: " + str(d['patient_zipcode']))
            print("\tpatient_status: " + str(d['patient_status']))
            print("\tcontact_list: " + str(d['contact_list']))
            print("\tevent_list: " + str(d['event_list']))
        print("----------------------------\n"*3)


    elif method.exchange == "hospital_list":
        # insert_hospital_data(data, sqlite_conn, sqlite_cursor)
        # print("Data: ", data)
        for d in data:
            print("*Python Class*")
            print("Hospital list")
            print("\thospital_id: " + str(d['hospital_id']))
            print("\tpatient_name: " + str(d['patient_name']))
            print("\tpatient_mrn: " + str(d['patient_mrn']))
            print("\tpatient_status: " + str(d['patient_status']))
        print("----------------------------\n"*3)
        

    elif method.exchange == "vax_list":
        # insert_vaccination_data(data)
        # print("Data: ", data)
        for d in data:
            print("*Python Class*")
            print("Vax list")
            print("\tvaccination_id: " + str(d['vaccination_id']))
            print("\tpatient_name: " + str(d['patient_name']))
            print("\tpatient_mrn: " + str(d['patient_mrn']))
        print("----------------------------\n"*3)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# close_sqlite_connection(sqlite_conn)
# close_mongo_connection(mongo_client)