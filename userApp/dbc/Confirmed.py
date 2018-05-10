from userApp.dbc import db

class Confirmed(db.Model):
    __tablename__ = "confirmed"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rec_id = db.Column(db.Integer, db.ForeignKey('recognized.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('testtypes.id'))
    date = db.Column(db.Date)

    # test = db.relationship('Testtypes', back_populates="confirmed")

    user = db.relationship("User", back_populates="confirmed")

    recognized = db.relationship("Recognized", back_populates="confirmed")

    picture = db.relationship("Picture", back_populates="confirmed")