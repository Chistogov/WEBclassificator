# -*- coding: utf-8 -*-
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
import datetime


def validateForm(form):
    if(form.has_key('fromRec')):
        if (form.has_key('fromApp')):
            return "Из назначенных/из распознанных - выберите один пункт"
    if not(form.has_key('forUser')):
        return "Не указан пользователь"
    if (form['count'] == ""):
        return "Не указано количество снимков"
    if not(form['count'].isdigit()):
        return "В поле \"Количество\" ожидалось число"
    else:
        return None

def toAppDb(pics, forUser):
    for pic in pics:
        app = Appoint.Appoint()
        app.user_id = forUser
        app.secondary = False
        app.pic_id = pic.id
        app.date = datetime.datetime.now().date()
        db.session.add(app)
    print ("Commit...")
    db.session.commit()