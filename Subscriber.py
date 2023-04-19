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


# Set up MongoDB
mongo_client = mongo_connection()

# Set up SQLite
sqlite_conn, sqlite_cursor = sqlite_connection()


credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                           port,
                                           virtualhost,
                                           credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

#set the appropirate channel here, there could be more than one, requiring seperate instances.
exchange_name = 'Danie_Sandesh_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = "#"

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    data = json.loads(body)

    if method.routing_key == "patient_list":
        insert_testing_data(data)
        for d in data:
            print("*Python Class*")
            print("\ttesting_id: " + str(test['testing_id']))
            print("\tpatient_name: " + str(test['patient_name']))
            print("\tpatient_mrn: " + str(test['patient_mrn']))
            print("\tpatient_zipcode: " + str(test['patient_zipcode']))
            print("\tpatient_status: " + str(test['patient_status']))
            print("\tcontact_list: " + str(test['contact_list']))
            print("\tevent_list: " + str(test['event_list']))

    elif method.routing_key == "hospital_list":
        insert_hospital_data(data, sqlite_conn, sqlite_cursor)
        for d in data:
            print("*Python Class*")
            print("\ttesting_id: " + str(test['testing_id']))
            print("\tpatient_name: " + str(test['patient_name']))
            print("\tpatient_mrn: " + str(test['patient_mrn']))
            print("\tpatient_zipcode: " + str(test['patient_zipcode']))
            print("\tpatient_status: " + str(test['patient_status']))
            print("\tcontact_list: " + str(test['contact_list']))
            print("\tevent_list: " + str(test['event_list']))

    elif method.routing_key == "vax_list":
        insert_vaccination_data(data)
        for d in data:
            print("*Python Class*")
            print("\ttesting_id: " + str(test['testing_id']))
            print("\tpatient_name: " + str(test['patient_name']))
            print("\tpatient_mrn: " + str(test['patient_mrn']))
            print("\tpatient_zipcode: " + str(test['patient_zipcode']))
            print("\tpatient_status: " + str(test['patient_status']))
            print("\tcontact_list: " + str(test['contact_list']))
            print("\tevent_list: " + str(test['event_list']))




channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()