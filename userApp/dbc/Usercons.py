# -*- coding: utf-8 -*-
from userApp.dbc import db

#Здесь хранятся названия консилиумов

class Usercons(db.Model):
    __tablename__ = "usercons"
    id = db.Column(db.Integer, primary_key=True)
    cons_num = db.Column(db.Integer, db.ForeignKey('consnames.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manager = db.Column(db.Boolean)

    user = db.relationship("User", back_populates="usercons")

    consname = db.relationship("Consnames", back_populates="usercons")
