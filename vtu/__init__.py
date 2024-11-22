from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///vtu_database.db'
app.config['SECRET_KEY'] = 'FOR ALL THE TIME THAT U SPEND IN MY PARADE!'

# initialize SQLAlchemy
db = SQLAlchemy(app)