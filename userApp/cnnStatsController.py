# -*- coding: utf-8 -*-
from flask import render_template, redirect
from userApp import *
from userApp.dbc import db, Picture, Symptom, Recognized, Appoint, Cnnrec
from flask_login import login_required, current_user
import logging


@userApp.route('/stats_cnn')
@login_required
def stats_cnn():
    if not(current_user.admin):
        return redirect('/')
    logging.info("StatsCnn")
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Cnnrec.Cnnrec.pic_id))\
        .join(Cnnrec.Cnnrec) \
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear)

    return render_template('cnnStats.pug', pics_by_symp=pics_by_symp, admin=current_user.admin)





