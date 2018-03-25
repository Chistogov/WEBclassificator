from userApp.dbc import db


class Recognized(db.Model):
    __tablename__ = "recognized"
    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    symp_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date)


    def __init__(self, id, pic_name, index_date, note, hash, first_rec, skipped):
        self.id = id
        self.pic_name = pic_name
        self.index_date = index_date
        self.note = note
        self.hash = hash
        self.first_rec = first_rec
        self.skipped = skipped
