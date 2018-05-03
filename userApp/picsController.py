# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for
from userApp import Pagination
from userApp import *
from userApp.dbc import User, db, Recognized, Symptom, Picture, Mistakes
from flask_login import login_required, current_user
import datetime
import logging


PER_PAGE = 21

@userApp.route('/pics/', defaults={'page': 0})
@userApp.route('/pics/<path:path>/<int:page>')
@login_required
def pic_view(path, page):
    symptomId = path
    symptom = Symptom.Symptom.query.filter(Symptom.Symptom.id==symptomId).first()
    pics_by_symp = db.session.query(Picture.Picture.pic_name) \
        .join(Recognized.Recognized) \
        .filter(Recognized.Recognized.symp_id==symptomId) \
        .group_by(Recognized.Recognized.symp_id, Picture.Picture.pic_name)
    count = len(list(pics_by_symp))
    pics = get_pics_for_page(page, symptomId)
    message = ""
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    return render_template('/pics_viewer/index.pug', admin=current_user.admin, pictures=pics, pagination=pagination, symptom=symptom)

def get_pics_for_page(page, symptomId):
    pics = db.session.query(Picture.Picture.pic_name, Picture.Picture.id, User.User.user_name, Recognized.Recognized.date)\
        .join(Recognized.Recognized, User.User, Symptom.Symptom) \
        .filter(Recognized.Recognized.symp_id==symptomId, User.User.id==Recognized.Recognized.user_id, Symptom.Symptom.id==Recognized.Recognized.symp_id) \
        .group_by(Recognized.Recognized.symp_id, Picture.Picture.pic_name,  Picture.Picture.id,  User.User.user_name, Recognized.Recognized.date)
    print str(len(list(pics)))
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    print str(len(list(pics)))
    if page:
        pics = pics.offset(page * PER_PAGE)
    print str(len(list(pics)))
    return pics

@userApp.route('/pics/<int:pic>/<int:symp>/remove')
@login_required
def pic_remove(pic, symp):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')

    deleting = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id==pic, Recognized.Recognized.symp_id==symp).all()

    for item in deleting:
        new_mistake = Mistakes.Mistakes()
        new_mistake.symp_id = item.symp_id
        new_mistake.user_id = item.user_id
        new_mistake.pic_id = item.pic_id
        new_mistake.date = item.date
        db.session.add(new_mistake)
        logging.info("Deleting Recognized - id=" + str(item.id))
    db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id==pic, Recognized.Recognized.symp_id==symp).delete()
    db.session.commit()

    return redirect(request.referrer)

@userApp.route('/pics/<int:pic>/<int:symp>/add')
@login_required
def pic_add_symp(pic, symp):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')

    new_tag = Recognized.Recognized()
    new_tag.user_id = current_user.id
    new_tag.symp_id = symp
    new_tag.pic_id = pic
    new_tag.date = datetime.datetime.now()
    new_tag.timer = 0
    db.session.add(new_tag)
    db.session.commit()

    return redirect(request.referrer)
