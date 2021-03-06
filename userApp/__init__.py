# -*- coding: utf-8 -*-
from flask import Flask
import logging
import sys
from jinja2 import Environment, FileSystemLoader
# from babel.support import Translations

userApp = Flask(__name__, instance_relative_config=True)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    userApp.run(debug=False)

# Load the views
from userApp import appointController
from userApp import cnnStatsController
from userApp import dependencies
from userApp import errorController
from userApp import indexController
from userApp import indexingController
from userApp import loginController
from userApp import parameterController
from userApp import primaryRecController
from userApp import statsController
from userApp import usersController
from userApp import picsController
from userApp import Pagination
from userApp import AlchemyEncoder
from userApp import rejectionController
from userApp import testsController
from userApp import consiliumController
from userApp import secondaryRecController
from userApp import cnnConfirmController
from userApp import jinjaHelper

from userApp import updateController

from userApp.dbc import *

# Load the config file
userApp.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
userApp.config.from_object('config')
userApp.secret_key = '2240641'
# locale_dir = "i18n"
# msgdomain = "html"
# list_of_desired_locales = ["cs", "en"]
# loader = FileSystemLoader("templates")
# extensions = ['jinja2.ext.i18n', 'jinja2.ext.autoescape', 'jinja2.ext.with_']
#
# env = Environment(extensions=extensions, loader=loader) # add any other env options if needed
#
# template = env.get_template("stack.html")
# rendered_template = template.render()
logging.basicConfig(level = logging.INFO)
db.create_all()

# request.url:                 http://127.0.0.1:5000/alert/dingding/test?x=y
# request.base_url:            http://127.0.0.1:5000/alert/dingding/test
# request.url_charset:         utf-8
# request.url_root:            http://127.0.0.1:5000/
# str(request.url_rule):       /alert/dingding/test
# request.host_url:            http://127.0.0.1:5000/
# request.host:                127.0.0.1:5000
# request.script_root:
# request.path:                /alert/dingding/test
# request.full_path:           /alert/dingding/test?x=y