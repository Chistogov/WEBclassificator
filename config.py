# -*- coding: utf-8 -*-
# Enable Flask's debugging features. Should be False in production
DEBUG = True

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True
# TESTING=True
# TEMPLATES_AUTO_RELOAD=True
SECRET_KEY='secret_xxx'

SQLALCHEMY_DATABASE_URI='postgresql://postgres:12345@127.0.0.1:5432/classdb'
SQLALCHEMY_TRACK_MODIFICATIONS = True