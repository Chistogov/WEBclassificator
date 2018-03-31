# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import Symptom, Picture, User, db, Recognized
from flask_login import login_required, current_user
import datetime
import logging

@userApp.route('/rec', methods=['GET'])
@login_required
def sec_rec():
    logging.info('second_rec')
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    return render_template('rec.pug', symptoms=symptoms)

@userApp.route('/rec', methods=['POST'])
@login_required
def sec_rec_post():
    form = request.form
    for item in form:
        new_tag = Recognized.Recognized()
        new_tag.user_id=current_user.id
        new_tag.symp_id=item
        new_tag.pic_id=1111
        new_tag.date=datetime.datetime.now().date()
        db.session.add(new_tag)
    db.session.commit()

    return redirect('/rec')