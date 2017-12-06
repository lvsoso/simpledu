#coding=utf-8

import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange
from wtforms import ValidationError
from wtforms import TextAreaField, IntegerField

from simpledu.models import db, User, Course



class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired("该字段是必填项目"), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired("该字段是必填项目"), Email(message="请输入合法的email地址")])
    password = PasswordField('密码', validators=[DataRequired("该字段是必填项目"), Length(6, 24, message='密码长度要在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired("该字段是必填项目"), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        # if len(re.sub("[0-9a-zA-Z]", "", field.data)) != 0:
        #     raise ValidationError("用户名只能包含数字或字母")
        if not field.data.isalnum():
            raise ValidationError("用户名只能包含数字或字母")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):
    #email = StringField("邮箱", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired("该字段是必填项目"), Length(3, 24)])
    password = PasswordField("密码", validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField("记住我")
    submit = SubmitField("提交")

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名未注册")

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱未注册")

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("密码错误")

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[DataRequired(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course