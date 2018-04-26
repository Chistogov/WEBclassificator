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
    user = None
    date = None
    form = request.form
    for item in form:
        if (item.isdigit()):
            symptoms.append(item)
    if (form.has_key('forUser')):
        user = form['forUser']
    if (form.has_key('dateRec')):
        date = form['dateRec']

    return redirect(url_for('rejection_search', page=0, user=user, date=date, symptoms=symptoms))




PER_PAGE = 21

@userApp.route('/rejection/search/', methods=['GET'])
@login_required
def rejection_search():
    page=int(request.args.get('page'))
    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    print str(len(list(pics)))
    if (len(request.args.getlist('symptoms'))!=0):
        print ('symptoms')
        pics = pics.filter(Recognized.Recognized.symp_id.in_(request.args.getlist('symptoms')))
    if(request.args.get('user')):
        print ('user')
        pics = pics.filter(Recognized.Recognized.user_id==request.args.get('user'))
    if (request.args.get('date')):
        print ('date')
        date = datetime.datetime.strptime(request.args.get('date'), "%Y-%m-%d")
        pics = pics.filter(db.func.DATE(Recognized.Recognized.date) == date)
    # for item in pics:
    #     print item.recognized.first().date
    #     print item.recognized.first().user.user_name
    #     for i in item.recognized:
    #         print i.symptom.symptom_name
    #     print "--------"
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    symptoms = db.session.query(Symptom.Symptom)
    return render_template('/rejection/pics.pug', admin=current_user.admin, pictures=pics, pagination=pagination, request=request, symptoms=symptoms)

def get_pics_for_page(page, pics):
    pics = pics.group_by(Picture.Picture.id)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics
