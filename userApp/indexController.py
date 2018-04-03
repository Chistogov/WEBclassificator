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
    # pics = len(list(User.User.query.get(current_user.id).stock.filter_by(date=datetime.datetime.now())))
    # pics = User.User.query.get(current_user.id).stock.all()
    # print pics
    # for a in pics:
    #     print a.picture.pic_name
    pics_today = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id, date=datetime.datetime.now().date()).group_by(Recognized.Recognized.pic_id)
    pics_in_wait = Appoint.Appoint.query.filter_by(user_id=current_user.id)
    rec_pics = db.session.query(Recognized.Recognized.pic_id).filter_by(user_id=current_user.id).group_by(Recognized.Recognized.pic_id)
    infoForm.name = current_user.user_name
    infoForm.today_rec = len(list(pics_today))
    infoForm.in_wait = len(list(pics_in_wait))
    infoForm.all_rec = len(list(rec_pics))
    messageHistory =db.session.query(Journal.Journal.user_From ,User.User.user_name, Journal.Journal.date, Journal.Journal.message)\
        .filter(Journal.Journal.userTo==current_user.id, Journal.Journal.user_From).order_by(Journal.Journal.date).limit(10)
    return render_template('index.pug', infoForm=infoForm, admin=current_user.admin, messageHistory=messageHistory)


class infoForm():
    name = ""
    today_rec = 0
    in_wait = 0
    all_rec = 0





