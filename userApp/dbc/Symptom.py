from flask_login import UserMixin
from userApp.dbc import db


class Symptom(db.Model, UserMixin):
    __tablename__ = "symptoms"
    id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(50), unique=True)


    def __init__(self, id, symptom_name):
        self.id = id
        self.symptom_name = symptom_name
