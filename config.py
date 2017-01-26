# project/config.py
import os
import vars

# System environments set for security purposes
mail                                = os.environ['mail']
mailPass                            = os.environ['mailPass'].replace("'","")
secretKey                           = os.environ['secretKey']
db                                  = os.environ['db']

# Flask settings
SECRET_KEY                          = secretKey
SQLALCHEMY_DATABASE_URI             = db
SQLALCHEMY_TRACK_MODIFICATIONS      = False
JSON_AS_ASCII                       = False #unicode settings
TEMPLATES_AUTO_RELOAD               = True

# Flask mail settings
MAIL_USERNAME                       = mail
MAIL_PASSWORD                       = mailPass
MAIL_DEFAULT_SENDER                 = '"MyApp" <noreply@address.dk>'
MAIL_SERVER                         = 'smtp.gmail.com'
MAIL_PORT                           = 465
MAIL_USE_SSL                        = True

# Bcrypt settings
BCRYPT_LOG_ROUNDS                   = 12

# Flask-htmlmin settings
MINIFY_PAGE                         = True

# Flask-sijax
path = os.path.join('.', os.path.dirname(__file__), 'app/static/js/sijax/')
SIJAX_STATIC_PATH = path
SIJAX_JSON_URI = 'app/static/js/sijax/json2.js'
