from userApp.dbc import db


class Confirmed(db.Model):
    __tablename__ = "confirmed"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rec_id = db.Column(db.Integer, db.ForeignKey('recognized.id'), nullable=False)
    date = db.Column(db.Date)

    user = db.relationship("User", back_populates="confirmed")

    recognized = db.relationship("Recognized", back_populates="confirmed")


    # def __init__(self, id, symptom_name):
    #     self.id = id
    #     self.symptom_name = symptom_name
