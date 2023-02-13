import pika
import faker
from pymongo import MongoClient

from random import randint
import json

import connect
from model import Contact


def generate_fake_contacts(contacts_number: int):
    fake_names = []
    fake_emails = []
    fake_data = faker.Faker()
    for _ in range(contacts_number):
        fake_names.append(fake_data.name())
    for _ in range(contacts_number):
        fake_emails.append(fake_data.email())
    return(fake_names, fake_emails)


def seed(contacts_number: int, contacts_generator):
    contacts = contacts_generator(contacts_number)
    for i in range(contacts_number):
        Contact(
            fullname=contacts[0][i],
            email=contacts[1][i]
        ).save()


def main():

    contacts_to_create = randint(3, 5)
    seed(contacts_to_create, generate_fake_contacts)

    client_mongo = MongoClient(connect.connection_string)
    db = client_mongo.ContactsDB

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='task_exchange', exchange_type='direct')
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_bind(exchange='task_exchange', queue='task_queue')

    contacts = db.contact.find({})

    for contact in contacts:
        message = {
            "id": str(contact["_id"])
        }
        channel.basic_publish(
            exchange='task_exchange',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    main()
