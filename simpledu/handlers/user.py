#coding=utf-8

from flask import Blueprint, request, render_template

from simpledu.models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/<string:username>")
def user_detail(username):
    user = User.query.filter_by(username=username).first()
    print(user.publish_courses)
    return render_template("user.html", user=user)