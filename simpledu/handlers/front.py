#coding=utf-8

from flask_login import login_user, logout_user, login_required
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from simpledu.models import Course, User

from simpledu.forms import LoginForm, RegisterForm


front = Blueprint("front", __name__)


@front.route("/")
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('index.html', pagination=pagination)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #user = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        #第一个参数是 User 对象，第二个参数是个布尔值，告诉 flask-login 是否需要记住该用户。
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.creat_user()
        flash('注册成功，请登录！', 'success')
        ".login 是 front.login 的简写，如果重定向到当前 Blueprint 下的某个路由就可以这样简写。"
        return redirect(url_for('.login'))
    return render_template("register.html", form=form)


from flask_login import login_user, logout_user, login_required

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

