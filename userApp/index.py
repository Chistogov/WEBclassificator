# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, request
from userApp import userApp

@userApp.route('/')
def index():
    print("Index")
    return render_template('index.pug', encoding='utf-8')

@userApp.route('/login', methods=['GET'])
def login():
    print("login")
    return render_template('login.pug', encoding='utf-8')

@userApp.route('/login', methods=['POST'])
def login_post():
    print unicode(request.form['login'])
    print unicode(request.form['loginpassword'])
    print("login_post")
    return render_template('login.pug', encoding='utf-8')

@userApp.route('/rec', methods=['GET'])
def rec():
    print("rec")
    return render_template('rec.pug', encoding='utf-8')\

@userApp.route('/second_rec', methods=['GET'])
def second_rec():
    print("second_rec")
    return render_template('second_rec.pug', encoding='utf-8')

#Настройки для CSS и HTML
@userApp.route('/fonts/<path:path>')
def send_fonts(path):
    print("Incude + " + path)
    return send_from_directory('templates/static/materialize/fonts', path)

@userApp.route('/css/<path:path>')
def send_css(path):
    print("Incude:" + path)
    return send_from_directory('templates/static/materialize/css', path)

@userApp.route('/js/<path:path>')
def send_js(path):
    print("Incude:" + path)
    return send_from_directory('templates/static/materialize/js', path)

@userApp.route('/dev/js/<path:path>')
def send_dev_js(path):
    print("Incude:" + path)
    return send_from_directory('templates/static/js', path)

@userApp.route('/dev/css/<path:path>')
def send_dev_css(path):
    print("Incude:" + path)
    return send_from_directory('templates/static/css', path)

@userApp.route('/img/<path:path>')
def send_dev_img(path):
    print("Incude: " + path)
    return send_from_directory('templates/static/images', path)
