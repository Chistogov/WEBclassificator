# -*- coding: utf-8 -*-
from flask import Flask
import logging

userApp = Flask(__name__, instance_relative_config=True)

# Load the views
from userApp import indexController
from userApp import loginController
from userApp import dependencies
from userApp import errorController
from userApp import primaryRecController
from userApp import parameterController
from userApp import appointController
from userApp import statsController
from userApp import usersController
from userApp import indexingController
from userApp import cnnStatsController
from userApp import updateController
from userApp.dbc import db

# Load the config file
userApp.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
userApp.config.from_object('config')
logging.basicConfig(level = logging.INFO)
db.create_all()





