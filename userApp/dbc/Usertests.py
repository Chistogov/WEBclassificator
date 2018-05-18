# -*- coding: utf-8 -*-
from userApp.dbc import db

#Здесь хранятся сформированные наборы данных для тестирования пользователей

class Usertests(db.Model):
    __tablename__ = "usertests"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)

    symptom = db.relationship("Symptom", back_populates="user_tests")

    user = db.relationship("User", back_populates="user_tests")

    picture = db.relationship("Picture", back_populates="user_tests")

    dataset = db.relationship("Datasets", back_populates="user_tests")
