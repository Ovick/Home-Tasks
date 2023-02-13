import pika
from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import json

import connect

client_mongo = MongoClient(connect.connection_string)
db = client_mongo.ContactsDB

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


def send_email(email_address: str):
    return f"Sent message to {email_address}"


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact = db.contact.find_one({"_id": ObjectId(message["id"])})
    print(f" [x] Received contact {contact['fullname']}")
    print(f" [x] {send_email(contact['email'])}")
    db.contact.update_one({"_id": ObjectId(message["id"])}, {
                          "$set": {"email_sent": True}})
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
