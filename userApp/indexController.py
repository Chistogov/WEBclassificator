# -*- coding: utf-8 -*-
from flask import render_template
from userApp import *
from userApp.dbc import User, db, Recognized, Appoint, Journal, Category, Usertests, Testresults, Tests, Datasets, Consnames, Consdata, Usercons
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/')
@login_required
def index():
    max_time_rec=userApp.config.get('MAX_TIME_REC')
    logging.info("Index")

    pics_today = db.session.query(Recognized.Recognized.pic_id).filter(
        db.func.DATE(Recognized.Recognized.date) == datetime.datetime.now().date(),
        Recognized.Recognized.user_id == current_user.id) \
        .group_by(Recognized.Recognized.pic_id)
    timers_today = db.session.query(Recognized.Recognized.timer).filter(db.func.DATE(Recognized.Recognized.date) == datetime.datetime.now().date(),Recognized.Recognized.user_id == current_user.id).group_by(Recognized.Recognized.pic_id, Recognized.Recognized.timer)
    time_today=0.0
    for timer in timers_today:
        if(timer==0 or timer>max_time_rec):
            time_today += max_time_rec
        else:
            time_today += timer
    time_today=round(time_today/60/60, 2)
    pics_in_wait = Appoint.Appoint.query.filter_by(user_id=current_user.id)
    rec_pics = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.pic_id)
    infoForm.name = current_user.user_name
    infoForm.today_rec = len(list(pics_today))
    infoForm.in_wait = len(list(pics_in_wait))
    infoForm.all_rec = len(list(rec_pics))
    infoForm.time_today = time_today
    messageHistory =db.session.query(Journal.Journal.fromUser ,User.User.user_name, Journal.Journal.date, Journal.Journal.message)\
        .filter(Journal.Journal.userTo==current_user.id, Journal.Journal.fromUser).order_by(Journal.Journal.date.desc()).limit(10)
    user_dates = db.session.query(db.func.DATE(Recognized.Recognized.date)).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.date).order_by(Recognized.Recognized.date.desc())
    rechistorylist = list()
    user_dates = list(set(user_dates))
    user_dates.sort(reverse=True)
    for item in user_dates:
        tmp = recHistory()
        tmp.date = item[0]
        tmp.count_rec = len(list(db.session.query(db.func.count(Recognized.Recognized.pic_id)).filter(Recognized.Recognized.user_id==current_user.id, db.func.DATE(Recognized.Recognized.date)==item[0]).group_by(Recognized.Recognized.pic_id)))
        timers = db.session.query(Recognized.Recognized.timer).filter(
            db.func.DATE(Recognized.Recognized.date) == item[0],
            Recognized.Recognized.user_id == current_user.id).group_by(Recognized.Recognized.pic_id,
                                                                       Recognized.Recognized.timer)
        for timer in timers:
            if (timer == 0 or timer > max_time_rec):
                tmp.time += max_time_rec
            else:
                tmp.time += timer
        tmp.time = round(tmp.time/60/60, 2)
        rechistorylist.append(tmp)
    return render_template('index.pug', infoForm=infoForm,
                           admin=current_user.admin, messageHistory=messageHistory,
                           recHistory=rechistorylist)


class infoForm():
    name = ""
    today_rec = 0
    in_wait = 0
    all_rec = 0
    time_today = 0.0

class recHistory():
    date = ""
    count_rec = 0
    time = 0.0