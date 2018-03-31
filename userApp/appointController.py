# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort, url_for
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/appoint', methods=['GET'])
@login_required
def appoint():
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
    return render_template('appoint.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, users=users, message=message)

@userApp.route('/appoint', methods=['POST'])
@login_required
def appoint_post():
    form = request.form
    if(validateForm(form)):
        message = validateForm(form)
        return redirect(url_for('appoint', message=message))
    forUser = form['forUser']
    count = form['count']
    in_app = db.session.query(Appoint.Appoint.pic_id).filter(Appoint.Appoint.user_id == forUser)
    for item in form:
        if (item == 'fromRec'):
            if (form['fromUser'] != "0"):
                print ('fromUser')
                rec = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.user_id == form['fromUser'])
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(in_app)).limit(count)
                toAppDb(pics, forUser)
                # printQ(pics)
                return redirect('/appoint')
            else:
                print ('not fromUser')
                rec = db.session.query(Recognized.Recognized.pic_id)
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(in_app)).limit(count)
                toAppDb(pics, forUser)
                # printQ(pics)
                return redirect('/appoint')
        if (item == 'fromApp'):
            print ('fromApp')
            app = db.session.query(Appoint.Appoint.pic_id)
            pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
            toAppDb(pics, forUser)
            # printQ(pics)
            return redirect('/appoint')
    print ('simple')
    rec = db.session.query(Recognized.Recognized.pic_id)
    app = db.session.query(Appoint.Appoint.pic_id)
    pics = db.session.query(Picture.Picture).filter(~Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
    toAppDb(pics, forUser)
    # printQ(pics)
    return redirect('/appoint')

def validateForm(form):
    if(form.has_key('fromRec')):
        if (form.has_key('fromApp')):
            return "Из назначенных/из распознанных - выберите один пункт"
    if not(form.has_key('forUser')):
        return "Не указан пользователь"
    if (form['count'] == ""):
        return "Не указано количество снимков"
    if not(form['count'].isdigit()):
        return "В поле \"Количество\" ожидалось число"
    else:
        return None

def toAppDb(pics, forUser):
    for pic in pics:
        app = Appoint.Appoint()
        app.user_id = forUser
        app.pic_id = pic.id
        app.date = datetime.datetime.now().date()
        db.session.add(app)
    db.session.commit()

def printQ(pics):
    print len(list(pics))
    for item in pics:
        print item.pic_name


class infoForm():
    rec_pics = 0
    all_pics = 0
    wait_pics = 0
    app_pics = 0




