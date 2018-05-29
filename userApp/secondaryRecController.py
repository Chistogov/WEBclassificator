# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import Symptom, Picture, db, Recognized, Appoint, Cnnrec, Category,User
from flask_login import login_required, current_user
import datetime
import logging

@userApp.route('/sec_rec', methods=['GET'])
@login_required
def sec_rec():
    logging.info('primary_rec')
    pic = db.session.query(Picture.Picture.id, Picture.Picture.pic_name, Appoint.Appoint.id, Appoint.Appoint.message).filter(Picture.Picture.id==Appoint.Appoint.pic_id, Appoint.Appoint.user_id==current_user.id,Appoint.Appoint.secondary==True).first()
    neural = ""
    pic_local = ""
    message = ""
    appointed = ""
    app_message = ""
    if(pic):
        app_message = pic.message
    if(pic):
        neural = db.session.query(Cnnrec.Cnnrec.symp_id, Symptom.Symptom.symptom_name).filter(Cnnrec.Cnnrec.pic_id==pic[0], Symptom.Symptom.id==Cnnrec.Cnnrec.symp_id).group_by(Cnnrec.Cnnrec.symp_id, Symptom.Symptom.symptom_name).all()
        pic_local = "data/" + pic[1]
        appointed = pic[2]
    else:
        message = "No data"
    symptoms = db.session.query(Symptom.Symptom)
    pics_today = db.session.query(Recognized.Recognized.pic_id).filter(db.func.DATE(Recognized.Recognized.date)==datetime.datetime.now().date(),
                                                                      Recognized.Recognized.user_id==current_user.id)\
                                                                    .group_by(Recognized.Recognized.pic_id)

    pics_in_wait = Appoint.Appoint.query.filter_by(user_id=current_user.id, secondary=True)
    categories = Category.Category.query.order_by(Category.Category.id).all()
    recognized = None
    if(pic):
        recognized = db.session.query(Recognized.Recognized.symp_id).filter(Recognized.Recognized.pic_id==pic[0],Recognized.Recognized.user_id==current_user.id)
    symp_list = list()
    if(recognized):
        for item in recognized:
            symp_list.append(item.symp_id)
    # ***
    symptom_list = list()
    if(pic):
        experts = db.session.query(User.User.id).filter(User.User.expert == True)
        recognized = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id == pic[0],
                                                                    Recognized.Recognized.user_id.in_(experts))
        symp_ids = list()
        for item in db.session.query(Recognized.Recognized.symp_id).filter(
                Recognized.Recognized.pic_id == pic[0]).group_by(Recognized.Recognized.user_id,
                                                                 Recognized.Recognized.symp_id):
            symp_ids.append(item.symp_id)
        user_rec = db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic[0],
                                                                          Recognized.Recognized.user_id.in_(
                                                                              experts)).group_by(
            Recognized.Recognized.user_id)
        user_rec = db.session.query(User.User).filter(User.User.id.in_(user_rec), User.User.expert == True)
        recognized_count = db.session.query(db.func.count(Recognized.Recognized.symp_id)).filter(
            Recognized.Recognized.pic_id == pic[0], Recognized.Recognized.user_id.in_(experts)).group_by(
            Recognized.Recognized.symp_id)
        symptoms2 = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.id.in_(symp_ids))

        diagnoses = db.session.query(Symptom.Symptom.id).filter(Symptom.Symptom.diagnos == True)
        count_users = len(list(user_rec))
        count_diagnoses = len(list(
            db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic[0],
                                                                   Recognized.Recognized.symp_id.in_(
                                                                       diagnoses)).group_by(
                Recognized.Recognized.user_id)))
        for symptom in symptoms2:
            symp = picSymps()
            symp.symptom = symptom
            if (symptom.ismedical and not (symptom.primary)):
                symp.count = (100 / count_users) * symp_ids.count(symptom.id)
            if (symptom.diagnos):
                symp.count = (100 / count_diagnoses) * symp_ids.count(symptom.id)
            symptom_list.append(symp)
    # ***
    if ('message' in request.args):
        message = request.args['message']
    return render_template('sec_rec.pug', symptoms=symptoms,
                           admin=current_user.admin, pic_local=pic_local,
                           message=message, appointed=appointed,
                           today_rec=len(list(pics_today)), in_wait=len(list(pics_in_wait)),
                           neural=neural, categories=categories, recognized=symp_list, symptom_list=symptom_list, app_message=app_message)

class picSymps():
    symptom = None
    count = 0

@userApp.route('/sec_rec', methods=['POST'])
@login_required
def sec_rec_post():
    if(current_user.user_name == "demo"):
        return redirect(url_for('sec_rec', message="Demo user, read only"))
    max_time_rec = userApp.config.get('MAX_TIME_REC')
    form = request.form
    if(form.has_key('appointed')):
        appointed = Appoint.Appoint.query.get(int(form['appointed']))
        db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id==appointed.pic_id, Recognized.Recognized.user_id==current_user.id).delete()
        for item in form:
            if(item.isdigit()):
                print item
                new_tag = Recognized.Recognized()
                new_tag.user_id=current_user.id
                new_tag.symp_id=item
                new_tag.pic_id=appointed.pic_id
                new_tag.date=datetime.datetime.now()
                if(form.has_key('timer')):
                    if(int(form['timer'])>max_time_rec or int(form['timer'])==0):
                        new_tag.timer = max_time_rec
                    else:
                        new_tag.timer = form['timer']
                db.session.add(new_tag)
        db.session.commit()
        pic = Picture.Picture.query.get(appointed.pic_id)
        pic.first_rec = True
        db.session.commit()
        db.session.delete(appointed)
        db.session.commit()

    return redirect('/sec_rec')

@userApp.route('/sec_rec/skip/<path:path>')
@login_required
def skip_sec(path):
    if(current_user.user_name == "demo"):
        return redirect(url_for('sec_rec', message="Demo user, read only"))
    appointed = Appoint.Appoint.query.get(int(path))
    pic = Picture.Picture.query.get(appointed.pic_id)
    pic.skipped = True
    db.session.commit()
    db.session.delete(appointed)
    db.session.commit()

    return redirect('/sec_rec')