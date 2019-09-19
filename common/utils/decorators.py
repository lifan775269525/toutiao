# -*-Coding:UTF-8 -*-
"""
程序：装饰器工具类
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
from flask import g
from functools import wraps

from models import db


# 登录验证装饰器
def login_required(func):
    """用户必须登录装饰器"""

    @wraps(func)
    def inner(*args, **kwargs):
        if not g.user_id:
            return {'message': "User must be authorized."}, 401
        if g.is_refresh_token:
            return {"message": "Do not use refresh token."}, 403
        else:
            return func(*args, **kwargs)

    return inner


def set_db_to_write(func):
    """
    设置使用写数据库
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)

    return wrapper


def set_db_to_read(func):
    """
    设置使用读数据库
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)

    return wrapper
