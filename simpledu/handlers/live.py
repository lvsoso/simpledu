#coding=utf-8

import json
from flask import Blueprint, render_template, flash, url_for, redirect
from simpledu.models import Live
from simpledu.forms import MessageForm
from simpledu.handlers.ws import my_redis

live = Blueprint("live", __name__, url_prefix="/live")

@live.route("/")
def index():
    live = Live.query.order_by(Live.created_at.desc()).limit(1).first()
    return render_template("live/index.html", live=live)

@live.route("/systemmessage", methods=['POST'])
def systemmessage():
    form = MessageForm()
    if form.validate_on_submit():
        my_redis.publish('chat', json.dumps(dict(
            username='System',
            text=form.text.data
        )))
        flash('系统消息发送成功', 'success')
        return redirect(url_for('admin.message'))