# -*- coding: utf-8 -*-
from userApp.dbc import db, Testresults

#Здесь хранятся назначенные пользователям тесты и их результаты

class Tests(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    results = db.Column(db.Float)
    date = db.Column(db.DATE)

    dataset = db.relationship("Datasets", back_populates="test")

    user = db.relationship("User", back_populates="test")

    test_results = db.relationship('Testresults', back_populates='test',
                                 lazy='dynamic',
                                 primaryjoin=id == Testresults.Testresults.test_id)

    # def __init__(self, id, pic_name, index_date, note, hash, first_rec, skipped):
    #     self.id = id
    #     self.pic_name = pic_name
    #     self.index_date = index_date
    #     self.note = note
    #     self.hash = hash
    #     self.first_rec = first_rec
    #     self.skipped = skipped
    #     super(Recognized, self).__init__()
