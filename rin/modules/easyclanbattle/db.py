from peewee import *

db = SqliteDatabase('res\battlelog.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.