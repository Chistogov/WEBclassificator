# -*- coding: utf-8 -*-
import glob
import os
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import Picture, db
from flask_login import login_required, current_user
import datetime


@userApp.route('/indexing', methods=['GET'])
@login_required
def indexing():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    logging.info('indexing')
    infoForm.db = db.session.query(db.func.count(Picture.Picture.id)).first()[0]
    os.chdir(userApp.config.get('DATA_PATH'))
    list_folder = list()
    for file in glob.glob("*.jpg"):
        list_folder.append(file)
    infoForm.folder = len(glob.glob("*.jpg"))
    infoForm.ready = len(list_folder)-(db.session.query(db.func.count(Picture.Picture.id)).filter(Picture.Picture.pic_name.in_(list_folder)).first()[0])
    return render_template('indexing.pug', admin=current_user.admin, infoForm=infoForm, message=message)

@userApp.route('/indexing/now')
@login_required
def indexing_post():
    if(current_user.user_name == "demo"):
        return redirect(url_for('indexing', message="Demo user, read only"))
    i = 0
    os.chdir(userApp.config.get('DATA_PATH'))
    for file in glob.glob("*.jpg"):
        num = db.session.query(Picture.Picture.id).filter(Picture.Picture.pic_name == file).all()
        if(len(num) == 0):
            pic = Picture.Picture()
            pic.pic_name = file
            pic.first_rec = False
            pic.skipped = False
            pic.index_date = datetime.datetime.now().date()
            db.session.add(pic)
            i = i + 1
    db.session.commit()
    return redirect(url_for('indexing', message = "Проиндексировано " + str(i) + "записей"))

class infoForm():
    db = 0
    ready = 0
    folder = 0