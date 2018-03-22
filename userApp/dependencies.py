from flask import send_from_directory
from userApp import userApp

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