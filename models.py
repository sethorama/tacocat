from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('tacos.db')

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE


    @classmethod
    def create_user(cls, email, password):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists.")


class Taco(Model):
    protein = CharField()
    shell = CharField()
    cheese = BooleanField(default=True)
    extras = CharField()
        
    class Meta:
        database = DATABASE

    @classmethod
    def create(self, protein, shell, cheese, extras):
        self.create(
            protein=protein,
            shell=shell,
            cheese=cheese,
            extras=extras)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()