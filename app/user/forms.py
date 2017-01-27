## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, validators, BooleanField, SelectMultipleField
from app.admin.services import emailValidator, requiredValidator, messageText, select2MultipleWidget

class changePasswordForm(FlaskForm):
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])

class userForm(FlaskForm):
    name = StringField(messageText('usernameLabel'), validators=[requiredValidator])
    email = StringField(messageText('emailLabel'), validators=[requiredValidator, emailValidator])
    phone = StringField(messageText('phoneLabel'))
    isAdmin = BooleanField(messageText('isAdminLabel'))
    isSuperuser = BooleanField(messageText('isSuLabel'))
    groups = SelectMultipleField(messageText('groupsLabel'), choices=[], widget=select2MultipleWidget())

class groupForm(FlaskForm):
    name = StringField(messageText('groupLabel'), [requiredValidator])
    desc = TextAreaField(messageText('descLabel'), [requiredValidator])
    users = SelectMultipleField(messageText('usersLabel'), validators=[], choices=[], widget=select2MultipleWidget())
