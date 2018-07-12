# -*- coding: utf-8 -*-
from userApp.dbc import db, Consdata, Usercons

#Здесь хранятся названия консилиумов

class Consnames(db.Model):
    __tablename__ = "consnames"
    id = db.Column(db.Integer, primary_key=True)
    cons_name = db.Column(db.String(50))

    consdata = db.relationship('Consdata', back_populates='consname',
                               lazy='dynamic',
                               primaryjoin=id == Consdata.Consdata.cons_num)

    usercons = db.relationship('Usercons', back_populates='consname',
                               lazy='dynamic',
                               primaryjoin=id == Usercons.Usercons.cons_num)