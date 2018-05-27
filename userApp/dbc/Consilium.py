from userApp.dbc import db

class Consilium(db.Model):
    __tablename__ = "consilium"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)

    user = db.relationship("User", back_populates="consilium")

    picture = db.relationship("Picture", back_populates="consilium")

    symptom = db.relationship("Symptom", back_populates="consilium")