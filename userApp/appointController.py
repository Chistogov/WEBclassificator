# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
from flask_login import login_required, current_user
import datetime


@userApp.route('/appoint')
@login_required
def appoint():
    print("Appoint")
    all_pics = db.session.query(Picture.Picture).all()
    rec_pics = db.session.query(Recognized.Recognized.pic_id).group_by(Recognized.Recognized.pic_id)
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Recognized.Recognized.pic_id))\
        .join(Recognized.Recognized)\
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear)

    infoForm.all_pics = len(list(all_pics))
    infoForm.rec_pics = len(list(rec_pics))
    users = User.User.query.all()
    return render_template('appoint.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, users=users)


class infoForm():
    rec_pics = 0;
    all_pics = 0;




