# -*- coding: utf-8 -*-
from userApp.dbc import Journal, db
from flask_login import current_user
import datetime

def newMessaage(userTo, message):
    note = Journal.Journal()
    note.userTo = userTo
    note.userFrom = current_user.id
    note.message = message
    note.date = datetime.datetime.now()
    db.session.add(note)
    print ("Commit...")
    db.session.commit()


