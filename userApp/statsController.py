# -*- coding: utf-8 -*-
from flask import render_template, redirect, jsonify, request, url_for
from userApp import *
from userApp import AlchemyEncoder
from userApp.dbc import db, Picture, Symptom, Recognized, Appoint, User, Category, Confirmed
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

    return render_template('/statistic/stats.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, admin=current_user.admin)

# /stats/search

@userApp.route('/stats/search', methods=['GET'])
@login_required
def stats_form():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if('message' in request.args):
        message = request.args['message']
    logging.info("appoint")
    symptoms = db.session.query(Symptom.Symptom)
    categories = Category.Category.query.order_by(Category.Category.id).all()
    users = User.User.query.all()
    return render_template('/statistic/statsForm.pug', symptoms=symptoms, users=users, message=message,
                           categories=categories,admin=current_user.admin)

@userApp.route('/stats/search', methods=['POST'])
@login_required
def stats_form_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('stats_form', message="Demo user, read only"))
    symptoms = list()
    users = list()
    form = request.form
    for item in form:
        if (item.isdigit()):
            symptoms.append(item)
        if ('user' in item):
            print form[item]
            users.append(form[item])

    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    if (len(symptoms) != 0):
        for item in symptoms:
            rec = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id == item))
            pics = pics.filter(Picture.Picture.id.in_(rec))
            # print str(len(list(pics)))
    if (form.has_key('opticalExclude')):
        rec = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id.in_([23,37,49,53])))
        pics = pics.filter(Picture.Picture.id.notin_(rec))
    if(len(users)>0):
        pics = pics.filter(Recognized.Recognized.user_id.in_(users))
    if (form['dateRecFrom']):
        date = datetime.datetime.strptime(form['dateRecFrom'], "%Y-%m-%d")
        pics = pics.filter(db.func.DATE(Recognized.Recognized.date) > date)
    if (form['dateRecTo']):
        date = datetime.datetime.strptime(form['dateRecTo'], "%Y-%m-%d")
        pics = pics.filter(db.func.DATE(Recognized.Recognized.date) < date)

    conf = db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.user_id==current_user.id)
    conflist = list()
    for item in conf:
        conflist.append(item.recognized.pic_id)
    # pics = pics.filter(Picture.Picture.id.notin_(conflist))

    picslist = list()
    for item in pics:
        picslist.append(item.id)
    symp_type = ""
    if (form['type']):
        symp_type = form['type']

    return redirect(url_for('stats_form', message=str(len(picslist))))

# @userApp.route('/stats/json')
# def stats_json():
#     logging.info("Stats_Json")
#     pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Picture.Picture.pic_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, Symptom.Symptom.ismedical)\
#         .join(Recognized.Recognized).filter(Symptom.Symptom.id==Recognized.Recognized.symp_id, Picture.Picture.id==Recognized.Recognized.pic_id)
#     return json.dumps(pics_by_symp.all(), cls=AlchemyEncoder.AlchemyEncoder, ensure_ascii=False).encode('utf8')


class infoForm():
    rec_pics = 0
    all_pics = 0
    wait_pics = 0
    app_pics = 0