# -*- coding: utf-8 -*-
from flask import render_template
from userApp import Pagination
from userApp import *
from userApp.dbc import User, db, Recognized, Symptom, Picture
from flask_login import login_required, current_user
import datetime
import logging


PER_PAGE = 21

@userApp.route('/pics/', defaults={'page': 0})
@userApp.route('/pics/<path:path>/<int:page>')
@login_required
def pic_view(path, page):
    print path
    symptomId = path
    symptom = Symptom.Symptom.query.filter(Symptom.Symptom.id==symptomId).first()
    pics_by_symp = db.session.query(Picture.Picture.pic_name) \
        .join(Recognized.Recognized) \
        .filter(Recognized.Recognized.symp_id==symptomId) \
        .group_by(Recognized.Recognized.symp_id, Picture.Picture.pic_name)
    count = len(list(pics_by_symp))
    pics = get_pics_for_page(page, count, symptomId)
    pagination = Pagination.Pagination(page, PER_PAGE, count)

    return render_template('/pics_viewer/index.pug', admin=current_user.admin, pictures=pics, pagination=pagination, symptom=symptom)


def get_pics_for_page(page, count, symptomId):
    pics = db.session.query(Picture.Picture.pic_name)\
        .join(Recognized.Recognized) \
        .filter(Recognized.Recognized.symp_id==symptomId) \
        .group_by(Recognized.Recognized.symp_id, Picture.Picture.pic_name)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics