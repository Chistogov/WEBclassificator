# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Journal
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/updates')
@login_required
def updates():
    logging.info("Update")
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    user = db.session.query(User.User.id).filter(User.User.user_name=="Updates").first()
    messageHistory =db.session.query(Journal.Journal.fromUser ,User.User.user_name, Journal.Journal.date, Journal.Journal.message)\
        .filter(Journal.Journal.userTo==user.id, Journal.Journal.fromUser).order_by(Journal.Journal.id.desc()).limit(10)
    return render_template('updates.pug', admin=current_user.admin, messageHistory=messageHistory, message=message)

@userApp.route('/updates', methods=['POST'])
@login_required
def update_post():
    if (current_user.user_name == "demo"):
        return redirect(url_for('updates', message="Demo user, read only"))
    form = request.form
    userTo = db.session.query(User.User).filter(User.User.user_name == "Updates").first()
    userFrom = current_user
    message = Journal.Journal()
    if(form['message'] != ""):
        message.userTo = userTo.id
        message.userFrom = userFrom.id
        message.message = form['message']
        message.date = datetime.datetime.now().date()
        db.session.add(message)
        db.session.commit()
    else:
        return redirect(url_for('updates', message="Введите сообщение"))
    return redirect('/updates')





