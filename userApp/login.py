# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, abort
from userApp import userApp, User
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

login_manager = LoginManager()
login_manager.init_app(userApp)
login_manager.login_view = "login"

users = [User.User(id) for id in range(1, 21)]

@login_manager.user_loader
def load_user(userid):
    return User.User(userid)

@userApp.route('/login', methods=['GET'])
def login():
    print("login")
    return render_template('login.pug', encoding='utf-8')

@userApp.route('/login', methods=['POST'])
def login_post():
    username = request.form['login']
    password = request.form['loginpassword']
    if password == username + "_secret":
        id = username.split('user')[1]
        user = User.User(id)
        login_user(user)
        return redirect(request.args.get("next"))
    else:
        return abort(401)
    return render_template('login.pug', encoding='utf-8')

# somewhere to logout
@userApp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.pug', encoding='utf-8')