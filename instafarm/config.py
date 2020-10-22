import os
import configparser

_basepath = os.path.dirname(os.path.dirname(__file__))

_config = configparser.ConfigParser()
_config.read(os.path.join(_basepath, 'env.ini'))

db_path = 'sqlite:///' + os.path.join(_basepath, 'instafarm.sqlite3')

if _config['database']['db_url']:
    db_path = _config['database']['db_url']
    print(db_path)

config ={
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SECRET_KEY': "random string",
    'SQLALCHEMY_DATABASE_URI': db_path
}

if 'mail' in _config:
    config['MAIL_SERVER'] = _config['mail']['server']
    config['MAIL_PORT']   = _config['mail']['port']
    config['MAIL_USERNAME'] = _config['mail']['username']
    config['MAIL_PASSWORD'] = _config['mail']['password']
    config['MAIL_USE_TLS'] = False
    config['MAIL_USE_SSL'] = False
    config['MAIL_DEFAULT_SENDER'] = _config['mail']['sender']
    config['SECURITY_EMAIL_SENDER '] = _config['mail']['sender']
    config['MAIL_ASCII_ATTACHMENTS'] = True
    config['DEBUG'] = True

config['UPLOAD_FOLDER']      = os.path.join(_basepath, 'uploads')
config['ALLOWED_EXTENTIONS'] = set(['png', 'jpeg', 'jpg', 'gif'])
config['STRIP_SECRET_KEY']      = _config['payment']['key_secret']
config['STRIP_PUBLISHABLE_KEY'] = _config['payment']['key_publishable']



