# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import User, db
from flask_login import login_required, current_user



@userApp.route('/')
@login_required
def index():
    print("Index")
    infoForm.name = current_user.user_name
    infoForm.today_rec = 10;
    infoForm.in_wait = 154;
    infoForm.all_rec = 2366;
    infoForm.confirmed = 562;
    return render_template('index.pug', infoForm=infoForm)


@userApp.route('/second_rec', methods=['GET'])
@login_required
def second_rec():
    print("second_rec")
    return render_template('second_rec.pug', encoding='utf-8')


class infoForm():
    name = "";
    today_rec = 0;
    in_wait = 0;
    all_rec = 0;
    confirmed = 0;




