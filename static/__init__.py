from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY']= "1234ffff"

db = SQLAlchemy(app)

from static import routes