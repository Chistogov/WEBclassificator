# -*- coding: utf-8 -*-
from flask import render_template
from userApp import *
from userApp.dbc import User, db, Recognized, Appoint, Journal
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/pics/<path:path>')
@login_required
def pic_view(path):
    symptomId = path
    print('Pics - ' + path)
        
    return render_template('/pics_viewer/index.pug', admin=current_user.admin)



