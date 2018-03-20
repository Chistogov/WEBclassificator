# -*- coding: cp1251 -*-
from flask import Flask

userApp = Flask(__name__, instance_relative_config=True)

# Load the views
from userApp import index

# Load the config file
userApp.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
# userApp.jinja_env.auto_reload = True
userApp.config.from_object('config')