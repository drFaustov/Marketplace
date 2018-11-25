from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///party_of_2.db'
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

from marketplace import routes
