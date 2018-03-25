# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import *
from userApp.dbc import User, db
from flask_login import login_required, current_user



@userApp.route('/')
@login_required
def index():
    print("Index")
    return render_template('index.pug', name=current_user.user_name)


@userApp.route('/second_rec', methods=['GET'])
@login_required
def second_rec():
    print("second_rec")
    return render_template('second_rec.pug', encoding='utf-8')



