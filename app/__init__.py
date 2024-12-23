from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'nobodywilleverknow'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure the app to use HTTPS as the preferred URL scheme
app.config['PREFERRED_URL_SCHEME'] = 'https'


db = SQLAlchemy(app)

from app import routes, models