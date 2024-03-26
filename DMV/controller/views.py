from flask import Flask, render_template, Blueprint
from flask_login import  login_required, current_user


views = Blueprint("views",__name__)


@views.route('/')
@login_required
def practice():
    return render_template("practice.html",user = current_user)

@views.route('/index')
@login_required
def index():
    return render_template("index.html", user = current_user)