from userApp.dbc import db



class Journal(db.Model):
    __tablename__ = "journal"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    userFrom = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    userTo = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date)

    fromUser = db.relationship("User", back_populates="journalFrom", foreign_keys=[userFrom])

    toUser = db.relationship("User", back_populates="journalTo", foreign_keys=[userTo])


    # def __init__(self, id, pic_name, index_date, note, hash, first_rec, skipped):
    #     self.id = id
    #     self.pic_name = pic_name
    #     self.index_date = index_date
    #     self.note = note
    #     self.hash = hash
    #     self.first_rec = first_rec
    #     self.skipped = skipped
