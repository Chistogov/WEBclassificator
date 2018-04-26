from userApp.dbc import db, Recognized, Cnnrec


class Symptom(db.Model):
    __tablename__ = "symptoms"
    id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(50), unique=True)
    ear = db.Column(db.Boolean, default=False)
    nose = db.Column(db.Boolean, default=False)
    throat = db.Column(db.Boolean, default=False)
    ismedical = db.Column(db.Boolean, default=False)
    recognized = db.relationship('Recognized', back_populates='symptom',
                            lazy='dynamic',
                            primaryjoin=id == Recognized.Recognized.symp_id)
    cnnRecognized = db.relationship('Cnnrec', back_populates='cnnSymptom',
                          lazy='dynamic',
                          primaryjoin=id == Cnnrec.Cnnrec.symp_id)

    # def __init__(self, id, symptom_name):
    #     self.id = id
    #     self.symptom_name = symptom_name
