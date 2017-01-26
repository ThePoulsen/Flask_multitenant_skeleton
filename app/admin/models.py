## -*- coding: utf-8 -*-
## project/app/admin/models.py

from app import db

class message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    title = db.Column(db.String(255), unique=True)
    parent = db.relationship("message", remote_side=[id])

    messageGroup_id = db.Column(db.Integer, db.ForeignKey('messageGroup.id'))

class messageGroup(db.Model):
    __tablename__ = 'messageGroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

class messageBody(db.Model):
    __tablename__ = 'messageBody'
    __table_args__ = (db.UniqueConstraint('message_id', 'language_id', name='_message_language'),)

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

class language(db.Model):
    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    abbr = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
