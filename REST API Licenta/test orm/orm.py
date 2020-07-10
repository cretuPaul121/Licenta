from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

file_path = os.path.abspath(os.getcwd()) +"\database.db"
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


