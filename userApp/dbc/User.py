from flask_login import UserMixin
from userApp.dbc import db, Recognized, Appoint, Journal, Mistakes, Confirmed, Tests, Usertests, Testresults, Consilium, Usercons


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean)
    expert = db.Column(db.Boolean)

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

    mistakes = db.relationship('Mistakes', back_populates='user',
                            lazy='dynamic',
                         primaryjoin=id == Mistakes.Mistakes.user_id)

    confirmed = db.relationship('Confirmed', back_populates='user',
                            lazy='dynamic',
                         primaryjoin=id == Confirmed.Confirmed.user_id)

    test = db.relationship('Tests', back_populates='user',
                            lazy='dynamic',
                         primaryjoin=id == Tests.Tests.user_id)

    user_tests = db.relationship('Usertests', back_populates='user',
                                 lazy='dynamic',
                                 primaryjoin=id == Usertests.Usertests.user_id)

    test_results = db.relationship('Testresults', back_populates='user',
                                 lazy='dynamic',
                                 primaryjoin=id == Testresults.Testresults.user_id)

    consilium = db.relationship('Consilium', back_populates='user',
                                 lazy='dynamic',
                                 primaryjoin=id == Consilium.Consilium.user_id)

    usercons = db.relationship('Usercons', back_populates='user',
                                lazy='dynamic',
                                primaryjoin=id == Usercons.Usercons.user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True