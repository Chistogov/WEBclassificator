# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import Symptom, db, Category
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
    symptoms = db.session.query(Symptom.Symptom)
    categories = Category.Category.query.order_by(Category.Category.id).all()
    return render_template('parameter.pug', symptoms=symptoms, admin=current_user.admin, message=message, category=categories)

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
        if(form.has_key('category')):
            symptom.cat_id = form['category']
        for item in form:
            if(item == 'ear'):
                symptom.ear = True
            if (item == 'nose'):
                symptom.nose = True
            if (item == 'throat'):
                symptom.throat = True
            if (item == 'ismedical'):
                symptom.ismedical = True
            if (item == 'primary'):
                symptom.diagnos = True
        db.session.add(symptom)
        db.session.commit()
    return redirect('/settings')


@userApp.route('/settings/symps', methods=['GET'])
@login_required
def parameter_weights():
    if not(current_user.admin):
        return redirect('/')
    logging.info('parameter')
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    symptoms = db.session.query(Symptom.Symptom)
    categories = Category.Category.query.order_by(Category.Category.id).all()
    return render_template('symptoms/weights.pug', symptoms=symptoms, admin=current_user.admin, message=message, categories=categories)

@userApp.route('/settings/symps', methods=['POST'])
@login_required
def parameter_weights_post():
    if not(current_user.admin):
        return redirect('/')
    form = request.form
    print "form"
    for item in form:
        symp = Symptom.Symptom.query.get(item)
        symp.weight = form[item]
        db.session.commit()
    return redirect(request.referrer)