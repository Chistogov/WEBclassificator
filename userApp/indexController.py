# -*- coding: utf-8 -*-
from flask import render_template
from userApp import *
from userApp.dbc import User, db, Recognized, Appoint, Journal
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/')
@login_required
def index():
    logging.info("Index")
    pics_today = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id, date=datetime.datetime.now().date()).group_by(Recognized.Recognized.pic_id)
    pics_in_wait = Appoint.Appoint.query.filter_by(user_id=current_user.id)
    rec_pics = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.pic_id)
    infoForm.name = current_user.user_name
    infoForm.today_rec = len(list(pics_today))
    infoForm.in_wait = len(list(pics_in_wait))
    infoForm.all_rec = len(list(rec_pics))
    messageHistory =db.session.query(Journal.Journal.user_From ,User.User.user_name, Journal.Journal.date, Journal.Journal.message)\
        .filter(Journal.Journal.userTo==current_user.id, Journal.Journal.user_From).order_by(Journal.Journal.date.desc()).limit(10)
    user_pics = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.pic_id)
    user_dates = db.session.query(Recognized.Recognized.date).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.date).order_by(Recognized.Recognized.date.desc())
    rechistorylist = list()
    for item in user_dates:
        tmp = recHistory()
        tmp.date = item[0]
        tmp.count_rec = len(list(db.session.query(db.func.count(Recognized.Recognized.pic_id)).filter_by(user_id=current_user.id, date=item[0]).group_by(Recognized.Recognized.pic_id)))
        rechistorylist.append(tmp)
    return render_template('index.pug', infoForm=infoForm,
                           admin=current_user.admin, messageHistory=messageHistory, recHistory=rechistorylist)


class infoForm():
    name = ""
    today_rec = 0
    in_wait = 0
    all_rec = 0

class recHistory():
    date = ""
    count_rec = 0





