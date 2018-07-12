# -*- coding: utf-8 -*-
from userApp.dbc import db

class Consdata(db.Model):
    __tablename__ = "consdata"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    cons_num = db.Column(db.Integer, db.ForeignKey('consnames.id'), nullable=False)

    picture = db.relationship("Picture", back_populates="consdata")

    consname = db.relationship("Consnames", back_populates="consdata")

