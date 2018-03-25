from flask_login import UserMixin
from userApp import userApp
from userApp.dbc import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=True)

    def __init__(self, id, user_name, password):
        self.id = id
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.user_name

    def is_active(self):
        return True

    def is_authenticated(self):
        return True