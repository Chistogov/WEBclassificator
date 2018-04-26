from flask_login import UserMixin
from userApp.dbc import db, Recognized, Appoint, Journal


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean)
    recognized = db.relationship('Recognized', back_populates='user',
                            lazy='dynamic',
                         primaryjoin=id == Recognized.Recognized.user_id)
    app = db.relationship('Appoint', back_populates='user',
                          lazy='dynamic',
                          primaryjoin=id == Appoint.Appoint.user_id)
    journalFrom = db.relationship('Journal', back_populates='fromUser',
                          lazy='dynamic',
                          primaryjoin=id == Journal.Journal.userFrom)
    journalTo = db.relationship('Journal', back_populates='toUser',
                          lazy='dynamic',
                          primaryjoin=id == Journal.Journal.userTo)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True