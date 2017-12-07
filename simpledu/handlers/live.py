#coding=utf-8

from flask import Blueprint, render_template
from simpledu.models import Live

live = Blueprint("live", __name__, url_prefix="/live")

@live.route("/")
def index():
    live = Live.query.order_by(Live.created_at.desc()).limit(1).first()
    return render_template("live/index.html", live=live)