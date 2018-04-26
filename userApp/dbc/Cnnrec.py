from userApp.dbc import db



class Cnnrec(db.Model):
    __tablename__ = "cnnrec"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    percentage = db.Column(db.Float)

    cnnSymptom = db.relationship("Symptom", back_populates="cnnRecognized")

    cnnPicture = db.relationship("Picture", back_populates="cnnRecognized")