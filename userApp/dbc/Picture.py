from flask_login import UserMixin
from userApp.dbc import db


class Picture(db.Model, UserMixin):
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    pic_name = db.Column(db.String(50), unique=True)
    index_date = db.Column(db.Date)
    note = db.Column(db.Text)
    hash = db.Column(db.String(100), unique=True)
    first_rec = db.Column(db.Boolean)
    skipped = db.Column(db.Boolean)

    def __init__(self, id, pic_name, index_date, note, hash, first_rec, skipped):
        self.id = id
        self.pic_name = pic_name
        self.index_date = index_date
        self.note = note
        self.hash = hash
        self.first_rec = first_rec
        self.skipped = skipped
