# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request, redirect, abort
from userApp import userApp
from flask_login import login_required


@userApp.route('/')
@login_required
def index():
    print("Index")
    return render_template('index.pug', encoding='utf-8')

@userApp.route('/rec', methods=['GET'])
@login_required
def rec():
    print("rec")
    return render_template('rec.pug', encoding='utf-8')

@userApp.route('/second_rec', methods=['GET'])
@login_required
def second_rec():
    print("second_rec")
    return render_template('second_rec.pug', encoding='utf-8')



