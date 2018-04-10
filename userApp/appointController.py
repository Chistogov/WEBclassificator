# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
from userApp.Service import appointService, journalService
from flask_login import login_required, current_user
import logging


@userApp.route('/appoint', methods=['GET'])
@login_required
def appoint():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if('message' in request.args):
        message = request.args['message']
    logging.info("appoint")
    all_pics = db.session.query(Picture.Picture).all()
    app_pics = db.session.query(Appoint.Appoint).all()
    rec_pics = db.session.query(Recognized.Recognized.pic_id).group_by(Recognized.Recognized.pic_id)
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Recognized.Recognized.pic_id))\
        .join(Recognized.Recognized)\
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear)

    infoForm.all_pics = len(list(all_pics))
    infoForm.rec_pics = len(list(rec_pics))
    infoForm.app_pics = len(list(app_pics))
    infoForm.wait_pics = infoForm.all_pics-infoForm.rec_pics
    users = User.User.query.all()
    return render_template('appoint.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, users=users, message=message, admin=current_user.admin)

@userApp.route('/appoint', methods=['POST'])
@login_required
def appoint_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('appoint', message="Demo user, read only"))
    form = request.form
    if(appointService.validateForm(form)):
        message = appointService.validateForm(form)
        return redirect(url_for('appoint', message=message))
    forUser = form['forUser']
    count = form['count']
    in_app = db.session.query(Appoint.Appoint.pic_id).filter(Appoint.Appoint.user_id == forUser)
    for item in form:
        if (item == 'fromRec'):
            if (form['fromUser'] != "0"):
                rec = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.user_id == form['fromUser'])
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(in_app)).limit(count)
                appointService.toAppDb(pics, forUser)
                return redirect('/appoint')
            else:
                rec = db.session.query(Recognized.Recognized.pic_id)
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(in_app)).limit(count)
                appointService.toAppDb(pics, forUser)
                return redirect('/appoint')
        if (item == 'fromApp'):
            app = db.session.query(Appoint.Appoint.pic_id)
            pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
            appointService.toAppDb(pics, forUser)
            return redirect('/appoint')
    rec = db.session.query(Recognized.Recognized.pic_id)
    app = db.session.query(Appoint.Appoint.pic_id)
    pics = db.session.query(Picture.Picture).filter(~Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
    appointService.toAppDb(pics, forUser)
    journalService.newMessaage(forUser, "Назначены новые снимки (" + str(len(list(pics))) + " шт.)")
    return redirect('/appoint')


class infoForm():
    rec_pics = 0
    all_pics = 0
    wait_pics = 0
    app_pics = 0




