# -*- coding: utf-8 -*-
from flask import render_template, redirect, jsonify
from userApp import *
from userApp import AlchemyEncoder
from userApp.dbc import db, Picture, Symptom, Recognized, Appoint
from flask_login import login_required, current_user
import logging, datetime, decimal, json


@userApp.route('/stats')
@login_required
def stats():
    if not(current_user.admin):
        return redirect('/')
    logging.info("Stats")
    all_pics = db.session.query(Picture.Picture).all()
    app_pics = db.session.query(Appoint.Appoint).all()
    rec_pics = db.session.query(Recognized.Recognized.pic_id).group_by(Recognized.Recognized.pic_id)
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Recognized.Recognized.pic_id).label('total'), Symptom.Symptom.ismedical, Symptom.Symptom.id)\
        .join(Recognized.Recognized) \
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear, Symptom.Symptom.ismedical, Symptom.Symptom.id).order_by(db.desc('total'))
    infoForm.all_pics = len(list(all_pics))
    infoForm.rec_pics = len(list(rec_pics))
    infoForm.app_pics = len(list(app_pics))
    infoForm.wait_pics = infoForm.all_pics-infoForm.rec_pics

    return render_template('stats.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, admin=current_user.admin)

@userApp.route('/stats/json')
def stats_json():
    logging.info("Stats_Json")
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Recognized.Recognized.pic_id).label('total'), Symptom.Symptom.ismedical, Symptom.Symptom.id)\
        .join(Recognized.Recognized) \
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear, Symptom.Symptom.ismedical, Symptom.Symptom.id).order_by(db.desc('total'))
    return json.dumps(pics_by_symp.all(), cls=AlchemyEncoder.AlchemyEncoder, ensure_ascii=False).encode('utf8')


class infoForm():
    rec_pics = 0
    all_pics = 0
    wait_pics = 0
    app_pics = 0




