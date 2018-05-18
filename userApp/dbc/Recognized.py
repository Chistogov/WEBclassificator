from userApp.dbc import db, Confirmed



class Recognized(db.Model):
    __tablename__ = "recognized"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timer = db.Column(db.Integer, default=0)
    date = db.Column(db.Date)

    symptom = db.relationship("Symptom", back_populates="recognized")

    user = db.relationship("User", back_populates="recognized")

    picture = db.relationship("Picture", back_populates="recognized")

    confirmed = db.relationship('Confirmed', back_populates='recognized',
                                lazy='dynamic',
                                primaryjoin=id == Confirmed.Confirmed.rec_id)
