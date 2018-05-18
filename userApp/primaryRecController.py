# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import Symptom, Picture, db, Recognized, Appoint, Cnnrec, Category
from flask_login import login_required, current_user
import datetime
import logging

@userApp.route('/rec', methods=['GET'])
@login_required
def sec_rec():
    logging.info('primary_rec')
    pic = db.session.query(Picture.Picture.id, Picture.Picture.pic_name, Appoint.Appoint.id).filter(Picture.Picture.id==Appoint.Appoint.pic_id, Appoint.Appoint.user_id==current_user.id).first()
    neural = ""
    pic_local = ""
    message = ""
    appointed = ""
    if(pic):
        neural = db.session.query(Cnnrec.Cnnrec.symp_id, Symptom.Symptom.symptom_name).filter(Cnnrec.Cnnrec.pic_id==pic[0], Symptom.Symptom.id==Cnnrec.Cnnrec.symp_id).group_by(Cnnrec.Cnnrec.symp_id, Symptom.Symptom.symptom_name).all()
        pic_local = "data/" + pic[1]
        appointed = pic[2]
    else:
        message = "No data"
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id)
    pics_today = db.session.query(Recognized.Recognized.pic_id).filter(db.func.DATE(Recognized.Recognized.date)==datetime.datetime.now().date(),
                                                                      Recognized.Recognized.user_id==current_user.id)\
                                                                    .group_by(Recognized.Recognized.pic_id)

    pics_in_wait = Appoint.Appoint.query.filter_by(user_id=current_user.id)
    categories = Category.Category.query.order_by(Category.Category.id).all()

    if ('message' in request.args):
        message = request.args['message']
    return render_template('rec.pug', symptoms=symptoms,
                           admin=current_user.admin, pic_local=pic_local,
                           message=message, appointed=appointed,
                           today_rec=len(list(pics_today)), in_wait=len(list(pics_in_wait)),
                           neural=neural, categories=categories)

@userApp.route('/rec', methods=['POST'])
@login_required
def sec_rec_post():
    if(current_user.user_name == "demo"):
        return redirect(url_for('sec_rec', message="Demo user, read only"))
    max_time_rec = userApp.config.get('MAX_TIME_REC')
    form = request.form
    if(form.has_key('appointed')):
        appointed = Appoint.Appoint.query.get(int(form['appointed']))
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

    return redirect('/rec')

@userApp.route('/rec/skip/<path:path>')
@login_required
def skip(path):
    if(current_user.user_name == "demo"):
        return redirect(url_for('sec_rec', message="Demo user, read only"))
    appointed = Appoint.Appoint.query.get(int(path))
    pic = Picture.Picture.query.get(appointed.pic_id)
    pic.skipped = True
    db.session.commit()
    db.session.delete(appointed)
    db.session.commit()

    return redirect('/rec')