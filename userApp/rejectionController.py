# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
from userApp.Service import appointService, journalService
from flask_login import login_required, current_user
import logging, datetime


@userApp.route('/rejection', methods=['GET'])
@login_required
def rejection():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if('message' in request.args):
        message = request.args['message']
    logging.info("appoint")
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id)
    users = User.User.query.all()
    return render_template('rejection.pug', symptoms=symptoms, users=users, message=message, admin=current_user.admin)

@userApp.route('/rejection', methods=['POST'])
@login_required
def rejection_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('rejection', message="Demo user, read only"))
    symptoms = list()
    form = request.form
    for item in form:
        if (item.isdigit()):
            symptoms.append(item)

    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    if (len(symptoms) != 0):
        print ('symptoms')
        for item in symptoms:
            rec = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id == item))
            pics = pics.filter(Picture.Picture.id.in_(rec))
            print str(len(list(pics)))
    if (form.has_key('forUser')):
        print ('user')
        pics = pics.filter(Recognized.Recognized.user_id == form['forUser'])
    if (form['dateRec']):
        print (form['dateRec'])
        date = datetime.datetime.strptime(form['dateRec'], "%Y-%m-%d")
        pics = pics.filter(db.func.DATE(Recognized.Recognized.date) == date)
    picslist = list()
    for item in pics:
        picslist.append(item.id)
    symp_type = ""
    if (form['type']):
        symp_type = form['type']
    return redirect(url_for('rejection_search', page=0, pics=picslist, symp_type=symp_type))




PER_PAGE = 12

@userApp.route('/rejection/search/', methods=['GET'])
@login_required
def rejection_search():
    page=int(request.args.get('page'))
    picslist = request.args.getlist('pics')
    symp_type = request.args.get('symp_type')
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(picslist))
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    symptoms = db.session.query(Symptom.Symptom)
    if(symp_type == "nose"):
        symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.nose == True)
    elif (symp_type == "throat"):
        symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.throat == True)
    elif (symp_type == "ear"):
        symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.ear == True)
    return render_template('/rejection/pics.pug', admin=current_user.admin, pictures=pics, pagination=pagination, request=request, symptoms=symptoms)

def get_pics_for_page(page, pics):
    pics = pics.group_by(Picture.Picture.id)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics
