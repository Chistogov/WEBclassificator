# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import Symptom, db
from flask_login import login_required, current_user
import logging

@userApp.route('/settings', methods=['GET'])
@login_required
def parameter():
    if not(current_user.admin):
        return redirect('/')
    logging.info('parameter')
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    return render_template('parameter.pug', symptoms=symptoms, admin=current_user.admin, message=message)

@userApp.route('/settings', methods=['POST'])
@login_required
def parameter_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('parameter', message="Demo user, read only"))
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
            if (item == 'ismedical'):
                symptom.ismedical = True
        db.session.add(symptom)
        db.session.commit()
    return redirect('/settings')

