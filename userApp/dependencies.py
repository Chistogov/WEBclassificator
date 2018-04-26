from flask import send_from_directory
from userApp import userApp
import logging

@userApp.route('/fonts/<path:path>')
def send_fonts(path):
    logging.info("Incude + " + path)
    return send_from_directory('templates/static/materialize/fonts', path)

@userApp.route('/css/<path:path>')
def send_css(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/materialize/css', path)

@userApp.route('/js/<path:path>')
def send_js(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/materialize/js', path)

@userApp.route('/css2/<path:path>')
def send_css2(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/bootstrap/css', path)

@userApp.route('/icons/<path:path>')
def send_icons(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/octicons/css', path)

@userApp.route('/js2/<path:path>')
def send_js2(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/bootstrap/js', path)

@userApp.route('/dev/js/<path:path>')
def send_dev_js(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/js', path)

@userApp.route('/dev/css/<path:path>')
def send_dev_css(path):
    logging.info("Incude:" + path)
    return send_from_directory('templates/static/css', path)

@userApp.route('/img/<path:path>')
def send_dev_img(path):
    logging.info("Incude: " + path)
    return send_from_directory('templates/static/images', path)

@userApp.route('/data/<path:path>')
def send_data(path):
    logging.info("Incude: " + path)
    return send_from_directory(userApp.config.get('DATA_PATH'), path)