from userApp.dbc import db, Recognized, Appoint, Cnnrec


class Picture(db.Model):
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    pic_name = db.Column(db.String(50), unique=True)
    index_date = db.Column(db.Date)
    note = db.Column(db.Text)
    hash = db.Column(db.String(100), unique=True)
    first_rec = db.Column(db.Boolean)
    skipped = db.Column(db.Boolean)
    rec = db.relationship('Recognized', backref='picture',
                            lazy='dynamic',
                         primaryjoin=id == Recognized.Recognized.pic_id)
    app = db.relationship('Appoint', backref='picture',
                          lazy='dynamic',
                          primaryjoin=id == Appoint.Appoint.pic_id)
    cnn = db.relationship('Cnnrec', backref='picture',
                          lazy='dynamic',
                          primaryjoin=id == Cnnrec.Cnnrec.pic_id)

    # def __init__(self, id, pic_name, index_date, note, hash, first_rec, skipped):
    #     self.id = id
    #     self.pic_name = pic_name
    #     self.index_date = index_date
    #     self.note = note
    #     self.hash = hash
    #     self.first_rec = first_rec
    #     self.skipped = skipped
