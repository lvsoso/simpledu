#coding=utf-8

from flask import abort
from flask_login import current_user
from functools import wraps
from simpledu.models import User

def role_required(role):
    """ 带参数的装饰器, 可以使用它来保护一个路由处理函数只能被特定的
    角色用户访问:
        @role_required(User.ADMIN)
        def admin():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            # 未登录用户或者角色不满足条件 触发 404
            # 403 会暴露路由
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwrargs)
        return wrapper
    return decorator

# 特定角色的装饰器
# 员工
staff_required = role_required(User.ROLE_STAFF)
# 管理员
admin_required = role_required(User.ROLE_ADMIN)