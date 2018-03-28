# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import Symptom, Picture, User, db
from flask_login import login_required, current_user

@userApp.route('/settings', methods=['GET'])
@login_required
def parameter():

    return render_template('parameter.pug')

@userApp.route('/settings', methods=['POST'])
@login_required
def parameter_post():
    form = request.form
    for item in form:
        print item
    return redirect('/settings')