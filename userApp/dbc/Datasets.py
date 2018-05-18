# -*- coding: utf-8 -*-
from userApp.dbc import db, Tests, Usertests

#Словарь с записями названий наборов данных

class Datasets(db.Model):
    __tablename__ = "datasets"
    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(100), unique=True)

    test = db.relationship('Tests', back_populates='dataset',
                                 lazy='dynamic',
                                 primaryjoin=id == Tests.Tests.dataset_id)

    user_tests = db.relationship('Usertests', back_populates='dataset',
                            lazy='dynamic',
                            primaryjoin=id == Usertests.Usertests.dataset_id)
