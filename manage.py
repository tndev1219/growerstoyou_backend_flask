import os
import sys
import hashlib
import configparser

from instafarm import app, db
from instafarm.models import model
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

_basepath = os.path.dirname(__file__)

_config = configparser.ConfigParser()
_config.read(os.path.join(_basepath, 'env.ini'))

server_host = ''
server_port = ''

if 'server' in _config:
    server_host = _config['server']['host']
    server_port = _config['server']['port']

server = Server(host=server_host, port=server_port)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)

def createDB():
    model.db.create_all()

def createAdmin():
    try:
        email    = _config['admin']['email']
        fname    = _config['admin']['fname']
        lname    = _config['admin']['lname']
        password = _config['admin']['password']

        if not model.User.check_exist_by_email(email):
            password = hashlib.md5(password.encode()).hexdigest()
            user = model.User(email=email, password=password, role=0, fname=fname, lname=lname)
            model.add(user)
            model.commit()
            print('Create admin success.')
        else:
            print('Admin already exist.')
            
    except:
        print('Create admin failed.')
        pass

if __name__ == '__main__':    
    if sys.argv[1] == 'create_db':
        createDB()
    elif sys.argv[1] == 'create_admin':
        createAdmin()
    else:
        manager.run()