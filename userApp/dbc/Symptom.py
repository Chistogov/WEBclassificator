from userApp.dbc import db, Recognized


class Symptom(db.Model):
    __tablename__ = "symptoms"
    id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(50), unique=True)
    users = db.relationship('users',
                            secondary=Recognized.Recognized,
                            backref=db.backref("users_", lazy="dynamic"))
    pictures = db.relationship('pictures',
                               secondary=Recognized.Recognized,
                               backref=db.backref("users_", lazy="dynamic"))


    def __init__(self, id, symptom_name):
        self.id = id
        self.symptom_name = symptom_name
