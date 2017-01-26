## -*- coding: utf-8 -*-
## project/app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from services import requiredValidator, select2Widget, messageText

class messageGroupForm(FlaskForm):
    messageGroup = StringField(messageText('msgGrpLabel'), [requiredValidator])

class messageForm(FlaskForm):
    title = StringField(messageText('messageLabel'), [requiredValidator])
    messageGroup = SelectField(messageText('msgGrpLabel'), choices=[], validators=[requiredValidator], widget=select2Widget())
    dk_text = TextAreaField(messageText('dkTextLabel'), [requiredValidator])
    en_text = TextAreaField(messageText('enTextLabel'), [requiredValidator])
    parent = SelectField(messageText('parentLabel'), validators=[], choices=[], widget=select2Widget())
