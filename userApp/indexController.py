# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import User, db, Picture, Symptom
from flask_login import login_required, current_user
import datetime


@userApp.route('/')
@login_required
def index():
    print("Index")
    # pics = len(list(User.User.query.get(current_user.id).stock.filter_by(date=datetime.datetime.now())))
    # pics = User.User.query.get(current_user.id).stock.all()
    # print pics
    # for a in pics:
    #     print a.picture.pic_name
    infoForm.name = current_user.user_name
    infoForm.today_rec = len(list(User.User.query.get(current_user.id).rec.filter_by(date=datetime.datetime.now())));
    infoForm.in_wait = 0;
    infoForm.all_rec = len(list(User.User.query.get(current_user.id).rec));
    infoForm.confirmed = 0;
    return render_template('index.pug', infoForm=infoForm)


class infoForm():
    name = "";
    today_rec = 0;
    in_wait = 0;
    all_rec = 0;
    confirmed = 0;




