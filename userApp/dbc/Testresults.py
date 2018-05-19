# -*- coding: utf-8 -*-
from userApp.dbc import db



class Testresults(db.Model):
    __tablename__ = "testresults"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    date = db.Column(db.Date)
    timer = db.Column(db.Integer, default=0)

    symptom = db.relationship("Symptom", back_populates="test_results")

    user = db.relationship("User", back_populates="test_results")

    picture = db.relationship("Picture", back_populates="test_results")

    test = db.relationship("Tests", back_populates="test_results")

