# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager, UserMixin

userApp = Flask(__name__, instance_relative_config=True)

# Load the views
from userApp import index
from userApp import login
from userApp import dependencies

# Load the config file
userApp.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
# userApp.jinja_env.auto_reload = True
userApp.config.from_object('config')



