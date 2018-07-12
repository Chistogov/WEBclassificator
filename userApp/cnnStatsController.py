# -*- coding: utf-8 -*-
from flask import render_template, redirect
from userApp import *
from userApp.dbc import db, Picture, Symptom, Recognized, Appoint, Cnnrec, User
from flask_login import login_required, current_user
import logging


@userApp.route('/stats_cnn')
@login_required
def stats_cnn():
    if not(current_user.admin):
        return redirect('/')
    logging.info("StatsCnn")
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Cnnrec.Cnnrec.pic_id), Symptom.Symptom.id)\
        .join(Cnnrec.Cnnrec) \
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear, Symptom.Symptom.id)

    return render_template('/statistic/cnnStats.pug', pics_by_symp=pics_by_symp, admin=current_user.admin)

PER_PAGE = 21

@userApp.route('/cnnpics/', defaults={'page': 0})
@userApp.route('/cnnpics/<path:path>/<int:page>')
@login_required
def cnn_pic_view(path, page):
    symptomId = path
    symptom = Symptom.Symptom.query.filter(Symptom.Symptom.id==symptomId).first()
    pics_by_symp = db.session.query(Picture.Picture.pic_name) \
        .join(Cnnrec.Cnnrec) \
        .filter(Cnnrec.Cnnrec.symp_id==symptomId) \
        .group_by(Cnnrec.Cnnrec.symp_id, Picture.Picture.pic_name)
    count = len(list(pics_by_symp))
    pics = get_pics_for_page(page, symptomId)
    message = ""
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    return render_template('/cnn/pics.pug', admin=current_user.admin, pictures=pics, pagination=pagination, symptom=symptom)

def get_pics_for_page(page, symptomId):
    pics = db.session.query(Picture.Picture.pic_name) \
        .join(Cnnrec.Cnnrec) \
        .filter(Cnnrec.Cnnrec.symp_id==symptomId) \
        .group_by(Cnnrec.Cnnrec.symp_id, Picture.Picture.pic_name)
    print str(len(list(pics)))
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    print str(len(list(pics)))
    if page:
        pics = pics.offset(page * PER_PAGE)
    print str(len(list(pics)))
    return pics