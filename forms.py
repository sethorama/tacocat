from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import *


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class TacoForm(Form):
    protein = StringField(
        'Protein',
        validators=[
            DataRequired()
        ])
    shell = StringField(
        'Shell',
        validators=[
            DataRequired()
        ])
    cheese = StringField(
        'Cheese',
        validators=[
            DataRequired()
        ])
    extras = StringField(
        'Extras',
        validators=[
            DataRequired()
        ])
