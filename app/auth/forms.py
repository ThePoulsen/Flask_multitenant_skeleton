## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, validators
from app.admin.services import emailValidator, requiredValidator, messageText

class setPasswordForm(FlaskForm):
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])

class changePasswordForm(FlaskForm):
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])

class loginForm(FlaskForm):
    regNo = StringField(messageText('VATNumberLabel'), validators=[requiredValidator])
    email = StringField(messageText('emailLabel'), validators=[requiredValidator, emailValidator])
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])

class registerForm(FlaskForm):
    regNo = StringField(messageText('VATNumberLabel'), id='regNo', validators=[requiredValidator])
    companyName = StringField(messageText('companyNameLabel'), id='companyName', validators=[requiredValidator])
    userName = StringField(messageText('usernameLabel'), validators=[requiredValidator])
    email = StringField(messageText('emailLabel'), validators=[requiredValidator, emailValidator])
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])
