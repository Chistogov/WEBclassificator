# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Recognized, Mistakes, Appoint
from flask_login import login_required, current_user
import logging


@userApp.route('/users', methods=['GET'])
@login_required
def users():
    #Form
    if not(current_user.admin):
        return redirect('/')
    logging.info("Users")
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    logging.info("Users")
    #AllUsers
    userList = list()
    users = User.User.query.all()
    for user in users:
        tmp = userForm()
        tmp.id = user.id
        tmp.user_name = user.user_name
        tmp.app = len(db.session.query(Appoint.Appoint.id).filter(user.id == Appoint.Appoint.user_id).all())
        userList.append(tmp)
    return render_template('users.pug', admin=current_user.admin, message=message, users=userList)


@userApp.route('/users', methods=['POST'])
@login_required
def users_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('users', message="Demo user, read only"))
    logging.info("Users Post")
    form = request.form
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

@userApp.route('/users/<path:path>', methods=['GET'])
@login_required
def user_page(path):
    if not(current_user.admin):
        return redirect('/')
    max_time_rec = userApp.config.get('MAX_TIME_REC')
    userId=path
    user=User.User.query.filter_by(id=userId).first()
    user_dates = db.session.query(db.func.DATE(Recognized.Recognized.date)).filter_by(user_id=userId).group_by(
        Recognized.Recognized.date).order_by(Recognized.Recognized.date.desc())
    rechistorylist = list()
    user_dates = list(set(user_dates))
    user_dates.sort(reverse=True)
    for item in user_dates:
        tmp = recHistory()
        tmp.date = item[0]
        tmp.count_rec = len(list(db.session.query(db.func.count(Recognized.Recognized.pic_id)).filter(
            Recognized.Recognized.user_id == userId,
            db.func.DATE(Recognized.Recognized.date) == item[0]).group_by(Recognized.Recognized.pic_id)))
        timers = db.session.query(Recognized.Recognized.timer).filter(
            db.func.DATE(Recognized.Recognized.date) == item[0],
            Recognized.Recognized.user_id == userId).group_by(Recognized.Recognized.pic_id,
                                                                       Recognized.Recognized.timer)
        for timer in timers:
            if (timer == 0 or timer > max_time_rec):
                tmp.time += max_time_rec
            else:
                tmp.time += timer
        tmp.time = round(tmp.time / 60 / 60, 2)
        tmp.mistakes = len(list(db.session.query(db.func.count(Mistakes.Mistakes.pic_id)).filter(
            Mistakes.Mistakes.user_id == userId,
            db.func.DATE(Mistakes.Mistakes.date) == item[0]).group_by(Mistakes.Mistakes.pic_id)))
        tmp.mpercentage = round(((100/(tmp.count_rec+tmp.mistakes))*tmp.mistakes), 2)
        rechistorylist.append(tmp)

    app_count = len(db.session.query(Appoint.Appoint.id).filter(user.id == Appoint.Appoint.user_id).all())

    return render_template('/users/index.pug', admin=current_user.admin, recHistory=rechistorylist, user=user, app_count=app_count)


class recHistory():
    date = ""
    count_rec = 0
    time = 0.0
    mistakes = 0
    mpercentage = 0.00

class userForm():
    user_name = ""
    app = 0







