# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import Symptom, Picture, User, db
from flask_login import login_required, current_user

@userApp.route('/rec', methods=['GET'])
@login_required
def sec_rec():
    symptoms_ear = Symptom.Symptom.query.filter_by(ear=True).order_by(Symptom.Symptom.id).all()
    symptoms_nose = Symptom.Symptom.query.filter_by(nose=True).order_by(Symptom.Symptom.id).all()
    symptoms_throat = Symptom.Symptom.query.filter_by(throat=True).order_by(Symptom.Symptom.id).all()
    return render_template('rec.pug', symptoms_ear=symptoms_ear,
                           symptoms_nose=symptoms_nose,
                           symptoms_throat=symptoms_throat)

@userApp.route('/rec', methods=['POST'])
@login_required
def sec_rec_post():
    form = request.form
    for item in form:
        print item
    return redirect('/rec')