from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)
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
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists.")


class Taco(Model):
    user = ForeignKeyField(
        rel_model=User,
        related_name='tacos')
    protein = CharField()
    shell = CharField()
    cheese = CharField()
    extras = CharField()
        
    class Meta:
        database = DATABASE

    @classmethod
    def create_taco(cls, user, protein, shell, cheese, extras):
        cls.create(
            user=user,
            protein=protein,
            shell=shell,
            cheese=cheese,
            extras=extras)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()