from enum import unique
from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(70))
    notes = db.relationship('ToDoItems')
    
class ToDoItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_info = db.Column(db.String(180),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CompletedItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))