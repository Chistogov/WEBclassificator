from flask_login import UserMixin
from userApp.dbc import db, Recognized, Appoint


# https://gist.github.com/kirang89/10030736


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean)
    rec = db.relationship('Recognized', backref='user',
                            lazy='dynamic',
                         primaryjoin=id == Recognized.Recognized.user_id)
    app = db.relationship('Appoint', backref='user',
                          lazy='dynamic',
                          primaryjoin=id == Appoint.Appoint.user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True