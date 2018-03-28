# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

userApp = Flask(__name__, instance_relative_config=True)

# Load the views
from userApp import indexController
from userApp import loginController
from userApp import dependencies
from userApp import errorController
from userApp import primaryRecController
from userApp import secondaryRecController
from userApp import parameterController
from userApp.dbc import db

# Load the config file
userApp.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
userApp.config.from_object('config')
db.create_all()
# userApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# userApp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@127.0.0.1:5432/classdb'





