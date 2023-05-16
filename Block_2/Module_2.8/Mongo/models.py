from mongoengine import EmbeddedDocument, Document, CASCADE
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField(unique=True, required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Tag(EmbeddedDocument):
    name = StringField(required=True)


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(unique=True, required=True)
