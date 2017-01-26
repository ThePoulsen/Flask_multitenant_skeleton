## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, validators
from app.admin.services import emailValidator, requiredValidator, messageText

class changePasswordForm(FlaskForm):
    password = PasswordField(messageText('passwordLabel'), validators=[requiredValidator])
