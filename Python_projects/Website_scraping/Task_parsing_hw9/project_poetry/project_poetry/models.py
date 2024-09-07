from mongoengine import Document, ListField, StringField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    author = StringField(required=True)
    quote = StringField(required=True)
    tags = ListField(StringField())

