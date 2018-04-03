# -*- coding: utf-8 -*-
from flask import render_template, request, redirect
from userApp import *
from userApp.dbc import Symptom, db
from flask_login import login_required, current_user
import logging

@userApp.route('/settings', methods=['GET'])
@login_required
def parameter():
    logging.info('parameter')
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    return render_template('parameter.pug', symptoms=symptoms, admin=current_user.admin)

@userApp.route('/settings', methods=['POST'])
@login_required
def parameter_post():
    form = request.form
    if(form['diagnos'] != ""):
        symptom = Symptom.Symptom()
        symptom.symptom_name = form['diagnos']
        for item in form:
            if(item == 'ear'):
                symptom.ear = True
            if (item == 'nose'):
                symptom.nose = True
            if (item == 'throat'):
                symptom.throat = True
        db.session.add(symptom)
        db.session.commit()
    return redirect('/settings')

