from userApp.dbc import db, Symptom


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)

    symptom = db.relationship('Symptom', back_populates='category',
                                 lazy='dynamic',
                                 primaryjoin=id == Symptom.Symptom.cat_id)