# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort, url_for
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/users', methods=['GET'])
@login_required
def users():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    logging.info("Users")

    return render_template('users.pug', admin=current_user.admin, message=message)


@userApp.route('/users', methods=['POST'])
@login_required
def users_post():
    if not(current_user.admin):
        return redirect('/')
    form = request.form
    print form
    if(form['password'] != form['password2']):
        return redirect(url_for('users', message="Пароли не совпадают"))
    if (form['username'] == ""):
        return redirect(url_for('users', message="Введите имя пользователя"))
    user_check = db.session.query(User.User.id).filter(User.User.user_name==form['username']).all()
    if (len(user_check) > 0):
        return redirect(url_for('users', message="Пользователь с именем \"" + form['username'] + "\" уже существует"))
    user = User.User()
    user.user_name = form['username']
    user.password = form['password']
    user.admin = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users', message="Пользователь " + form['username'] + " добавлен"))






