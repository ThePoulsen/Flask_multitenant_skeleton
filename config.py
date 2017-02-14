# project/config.py
import os
import vars

# Flask settings
SECRET_KEY                          = os.environ['secretKey']
SQLALCHEMY_DATABASE_URI             = os.environ['db']
SQLALCHEMY_TRACK_MODIFICATIONS      = False
JSON_AS_ASCII                       = False #unicode settings
TEMPLATES_AUTO_RELOAD               = True

# Flask mail settings
MAIL_USERNAME                       = os.environ['mail']
MAIL_PASSWORD                       = os.environ['mailPass']
MAIL_DEFAULT_SENDER                 = os.environ['mailSender']
MAIL_SERVER                         = os.environ['mailServer']
MAIL_PORT                           = os.environ['mailPort']
MAIL_USE_SSL                        = os.environ['mailSSL']

# Bcrypt settings
BCRYPT_LOG_ROUNDS                   = int(os.environ['BCRYPT_LOG_ROUNDS'])

# Flask-htmlmin settings
MINIFY_PAGE                         = True

# Flask-sijax
path = os.path.join('.', os.path.dirname(__file__), 'app/static/js/sijax/')
SIJAX_STATIC_PATH = path
SIJAX_JSON_URI = 'app/static/js/sijax/json2.js'
