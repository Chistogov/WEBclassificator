from flask import render_template
from userApp import userApp


@userApp.errorhandler(401)
def page_not_found(e):
    return render_template('<p>Login failed</p>')