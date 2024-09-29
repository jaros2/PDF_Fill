from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.db'
app.config['SECRET_KEY'] = 'youwillneverguess'
db = SQLAlchemy(app)

from app import routes, models