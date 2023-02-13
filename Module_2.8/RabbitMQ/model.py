from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, BooleanField

from datetime import datetime


class Contact(Document):
    fullname = StringField(unique=True, required=True)
    email = StringField(required=True)
    operation_date = DateTimeField(default=datetime.now().isoformat())
    email_sent = BooleanField(default=False)
