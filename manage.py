#!/usr/bin/python
# -*- coding: utf-8 -*-
# project/manage.py

from flask_script import Server,Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from data import createMessages, deleteData

# Enable flask-migrate
migrate = Migrate(app, db)

# Enable flask-manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def messages():
    createMessages()

@manager.command
def delete():
    deleteData()

if __name__ == '__main__':
    manager.run()
