#!/usr/bin/python
# -*- coding: utf-8 -*-
# project/data.py

from app import db
from app.admin.models import messageGroup, language, message, messageBody
from datetime import datetime
import csv

def createMessages():
    Languages = [['Dansk','dk'],['English','en']]
    for r in Languages:
        db.session.add(language(name=r[0], abbr=r[1]))

    messageGroups = ['error', 'success', 'info', 'warning', 'validate', 'column', 'view', 'title', 'label']
    for r in messageGroups:
        if not r in [row.name for row in messageGroup.query.all()]:
            db.session.add(messageGroup(name=r))

    messageCSV = open('messages.csv', 'rb')
    reader = csv.reader(messageCSV, delimiter=';')
    reader.next()

    for r in reader:
        msgGrp = messageGroup.query.filter_by(name=r[1]).first()
        if not r[0] in [row.title for row in message.query.all()]:
            try:
                parent = message.query.filter_by(title=r[4]).first()
                msg = message(title=r[0],
                              messageGroup_id=msgGrp.id,
                              parent_id=parent.id)
                db.session.add(msg)
            except:
                msg = message(title=r[0],
                              messageGroup_id=msgGrp.id)
                db.session.add(msg)
            dk = language.query.filter_by(abbr='dk').first()
            en = language.query.filter_by(abbr='en').first()
            dkMsgBody = messageBody(message_id=msg.id, language_id=dk.id, text = r[2])
            db.session.add(dkMsgBody)
            enMsgBody = messageBody(message_id=msg.id, language_id=en.id, text = r[3])
            db.session.add(enMsgBody)
    db.session.commit()

def deleteData():
    pass
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
