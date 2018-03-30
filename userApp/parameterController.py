# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import Symptom, Picture, User, db
from flask_login import login_required, current_user

@userApp.route('/settings', methods=['GET'])
@login_required
def parameter():
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id).all()
    return render_template('parameter.pug', symptoms=symptoms)

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

