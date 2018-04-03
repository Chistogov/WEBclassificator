# -*- coding: utf-8 -*-
from flask import render_template, request, redirect
from userApp import *
from userApp.dbc import Symptom
from flask_login import login_required, current_user
import logging

@userApp.route('/second_rec', methods=['GET'])
@login_required
def rec():
    logging.info('second_rec')
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    return render_template('second_rec.pug', symptoms=symptoms, admin=current_user.admin)

@userApp.route('/second_rec', methods=['POST'])
@login_required
def rec_post():
    form = request.form
    for item in form:
        print item
    return redirect('/second_rec')