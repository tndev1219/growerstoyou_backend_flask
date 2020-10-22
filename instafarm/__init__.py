from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from instafarm.config import config


app = Flask(__name__)
CORS(app)

app.config.update(config)
app.environment = 'development'
app.debug = True

db = SQLAlchemy(app)

from instafarm.viewset import apis
