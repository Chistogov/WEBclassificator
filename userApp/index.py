# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from flask import render_template, send_from_directory
from jinja2 import Environment, PackageLoader
#env = Environment(loader=PackageLoader('userApp', 'templates'))

from userApp import userApp
import os
# from requests import request

@userApp.route('/')
def index():
    print(render_template('index.pug'))
    # myvar = 'Привет World'
    # index_variables = {'title': ''}
    # index_variables['title'] = myvar.decode('utf-8')
    # template = env.get_template('index.pug')
    # with open("index.pug", "w") as index_file:
    #     output = template.render(index_variables)
    #     index_file.write(output.encode('utf-8'))  
    return render_template('index.pug', encoding='utf-8')

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
