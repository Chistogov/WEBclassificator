# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import Symptom, Picture, User, db, Recognized, Appoint
from flask_login import login_required, current_user
import datetime
import logging

@userApp.route('/rec', methods=['GET'])
@login_required
def sec_rec():
    logging.info('primary_rec')
    pic = db.session.query(Picture.Picture.id, Picture.Picture.pic_name, Appoint.Appoint.id).filter(Picture.Picture.id==Appoint.Appoint.pic_id, Appoint.Appoint.user_id==current_user.id).first()
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    pic_local = ""
    message = ""
    appointed = ""
    if(pic):
        pic_local = "data/" + pic[1]
        appointed = pic[2]
    else:
        message = "Вам не назначено снимков, обратитесь к администратору"
    return render_template('rec.pug', symptoms=symptoms, admin=current_user.admin, pic_local=pic_local, message=message, appointed=appointed)

@userApp.route('/rec', methods=['POST'])
@login_required
def sec_rec_post():
    form = request.form
    if(form.has_key('appointed')):
        appointed = Appoint.Appoint.query.get(int(form['appointed']))
        for item in form:
            if(item.isdigit()):
                new_tag = Recognized.Recognized()
                new_tag.user_id=current_user.id
                new_tag.symp_id=item
                new_tag.pic_id=appointed.pic_id
                new_tag.date=datetime.datetime.now().date()
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
    appointed = Appoint.Appoint.query.get(int(path))
    pic = Picture.Picture.query.get(appointed.pic_id)
    pic.skipped = True
    db.session.commit()
    db.session.delete(appointed)
    db.session.commit()

    return redirect('/rec')