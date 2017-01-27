## -*- coding: utf-8 -*-
## project/app/settings/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, BooleanField, IntegerField
from app.admin.services import select2Widget, select2MultipleWidget, requiredValidator, emailValidator, messageText

class companyForm(FlaskForm):
    VATNumber = StringField(messageText('VATNumberLabel'), validators=[requiredValidator])
    companyName = StringField(messageText('companyNameLabel'), validators=[requiredValidator])
    addr = StringField(messageText('addrLabel'))
    addr2 = StringField(messageText('addr2Label'))
    postcode = StringField(messageText('postcodeLabel'))
    city = StringField(messageText('cityLabel'))
    contactName = SelectField(messageText('usernameLabel'), choices=[], widget=select2Widget(), validators=[requiredValidator])
    email = StringField(messageText('emailLabel'), validators=[requiredValidator, emailValidator])
    phone = IntegerField(messageText('phoneLabel'))
